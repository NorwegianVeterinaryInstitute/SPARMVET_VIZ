from typing import Dict, Any
from plotnine import (
    scale_color_gradient, scale_fill_gradient,
    scale_color_gradient2, scale_fill_gradient2,
    scale_color_gradientn, scale_fill_gradientn,
    ggplot
)
from viz_factory.registry import register_plot_component


@register_plot_component("scale_color_gradient")
def handle_color_gradient(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Color Gradient component wrapper."""
    return p + scale_color_gradient(**spec)


@register_plot_component("scale_fill_gradient")
def handle_fill_gradient(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Fill Gradient component wrapper."""
    return p + scale_fill_gradient(**spec)


@register_plot_component("scale_color_gradient2")
def handle_color_gradient2(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Color Gradient 2 component wrapper."""
    return p + scale_color_gradient2(**spec)


@register_plot_component("scale_fill_gradient2")
def handle_fill_gradient2(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Fill Gradient 2 component wrapper."""
    return p + scale_fill_gradient2(**spec)


@register_plot_component("scale_color_gradientn")
def handle_color_gradientn(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Color Gradient n component wrapper."""
    return p + scale_color_gradientn(**spec)


@register_plot_component("scale_fill_gradientn")
def handle_fill_gradientn(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Fill Gradient n component wrapper."""
    return p + scale_fill_gradientn(**spec)
