#!/usr/bin/env python3
from libs.transformer.src.data_wrangler import DataWrangler
import sys
import argparse
from pathlib import Path
import polars as pl
import yaml
import os

# Add project root to PYTHONPATH
root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(root_dir))


def run_contract_test(manifest_path: str, data_path: str):
    """
    Executes a specific contract test as per the verification_protocol.md.
    """
    manifest_name = Path(manifest_path).stem
    action_name = manifest_name.replace("_manifest", "")

    print(f"\n[CONTRACT TEST: {action_name.upper()}]")
    print("-" * 40)

    # Load manifest
    try:
        with open(manifest_path, 'r') as f:
            manifest = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Failed to load manifest: {e}")
        return

    wrangling_rules = manifest.get("wrangling", [])

    # Load data
    try:
        lf = pl.scan_csv(data_path)
    except Exception as e:
        print(f"❌ Failed to load test data: {e}")
        return

    # Execute Wrangler
    # For contract tests, we use an empty fields_schema
    wrangler = DataWrangler({})
    try:
        transformed_lf = wrangler.apply_wrangling_rules(lf, wrangling_rules)
        df = transformed_lf.collect()

        # Mandatory Console Glimpse
        print("\n--- [CONSOLE GLIMPSE] ---")
        # Polars glimpse() prints directly.
        # Using print(df.glimpse()) to ensure capture.
        print(df.glimpse(return_as_string=True))
        print("--------------------------\n")

        # Evidence Generation
        # Ensure /tmp/ and project-specific tmp/ both exist?
        # Protocol says tmp/{{ACTION_NAME}}_debug_view.csv (usually project root/tmp)
        tmp_dir = root_dir / "tmp"
        tmp_dir.mkdir(exist_ok=True)

        debug_file = tmp_dir / f"{action_name}_debug_view.csv"
        user_debug_file = tmp_dir / "USER_debug_view.csv"

        df.write_csv(str(debug_file))
        df.write_csv(str(user_debug_file))

        print(f"✅ Evidence generated:")
        print(f"  └── {debug_file}")
        print(f"  └── {user_debug_file}")

    except Exception as e:
        print(f"❌ Execution failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Verification Protocol Runner")
    parser.add_argument("--manifest", type=str,
                        help="Path to the test manifest YAML")
    parser.add_argument("--csv", type=str, help="Path to the test CSV data")

    args = parser.parse_args()

    if args.manifest and args.csv:
        run_contract_test(args.manifest, args.csv)
    else:
        print("Usage: python test_wrangler.py --manifest <yaml> --csv <csv>")
