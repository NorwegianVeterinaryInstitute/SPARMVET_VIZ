from utils.errors import ManifestError
from transformer.metadata_validator import MetadataValidator
from transformer.actions.persistence.anchor import action_sink_parquet
from transformer.data_assembler import DataAssembler
import polars as pl
import os
import sys
from pathlib import Path

# Setup Path
project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
# STRICT BAN: sys.path.append / sys.path.insert are explicitly forbidden. Rely on pip install -e.


def test_hashing_and_shortcircuit():
    print("🧪 Testing Decision Metadata Hashing...")

    # Mock data
    df = pl.DataFrame({"sample_id": ["S1", "S2"], "val": [1, 2]}).lazy()
    ingredients = {"test_ds": df}

    parquet_path = "tmp/phase3_test_hash.parquet"
    if os.path.exists(parquet_path):
        os.remove(parquet_path)

    recipe = [
        {"action": "sink_parquet", "path": parquet_path, "force_recompute": False}
    ]

    # 1. First run: Should materialize
    assembler = DataAssembler(ingredients)
    print("▶ Run 1 (Initial Materialization)")
    assembler.assemble(recipe)

    # Check if hash is in metadata
    from utils.hashing import get_parquet_metadata_hash
    h1 = get_parquet_metadata_hash(parquet_path)
    print(f"✅ Metadata Hash found: {h1}")

    # 2. Second run: Same recipe, should short-circuit
    print("\n▶ Run 2 (Same Recipe - Expect Short-Circuit)")
    # We should see the log message from DataAssembler
    assembler.assemble(recipe)

    # 3. Third run: Modified recipe, should invalidate cache
    print("\n▶ Run 3 (Recipe Change - Expect Cache Invalidation)")
    recipe_new = [
        {"action": "filter_eq", "column": "sample_id", "value": "S1"},
        {"action": "sink_parquet", "path": parquet_path, "force_recompute": False}
    ]
    assembler.assemble(recipe_new)


def test_malformed_gatekeeping():
    print("\n🧪 Testing Malformed Data Gatekeeping (ADR-034)...")

    # Data with 'sample_id'
    df = pl.DataFrame({"sample_id": ["S1"], "value": [10]}).lazy()

    # Manifest with typo 'sample_idd'
    contract = {"sample_idd": {"type": "string"}}

    validator = MetadataValidator()
    try:
        validator.validate(df, contract, context="TestDataset")
    except ManifestError as e:
        print(f"✅ Caught expected error: {e}")
        if "Hint: Did you mean ['sample_id']" in str(e.tip):
            print("✅ Typo suggestion verified!")
        else:
            print(f"❌ Typo suggestion missing or wrong. Tip was: {e.tip}")


if __name__ == "__main__":
    test_hashing_and_shortcircuit()
    test_malformed_gatekeeping()
