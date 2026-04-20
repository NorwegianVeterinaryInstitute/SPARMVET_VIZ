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
# if str(project_root) not in sys.path:
# STRICT BAN: sys.path.append / sys.path.insert are explicitly forbidden. Rely on pip install -e.

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
            # Resolve tier1 + tier2 for assembly debugging
            resolved_rules = DataWrangler._resolve_tier(wrangling_rules, "all")

            if resolved_rules:
                wrangler = DataWrangler(input_fields)
                lf = wrangler.run(lf, resolved_rules)

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
        recipe = []

        if isinstance(recipe_data, list):
            recipe = recipe_data
        elif isinstance(recipe_data, dict):
            if "steps" in recipe_data:
                recipe = recipe_data["steps"]
            elif "tier1" in recipe_data:
                # Handle ADR-024 tiered assembly logic
                recipe = recipe_data["tier1"]
                if "tier2" in recipe_data:
                    recipe.extend(recipe_data["tier2"])
            else:
                # Fallback: maybe it's the raw included dict with !include tag (unlikely if ConfigManager was used)
                recipe = []

        for i in range(len(recipe) - 1, -1, -1):
            step = recipe[i]
            if step.get("action") == "sink_parquet":
                path = step.get("path")
                force = step.get("force_recompute", False)

                if path and os.path.exists(path) and not force:
                    # ADR-024 Refinement: Check for Stale Parquet
                    parquet_mtime = os.path.getmtime(path)

                    # Check manifest mtime (including its directory components)
                    manifest_dir = os.path.join(os.path.dirname(manifest_path),
                                                os.path.basename(manifest_path).replace(".yaml", ""))

                    # Heuristic: Find most recent mod time in manifest + logic dir
                    manifest_files = [manifest_path]
                    if os.path.exists(manifest_dir):
                        for root, _, files in os.walk(manifest_dir):
                            for f in files:
                                if f.endswith((".yaml", ".qmd", ".py")):
                                    manifest_files.append(
                                        os.path.join(root, f))

                    max_manifest_mtime = max(os.path.getmtime(f)
                                             for f in manifest_files)

                    if max_manifest_mtime > parquet_mtime:
                        print(
                            f"  ─── ⚠  Manifest has changed since last assembly. Invaliding Short-Circuit for {path}.")
                        step["force_recompute"] = True
                    else:
                        print(
                            f"  ─── 🗲  Short-Circuit: Existing Parquet branch found at {path}. Skipping early steps.")
                        consolidated_lf = pl.scan_parquet(path)
                        start_index = i + 1
                        break

        if not recipe and recipe_data:
            print(
                f"  └── ⚠️  Warning: Could not extract steps from recipe_data: {type(recipe_data)}")

        print(f"  └── 🏗️  Assembling using recipe: {len(recipe)} steps.")

        assembler = DataAssembler(ingredient_cache)
        try:
            consolidated_lf = assembler.assemble(recipe)
        except Exception as e:
            print(f"  └── ❌ Assembly Error: {e}")
            continue

        # c) Final Assembly Contract Guard (ADR-013)
        final_contract_data = assembly_info.get("final_contract", [])
        final_contract = {}

        if isinstance(final_contract_data, list):
            # Handle list of column names or list of dictionaries
            for item in final_contract_data:
                if isinstance(item, str):
                    final_contract[item] = None
                elif isinstance(item, dict):
                    # Take the first key (standard pattern for sequential list of dicts)
                    final_contract[list(item.keys())[0]] = list(
                        item.values())[0]
        elif isinstance(final_contract_data, dict):
            # If it's a dict and has 'output_fields', use that. Otherwise use the dict itself.
            if "output_fields" in final_contract_data:
                final_contract = final_contract_data["output_fields"]
            else:
                final_contract = final_contract_data

        if final_contract:
            # ADR-013 Projection with optional renaming
            projection = []
            for col_alias, col_info in final_contract.items():
                if isinstance(col_info, dict) and "original_name" in col_info:
                    projection.append(
                        pl.col(col_info["original_name"]).alias(col_alias))
                else:
                    projection.append(pl.col(col_alias))

            print(
                f"  └── 🛡️  Applying Final Contract Guard: {len(projection)} columns.")
            try:
                consolidated_lf = consolidated_lf.select(projection)
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
            if mat_path.endswith(".parquet"):
                df.write_parquet(mat_path)
                print(
                    f"  └── 💾 Materialized resulting assembly to PARQUET: {mat_path}")
            else:
                df.write_csv(mat_path, separator='\t')
                print(
                    f"  └── 💾 Materialized resulting assembly to TSV: {mat_path}")

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
