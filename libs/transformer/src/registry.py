# ==========================================
# The Central Action Registry Interface
# ==========================================
# This file now serves purely as a lightweight interface bridge to the
# dynamic plugin sub-modules located in `actions/`.
#
# Do NOT write wrangling logic here. Add new files to `actions/core/`
# or `actions/advanced/` instead.

from typing import Callable, Dict, Any
import polars as pl
from libs.transformer.src.actions.base import AVAILABLE_WRANGLING_ACTIONS

# We must import the main actions __init__.py here just to trigger the auto-load process
import libs.transformer.src.actions


def get_action_function(action_name: str) -> Callable:
    """Returns the function for a given action, or raises a friendly error."""
    if action_name not in AVAILABLE_WRANGLING_ACTIONS:
        available = ", ".join(AVAILABLE_WRANGLING_ACTIONS.keys())
        raise ValueError(
            f"Action '{action_name}' is not registered. Available actions: {available}")
    return AVAILABLE_WRANGLING_ACTIONS[action_name]


# Future expansion: Plotting Defaults Registry
AVAILABLE_PLOT_DEFAULTS = {
    # e.g., "color_scale": apply_color_scale_default
}
