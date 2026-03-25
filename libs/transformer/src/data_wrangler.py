import polars as pl
from typing import Dict, Any, List
# Import the registry functions
from libs.transformer.src.registry import get_action_function


class DataWrangler:
    """
    Applies declarative YAML configuration rules to a Polars LazyFrame.

    It maps column names to specific transformation actions defined in
    the central Action Registry.
    """

    def __init__(self, data_schema: Dict[str, Any]):
        """
        Args:
            data_schema: The dictionary from the YAML representing the schema (categories, types, etc.)
        """
        self.data_schema = data_schema

    def _resolve_category_targets(self, key: str) -> List[str]:
        """
        If a rule targets a category (e.g. "@AMR"), this returns all column names
        in the data_schema that have that category. Otherwise, returns the single column name.
        """
        if not key.startswith("@"):
            return [key]

        category_name = key[1:]  # strip the '@'
        target_cols = []
        for col_name, col_props in self.data_schema.items():
            if "categories" in col_props and category_name in col_props["categories"]:
                target_cols.append(col_name)

        return target_cols

    def apply_wrangling_rules(self, lf: pl.LazyFrame, wrangling_rules: List[Dict[str, Any]]) -> pl.LazyFrame:
        """
        Applies a list of declarative wrangling rules sequentially to the LazyFrame.

        Args:
            lf: The input Polars LazyFrame.
            wrangling_rules: The `wrangling` block from the YAML.
                             E.g., [{"action": "fill_nulls", "columns": ["@AMR"], "value": "None"}]

        Returns:
            The transformed LazyFrame.
        """
        if not wrangling_rules:
            return lf

        transformed_lf = lf

        for rule in wrangling_rules:
            action_name = rule.get("action")
            if not action_name:
                raise ValueError(
                    "A wrangling rule is missing the 'action' key.")

            # Identify which key determines the execution targets.
            # 'columns' is preferred per ADR-004, but 'target_column'/'source_column' are supported for legacy.
            raw_selectors = rule.get("columns", rule.get(
                "source_column", rule.get("target_column")))

            if not raw_selectors:
                raise ValueError(
                    f"Action '{action_name}' is missing a 'columns', 'target_column', or 'source_column'."
                )

            # Standardize selectors into a list
            if isinstance(raw_selectors, str):
                raw_selectors = [raw_selectors]

            # Resolve the selectors (e.g. ["@AMR", "species"] -> ["gene_A", "gene_B", "species"])
            target_columns = []
            for selector in raw_selectors:
                target_columns.extend(self._resolve_category_targets(selector))

            # Ensure unique columns while preserving resolution order
            target_columns = list(dict.fromkeys(target_columns))

            # Resolve primary keys from schema for safety checks
            pks = [col for col, props in self.data_schema.items()
                   if props.get("is_primary_key")]
            rule["__metadata__"] = {"primary_keys": pks}

            # 1. Fetch the correct function from the Python Registry
            action_func = get_action_function(action_name)

            # 2. Apply the registered action once to the resolved column list
            transformed_lf = action_func(transformed_lf, target_columns, rule)

        return transformed_lf

    def wrangle(self, dataframe: pl.DataFrame, wrangling_rules: List[Dict[str, Any]]) -> pl.DataFrame:
        """
        Convenience wrapper bridging Eager DataFrames to Lazy execution.
        """
        lf = dataframe.lazy()
        result_lf = self.apply_wrangling_rules(lf, wrangling_rules)
        return result_lf.collect()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Manual execution hook for testing.")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    if args.test:
        print(f"Executing {__file__} in test mode.")
