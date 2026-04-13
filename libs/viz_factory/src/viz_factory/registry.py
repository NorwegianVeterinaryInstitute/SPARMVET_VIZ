import logging
from typing import Callable, Dict, Any

logger = logging.getLogger(__name__)

# The Central Repository for all Registered Plotting Components (geoms, scales, themes, etc.)
# Components MUST accept (plot, spec) and return a modified plot.
PLOT_COMPONENTS: Dict[str, Callable[[Any, Dict[str, Any]], Any]] = {}


def register_plot_component(name: str):
    """
    Standard Plugin Decorator for Plotting Components.
    Any function decorated with `@register_plot_component("name")` 
    will automatically become available to the VizFactory.
    """
    def decorator(func: Callable):
        if name in PLOT_COMPONENTS:
            logger.warning(f"Overwriting plotting component: {name}")
        PLOT_COMPONENTS[name] = func
        return func
    return decorator


def get_component(name: str) -> Callable:
    """Returns the function for a given plotting component, or raises error."""
    if name not in PLOT_COMPONENTS:
        available = ", ".join(PLOT_COMPONENTS.keys())
        raise ValueError(
            f"Plot component '{name}' not found. Available: {available}")
    return PLOT_COMPONENTS[name]
