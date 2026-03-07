#!/usr/bin/env python3
import argparse
import polars as pl
import numpy as np
import random
from pathlib import Path
from datetime import datetime


def generate_fake_column(series: pl.Series, n_rows: int) -> pl.Series:
    """Generates synthetic data matching the type and distribution of a polar series."""
    dtype = series.dtype
    if dtype in [pl.Int32, pl.Int64]:
        min_val, max_val = series.min(), series.max()
        return pl.Series(series.name, np.random.randint(min_val, max_val + 1, size=n_rows))
    elif dtype in [pl.Float32, pl.Float64]:
        min_val, max_val = series.min(), series.max()
        return pl.Series(series.name, np.random.uniform(min_val, max_val, size=n_rows))
    elif dtype in [pl.Date, pl.Datetime]:
        min_val, max_val = series.min(), series.max()
        # Fallback if nulls make min/max None
        if min_val is None or max_val is None:
            return pl.Series(series.name, [None] * n_rows)
        min_ts = int(min_val.strftime("%s")) if hasattr(
            min_val, 'strftime') else min_val
        max_ts = int(max_val.strftime("%s")) if hasattr(
            max_val, 'strftime') else max_val
        random_timestamps = np.random.randint(min_ts, max_ts, size=n_rows)
        if dtype == pl.Date:
            return pl.Series(series.name, [datetime.fromtimestamp(ts).date() for ts in random_timestamps])
        else:
            return pl.Series(series.name, [datetime.fromtimestamp(ts) for ts in random_timestamps])
    elif dtype in [pl.Boolean]:
        return pl.Series(series.name, np.random.choice([True, False], size=n_rows))
    else:
        # Categorical / String
        unique_vals = series.drop_nulls().unique().to_list()
        if not unique_vals:
            unique_vals = ["unknown"]
        return pl.Series(series.name, np.random.choice(unique_vals, size=n_rows))


def introduce_missing_values(df: pl.DataFrame, missing_fraction=0.1) -> pl.DataFrame:
    """Randomly injects null values and messy strings into the dataframe to test fail-fast systems."""
    exprs = []

    # Common real-world messy strings for categorical/character data
    messy_strings = [None, "-", "unknown", "N/A", "not found", "None", ""]

    for col in df.columns:
        series = df[col]
        dtype = series.dtype

        # Create a boolean mask for rows to affect
        mask = pl.Series(np.random.rand(df.height) < missing_fraction)

        if dtype in [pl.Categorical, pl.String, pl.Utf8]:
            # For strings, inject a random mix of messy values
            random_messy = pl.Series(
                np.random.choice(messy_strings, size=df.height))
            expr = pl.when(mask).then(random_messy).otherwise(
                pl.col(col)).alias(col)
        else:
            # For dates/numerics, inject pure system nulls
            expr = pl.when(mask).then(None).otherwise(pl.col(col)).alias(col)

        exprs.append(expr)

    return df.with_columns(exprs)


def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic, anonymized test data from real datasets.")
    parser.add_argument("--data_file", required=True,
                        help="Path to real data file.")
    parser.add_argument("--metadata_file", required=False,
                        help="Path to real metadata file.")
    parser.add_argument("--primary_key_data", required=True,
                        help="Primary key column in the data file.")
    parser.add_argument("--primary_key_metadata", required=False,
                        help="Primary key column in the metadata file.")
    parser.add_argument("--mismatches", action="store_true",
                        help="Introduce mismatched primary keys.")
    parser.add_argument("--missing_values", action="store_true",
                        help="Randomly drop values (NA/null) into the data.")
    args = parser.parse_args()

    # Create output directory
    out_dir = Path("assets/test_data")
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 1. Process Main Data
    try:
        # Try TSV first, fallback to CSV if user passed original CSV.
        df_real = pl.read_csv(
            args.data_file, separator='\t' if args.data_file.endswith('.tsv') else ',')
    except Exception as e:
        print(f"Error reading {args.data_file}: {e}")
        return

    n_rows = df_real.height
    fake_data_cols = []

    # Generate fake primary keys
    fake_ids = [f"fake_id_{i:04d}" for i in range(1, n_rows + 1)]

    for col in df_real.columns:
        if col == args.primary_key_data:
            fake_data_cols.append(pl.Series(col, fake_ids))
        else:
            fake_data_cols.append(generate_fake_column(df_real[col], n_rows))

    df_fake = pl.DataFrame(fake_data_cols)

    if args.missing_values:
        print("Injecting missing values...")
        df_fake = introduce_missing_values(df_fake, 0.05)

    data_out_path = out_dir / f"test_data_{timestamp}.tsv"
    df_fake.write_csv(data_out_path, separator='\t')
    print(f"Created synthetic main data: {data_out_path}")

    # 2. Process Metadata if requested
    if args.metadata_file and args.primary_key_metadata:
        try:
            df_meta = pl.read_csv(
                args.metadata_file, separator='\t' if args.metadata_file.endswith('.tsv') else ',')
        except Exception as e:
            print(f"Error reading {args.metadata_file}: {e}")
            return

        m_rows = df_meta.height
        fake_meta_cols = []

        # Determine IDs for metadata
        # By default, match the generated fake_ids to ensure valid joins
        m_rows_int = int(m_rows)
        meta_ids = [fake_ids[i] for i in range(min(len(fake_ids), m_rows_int))]
        if len(meta_ids) < m_rows_int:
            # If metadata is larger than main data
            meta_ids.extend([f"fake_id_{i:04d}" for i in range(
                n_rows + 1, n_rows + 1 + (m_rows - len(meta_ids)))])

        if args.mismatches:
            print("Introducing mismatched primary keys...")
            # Shift the slice to break the join for 20% of the metadata
            shift = max(1, int(m_rows * 0.2))
            meta_ids = [f"fake_id_{i:04d}" for i in range(
                1 + shift, m_rows + 1 + shift)]

        for col in df_meta.columns:
            if col == args.primary_key_metadata:
                fake_meta_cols.append(pl.Series(col, meta_ids))
            else:
                fake_meta_cols.append(
                    generate_fake_column(df_meta[col], m_rows))

        df_fake_meta = pl.DataFrame(fake_meta_cols)

        if args.missing_values:
            df_fake_meta = introduce_missing_values(df_fake_meta, 0.05)

        meta_out_path = out_dir / f"test_metadata_{timestamp}.tsv"
        df_fake_meta.write_csv(meta_out_path, separator='\t')
        print(f"Created synthetic metadata: {meta_out_path}")


if __name__ == "__main__":
    main()
