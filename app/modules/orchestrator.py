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

    def materialize_tier1(self, pipeline_id: str, assembly_id: str, output_path: Path) -> pl.LazyFrame:
        """
        Executes the full pipeline ingestion and assembly to create a Tier 1 Anchor.
        """
        manifest_path = self.manifests_dir / f"{pipeline_id}.yaml"
        if not manifest_path.exists():
            raise FileNotFoundError(
                f"Pipeline manifest not found: {manifest_path}")

        # 1. Load Manifest
        cm = ConfigManager(str(manifest_path))
        manifest = cm.raw_config

        # 2. Ingest and Wrangle Ingredients
        ingredients = {}
        all_schemas = {}
        all_schemas.update(manifest.get("data_schemas", {}))
        if "metadata_schema" in manifest:
            all_schemas["metadata_schema"] = manifest["metadata_schema"]
        all_schemas.update(manifest.get("additional_datasets_schemas", {}))

        for ds_id, ds_schema in all_schemas.items():
            lf, _ = self.ingestor.ingest(ds_id, ds_schema)

            # Wrangle
            rules = ds_schema.get("wrangling", [])
            wrangler = DataWrangler(
                data_schema=ds_schema.get("input_fields", {}))
            lf = wrangler.run(lf, rules)

            ingredients[ds_id] = lf

        # 3. Assemble
        assembly_spec = manifest.get(
            "assembly_manifests", {}).get(assembly_id, {})
        if not assembly_spec:
            raise ValueError(
                f"Assembly '{assembly_id}' not found in manifest.")

        recipe_data = assembly_spec.get("recipe", [])
        if isinstance(recipe_data, dict) and "steps" in recipe_data:
            recipe = recipe_data["steps"]
        else:
            recipe = recipe_data

        # Add sink_parquet step (Tier 1 Anchor)
        recipe.append({
            "action": "sink_parquet",
            "path": str(output_path),
            "force_recompute": True  # Forcing recompute for this correction session
        })

        assembler = DataAssembler(ingredients)
        return assembler.assemble(recipe)
