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

    parser.add_argument("--data_dir", required=False,
                        help="Path to a directory containing real data files (*.tsv or *.csv).")
    parser.add_argument("--data_files", nargs='+', required=False,
                        help="Path to real data file(s).")
    parser.add_argument("--metadata_file", required=False,
                        help="Path to real metadata file.")
    parser.add_argument("--primary_key_data", nargs='+', required=True,
                        help="Primary key column(s) in the input data files (checks each file sequentially).")
    parser.add_argument("--primary_key_metadata", required=False,
                        help="Primary key column in the metadata file.")
    parser.add_argument("--output_primary_key", required=False, default=None,
                        help="If set, all datasets and metadata will have their primary key renamed to this standard name in the output TSVs.")
    parser.add_argument("--mismatches", action="store_true",
                        help="Introduce mismatched primary keys in metadata.")
    parser.add_argument("--duplicates", action="store_true",
                        help="Introduce duplicate primary keys to test data robustness.")
    parser.add_argument("--missing_values", action="store_true",
                        help="Randomly drop values (NA/null) into the data.")
    parser.add_argument("--out_dir", required=False, default=".",
                        help="Output directory for the generated test data files.")
    args = parser.parse_args()

    # Create output directory
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Resolve data files
    all_data_files = []

    if args.data_dir:
        dpath = Path(args.data_dir)
        if not dpath.is_dir():
            print(
                f"Error: --data_dir '{args.data_dir}' is not a valid directory.")
            return

        if args.data_files:
            # User provided a directory AND specific file names inside it
            for f_name in args.data_files:
                all_data_files.append(str(dpath / f_name))
        else:
            # User provided ONLY a directory, so grab everything
            found_files = list(dpath.glob("*.tsv")) + list(dpath.glob("*.csv"))
            all_data_files.extend([str(p) for p in found_files])
    else:
        # User provided NO directory, so data_files must be absolute/relative paths
        if args.data_files:
            all_data_files.extend(args.data_files)

    if not all_data_files:
        print("Error: You must provide either --data_files or --data_dir.")
        return

    # Strict File Existence Check
    missing_files = []
    valid_data_files = []

    for f in all_data_files:
        if not Path(f).exists():
            missing_files.append(f)
        else:
            valid_data_files.append(f)

    if missing_files:
        print("\n" + "="*40)
        print("CRITICAL ERROR: FILES NOT FOUND")
        print("="*40)
        print("The following requested data files do not exist at the resolved paths:")
        for mf in missing_files:
            print(f"  - {mf}")
        print("\nPlease check your --data_dir and --data_files arguments.")
        print("="*40 + "\n")
        return

    # 1. Harvest all real keys to build a consistent translation dictionary
    global_keys = set()
    data_dfs = []

    for d_file in valid_data_files:
        try:
            df = pl.read_csv(
                d_file, separator='\t' if d_file.endswith('.tsv') else ',')

            # Find which of the provided primary keys exists in this dataframe
            actual_key = next(
                (k for k in args.primary_key_data if k in df.columns), None)

            data_dfs.append((Path(d_file), df, actual_key))
            if actual_key:
                # Add all unique non-null keys to our global set
                global_keys.update(df[actual_key].drop_nulls().to_list())
            else:
                print(
                    f"Warning: None of the primary keys {args.primary_key_data} found in {d_file}")
        except Exception as e:
            print(f"Error reading {d_file}: {e}")

    df_meta = None
    if args.metadata_file and args.primary_key_metadata:
        try:
            df_meta = pl.read_csv(
                args.metadata_file, separator='\t' if args.metadata_file.endswith('.tsv') else ',')
            if args.primary_key_metadata in df_meta.columns:
                global_keys.update(
                    df_meta[args.primary_key_metadata].drop_nulls().to_list())
        except Exception as e:
            print(f"Error reading metadata {args.metadata_file}: {e}")

    n_unique = len(global_keys)
    if n_unique == 0:
        print("No primary keys found across provided files. Exiting.")
        return

    # Generate a massive pool of unique 8-digit fake IDs and map them to the original keys
    fake_ids_ints = random.sample(range(10000000, 99999999), n_unique)
    id_map = dict(zip(global_keys, [str(x) for x in fake_ids_ints]))

    # 2. Process Datasets
    for filepath, df_real, actual_key in data_dfs:
        n_rows = df_real.height
        fake_data_cols = []

        # Get translated IDs
        if actual_key:
            # Map original names to the new consistent random ones
            file_ids = [id_map.get(x, str(random.randint(10000000, 99999999)))
                        for x in df_real[actual_key].to_list()]
        else:
            file_ids = [str(x) for x in random.sample(
                range(10000000, 99999999), n_rows)]

        if args.duplicates and n_rows > 1:
            print(f"Introducing duplicate primary keys in {filepath.name}...")
            num_dups = max(1, int(n_rows * 0.05))  # 5% duplicates
            population_size = len(file_ids) - num_dups
            population = [file_ids[i] for i in range(population_size)]
            dup_sources = random.choices(population, k=num_dups)
            for i in range(num_dups):
                file_ids[population_size + i] = dup_sources[i]
            random.shuffle(file_ids)  # Scatter the duplicates around

        target_key_name = args.output_primary_key if args.output_primary_key else actual_key
        target_key_name = target_key_name or "sample_id"  # Fallback if no key

        for col in df_real.columns:
            if col == actual_key:
                fake_data_cols.append(pl.Series(target_key_name, file_ids))
            else:
                fake_data_cols.append(
                    generate_fake_column(df_real[col], n_rows))

        df_fake = pl.DataFrame(fake_data_cols)

        if args.missing_values:
            print(f"Injecting missing values into {filepath.name}...")
            df_fake = introduce_missing_values(df_fake, 0.05)

        data_out_path = out_dir / f"test_data_{filepath.stem}_{timestamp}.tsv"
        df_fake.write_csv(data_out_path, separator='\t')
        print(f"Created synthetic main data: {data_out_path}")

    # 3. Process Metadata if requested
    if df_meta is not None and args.primary_key_metadata:
        m_rows = df_meta.height
        fake_meta_cols = []

        # Translate metadata keys
        if args.primary_key_metadata in df_meta.columns:
            meta_ids = [id_map.get(x, str(random.randint(10000000, 99999999)))
                        for x in df_meta[args.primary_key_metadata].to_list()]
        else:
            meta_ids = [str(x) for x in random.sample(
                range(10000000, 99999999), m_rows)]

        if args.mismatches:
            print("Introducing mismatched primary keys in metadata...")
            # Shift the slice to break the join for 20% of the metadata
            shift = max(1, int(m_rows * 0.2))
            mismatch_ints = random.sample(range(10000000, 99999999), shift)
            mismatch_strs = [str(x) for x in mismatch_ints]
            start_idx = len(meta_ids) - shift
            for i in range(shift):
                meta_ids[start_idx + i] = mismatch_strs[i]

        if args.duplicates and m_rows > 1:
            print("Introducing duplicate primary keys in metadata...")
            num_dups = max(1, int(m_rows * 0.05))
            population_size = len(meta_ids) - num_dups
            population = [meta_ids[i] for i in range(population_size)]
            dup_sources = random.choices(population, k=num_dups)
            for i in range(num_dups):
                meta_ids[population_size + i] = dup_sources[i]
            random.shuffle(meta_ids)

        target_meta_key_name = args.output_primary_key if args.output_primary_key else args.primary_key_metadata

        for col in df_meta.columns:
            if col == args.primary_key_metadata:
                fake_meta_cols.append(
                    pl.Series(target_meta_key_name, meta_ids))
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
