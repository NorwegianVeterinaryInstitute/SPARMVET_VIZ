import polars as pl
from typing import List, Dict, Any
from libs.transformer.src.actions.base import register_action
from typing import List, Dict, Any, Union


@register_action("keep_columns")
def action_keep_columns(lf: pl.LazyFrame, columns: Union[str, List[str]], args: Dict[str, Any]) -> pl.LazyFrame:
    """
    Selects only the specified columns, ensuring that primary keys defined in the schema
    are always preserved to prevent join breakage.
    """
    # 1. Verification: Ensure all requested columns exist
    existing_cols = lf.columns
    missing = [c for c in columns if c not in existing_cols]
    if missing:
        raise ValueError(
            f"Action 'keep_columns' failed: The following columns were not found in the dataset: {missing}. "
            f"Ensure you are using the sanitized column names (snake_case)."
        )

    # 2. Safety: Resolve primary keys from rule metadata
    pks = args.get("__metadata__", {}).get("primary_keys", [])

    # Merge requested columns with primary keys, ensuring PKs come first
    final_selection = list(dict.fromkeys(pks + columns))

    return lf.select(final_selection)
