from typing import Callable, Dict, Any
import polars as pl
import logging

logger = logging.getLogger(__name__)

# The Central Repository for all Registered Plotting Factories
AVAILABLE_PLOTS: Dict[str, Callable[[pl.DataFrame, Dict[str, Any]], Any]] = {}


def register_plot(factory_id: str):
    """
    Standard Plugin Decorator for Plotting Factories.
    Any function decorated with `@register_plot("factory_id")` 
    will automatically become available to the YAML manifest executor.
    """
    def decorator(func: Callable):
        if factory_id in AVAILABLE_PLOTS:
            logger.warning(
                f"Warning: Plotting factory '{factory_id}' is already registered and will be overwritten.")
        AVAILABLE_PLOTS[factory_id] = func
        return func
    return decorator


def get_plot_function(factory_id: str) -> Callable:
    """Returns the function for a given plot factory, or raises an error."""
    if factory_id not in AVAILABLE_PLOTS:
        available = ", ".join(AVAILABLE_PLOTS.keys())
        raise ValueError(
            f"Plot factory '{factory_id}' is not registered. Available: {available}")
    return AVAILABLE_PLOTS[factory_id]
