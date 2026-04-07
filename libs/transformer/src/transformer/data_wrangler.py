import polars as pl
from typing import Dict, Any, List
# Import the registry functions
from transformer.registry import get_action_function


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

    def run(self, lf: pl.LazyFrame, wrangling_rules: List[Dict[str, Any]]) -> pl.LazyFrame:
        """
        Applies a list of declarative wrangling rules sequentially to the LazyFrame.
        Each rule is a dictionary containing an 'action' and parameters.
        """
        if not wrangling_rules:
            return lf

        transformed_lf = lf

        for rule in wrangling_rules:
            action_name = rule.get("action")
            if not action_name:
                raise ValueError(
                    "A wrangling rule is missing the 'action' key.")

            # 1. Resolve targets (inject back into rule for standard spec compliance)
            raw_selectors = rule.get("columns", rule.get(
                "source", rule.get(
                    "source_column", rule.get("target_column"))))

            target_columns = []
            if raw_selectors:
                if isinstance(raw_selectors, str):
                    raw_selectors = [raw_selectors]
                for selector in raw_selectors:
                    target_columns.extend(
                        self._resolve_category_targets(selector))

            # Ensure unique columns while preserving resolution order
            # This 'resolved_columns' becomes the truth for the action
            rule["columns"] = list(dict.fromkeys(target_columns))

            # 2. Resolve primary keys for safety
            pks = [col for col, props in self.data_schema.items()
                   if isinstance(props, dict) and props.get("is_primary_key")]
            rule["__metadata__"] = {"primary_keys": pks}

            # 3. Fetch and execute the action with (lf, spec) signature
            action_func = get_action_function(action_name)
            transformed_lf = action_func(transformed_lf, rule)

        return transformed_lf

    def wrangle(self, dataframe: pl.DataFrame, wrangling_rules: List[Dict[str, Any]]) -> pl.DataFrame:
        """
        Convenience wrapper bridging Eager DataFrames to Lazy execution.
        """
        lf = dataframe.lazy()
        result_lf = self.run(lf, wrangling_rules)
        return result_lf.collect()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Manual execution hook for testing.")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    if args.test:
        print(f"Executing {__file__} in test mode.")
