import polars as pl
from typing import Dict, Any
from transformer.actions.base import register_action


from typing import Dict, Any, List, Union


@register_action("drop_duplicates")
def action_drop_duplicates(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Drops duplicate rows based on one or more columns as a subset.
    The new DataWrangler architecture allows passing multiple columns to a single
    unique() call, maximizing Polars' parallel execution performance.
    """
    columns = spec.get("columns", [])
    maintain_order = spec.get("maintain_order", False)
    # We use subset=columns to target the entire resolved set.
    if maintain_order:
        return lf.unique(subset=columns, maintain_order=True)
    return lf.unique(subset=columns)


@register_action("unique_rows")
def action_unique_rows(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Drops duplicate rows based on ALL columns (subset=None).
    Polar default for unique() is subset=None if not provided.
    """
    maintain_order = spec.get("maintain_order", True)
    return lf.unique(subset=None, maintain_order=maintain_order)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Manual execution hook for testing.")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    if args.test:
        print(f"Executing {__file__} in test mode.")
