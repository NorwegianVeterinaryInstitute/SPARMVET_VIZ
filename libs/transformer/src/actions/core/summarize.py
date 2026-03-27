import polars as pl
from typing import Dict, Any
from transformer.actions.base import register_action


from typing import Dict, Any, List, Union


@register_action("summarize")
def action_summarize(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Groups by specific columns and aggregates the target column(s).
    Useful for collapsing data before visualization.
    """
    columns = spec.get("columns", [])
    group_by_cols = spec.get("group_by", [])
    agg_type = spec.get("agg", "count")
    new_name = spec.get("new_name")

    # Standardize inputs
    if isinstance(group_by_cols, str):
        group_by_cols = [group_by_cols]
    if isinstance(columns, str):
        columns = [columns]

    # Build the aggregation expressions
    if agg_type == "count":
        agg_exprs = [pl.col(c).count().alias(new_name if (
            new_name and len(columns) == 1) else f"{c}_count") for c in columns]
    elif agg_type == "sum":
        agg_exprs = [pl.col(c).sum().alias(new_name if (
            new_name and len(columns) == 1) else f"{c}_sum") for c in columns]
    elif agg_type == "mean":
        agg_exprs = [pl.col(c).mean().alias(new_name if (
            new_name and len(columns) == 1) else f"{c}_mean") for c in columns]
    else:
        agg_exprs = [pl.col(c).count().alias(new_name if (
            new_name and len(columns) == 1) else f"{c}_count") for c in columns]

    if not group_by_cols:
        return lf.select(agg_exprs)

    return lf.group_by(group_by_cols).agg(agg_exprs)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Manual execution hook for testing.")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    if args.test:
        print(f"Executing {__file__} in test mode.")
