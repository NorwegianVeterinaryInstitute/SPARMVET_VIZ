#!/usr/bin/env python3
import argparse
import os
import sys
import yaml
import polars as pl
from pathlib import Path
from typing import Dict, List, Any

# ADR-016: Use Package-First Authority (Editable Installs)
# Ensure project root is in sys.path for fallback
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from ingestion.ingestor import DataIngestor
    from utils.config_loader import ConfigManager
    from transformer.data_wrangler import DataWrangler
    from transformer.data_assembler import DataAssembler
except ImportError as e:
    print(
        f"❌  ERROR: [Layer 2 Runner] Core imports failed. Check .venv install. {e}")
    sys.exit(1)


def run_assembler_debug(manifest_path: str, data_dir_override: str = None, output_path: str = None):
    """
    Consolidated Assembly Layer Debugger (ADR 012 / ADR 018).
    Orchestrates Layer 1 (Wrangler) and Layer 2 (Assembler) execution.
    """
    print(f"\n[{'='*60}]")
    print(f" 🏗️  LAYER 2 ASSEMBLY DEBUGGER (Consolidated)")
    print(f"[{'='*60}]\n")

    # 1. Load Manifest
    try:
        config_manager = ConfigManager(manifest_path)
        manifest = config_manager.raw_config
    except Exception as e:
        print(f"  └── ❌ Manifest Error: Failed to load {manifest_path}. {e}")
        sys.exit(1)

    assemblies = manifest.get("assembly_manifests", {})
    if not assemblies:
        print("  └── ❌ Error: No 'assembly_manifests' found in manifest.")
        return

    # 2. Initialize Ingestor
    # Default search directory for mock assets per Project Conventions
    default_data_dir = str(project_root / "assets/test_data")
    data_dir = data_dir_override or default_data_dir

    if not os.path.exists(data_dir):
        print(
            f"  └── ⚠️  Warning: Data directory '{data_dir}' not found. Falling back to project assets.")
        data_dir = default_data_dir

    ingestor = DataIngestor(data_dir)
    print(f"  └── 📥 Ingestion Base: {data_dir}")

    # 3. Identify all available schemas in manifest
    all_schemas = {}
    all_schemas.update(manifest.get("data_schemas", {}))
    # metadata_schema is a single block
    if "metadata_schema" in manifest:
        all_schemas["metadata_schema"] = manifest["metadata_schema"]
    all_schemas.update(manifest.get("additional_datasets_schemas", {}))

    # Global cache for all materialized assemblies in this run (ADR-024)
    assembly_results_cache: Dict[str, pl.LazyFrame] = {}

    # 4. Assembly Execution Loop
    for assembly_id, assembly_info in assemblies.items():
        print(f"\n[ASSEMBLY: {assembly_id}]")

        # a) Prepare Ingredients (Layer 1: Individual Wrangling)
        ingredient_cache: Dict[str, pl.LazyFrame] = {}
        ingredients_list = assembly_info.get("ingredients", [])

        for ing in ingredients_list:
            dataset_id = ing.get("dataset_id")

            # Check if this ingredient is a previously materialized assembly in this run
            if dataset_id in assembly_results_cache:
                print(f"  └── ⚡ Using Assembly Result: {dataset_id}")
                ingredient_cache[dataset_id] = assembly_results_cache[dataset_id]
                continue

            if dataset_id not in all_schemas:
                print(
                    f"  └── ❌ Error: Ingredient '{dataset_id}' schema not found in manifest.")
                continue

            schema = all_schemas[dataset_id]
            print(f"  └── 🛠️  Processing Ingredient: {dataset_id}")

            # i. Ingest
            try:
                lf, source_tsv = ingestor.ingest(dataset_id, schema)
            except Exception as e:
                print(f"      └── ❌ Ingest failure: {e}")
                continue

            # ii. Wrangle (Layer 1 Atomic actions)
            input_fields = schema.get("input_fields", {})
            if isinstance(input_fields, dict) and "input_fields" in input_fields:
                input_fields = input_fields["input_fields"]

            wrangling_rules = schema.get("wrangling", [])
            if isinstance(wrangling_rules, dict) and "wrangling" in wrangling_rules:
                wrangling_rules = wrangling_rules["wrangling"]

            if wrangling_rules:
                wrangler = DataWrangler(input_fields)
                lf = wrangler.run(lf, wrangling_rules)

            # iii. Ingredient Contract Guard (ADR-013)
            output_fields = schema.get("output_fields", {})
            if isinstance(output_fields, dict) and "output_fields" in output_fields:
                output_fields = output_fields["output_fields"]

            if output_fields:
                target_cols = list(output_fields.keys()) if isinstance(
                    output_fields, dict) else output_fields
                lf = lf.select(target_cols)

            ingredient_cache[dataset_id] = lf

        # b) Execute Assembly (Layer 2: Relational recipe)
        recipe_data = assembly_info.get("recipe", [])
        # Handle !include or inline list
        if isinstance(recipe_data, dict) and "!include" in recipe_data:
            recipe_path = project_root / \
                "config/manifests/pipelines" / recipe_data["!include"]
            try:
                with open(recipe_path, 'r') as rf:
                    recipe = yaml.safe_load(rf).get("steps", [])
            except Exception as e:
                print(
                    f"  └── ❌ Recipe Error: Failed to load {recipe_path}. {e}")
                continue
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

        # c) Final Assembly Contract Guard (ADR-013)
        final_contract_data = assembly_info.get("final_contract", [])
        if isinstance(final_contract_data, dict) and "!include" in final_contract_data:
            contract_path = project_root / "config/manifests/pipelines" / \
                final_contract_data["!include"]
            try:
                with open(contract_path, 'r') as cf:
                    final_contract = yaml.safe_load(
                        cf).get("output_fields", {})
            except:
                final_contract = {}
        elif isinstance(final_contract_data, list):
            # Handle list of column names or list of dictionaries
            final_contract = {}
            for item in final_contract_data:
                if isinstance(item, str):
                    final_contract[item] = None
                elif isinstance(item, dict):
                    # Take the first key (standard pattern for sequential list of dicts)
                    final_contract[list(item.keys())[0]] = list(
                        item.values())[0]
        else:
            final_contract = final_contract_data
            # If it's a dict and has 'output_fields', use that. Otherwise use the dict itself.
            if isinstance(final_contract, dict) and "output_fields" in final_contract:
                final_contract = final_contract["output_fields"]

        if final_contract:
            target_cols = list(final_contract.keys())
            print(
                f"  └── 🛡️  Applying Final Contract Guard: {len(target_cols)} columns.")
            try:
                consolidated_lf = consolidated_lf.select(target_cols)
            except Exception as e:
                print(f"      └── ❌ Contract Mismatch: {e}")
                continue

        # d) Materialization (ADR-010: .collect() here, not in libs)
        # Priority: cli override > default tmp location
        mat_path = output_path or str(
            project_root / f"tmp/EVE_assembly_{assembly_id}.tsv")
        os.makedirs(os.path.dirname(mat_path), exist_ok=True)

        try:
            df = consolidated_lf.collect()
            df.write_csv(mat_path, separator='\t')
            print(f"  └── 💾 Materialized resulting assembly to: {mat_path}")

            # Cache the result for downstream assemblies
            assembly_results_cache[assembly_id] = df.lazy()

            # e) Inspection
            print(f"\n  [ASSEMBLY PREVIEW: {assembly_id}]")

            print(f"  └── Final Schema: {df.schema}")
            print(df.head(5))
            print(f"  └── ✅ Final: {len(df.columns)} columns, {len(df)} rows.")

        except Exception as e:
            print(f"  └── ❌ Materialization Error: {e}")
            continue

    print(f"\n[{'='*60}]")
    print(f" ✅ ALL ASSEMBLY STEPS COMPLETE.")
    print(f"[{'='*60}]\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Consolidated Assembly Layer Debugger (ADR 012/018)")
    parser.add_argument("--manifest", required=True,
                        help="Path to pipeline manifest YAML.")
    parser.add_argument(
        "--data", help="Optional override for source data directory.")
    parser.add_argument(
        "--output", help="Optional override for final output path.")

    args = parser.parse_args()
    run_assembler_debug(args.manifest, args.data, args.output)
