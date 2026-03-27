import polars as pl
from typing import Dict, Any
from transformer.actions.base import register_action


from typing import Dict, Any, List, Union


@register_action("rename")
def action_rename(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Renames columns according to spec.
    Supports:
        mapping: Dict[str, str]  - Multiple renames at once.
        new_name: str, columns: str or List[str] - 1:1 rename.
    """
    mapping = spec.get("mapping")
    if mapping:
        return lf.rename(mapping)

    new_name = spec.get("new_name")
    if not new_name:
        raise ValueError(
            f"'rename' action requires 'mapping' or 'new_name' parameter. Spec: {spec}")

    columns = spec.get("columns", [])
    if not columns:
        # Check for 'target_column' alias used in some scripts
        columns = spec.get("target_column")

    if not columns:
        raise ValueError(
            f"'rename' action missing source column(s). Spec: {spec}")

    # Convert to single string for the dictionary mapping if it's a single-item list
    target = columns if isinstance(columns, str) else columns[0]
    return lf.rename({target: new_name})


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Manual execution hook for testing.")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    if args.test:
        print(f"Executing {__file__} in test mode.")
