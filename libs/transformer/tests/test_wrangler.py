#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path
import polars as pl

# Ensure the project root is in PYTHONPATH
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Using dynamic import inside a wrapper to bypass mandatory import auto-sorting
# that happens in certain IDE/environment hooks, which breaks the path setup above.


def _dynamic_imports():
    from libs.transformer.src.data_wrangler import DataWrangler
    from libs.utils.src.config_loader import ConfigManager
    return DataWrangler, ConfigManager


def run_test_wrangler(data_path: str, manifest_path: str, output_path: str):
    """
    Universal Wrangler Runner (ADR 005 compliant).
    Agnostically loads any --data (tsv/csv) and any --manifest (yaml),
    applies the wrangling rules, and saves the output.
    """
    DataWrangler, ConfigManager = _dynamic_imports()

    print(f"\n[{'*'*40}]")
    print(f" 🚀 UNIVERSAL WRANGLER RUNNER")
    print(f"[{'*'*40}]\n")

    # 1. Load Data
    try:
        data_p = Path(data_path)
        if not data_p.exists():
            raise FileNotFoundError(f"Data file not found: {data_path}")

        # Determine separator based on extension; default to TSV per ADR-002
        separator = '\t' if data_p.suffix == '.tsv' else ','
        lf = pl.scan_csv(data_path, separator=separator,
                         null_values=["null", "NA", ""])
        print(f"  └── 📥 Loaded Data: {data_p.name} (separator: '{separator}')")
    except Exception as e:
        print(f"  └── ❌ Data Load Failed: {e}")
        sys.exit(1)

    # 2. Load Manifest & Identify Schema
    try:
        config = ConfigManager(manifest_path)
        data_schemas = config.get_data_schemas()

        if not data_schemas:
            # Fallback if the YAML structure is flat
            raw_yaml = config.raw_config
            if "wrangling" in raw_yaml:
                definitions = raw_yaml
            else:
                raise ValueError(
                    "No 'data_schemas' or top-level 'wrangling' found in manifest.")
        else:
            # Dynamically identify the first schema definition in the manifest
            dataset_id = next(iter(data_schemas))
            definitions = data_schemas[dataset_id]
            print(f"  └── 📜 Using Schema: {dataset_id}")

    except Exception as e:
        print(f"  └── ❌ Manifest Load Failed: {e}")
        sys.exit(1)

    # 3. Initialize Wrangler and Apply Rules
    try:
        wrangling_rules = definitions.get("wrangling", [])
        fields_schema = definitions.get("fields", {})

        if not wrangling_rules:
            print(f"  └── ℹ️  No wrangling actions defined.")
            lf_result = lf
        else:
            print(
                f"  └── ⚙️  Applying {len(wrangling_rules)} wrangling actions...")
            wrangler = DataWrangler(fields_schema)
            # Apply rules using the vectorized multi-column architecture
            lf_result = wrangler.apply_wrangling_rules(lf, wrangling_rules)
            print(f"  └── ✅  Wrangling complete.")
    except Exception as e:
        print(f"  └── ❌ Transformation Failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 4. Materialize and save output
    try:
        df = lf_result.collect()
        output_p = Path(output_path)
        output_p.parent.mkdir(parents=True, exist_ok=True)

        # Respect output extension        # Output MUST be TSV per Project Rule (ADR 002)
        df.write_csv(output_path, separator="\t", include_header=True)
        print(f"  └── 💾 Saved Result: {output_path} (TSV format enforced)")
    except Exception as e:
        print(f"  └── ❌ Save Failed: {e}")
        sys.exit(1)

    # 5. Evidence & Inspection
    print("\n  [TRANSFORMED DATA GLIMPSE:]")
    print(df.glimpse())
    print("\n" + "-"*40)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Universal Wrangler Runner (ADR 005)")
    parser.add_argument("--data", type=str, required=True,
                        help="Path to raw .tsv or .csv data.")
    parser.add_argument("--manifest", type=str, required=True,
                        help="Path to manifest .yaml.")
    parser.add_argument("--output", type=str, required=True,
                        help="Path to save the result.")

    args = parser.parse_args()
    run_test_wrangler(args.data, args.manifest, args.output)
