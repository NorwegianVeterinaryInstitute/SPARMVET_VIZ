import polars as pl
from typing import Dict, Any, List, Union
from libs.transformer.src.actions.base import register_action


@register_action("fill_nulls")
def action_fill_nulls(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Replaces null values with a specified value across one or more columns.
    Requires 'value' in spec.
    """
    columns = spec.get("columns", [])
    fill_value = spec.get("value")
    if fill_value is None:
        raise ValueError(
            f"'fill_nulls' action requires a 'value' parameter. Spec: {spec}")
    return lf.with_columns(pl.col(columns).fill_null(fill_value))


@register_action("drop_nulls")
def action_drop_nulls(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Drops rows where any of the specified columns are null.
    """
    columns = spec.get("columns", [])
    return lf.drop_nulls(subset=columns)


@register_action("replace_values")
def action_replace_values(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Replaces a specific list of strings with a new value across multiple columns.
    Requires 'to_replace' (list) and 'new_value' in spec.
    """
    columns = spec.get("columns", [])
    to_replace = spec.get("to_replace")
    new_value = spec.get("new_value")

    if not isinstance(to_replace, list):
        raise ValueError(
            f"'replace_values' action requires 'to_replace' to be a list. Spec: {spec}")

    mapping = {old_val: new_value for old_val in to_replace}
    return lf.with_columns(pl.col(columns).replace(mapping, default=pl.col(columns)))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Manual execution hook for testing.")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    if args.test:
        print(f"Executing {__file__} in test mode.")
