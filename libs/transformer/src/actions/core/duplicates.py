import polars as pl
from typing import Dict, Any
from libs.transformer.src.actions.base import register_action


from typing import Dict, Any, List, Union


@register_action("drop_duplicates")
def action_drop_duplicates(lf: pl.LazyFrame, columns: Union[str, List[str]], args: Dict[str, Any]) -> pl.LazyFrame:
    """
    Drops duplicate rows based on one or more columns as a subset.
    The new DataWrangler architecture allows passing multiple columns to a single
    unique() call, maximizing Polars' parallel execution performance.
    """
    maintain_order = args.get("maintain_order", False)
    # We use subset=columns to target the entire resolved set.
    # This replaces the previous inefficient per-column loop.
    if maintain_order:
        return lf.unique(subset=columns, maintain_order=True)
    return lf.unique(subset=columns)


@register_action("unique_rows")
def action_unique_rows(lf: pl.LazyFrame, columns: Union[str, List[str]], args: Dict[str, Any]) -> pl.LazyFrame:
    """
    Drops duplicate rows based on ALL columns (subset=None).
    Polar default for unique() is subset=None if not provided.
    """
    maintain_order = args.get("maintain_order", True)
    return lf.unique(subset=None, maintain_order=maintain_order)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Manual execution hook for testing.")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    if args.test:
        print(f"Executing {__file__} in test mode.")
