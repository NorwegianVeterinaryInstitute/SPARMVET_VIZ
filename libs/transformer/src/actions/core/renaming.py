import polars as pl
from typing import Dict, Any
from libs.transformer.src.actions.base import register_action


@register_action("rename")
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


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Manual execution hook for testing.")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    if args.test:
        print(f"Executing {__file__} in test mode.")
