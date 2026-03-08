import polars as pl
from typing import Dict, Callable, Any
import os


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


def action_split_and_explode(lf: pl.LazyFrame, col_name: str, args: Dict[str, Any]) -> pl.LazyFrame:
    """
    Splits a string by a separator and explodes it into long format.
    Requires 'separator' in args.
    """
    separator = args.get("separator")
    if not separator:
        raise ValueError(
            f"'split_and_explode' action on '{col_name}' requires a 'separator' parameter.")
    return lf.with_columns(pl.col(col_name).str.split(separator)).explode(col_name)


def action_rename(lf: pl.LazyFrame, col_name: str, args: Dict[str, Any]) -> pl.LazyFrame:
    """
    Renames the column to a new name.
    Requires 'new_name' in args.
    """
    new_name = args.get("new_name")
    if not new_name:
        raise ValueError(
            f"'rename' action on '{col_name}' requires a 'new_name' parameter.")
    return lf.rename({col_name: new_name})


def action_drop_nulls(lf: pl.LazyFrame, col_name: str, args: Dict[str, Any]) -> pl.LazyFrame:
    """
    Drops rows where this specific column is null.
    """
    return lf.drop_nulls(subset=[col_name])


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

    # In Polars, we use pl.col().replace() or pl.when().then()
    # For a list of exact matches, replace() is the most efficient.
    # We construct a mapping dictionary
    mapping = {old_val: new_value for old_val in to_replace}

    return lf.with_columns(pl.col(col_name).replace(mapping, default=pl.col(col_name)))


def action_derive_categories(lf: pl.LazyFrame, col_name: str, args: Dict[str, Any]) -> pl.LazyFrame:
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
            f"'derive_categories' action on '{col_name}' missing required reference arguments.")

    if not os.path.exists(ref_file):
        raise FileNotFoundError(f"Reference file not found: {ref_file}")

    # Read reference eagerly to construct the fast lookup HashMap
    ref_df = pl.read_csv(ref_file, separator="\t")
    mapping = dict(zip(ref_df[lookup_right], ref_df[extract_col]))

    # Perform the Explode-Join-Collapse entirely within the element-wise list namespace
    expr = (
        pl.col(col_name)
        .str.split(separator)
        .list.eval(
            pl.element().str.strip_chars().replace(mapping, default=pl.element())
        )
        .list.drop_nulls()
        .list.unique()
        .list.join(", ")
    )

    return lf.with_columns(expr.alias(target_col))

# ==========================================
# The Central Action Registry
# ==========================================
# This dictionary is the "Source of Truth" for all YAML wrangling actions.
# The UI Help tab imports this dictionary to auto-generate documentation.


AVAILABLE_WRANGLING_ACTIONS: Dict[str, Callable[[pl.LazyFrame, str, Dict[str, Any]], pl.LazyFrame]] = {
    "fill_nulls": action_fill_nulls,
    "split_and_explode": action_split_and_explode,
    "rename": action_rename,
    "drop_nulls": action_drop_nulls,
    "replace_values": action_replace_values,
    "derive_categories": action_derive_categories
}


def get_action_function(action_name: str) -> Callable:
    """Returns the function for a given action, or raises a friendly error."""
    if action_name not in AVAILABLE_WRANGLING_ACTIONS:
        available = ", ".join(AVAILABLE_WRANGLING_ACTIONS.keys())
        raise ValueError(
            f"Action '{action_name}' is not registered. Available actions: {available}")
    return AVAILABLE_WRANGLING_ACTIONS[action_name]


# Future expansion: Plotting Defaults Registry
AVAILABLE_PLOT_DEFAULTS = {
    # e.g., "color_scale": apply_color_scale_default
}
