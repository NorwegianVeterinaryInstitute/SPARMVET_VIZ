import polars as pl
from pathlib import Path
from typing import Dict, Any, List
from utils.config_loader import ConfigManager
from ingestion.ingestor import DataIngestor
from transformer.data_wrangler import DataWrangler
from transformer.data_assembler import DataAssembler


class DataOrchestrator:
    """
    Handles the ingestion and assembly logic (Tier 1 Materialization).
    Ensures the UI remains 'Thin' by delegating heavy processing to libraries.
    """

    def __init__(self, manifests_dir: Path, raw_data_dir: Path):
        self.manifests_dir = manifests_dir
        self.raw_data_dir = raw_data_dir
        self.ingestor = DataIngestor(data_dir=str(raw_data_dir))

    def materialize_tier1(self, project_id: str, collection_id: str, output_path: Path) -> pl.LazyFrame:
        """
        Executes the full project ingestion and assembly to create a Tier 1 Anchor.
        """
        manifest_path = self.manifests_dir / f"{project_id}.yaml"
        if not manifest_path.exists():
            raise FileNotFoundError(
                f"Project manifest not found: {manifest_path}")

        # 1. Load Manifest
        cm = ConfigManager(str(manifest_path))
        manifest = cm.raw_config

        # 2. Ingest and Wrangle Ingredients
        ingredients = {}
        all_schemas = {}
        all_schemas.update(manifest.get("data_schemas", {}))

        # Optional Metadata Support (ADR-014)
        if "metadata_schema" in manifest:
            all_schemas["metadata_schema"] = manifest["metadata_schema"]

        all_schemas.update(manifest.get("additional_datasets_schemas", {}))

        from transformer.metadata_validator import MetadataValidator
        validator = MetadataValidator()

        for ds_id, ds_schema in all_schemas.items():
            try:
                lf, _ = self.ingestor.ingest(ds_id, ds_schema)

                # --- ADR-034: Malformed Data Gatekeeping ---
                input_contract = ds_schema.get("input_fields", {})
                validator.validate(lf, input_contract,
                                   context=f"Dataset [{ds_id}]")
                lf = validator.enforce_schema(lf, input_contract)

                # Wrangle (Tier 1 only for ingredients)
                wrangling_raw = ds_schema.get("wrangling", [])
                rules = DataWrangler._resolve_tier(wrangling_raw, "tier1")

                wrangler = DataWrangler(data_schema=input_contract)
                lf = wrangler.run(lf, rules)

                ingredients[ds_id] = lf
            except Exception as e:
                # ADR-034: Propagate SPARMVET_Errors or wrap generic ones
                print(
                    f"⚠️ Ingestion Error in '{ds_id}': {str(e)}")
                # If it's a critical schema mismatch, we might want to halt here
                # but for 'optional' ingredients we continue.
                continue

        # 3. Assemble
        collection_spec = manifest.get(
            "assembly_manifests", {}).get(collection_id, {})
        if not collection_spec:
            # Fallback for agnostic discovery
            collections = manifest.get("assembly_manifests", {})
            if collections:
                collection_id = list(collections.keys())[0]
                collection_spec = collections[collection_id]
            else:
                raise ValueError(
                    f"No collections found in project '{project_id}'.")

        recipe_raw = collection_spec.get("recipe", [])
        # Resolve Tier 1 (Relational) steps for the assembly
        recipe = DataWrangler._resolve_tier(recipe_raw, "tier1")

        # Extract the ordered ingredient IDs for this collection so DataAssembler
        # starts from the correct base (first declared ingredient), not the first
        # schema that happens to be in the all-schemas dict.
        ingredient_ids = [
            item.get("dataset_id") if isinstance(item, dict) else item
            for item in collection_spec.get("ingredients", [])
            if (item.get("dataset_id") if isinstance(item, dict) else item)
        ]
        # Build an ordered dict containing only this collection's ingredients,
        # in declaration order — DataAssembler uses keys()[0] as its base frame.
        assembly_ingredients = {
            ds_id: ingredients[ds_id]
            for ds_id in ingredient_ids
            if ds_id in ingredients
        }
        if not assembly_ingredients:
            # Fallback: pass all ingredients (old behaviour) if none declared
            assembly_ingredients = ingredients

        # Agnostic Filtering: Remove steps referring to missing ingredients
        filtered_recipe = []
        for step in recipe:
            right_id = step.get("right_ingredient")
            if right_id and right_id not in assembly_ingredients:
                print(
                    f"⚠️ Skipping recipe step '{step.get('action')}' due to missing ingredient '{right_id}'")
                continue
            filtered_recipe.append(step)

        # Add sink_parquet step (Tier 1 Anchor)
        # ADR-024 Refinement: force_recompute=False allows the Decision Hash
        # logic in DataAssembler to skip re-joins if manifest is unchanged.
        filtered_recipe.append({
            "action": "sink_parquet",
            "path": str(output_path),
            "force_recompute": False
        })

        assembler = DataAssembler(assembly_ingredients)
        return assembler.assemble(filtered_recipe)
