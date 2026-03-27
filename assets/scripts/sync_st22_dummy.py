import polars as pl
from pathlib import Path


def sync():
    root = Path(".")
    meta_path = root / "assets/test_data/1_test_data_ST22_dummy/test_metadata_20260307_105756.tsv"
    mlst_path = root / \
        "assets/test_data/1_test_data_ST22_dummy/test_data_MLST_results_20260307_105756.tsv"
    vir_path = root / "assets/test_data/2_VIGAS-P_ST22_dummy/test_data_VIGAS_VirulenceFinder_20260307_105756.tsv"

    # 1. Read metadata IDs
    meta_df = pl.read_csv(meta_path, separator='\t')
    meta_ids = meta_df["sample_id"].to_list()
    print(f"Loaded {len(meta_ids)} IDs from metadata.")

    # 2. Sync MLST (Ensure it matches metadata IDs if not already)
    mlst_df = pl.read_csv(mlst_path, separator='\t')
    # If lengths differ, we truncate mlst or metadata, but usually they are 43 rows both.
    n = min(len(meta_ids), len(mlst_df))
    mlst_df = mlst_df.head(n).with_columns(
        pl.Series("sample_id", meta_ids[:n]))
    mlst_df.write_csv(mlst_path, separator='\t')
    print(f"Synced {n} IDs into MLST results.")

    # 3. Sync VirulenceFinder and make it LONG format
    vir_df = pl.read_csv(vir_path, separator='\t')

    # We want to take meta_ids and match them to vir_df rows.
    # To make it 'long', we explode the gene column.
    # Note: Current vir_df has one row per sample with comma-sep genes.

    # First, replace sample_id 1:1 if possible
    m = min(len(meta_ids), len(vir_df))
    vir_df = vir_df.head(m).with_columns(pl.Series("sample_id", meta_ids[:m]))

    # Now Explode virulence genes to make it long format
    # The column name is 'virulence_finder_virulencegenes_proteinname'
    gene_col = "virulence_finder_virulencegenes_proteinname"
    long_vir_df = (
        vir_df.with_columns(pl.col(gene_col).str.split(","))
        .explode(gene_col)
        .with_columns(pl.col(gene_col).str.strip_chars())
    )

    # Save as TSV
    long_vir_df.write_csv(vir_path, separator='\t')
    print(
        f"Synced {m} IDs into VirulenceFinder and converted to LONG format ({len(long_vir_df)} rows).")


if __name__ == "__main__":
    sync()
