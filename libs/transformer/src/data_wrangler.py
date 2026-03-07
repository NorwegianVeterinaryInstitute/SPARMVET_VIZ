import polars as pl
from typing import Dict, Any, List
# Import the registry functions
from src.registry import get_action_function


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

    def apply_wrangling_rules(self, lf: pl.LazyFrame, wrangling_rules: Dict[str, List[Dict[str, Any]]]) -> pl.LazyFrame:
        """
        Applies a dictionary of wrangling rules sequentially to the LazyFrame.

        Args:
            lf: The input Polars LazyFrame.
            wrangling_rules: The `data_wrangling` or `metadata_wrangling` block from the YAML.
                             E.g., {"@AMR": [{"action": "fill_nulls", "value": "None"}], "date": [...]}

        Returns:
            The transformed LazyFrame.
        """
        if not wrangling_rules:
            return lf

        transformed_lf = lf

        for rule_target, actions in wrangling_rules.items():
            # rule_target could be a specific column like "sample_id",
            # or a category selector like "@AMR"
            target_columns = self._resolve_category_targets(rule_target)

            for col_name in target_columns:
                for rule in actions:
                    action_name = rule.get("action")
                    if not action_name:
                        raise ValueError(
                            f"A wrangling rule on '{rule_target}' is missing the 'action' key.")

                    # 1. Fetch the correct function from the Python Registry
                    #    This will raise a friendly error if the action doesn't exist.
                    action_func = get_action_function(action_name)

                    # 2. Apply the registered action to the LazyFrame
                    transformed_lf = action_func(
                        transformed_lf, col_name, rule)

        return transformed_lf

    def wrangle(self, dataframe: pl.DataFrame, wrangling_rules: Dict[str, List[Dict[str, Any]]]) -> pl.DataFrame:
        """
        Convenience wrapper bridging Eager DataFrames to Lazy execution.
        """
        lf = dataframe.lazy()
        result_lf = self.apply_wrangling_rules(lf, wrangling_rules)
        return result_lf.collect()
