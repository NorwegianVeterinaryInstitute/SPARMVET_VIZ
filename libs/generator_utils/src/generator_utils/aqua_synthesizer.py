import polars as pl
import numpy as np
import random
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from datetime import datetime


class AquaSynthesizer:
    """
    Logic for generating synthetic relational test data from real ground truth.
    Implements 'Relational Anchoring' (Shared PK Pools) to ensure join integrity.
    """

    def __init__(self, anchor_key_name: str = "id", n_samples: int = 20):
        self.anchor_key_name = anchor_key_name
        self.n_samples = n_samples
        self.anchor_pool: List[str] = []
        self._generate_anchor_pool()

    def _generate_anchor_pool(self):
        """Creates a deterministic or randomized pool of unique 8-digit IDs with a prefix."""
        ids = random.sample(range(10000000, 99999999), self.n_samples)
        self.anchor_pool = [f"SYN_{i}" for i in ids]

    def _generate_column(self, series: pl.Series, n_rows: int) -> pl.Series:
        """Generates synthetic data matching the type and distribution of a real series."""
        dtype = series.dtype
        name = series.name

        if dtype.is_integer():
            min_v, max_v = series.min() or 0, series.max() or 100
            return pl.Series(name, np.random.randint(min_v, max_v + 1, size=n_rows))
        elif dtype.is_float():
            min_v, max_v = series.min() or 0.0, series.max() or 1.0
            return pl.Series(name, np.random.uniform(min_v, max_v, size=n_rows))
        elif dtype.is_temporal():
            return pl.Series(name, [datetime.now().date()] * n_rows)
        elif isinstance(dtype, pl.Boolean):
            return pl.Series(name, np.random.choice([True, False], size=n_rows))
        else:
            # Categorical / String
            unique_vals = series.drop_nulls().unique().to_list()
            if not unique_vals:
                unique_vals = ["unknown"]
            return pl.Series(name, np.random.choice(unique_vals, size=n_rows))

    def synthesize(self, tsv_paths: List[Path], out_dir: Path, mismatch_fraction: float = 0.0, messy_fraction: float = 0.1) -> List[Path]:
        """
        Generates synthetic TSVs from a list of real TSVs, ensuring PK relational anchoring.
        """
        out_dir.mkdir(parents=True, exist_ok=True)
        synthetic_files = []

        for tsv_p in tsv_paths:
            df_real = pl.read_csv(tsv_p, separator='\t')
            n_rows = self.n_samples

            synthetic_cols = []

            # PK Anchoring
            is_metadata = "metadata" in tsv_p.name.lower()
            if is_metadata:
                pk_col = self.anchor_pool
                # Introduce mismatches if metadata
                if mismatch_fraction > 0:
                    n_mismatch = int(self.n_samples * mismatch_fraction)
                    mismatch_pool = [str(i) for i in random.sample(
                        range(20000000, 30000000), n_mismatch)]
                    pk_col = pk_col[:-n_mismatch] + mismatch_pool
                    random.shuffle(pk_col)
            else:
                # Analytical tables use the anchor pool, possibly repeated or subset
                pk_col = random.choices(self.anchor_pool, k=n_rows)

            # Apply PK
            synthetic_cols.append(pl.Series(self.anchor_key_name, pk_col))

            # Apply Other Cols
            for col in df_real.columns:
                if col.lower() == self.anchor_key_name.lower():
                    continue
                synthetic_cols.append(
                    self._generate_column(df_real[col], n_rows))

            df_fake = pl.DataFrame(synthetic_cols)

            # Inject Messihess
            if messy_fraction > 0:
                messy_strings = [None, "-", "unknown", "N/A", ""]
                exprs = []
                for col in df_fake.columns:
                    mask = pl.Series(np.random.rand(n_rows) < messy_fraction)
                    if df_fake[col].dtype == pl.String:
                        messy_data = [str(x) if x is not None else None for x in np.random.choice(
                            messy_strings, size=n_rows)]
                        random_messy = pl.Series(
                            col, messy_data, dtype=pl.String)
                        exprs.append(pl.when(mask).then(
                            random_messy).otherwise(pl.col(col)).alias(col))
                    else:
                        exprs.append(pl.when(mask).then(
                            None).otherwise(pl.col(col)).alias(col))
                df_fake = df_fake.with_columns(exprs)

            out_file = out_dir / f"test_data_{tsv_p.name}"
            df_fake.write_csv(out_file, separator='\t')
            synthetic_files.append(out_file)

        return synthetic_files
