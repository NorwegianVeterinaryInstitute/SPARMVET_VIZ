import polars as pl
from typing import Dict, Any
from libs.transformer.src.actions.base import register_action


@register_action("drop_duplicates")
def action_drop_duplicates(lf: pl.LazyFrame, col_name: str, args: Dict[str, Any]) -> pl.LazyFrame:
    """
    Drops duplicate rows.
    If col_name is provided (via target_column), it uses it as part of the subset.
    Note: DataWrangler loops over target_columns, so this will be called for each.
    This might be inefficient if multiple columns are targeted for a single drop_duplicates.
    """
    maintain_order = args.get("maintain_order", False)
    # We use subset=[col_name] to specifically target the column being iterated.
    # If the user wants to drop duplicates based on MULTIPLE columns in one go,
    # the current DataWrangler architecture (one call per column) might need
    # a 'global' action type. For now, we follow the standard per-column pattern.
    if maintain_order:
        return lf.unique(subset=[col_name], maintain_order=True)
    return lf.unique(subset=[col_name])


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Manual execution hook for testing.")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    if args.test:
        print(f"Executing {__file__} in test mode.")
