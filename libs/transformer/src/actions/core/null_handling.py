import polars as pl
from typing import Dict, Any
from libs.transformer.src.actions.base import register_action


@register_action("fill_nulls")
def action_fill_nulls(lf: pl.LazyFrame, col_name: str, args: Dict[str, Any]) -> pl.LazyFrame:
    """
    Replaces null values with a specified value.
    Requires 'value' in args.
    """
    fill_value = args.get("value")
    if fill_value is None:
        raise ValueError(
            f"'fill_nulls' action on '{col_name}' requires a 'value' parameter.")
    return lf.with_columns(pl.col(col_name).fill_null(fill_value))


@register_action("drop_nulls")
def action_drop_nulls(lf: pl.LazyFrame, col_name: str, args: Dict[str, Any]) -> pl.LazyFrame:
    """
    Drops rows where this specific column is null.
    """
    return lf.drop_nulls(subset=[col_name])


@register_action("replace_values")
def action_replace_values(lf: pl.LazyFrame, col_name: str, args: Dict[str, Any]) -> pl.LazyFrame:
    """
    Replaces a specific list of strings with a new value (which can be null).
    Requires 'to_replace' (list) and 'new_value' in args.
    """
    to_replace = args.get("to_replace")
    new_value = args.get("new_value")

    if not isinstance(to_replace, list):
        raise ValueError(
            f"'replace_values' action on '{col_name}' requires 'to_replace' to be a list of strings.")

    mapping = {old_val: new_value for old_val in to_replace}
    return lf.with_columns(pl.col(col_name).replace(mapping, default=pl.col(col_name)))
