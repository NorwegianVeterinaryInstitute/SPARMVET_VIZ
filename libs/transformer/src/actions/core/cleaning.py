import polars as pl
from typing import Dict, Any, List, Union
from libs.transformer.src.actions.base import register_action


@register_action("strip_whitespace")
def action_strip_whitespace(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Strips leading and trailing whitespace from string columns.
    If 'columns' is not provided in spec, targets all pl.String columns.
    """
    columns = spec.get("columns", [])

    if not columns:
        # Smart Selection: auto-target String columns
        schema = lf.collect_schema()
        process_cols = [name for name,
                        dtype in schema.items() if dtype == pl.String]
    else:
        process_cols = columns if isinstance(columns, list) else [columns]

    if not process_cols:
        return lf

    # Aggressively strip multiple characters (whitespace, tabs, newlines, and flanking quotes)
    return lf.with_columns(pl.col(process_cols).str.strip_chars(' \t\n\r"'))


@register_action("round_numeric")
def action_round_numeric(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Rounds numeric columns to a specified number of decimal places.
    Spec: { columns: ["col1"], decimals: 2 }
    """
    columns = spec.get("columns", [])
    decimals = spec.get("decimals", 2)

    if not columns:
        return lf

    return lf.with_columns(pl.col(columns).round(decimals))


@register_action("filter_range")
def action_filter_range(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Filters rows based on a numeric range (inclusive).
    Spec: { columns: ["col1"], min: 0.0, max: 100.0 }
    Note: Always operates on the first column in the list if multiple provided.
    """
    columns = spec.get("columns", [])
    if not columns:
        return lf

    target = columns[0]
    min_val = spec.get("min")
    max_val = spec.get("max")

    if min_val is not None:
        lf = lf.filter(pl.col(target) >= min_val)
    if max_val is not None:
        lf = lf.filter(pl.col(target) <= max_val)

    return lf


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Manual execution hook for testing.")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    if args.test:
        print(f"Executing {__file__} in test mode.")
