#!/usr/bin/env python3
from libs.ingestion.src.ingestor import DataIngestor
from libs.utils.src.config_loader import ConfigManager
import sys
import argparse
from pathlib import Path

# Add project root to PYTHONPATH
root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(root_dir))


def test_ingestion(manifest_path: str, data_dir: str):
    """
    A developer utility for the Ingestion layer. 
    It tests loading data from disk and comparing raw columns to the declared _fields schema.
    It DOES NOT execute data wrangling (Transformer layer).
    """
    print(f"\n[{'*'*40}]")
    print(f" TESTING INGESTION LAYER")
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

        # 1. Use the official Ingestor to load the data
        try:
            lf, tsv_path = ingestor.ingest(dataset_name, definitions)
            print(f"  └── 📥 Successfully ingested {tsv_path.name}")
        except FileNotFoundError as e:
            print(f"  └── ⚠️ {e}")
            continue
        except Exception as e:
            print(f"  └── ❌ {e}")
            continue

        # 2. Validation preview against defined fields
        fields_schema = definitions.get("fields", {})
        raw_cols = lf.columns
        print(
            f"  └── Found {len(raw_cols)} columns on disk vs {len(fields_schema)} declared in YAML.")

        # 3. Preview Data (Raw)
        print("\n  [RAW INGESTED PREVIEW:]")
        print(lf.head(5).collect())
        print("\n" + "-"*40)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Dashboard Ingestion.")
    parser.add_argument("--yaml", type=str, required=True,
                        help="Path to the master manifest YAML file.")
    parser.add_argument("--data", type=str, required=True,
                        help="Path to the folder containing the raw TSV files.")

    args = parser.parse_args()
    test_ingestion(args.yaml, args.data)
