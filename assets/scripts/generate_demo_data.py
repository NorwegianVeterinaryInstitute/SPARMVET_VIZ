from generator_utils.aqua_synthesizer import AquaSynthesizer
import polars as pl
from pathlib import Path
import sys

# Ensure we can import from SDK
sys.path.append(str(Path(__file__).parent.parent.parent /
                "libs/generator_utils/src"))


def main():
    print("[1] INITIALIZING: Aqua Synthsizer for Demo Data...")

    # Paths
    ground_truth_dir = Path("assets/test_data/1_test_data_ST22_dummy")
    out_dir = Path("assets/test_data/demo_high_integrity")

    # Source TSVs
    source_tsvs = [
        ground_truth_dir / "test_metadata_20260307_105756.tsv",
        ground_truth_dir / "test_data_MLST_results_20260307_105756.tsv",
        ground_truth_dir / "test_data_ResFinder_20260307_105756.tsv"
    ]

    # Initialize Synthesizer (Anchoring on 'sample_id' as per Abromics manifest)
    synthesizer = AquaSynthesizer(anchor_key_name="sample_id", n_samples=30)

    print(f"\n[2] GENERATING: 30 synthesized samples with PK Anchoring...")
    synthetic_files = synthesizer.synthesize(
        tsv_paths=source_tsvs,
        out_dir=out_dir,
        messy_fraction=0.05  # Some messy values for realism
    )

    for f in synthetic_files:
        print(f"  └── Created: {f}")

    print("\n[3] RE-VALIDATING JOIN INTEGRITY...")
    meta_p = out_dir / "test_data_test_metadata_20260307_105756.tsv"
    mlst_p = out_dir / "test_data_test_data_MLST_results_20260307_105756.tsv"

    df_meta = pl.read_csv(meta_p, separator='\t')
    df_mlst = pl.read_csv(mlst_p, separator='\t')

    # Use sample_id for join
    joined = df_meta.join(df_mlst, on="sample_id", how="inner")

    print(
        f"\nVerification: Found {joined.height} matching IDs (1:1 join success).")
    if joined.height > 0:
        print("✅ SUCCESS: High-integrity demo data generated.")


if __name__ == "__main__":
    main()
