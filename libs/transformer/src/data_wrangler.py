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

    def apply_wrangling_rules(self, lf: pl.LazyFrame, wrangling_rules: List[Dict[str, Any]]) -> pl.LazyFrame:
        """
        Applies a list of declarative wrangling rules sequentially to the LazyFrame.

        Args:
            lf: The input Polars LazyFrame.
            wrangling_rules: The `wrangling` block from the YAML.
                             E.g., [{"action": "fill_nulls", "target_column": "@AMR", "value": "None"}]

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
            # Usually 'target_column', but 'derive_categories' natively maps via 'source_column'.
            selector_key = rule.get("source_column", rule.get("target_column"))
            if not selector_key:
                raise ValueError(
                    f"Action '{action_name}' is missing a 'target_column' or 'source_column'."
                )

            # Resolve the selector (e.g. "@AMR" becomes ["gene_A", "gene_B"])
            target_columns = self._resolve_category_targets(selector_key)

            for col_name in target_columns:
                # 1. Fetch the correct function from the Python Registry
                action_func = get_action_function(action_name)

                # 2. Apply the registered action to the LazyFrame
                transformed_lf = action_func(transformed_lf, col_name, rule)

        return transformed_lf

    def wrangle(self, dataframe: pl.DataFrame, wrangling_rules: List[Dict[str, Any]]) -> pl.DataFrame:
        """
        Convenience wrapper bridging Eager DataFrames to Lazy execution.
        """
        lf = dataframe.lazy()
        result_lf = self.apply_wrangling_rules(lf, wrangling_rules)
        return result_lf.collect()
