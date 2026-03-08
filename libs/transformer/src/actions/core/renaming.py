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
