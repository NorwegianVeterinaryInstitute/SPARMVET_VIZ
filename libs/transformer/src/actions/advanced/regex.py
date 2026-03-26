import polars as pl
from typing import Dict, Any
from libs.transformer.src.actions.base import register_action


@register_action("regex_extract")
def action_regex_extract(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Extracts a substring based on a Regex pattern with capture groups.

    Usage in YAML:
      - action: "regex_extract"
        source: "some_col"
        pattern: r"v(\d+)\.(\d+)"
        target_column: "major_version"
        group: 1
    """
    source = spec.get("source", spec.get("target_column"))
    pattern = spec.get("pattern")
    target = spec.get("target_column")
    group = spec.get("group", 1)

    if not source or not pattern or not target:
        return lf

    # Implementation: Use str.extract to generate a new column
    return lf.with_columns(
        pl.col(source).str.extract(pattern, group_index=group).alias(target)
    )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Manual execution hook for testing.")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    if args.test:
        print(f"Executing {__file__} in test mode.")
