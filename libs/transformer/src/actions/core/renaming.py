import polars as pl
from typing import Dict, Any
from libs.transformer.src.actions.base import register_action


from typing import Dict, Any, List, Union


@register_action("rename")
def action_rename(lf: pl.LazyFrame, columns: Union[str, List[str]], args: Dict[str, Any]) -> pl.LazyFrame:
    """
    Renames the column to a new name.
    Requires 'new_name' in args. 
    Note: For multiple columns, this action expects a one-to-one mapping in args (future)
    but currently enforces a single target for a single new_name.
    """
    new_name = args.get("new_name")
    if not new_name:
        raise ValueError(
            f"'rename' action on '{columns}' requires a 'new_name' parameter.")

    # Convert to single string for the dictionary mapping if it's a single-item list
    target = columns if isinstance(columns, str) else columns[0]
    if isinstance(columns, list) and len(columns) > 1:
        raise ValueError(
            f"'rename' action currently only supports 1:1 renaming. Received: {columns}")

    return lf.rename({target: new_name})


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Manual execution hook for testing.")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    if args.test:
        print(f"Executing {__file__} in test mode.")
