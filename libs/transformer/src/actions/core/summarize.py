import polars as pl
from typing import Dict, Any
from libs.transformer.src.actions.base import register_action


@register_action("summarize")
def action_summarize(lf: pl.LazyFrame, col_name: str, args: Dict[str, Any]) -> pl.LazyFrame:
    """
    Groups by specific columns and aggregates the target column.
    Useful for collapsing data before visualization.

    Parameters:
    - group_by (list): Columns to group by (optional).
    - agg (str): Aggregation type ('count', 'sum', 'mean').
    - new_name (str): Name for the resulting aggregated column.
    """
    group_by_cols = args.get("group_by", [])
    agg_type = args.get("agg", "count")
    new_name = args.get("new_name", f"{col_name}_{agg_type}")

    # Standardize to list if single string provided
    if isinstance(group_by_cols, str):
        group_by_cols = [group_by_cols]

    # Build the aggregation expression
    if agg_type == "count":
        agg_expr = pl.col(col_name).count().alias(new_name)
    elif agg_type == "sum":
        agg_expr = pl.col(col_name).sum().alias(new_name)
    elif agg_type == "mean":
        agg_expr = pl.col(col_name).mean().alias(new_name)
    else:
        # Default fallback or raise error?
        agg_expr = pl.col(col_name).count().alias(new_name)

    if not group_by_cols:
        return lf.select(agg_expr)

    return lf.group_by(group_by_cols).agg(agg_expr)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Manual execution hook for testing.")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    if args.test:
        print(f"Executing {__file__} in test mode.")
