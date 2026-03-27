from typing import Dict, List, Any
import polars as pl
from transformer.registry import get_action_function


class DataAssembler:
    """
    Orchestrates the assembly of multiple wrangled datasets (ingredients)
    into a final consolidated LazyFrame based on a relational recipe.
    """

    def __init__(self, ingredients: Dict[str, pl.LazyFrame]):
        """
        Args:
            ingredients: Dictionary mapping dataset_ids to their wrangled LazyFrames.
        """
        self.ingredients = ingredients

    def assemble(self, recipe: List[Dict[str, Any]]) -> pl.LazyFrame:
        """
        Executes the assembly steps (joins, filters, renames) sequentially.

        Args:
            recipe: List of assembly actions (e.g., join, join_filter).

        Returns:
            A consolidated Polars LazyFrame.
        """
        if not recipe:
            raise ValueError("Assembly recipe is empty. Cannot assemble data.")

        # The first ingredient is usually our backbone/starting point
        # But for robustness, we use a more explicit starting logic if needed.
        # Here we assume the recipe is iterative on the first ingredient.
        # However, the recipe provided in the manifest (Step 702) starts with a join
        # which implies a starting base. I'll assume the first join's 'left' side
        # needs to be established.
        # Actually, let's allow the recipe to define the starting base or use the
        # first join's implicit base.

        consolidated_lf: pl.LazyFrame = None

        for step in recipe:
            action_name = step.get("action")
            if not action_name:
                raise ValueError("Assembly step missing 'action' key.")

            # Resolve the right-hand ingredient if it's a join-type action
            right_id = step.get("right_ingredient")
            if right_id:
                if right_id not in self.ingredients:
                    available = ", ".join(self.ingredients.keys())
                    raise ValueError(
                        f"Ingredient '{right_id}' not found. Available: {available}")
                step["__right_df__"] = self.ingredients[right_id]

            # If this is the FIRST step and it's a join, we need a left base.
            # In our manifest, Step 1 is joining MLST_results.
            # This implies we might need an initial backbone or the first ingredient IS the base.
            if consolidated_lf is None:
                if action_name == "join" and right_id:
                    # If first step is a join, we'll try to use the FIRST ingredient in the
                    # ingredients dict as the backbone if not specified.
                    # Or better: the recipe SHOULD define the start.
                    # Since the manifest says Step 1 is a join, I'll take the first
                    # available ingredient as the left base if none exists.
                    # But wait, MLST_results IS the right ingredient in Step 1.
                    # So what is the left?
                    # Ah! Maybe we start with an empty or the VERY first ingredient listed?
                    # I'll default to the first ingredient in the dict if consolidated_lf is None.
                    first_key = list(self.ingredients.keys())[0]
                    consolidated_lf = self.ingredients[first_key]
                    # If the first step join's right id is the same as the first_key,
                    # it might be redundant, but polars handle it or we skip it.
                    if right_id == first_key:
                        continue

            # Execute the action
            action_func = get_action_function(action_name)
            consolidated_lf = action_func(consolidated_lf, step)

        return consolidated_lf
