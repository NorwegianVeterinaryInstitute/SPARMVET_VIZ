#!/usr/bin/env python3
import os
import sys
import datetime
import argparse
from pathlib import Path
import polars as pl

# Ensure project root is in sys.path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root / "libs" / "ingestion" / "src"))

try:
    from ingestion.ingestor import DataIngestor
except ImportError as e:
    print(f"❌ ERROR: [Ingestion Suite] Failed to load DataIngestor. {e}")
    sys.exit(1)


def run_suite(output_dir: Path):
    os.makedirs(output_dir, exist_ok=True)
    report_path = output_dir / "ingestion_integrity_report.txt"

    report_lines = []

    def log(msg: str):
        print(msg)
        report_lines.append(msg)

    log(f"[{'='*60}]")
    log(f" 🛡️  INGESTION MASTER INTEGRITY SUITE")
    log(f" Date: {datetime.datetime.now().isoformat()}")
    log(f"[{'='*60}]\n")

    # Setup test data
    test_tsv = output_dir / "test_data.tsv"
    with open(test_tsv, "w") as f:
        f.write("Raw_ID\tValue\n1\t100\n2\t200\n")

    test_parquet = output_dir / "test_data.parquet"
    pl.DataFrame({"Raw_ID": [3, 4], "Value": [300, 400]}
                 ).write_parquet(test_parquet)

    ingestor = DataIngestor(str(output_dir))

    # Test Case 1: Legacy Discovery (TSV)
    log("🧪 Test 1: Legacy Discovery (TSV)")
    try:
        lf, path = ingestor.ingest("test_data", {})
        df = lf.collect()
        if len(df) == 2 and "Raw_ID" in df.columns:
            log("🟢 PASSED: Loaded TSV via discovery")
        else:
            log(f"🔴 FAILED: Unexpected data {df.columns}")
    except Exception as e:
        log(f"🔴 FAILED: {e}")

    # Test Case 2: Explicit Source (TSV)
    log("🧪 Test 2: Explicit Source (TSV)")
    schema = {
        "source": {"type": "local_tsv", "path": str(test_tsv)},
        "input_fields": {
            "id": {"original_name": "Raw_ID", "type": "numeric"}
        }
    }
    try:
        lf, path = ingestor.ingest("explicit_test", schema)
        df = lf.collect()
        if "id" in df.columns and df["id"].dtype == pl.Float64:
            log("🟢 PASSED: Renamed and Cast (numeric)")
        else:
            status = "N/A"
            if "id" in df.columns:
                status = str(df["id"].dtype)
            log(f"🔴 FAILED: {df.columns} / {status}")
    except Exception as e:
        log(f"🔴 FAILED: {e}")

    # Test Case 3: Explicit Source (Parquet)
    log("🧪 Test 3: Explicit Source (Parquet)")
    schema_pq = {
        "source": {"type": "local_parquet", "path": str(test_parquet)},
        "input_fields": {
            "id": {"original_name": "Raw_ID", "type": "categorical"}
        }
    }
    try:
        lf, path = ingestor.ingest("parquet_test", schema_pq)
        df = lf.collect()
        if "id" in df.columns and (df["id"].dtype == pl.String or df["id"].dtype == pl.Categorical):
            log("🟢 PASSED: Loaded Parquet and Cast (categorical)")
        else:
            log(f"🔴 FAILED: {df.columns} / {df['id'].dtype}")
    except Exception as e:
        log(f"🔴 FAILED: {e}")

    # Test Case 4: Case-Insensitive Rename
    log("🧪 Test 4: Case-Insensitive Rename")
    schema_ci = {
        "input_fields": {
            "val": {"original_name": "value"}  # 'Value' in file
        }
    }
    try:
        lf, path = ingestor.ingest("test_data", schema_ci)
        df = lf.collect()
        if "val" in df.columns:
            log("🟢 PASSED: Case-insensitive match success")
        else:
            log(f"🔴 FAILED: {df.columns}")
    except Exception as e:
        log(f"🔴 FAILED: {e}")

    log(f"\n[{'='*60}]")
    log(" ✅ Ingestion Integrity Check Complete.")
    log(f"[{'='*60}]")

    with open(report_path, "w") as f:
        f.write("\n".join(report_lines))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", type=str,
                        default="tmp/ingestion_integrity")
    args = parser.parse_args()
    run_suite(Path(args.output_dir))
