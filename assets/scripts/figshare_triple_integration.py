#!/usr/bin/env python3
"""
figshare_triple_integration.py
==============================
Stage 1: CSV → TSV conversion
Stage 2: 3-way left join (metadata anchor → phenotypes → genotypes)
Stage 3: glimpse + materialize to tmp/figshare_join_check.tsv

Usage:
    ./.venv/bin/python assets/scripts/figshare_triple_integration.py

HALT protocol: Stops after Stage 2 and writes to tmp/ for @verify.
"""

import sys
import os
import polars as pl
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CSV_DIR = PROJECT_ROOT / "assets" / "test_data" / "figshare.21737288" / "csv"
TSV_DEST = PROJECT_ROOT / "libs" / "transformer" / "tests" / "data"
TMP_DIR = PROJECT_ROOT / "tmp" / "integration"

TMP_DIR.mkdir(parents=True, exist_ok=True)
TSV_DEST.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "fg_metadata":   "fg_metadata.csv",
    "fg_phenotypes": "fg_phenotypes.csv",
    "fg_genotypes":  "fg_genotypes.csv",
}

# ---------------------------------------------------------------------------
# STAGE 1: CSV → TSV (separator conversion)
# ---------------------------------------------------------------------------
print("\n" + "="*60)
print("STAGE 1: CSV → TSV NORMALIZATION")
print("="*60)

lazy_frames = {}
for key, fname in SOURCES.items():
    src = CSV_DIR / fname
    dst = TSV_DEST / fname.replace(".csv", ".tsv")
    print(f"\n  [{key}] Reading {src.name} ...")
    lf = pl.scan_csv(src, separator=",", infer_schema_length=5000)
    # Materialize to TSV
    df = lf.collect()
    df.write_csv(dst, separator="\t")
    print(f"  → Written: {dst} ({df.shape[0]} rows × {df.shape[1]} cols)")
    lazy_frames[key] = pl.scan_csv(
        dst, separator="\t", infer_schema_length=5000)

print("\n  [DONE] All TSV files written to:", TSV_DEST)

# ---------------------------------------------------------------------------
# STAGE 1b: Drop redundant column from genotypes before join
# ---------------------------------------------------------------------------
print("\n" + "="*60)
print("STAGE 1b: DROP REDUNDANT COLUMN (host_animal_common from genotypes)")
print("="*60)

lf_meta = lazy_frames["fg_metadata"]
lf_pheno = lazy_frames["fg_phenotypes"]
lf_geno = lazy_frames["fg_genotypes"].drop("host_animal_common")

print("  Genotype columns after drop:", lf_geno.columns)

# Apply strip_whitespace and categorical casts where needed
# Metadata output contract
lf_meta = lf_meta.with_columns([
    pl.col("host_animal_common").cast(pl.Categorical),
    pl.col("animal_infection_site_uti").cast(pl.Categorical),
]).select(["sample_id", "host_animal_common", "specimen_source_tissue", "animal_infection_site_uti"])

# Phenotypes output contract
lf_pheno = lf_pheno.with_columns([
    pl.col("mic_id").cast(pl.Categorical),
    pl.col("breakpoint").cast(pl.Categorical),
    pl.col("phenotype").cast(pl.Categorical),
])

# Genotypes output contract
lf_geno = lf_geno.with_columns([
    pl.col("gene_name_family").str.strip_chars().cast(pl.Categorical),
    pl.col("resistance_class").str.strip_chars().cast(pl.Categorical),
]).select(["sample_id", "gene", "gene_name_family", "resistance_class"])

# ---------------------------------------------------------------------------
# STAGE 2: 3-WAY LEFT JOIN
# ---------------------------------------------------------------------------
print("\n" + "="*60)
print("STAGE 2: 3-WAY LEFT JOIN")
print("  Anchor: fg_metadata (991 samples)")
print("  Join 1: fg_phenotypes ON sample_id (left)")
print("  Join 2: fg_genotypes  ON sample_id (left)")
print("="*60)

# Step 1: metadata → phenotypes
lf_joined = lf_meta.join(lf_pheno, on="sample_id", how="left")
# Step 2: add genotypes
lf_joined = lf_joined.join(lf_geno, on="sample_id", how="left")

# ---------------------------------------------------------------------------
# STAGE 2: MATERIALIZE & GLIMPSE
# ---------------------------------------------------------------------------
print("\n  Collecting 3-way join (this may take a moment) ...")
df_full = lf_joined.collect()

out_path = TMP_DIR / "figshare_join_check.tsv"
df_full.write_csv(out_path, separator="\t")

print("\n" + "="*60)
print("GLIMPSE (first 10 rows, schema summary)")
print("="*60)
print(f"\n  Total shape: {df_full.shape[0]:,} rows × {df_full.shape[1]} cols")
print(f"  Written to: {out_path}\n")

# Manual glimpse (polars .glimpse equivalent)
for col in df_full.columns:
    col_series = df_full[col]
    n_null = col_series.null_count()
    sample_vals = col_series.drop_nulls().head(3).to_list()
    print(f"  {col:<35} dtype={str(col_series.dtype):<20} n_null={n_null:<5} sample={sample_vals}")

print("\n" + "="*60)
print("UNIQUE COUNTS (key columns)")
print("="*60)
print(f"  Unique sample_ids:       {df_full['sample_id'].n_unique()}")
print(
    f"  Unique mic_ids:          {df_full['mic_id'].n_unique()}" if 'mic_id' in df_full.columns else "")
print(
    f"  Unique gene_name_family: {df_full['gene_name_family'].n_unique()}" if 'gene_name_family' in df_full.columns else "")
print(
    f"  Unique resistance_class: {df_full['resistance_class'].n_unique()}" if 'resistance_class' in df_full.columns else "")
print(f"  Unique host_animal:      {df_full['host_animal_common'].n_unique()}")

print("\n" + "="*60)
print("🛑 HALT — Data ready at: tmp/integration/figshare_join_check.tsv")
print("         Waiting for @verify before proceeding to Stage 3 (plots).")
print("="*60)
