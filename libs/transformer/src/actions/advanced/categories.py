import polars as pl
from typing import Dict, Any, List, Union
import os
from pathlib import Path  # Added for Path object
from libs.transformer.src.actions.base import register_action


@register_action("split_and_explode")
def action_split_and_explode(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Splits a string column by a separator and explodes it into multiple rows.
    """
    columns = spec.get("columns", [])
    separator = spec.get("separator", ",")

    # split_and_explode currently only supports one column at a time for safety
    target = columns if isinstance(columns, str) else columns[0]

    return lf.with_columns(
        pl.col(target).str.split(separator)
    ).explode(target)


@register_action("derive_categories")
def action_derive_categories(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    A lookup-based action that maps messy strings to clean categories
    using an external reference TSV.
    """
    columns = spec.get("columns", [])
    target_column = spec.get("target_column")
    separator = spec.get("separator", ", ")
    reference_file = spec.get("reference_file")
    lookup_left = spec.get("lookup_left")  # New parameter
    lookup_right = spec.get("lookup_right")
    extract_column = spec.get("extract_column")

    # Basic Validation
    if not all([reference_file, lookup_left, lookup_right, extract_column]):
        raise ValueError(
            f"'derive_categories' missing mandatory parameters. Spec: {spec}")

    if not Path(reference_file).exists():
        raise FileNotFoundError(f"Reference file not found: {reference_file}")

    # 1. Load Reference Data
    ref_df = pl.read_csv(reference_file, separator="\t")
    ref_map = dict(zip(ref_df[lookup_right], ref_df[extract_column]))

    source_col = columns if isinstance(columns, str) else columns[0]

    # 2. Vectorized Transformation
    def lookup_fn(s: str) -> Union[str, None]:
        if not s:
            return None
        parts = [p.strip() for p in s.split(separator.strip())]
        mapped = [ref_map.get(p) for p in parts if p in ref_map]
        return separator.join(sorted(list(set(mapped)))) if mapped else None

    return lf.with_columns([
        pl.col(source_col).map_elements(
            lookup_fn, return_dtype=pl.String).alias(target_column)
    ])


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Manual execution hook for testing.")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    if args.test:
        print(f"Executing {__file__} in test mode.")
