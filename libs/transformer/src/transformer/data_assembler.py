import os
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
        Includes ADR-024 Short-Circuit logic for Tier 1 Parquet anchors.

        Args:
            recipe: List of assembly actions (e.g., join, join_filter, sink_parquet).

        Returns:
            A consolidated Polars LazyFrame.
        """
        if not recipe:
            raise ValueError("Assembly recipe is empty. Cannot assemble data.")

        consolidated_lf: pl.LazyFrame = None
        start_index = 0

        # --- ADR-024: Tier 1 Short-Circuit Logic ---
        # Search the recipe for the latest available 'sink_parquet' anchor.
        # If the file exists on disk, we skip all steps leading up to it.
        for i, step in enumerate(recipe):
            if step.get("action") == "sink_parquet":
                path = step.get("path")
                force = step.get("force_recompute", False)
                if path and os.path.exists(path) and not force:
                    print(
                        f"  ─── 🗲  Short-Circuit: Existing Parquet anchor found at {path}. Skipping early steps.")
                    consolidated_lf = pl.scan_parquet(path)
                    start_index = i + 1  # Start loop from the step AFTER sink_parquet
                    break

        # Process the remaining steps (or all steps if no anchor was found)
        for i in range(start_index, len(recipe)):
            step = recipe[i]
            action_name = step.get("action")
            if not action_name:
                raise ValueError(f"Assembly step {i} missing 'action' key.")

            # Resolve the right-hand ingredient if it's a join-type action
            right_id = step.get("right_ingredient")
            if right_id:
                if right_id not in self.ingredients:
                    available = ", ".join(self.ingredients.keys())
                    raise ValueError(
                        f"Ingredient '{right_id}' not found. Available: {available}")
                step["__right_df__"] = self.ingredients[right_id]

            # Initialize base if this is the first effective step
            if consolidated_lf is None:
                # Default to the first ingredient in the cache as the backbone
                # unless the first action itself provides a source.
                first_key = list(self.ingredients.keys())[0]
                consolidated_lf = self.ingredients[first_key]
                
                # If the first step is a join involving this first ingredient, we might skip redundant join
                if action_name == "join" and right_id == first_key:
                    continue

            # Execute the action via the shared registry (ADR-018)
            action_func = get_action_function(action_name)
            consolidated_lf = action_func(consolidated_lf, step)

        return consolidated_lf
