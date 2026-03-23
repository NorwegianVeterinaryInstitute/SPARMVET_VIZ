#!/usr/bin/env python3
from libs.transformer.src.data_wrangler import DataWrangler
from libs.utils.src.config_loader import ConfigManager
import sys
import argparse
from pathlib import Path
import polars as pl
from libs.ingestion.src.ingestor import DataIngestor

# Add project root to PYTHONPATH
root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(root_dir))


def test_wrangler(manifest_path: str, data_dir: str):
    """
    A developer utility for the Transformer layer.
    Preview the effect of `_wrangling.yaml` rules on the data.
    """
    print(f"\n[{'*'*40}]")
    print(f" PREVIEWING TRANSFORMER (WRANGLING) LAYER")
    print(f"[{'*'*40}]\n")

    try:
        config = ConfigManager(manifest_path)
    except Exception as e:
        print(f"❌ Failed to load manifest configuration: {e}")
        sys.exit(1)

    schemas = config.get_data_schemas()
    if not schemas:
        print("❌ No 'data_schemas' found in the configuration.")
        sys.exit(1)

    try:
        ingestor = DataIngestor(data_dir)
    except Exception as e:
        print(f"❌ Failed to initialize DataIngestor: {e}")
        sys.exit(1)

    for dataset_name, definitions in schemas.items():
        print(f"\n[{dataset_name.upper()}]")

        # Official Ingestion Layer
        try:
            lf, tsv_path = ingestor.ingest(dataset_name, definitions)
            print(f"  └── 📥 Read raw dataset: {tsv_path.name}")
        except FileNotFoundError as e:
            print(f"  └── ⚠️ {e}")
            continue
        except Exception as e:
            print(f"  └── ❌ Failed to ingest: {e}")
            continue

        # Execute TRANSFORMER Layer
        wrangling_rules = definitions.get("wrangling", [])
        if wrangling_rules:
            print(
                f"  └── ⚙️  Found {len(wrangling_rules)} wrangling actions. Applying...")
            try:
                fields_schema = definitions.get("fields", {})
                wrangler = DataWrangler(fields_schema)
                lf = wrangler.apply_wrangling_rules(lf, wrangling_rules)
                print(f"  └── ✅  Wrangling rules applied successfully!")
            except Exception as e:
                print(f"  └── ❌ Wrangling Execution Failed: {e}")
                import traceback
                traceback.print_exc()
                continue
        else:
            print(f"  └── ℹ️  No wrangling actions defined.")

        print("\n  [TRANSFORMED TABLE PREVIEW:]")
        print(lf.head(5).collect())
        print("\n" + "-"*40)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test Dashboard Data Wrangler.")
    parser.add_argument("--yaml", type=str, required=True,
                        help="Path to the master manifest YAML file.")
    parser.add_argument("--data", type=str, required=True,
                        help="Path to the folder containing the raw TSV files.")

    args = parser.parse_args()
    test_wrangler(args.yaml, args.data)
