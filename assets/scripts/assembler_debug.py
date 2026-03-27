import argparse
import os
import sys
import yaml
import polars as pl
from pathlib import Path
from typing import Dict, List, Any

# Fix path to include libs
# ADR-016: Use Package-First Authority (Editable Installs)
try:
    from ingestion.ingestor import DataIngestor
    from utils.config_loader import ConfigManager
    from transformer.data_wrangler import DataWrangler
    from transformer.data_assembler import DataAssembler
except ImportError as e:
    print(f"ERROR: Could not import core libraries. Check .venv install. {e}")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Assembly Layer Debugger (Wrangler + Assembler).")
    parser.add_argument("--manifest", required=True,
                        help="Path to general pipeline manifest.")
    args = parser.parse_args()

    # Determine project root from script location
    project_root = Path(__file__).parents[2].absolute()

    # Load manifest using official ConfigManager (handles !include)
    try:
        config = ConfigManager(args.manifest)
        manifest = config.raw_config
    except Exception as e:
        print(f"ERROR: Failed to load manifest {args.manifest}: {e}")
        sys.exit(1)

    assemblies = manifest.get("assembly_manifests", {})
    if not assemblies:
        print("No 'assembly_manifests' found in manifest.")
        return

    # Initialize components
    # data_dir is relative to assets/test_data/
    # Actually, ingestor will resolve from 'source' blocks.
    ingestor = DataIngestor(str(project_root / "assets/test_data"))

    # Ingredient Cache
    ingredient_cache: Dict[str, pl.LazyFrame] = {}

    # Identify datasets in the manifest (data_schemas, metadata_schema, additional_datasets_schemas)
    all_schemas = {}
    all_schemas.update(manifest.get("data_schemas", {}))
    # metadata_schema is a single block, but might be categorized
    all_schemas["metadata_schema"] = manifest.get("metadata_schema", {})
    all_schemas.update(manifest.get("additional_datasets_schemas", {}))

    for assembly_id, assembly_info in assemblies.items():
        print(f"\n[ASSEMBLY: {assembly_id}]")
        ingredients_list = assembly_info.get("ingredients", [])

        # 1. Prepare Ingredients (Load + Wrangle)
        for ing in ingredients_list:
            dataset_id = ing.get("dataset_id")
            if dataset_id not in all_schemas:
                print(
                    f"  └── ❌ Error: Ingredient '{dataset_id}' not found in manifest schemas.")
                continue

            schema = all_schemas[dataset_id]
            print(f"  └── 🛠️  Processing Ingredient: {dataset_id}")

            # Load
            try:
                lf, _ = ingestor.ingest(dataset_id, schema)
            except Exception as e:
                print(f"      └── ❌ Ingest failure: {e}")
                continue

            # Wrangle
            input_fields = schema.get("input_fields", {})
            # Handle nested include from Step 495
            if isinstance(input_fields, dict) and "input_fields" in input_fields:
                input_fields = input_fields["input_fields"]

            wrangling_rules = schema.get("wrangling", [])
            if isinstance(wrangling_rules, dict) and "wrangling" in wrangling_rules:
                wrangling_rules = wrangling_rules["wrangling"]

            if wrangling_rules:
                wrangler = DataWrangler(input_fields)
                lf = wrangler.run(lf, wrangling_rules)

            # Apply Contract Guard (ADR-013)
            output_fields = schema.get("output_fields", {})
            if isinstance(output_fields, dict) and "output_fields" in output_fields:
                output_fields = output_fields["output_fields"]

            if output_fields:
                target_cols = list(output_fields.keys())
                lf = lf.select(target_cols)

            ingredient_cache[dataset_id] = lf

        # 2. Assemble
        # Recipe can be a list (inline) or a dict with !include or 'steps' key
        recipe_data = assembly_info.get("recipe", [])
        if isinstance(recipe_data, dict) and "!include" in recipe_data:
            recipe_path = project_root / \
                "config/manifests/pipelines" / recipe_data["!include"]
            with open(recipe_path, 'r') as rf:
                recipe = yaml.safe_load(rf).get("steps", [])
        elif isinstance(recipe_data, list):
            recipe = recipe_data
        else:
            recipe = recipe_data.get("steps", [])

        print(f"  └── 🏗️  Assembling using recipe: {len(recipe)} steps.")

        assembler = DataAssembler(ingredient_cache)
        try:
            consolidated_lf = assembler.assemble(recipe)
        except Exception as e:
            print(f"  └── ❌ Assembly Error: {e}")
            continue

        # 3. Final Contract Guard
        final_contract_data = assembly_info.get("final_contract", [])
        if isinstance(final_contract_data, dict) and "!include" in final_contract_data:
            contract_path = project_root / "config/manifests/pipelines" / \
                final_contract_data["!include"]
            with open(contract_path, 'r') as cf:
                final_contract = yaml.safe_load(cf).get("output_fields", {})
        elif isinstance(final_contract_data, list):
            # If it's a list, it might be the contract fields directly or empty
            final_contract = {
                c: None for c in final_contract_data} if final_contract_data else {}
        else:
            final_contract = final_contract_data.get("output_fields", {})

        if final_contract:
            target_cols = list(final_contract.keys())
            print(
                f"  └── 🛡️  Applying Final Contract Guard: {len(target_cols)} columns.")
            try:
                consolidated_lf = consolidated_lf.select(target_cols)
            except Exception as e:
                print(f"      └── ❌ Contract Mismatch: {e}")
                # print(f"          Available: {consolidated_lf.collect_schema().names()}")
                continue

        # 4. Materialize
        output_tsv = project_root / f"tmp/EVE_assembler_{assembly_id}.tsv"
        os.makedirs(output_tsv.parent, exist_ok=True)
        try:
            df = consolidated_lf.collect()
            df.write_csv(output_tsv, separator='\t')
            print(f"  └── 💾 Materialized resulting assembly to: {output_tsv}")
            print(
                f"  └── ✅ Final Result: {len(df.columns)} columns, {len(df)} rows.")
            print(f"  └── 📊 Schema: {df.schema}")
            print(df.head(5))
        except Exception as e:
            print(f"  └── ❌ Materialization Error: {e}")


if __name__ == "__main__":
    main()
