import polars as pl
from typing import Dict, Any
import os
from libs.transformer.src.actions.base import register_action


@register_action("split_and_explode")
def action_split_and_explode(lf: pl.LazyFrame, columns: Union[str, List[str]], args: Dict[str, Any]) -> pl.LazyFrame:
    """
    Splits strings by a separator and explodes them into long format across one or more columns.
    Requires 'separator' in args. 
    Note: When multiple columns are provided, Polars will perform a simultaneous vertical explosion (parallel).
    """
    separator = args.get("separator")
    if not separator:
        raise ValueError(
            f"'split_and_explode' action on '{columns}' requires a 'separator' parameter.")
    return lf.with_columns(pl.col(columns).str.split(separator)).explode(columns)


@register_action("derive_categories")
def action_derive_categories(lf: pl.LazyFrame, columns: Union[str, List[str]], args: Dict[str, Any]) -> pl.LazyFrame:
    """
    Advanced Dimensional Modeling. Maps comma-separated strings against an external reference file.
    Utilizes Polars list.eval mapping to avoid row explosion and preserve origin dataframe grain.
    """
    target_col = args.get("target_column")
    separator = args.get("separator", ", ")
    ref_file = args.get("reference_file")
    lookup_right = args.get("lookup_right")
    extract_col = args.get("extract_column")

    if not all([target_col, ref_file, lookup_right, extract_col]):
        raise ValueError(
            f"'derive_categories' action on '{columns}' missing required reference arguments.")

    if not os.path.exists(ref_file):
        raise FileNotFoundError(f"Reference file not found: {ref_file}")

    ref_df = pl.read_csv(ref_file, separator="\t")
    mapping = dict(zip(ref_df[lookup_right], ref_df[extract_col]))

    expr = (
        pl.col(columns)
        .str.split(separator)
        .list.eval(
            pl.element().str.strip_chars().replace(mapping, default=pl.element())
        )
        .list.drop_nulls()
        .list.unique()
        .list.join(", ")
    )

    return lf.with_columns(expr.alias(target_col))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Manual execution hook for testing.")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    if args.test:
        print(f"Executing {__file__} in test mode.")
