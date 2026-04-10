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

        for ds_id, ds_schema in all_schemas.items():
            try:
                lf, _ = self.ingestor.ingest(ds_id, ds_schema)

                # Wrangle (Tier 1 only for ingredients)
                wrangling_raw = ds_schema.get("wrangling", [])
                rules = DataWrangler._resolve_tier(wrangling_raw, "tier1")

                wrangler = DataWrangler(
                    data_schema=ds_schema.get("input_fields", {}))
                lf = wrangler.run(lf, rules)

                ingredients[ds_id] = lf
            except Exception as e:
                print(
                    f"⚠️ Warning: Optional ingredient '{ds_id}' failed to ingest: {e}")
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

        # Agnostic Filtering: Remove steps referring to missing ingredients
        filtered_recipe = []
        for step in recipe:
            right_id = step.get("right_ingredient")
            if right_id and right_id not in ingredients:
                print(
                    f"⚠️ Skipping recipe step '{step.get('action')}' due to missing ingredient '{right_id}'")
                continue
            filtered_recipe.append(step)

        # Add sink_parquet step (Tier 1 Anchor)
        filtered_recipe.append({
            "action": "sink_parquet",
            "path": str(output_path),
            "force_recompute": True
        })

        assembler = DataAssembler(ingredients)
        return assembler.assemble(filtered_recipe)
