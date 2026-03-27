#!/usr/bin/env python3
import argparse
import os
import sys
import polars as pl
from pathlib import Path

# Ensure paths are correct (Rule 5: Use ./.venv/bin/python)
# We assume the script is executed from the project root.
project_root = os.getcwd()
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# ADR-016: Use Package-First Authority
try:
    from ingestion.ingestor import DataIngestor
    from utils.config_loader import ConfigManager
    from transformer.data_wrangler import DataWrangler
except ImportError as e:
    print(f"ERROR: Could not import core libraries. Check .venv install. {e}")
    sys.exit(1)


def debug_wrangle(manifest_path: str):
    """
    Reworked Wrangle Debugger (v2) based on ADR-013, ADR-014, and ADR-015.
    """
    if not os.path.exists(manifest_path):
        print(f"ERROR: Manifest not found at {manifest_path}")
        return

    # 1. Load Manifest (handles !include)
    print(f"Loading manifest: {manifest_path}")
    try:
        manager = ConfigManager(manifest_path)
        config = manager.raw_config
    except Exception as e:
        print(f"ERROR: Failed to load manifest or its includes: {e}")
        return

    # 2. Extract Dataset Blocks
    # Determine if it's a Combined Pipeline Manifest or a Standalone Dataset Manifest
    dataset_blocks = {}

    # Check for direct blocks (Standalone)
    if "input_fields" in config:
        # Standalone
        dataset_id = config.get("id") or config.get(
            "name") or Path(manifest_path).stem
        dataset_blocks[dataset_id] = config
    else:
        # Combined (Pipeline style)
        # Search in standard containers
        for group_key in ["data_schemas", "metadata_schema", "additional_datasets_schemas"]:
            group_data = config.get(group_key, {})
            if isinstance(group_data, dict) and group_data:
                # metadata_schema is often a direct block, not a dict of blocks
                if group_key == "metadata_schema" and "input_fields" in group_data:
                    dataset_blocks["metadata_schema"] = group_data
                else:
                    dataset_blocks.update(group_data)

    if not dataset_blocks:
        print(
            f"ERROR: No valid dataset blocks (with input_fields) found in {manifest_path}")
        return

    # 3. Setup Ingestor (using project assets as base)
    ingestor = DataIngestor(data_dir=os.path.join(project_root, "assets"))

    print(f"Found {len(dataset_blocks)} dataset(s) to process.")
    print("-" * 40)

    for dataset_id, schema in dataset_blocks.items():
        if not isinstance(schema, dict) or "input_fields" not in schema:
            continue

        print(f"\n[TARGET: {dataset_id}]")

        # a) Ingest Raw Data (ADR-015 compliant)
        try:
            lf, tsv_path = ingestor.ingest(dataset_id, schema)
            print(f"  └── 📥 Load: {tsv_path}")
        except FileNotFoundError as e:
            print(f"  └── ❌ Skipping: {e}")
            continue
        except Exception as e:
            print(f"  └── ❌ Ingestion failure: {e}")
            continue

        # ADR-013/ADR-014 block resolution (handling nested includes)
        input_fields = schema.get("input_fields", {})
        if isinstance(input_fields, dict) and "input_fields" in input_fields:
            input_fields = input_fields["input_fields"]

        wrangling_rules = schema.get("wrangling", [])
        if isinstance(wrangling_rules, dict) and "wrangling" in wrangling_rules:
            wrangling_rules = wrangling_rules["wrangling"]

        output_fields_manifest = schema.get("output_fields", {})
        if isinstance(output_fields_manifest, dict) and "output_fields" in output_fields_manifest:
            output_fields_manifest = output_fields_manifest["output_fields"]

        # b) Execute Wrangling Actions
        if not wrangling_rules:
            print("  └── ⚡ Identity Mode: Bypassing wrangling block (ADR-014).")
            transformed_lf = lf
        else:
            wrangler = DataWrangler(input_fields)
            try:
                transformed_lf = wrangler.run(lf, wrangling_rules)
                print(
                    f"  └── 🛠️  Wrangling: Applied {len(wrangling_rules)} actions.")
            except Exception as e:
                print(f"  └── ❌ Wrangling Error: {e}")
                continue

        # c) Final Guard Contract (output_fields .select())
        if not output_fields_manifest:
            # ADR-014: Retain all columns if output_fields is empty
            print("  └── ⚡ Identity Mode: Retaining all columns (ADR-014).")
        else:
            # output_fields is a dictionary of the final contract
            target_columns = list(output_fields_manifest.keys())
            print(
                f"  └── 🛡️  Contract Guard: Selecting {len(target_columns)} columns...")
            try:
                transformed_lf = transformed_lf.select(target_columns)
            except Exception as e:
                print(f"  └── ❌ Contract Mismatch: {e}")
                # print(f"      Available: {transformed_lf.collect_schema().names()}")
                continue

        # d) Sink to tmp (Materialize)
        output_tsv = os.path.join(project_root, f"tmp/{dataset_id}_debug.tsv")
        os.makedirs(os.path.dirname(output_tsv), exist_ok=True)
        try:
            # Materialize LazyFrame for inspection
            transformed_lf.collect().write_csv(output_tsv, separator='\t')
            print(f"  └── 💾 Materialized resulting LazyFrame to: {output_tsv}")
        except Exception as e:
            print(f"  └── ❌ Materialization Error: {e}")
            continue

        # e) Final columns report
        final_cols = transformed_lf.collect_schema().names()
        print(f"  └── ✅ Final Result: {len(final_cols)} columns retained.")
        print(f"  └── 📊 Columns: {final_cols}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Wrangle Debugger v2 (ADR-013/14/15)")
    parser.add_argument("--manifest", required=True,
                        help="Path to YAML manifest (Pipeline or Standalone)")
    args = parser.parse_args()
    debug_wrangle(args.manifest)
