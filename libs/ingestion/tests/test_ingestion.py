#!/usr/bin/env python3
from libs.utils.src.loader2 import ConfigManager
import sys
import argparse
from pathlib import Path
import polars as pl

# Add project root to PYTHONPATH
root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(root_dir))


def test_ingestion(manifest_path: str, data_dir: str):
    """
    A developer utility for visualizing the effect of _wrangling.yaml instructions
    on the raw datasets using Polars.
    """
    print(f"\n[{'*'*40}]")
    print(f" PREVIEWING INGESTION & WRANGLING")
    print(f"[{'*'*40}]\n")

    try:
        config = ConfigManager(manifest_path)
    except Exception as e:
        print(f"❌ Failed to load manifest configuration: {e}")
        sys.exit(1)

    schemas = config.data.get("data_schemas", {})
    if not schemas:
        print("❌ No 'data_schemas' found in the configuration.")
        sys.exit(1)

    base_data_path = Path(data_dir)

    for dataset_name, definitions in schemas.items():
        print(f"\n[{dataset_name.upper()}]")

        # 1. Attempt to find matching TSV file
        # We assume the user has a TSV file matching the dataset name, e.g., "ResFinder.tsv"
        tsv_path = base_data_path / f"{dataset_name}.tsv"
        if not tsv_path.exists():
            # If standard name isn't found, try to find any file that contains the name
            potential_files = list(
                base_data_path.glob(f"*{dataset_name}*.tsv"))
            if potential_files:
                tsv_path = potential_files[0]
                print(
                    f"  └── Note: Discovered approximate file: {tsv_path.name}")
            else:
                print(
                    f"  └── ⚠️ Could not find a matching .tsv file for {dataset_name} in {data_dir}. Skipping.")
                continue

        # 2. Open LazyFrame
        try:
            lf = pl.scan_csv(tsv_path, separator="\t")
        except Exception as e:
            print(f"  └── ❌ Failed to read TSV: {e}")
            continue

        print(f"  └── Successfully loaded {tsv_path.name}")

        # 3. Check for wrangling rules
        wrangling_rules = definitions.get("wrangling", [])
        if wrangling_rules:
            print(f"  └── Found {len(wrangling_rules)} wrangling actions.")
            print(
                f"  └── (Wrangler execution engine is pending implementation - Previewing RAW for now.)")
        else:
            print(f"  └── No wrangling actions defined.")

        # 4. Preview Table
        print("\n  [TABLE PREVIEW:]")
        print(lf.head(5).collect())
        print("\n" + "-"*40)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Preview DataFrame outputs after Data Contract ingestion.")
    parser.add_argument("--yaml", type=str, required=True,
                        help="Path to the master manifest YAML file.")
    parser.add_argument("--data", type=str, required=True,
                        help="Path to the folder containing the raw TSV files.")

    args = parser.parse_args()
    test_ingestion(args.yaml, args.data)
