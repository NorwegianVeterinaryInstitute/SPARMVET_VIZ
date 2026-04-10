import polars as pl
from transformer.data_wrangler import DataWrangler
from utils.errors import TransformationError


def test_typo_error():
    print("Testing Typo Detection in WrangleStudio...")
    df = pl.DataFrame({"sample_id": [1], "species": ["E. coli"]})
    wrangler = DataWrangler(
        {"sample_id": {"is_primary_key": True}, "species": {}})

    # Intentional typo in column name: 'specie' instead of 'species'
    rules = [{"action": "fill_nulls", "columns": ["specie"], "value": "Unknown"}]

    try:
        wrangler.run(df.lazy(), rules)
    except TransformationError as e:
        print(f"✅ Caught Expected Error: {e.message}")
        print(f"💡 Tip: {e.tip}")
    except Exception as e:
        print(f"❌ Caught Unexpected Error: {type(e).__name__}: {e}")


if __name__ == "__main__":
    test_typo_error()
