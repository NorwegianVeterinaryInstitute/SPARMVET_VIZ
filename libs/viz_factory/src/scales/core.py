from typing import Dict, Any
from plotnine import (
    scale_color_gradient, scale_fill_gradient,
    scale_color_gradient2, scale_fill_gradient2,
    scale_color_gradientn, scale_fill_gradientn,
    scale_color_distiller, scale_fill_distiller,
    scale_color_cmap, scale_fill_cmap,
    scale_color_discrete, scale_fill_discrete,
    scale_color_brewer, scale_fill_brewer,
    scale_color_manual, scale_fill_manual,
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


@register_plot_component("scale_color_distiller")
def handle_color_distiller(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Color Distiller component wrapper."""
    return p + scale_color_distiller(**spec)


@register_plot_component("scale_fill_distiller")
def handle_fill_distiller(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Fill Distiller component wrapper."""
    return p + scale_fill_distiller(**spec)


@register_plot_component("scale_color_cmap")
def handle_color_cmap(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Color Matplotlib Cmap component wrapper."""
    return p + scale_color_cmap(**spec)


@register_plot_component("scale_fill_cmap")
def handle_fill_cmap(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Fill Matplotlib Cmap component wrapper."""
    return p + scale_fill_cmap(**spec)


@register_plot_component("scale_color_viridis_c")
def handle_color_viridis_c(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Color Viridis (Continuous) via cmap mapping."""
    if "cmap_name" not in spec:
        spec["cmap_name"] = "viridis"
    return p + scale_color_cmap(**spec)


@register_plot_component("scale_fill_viridis_c")
def handle_fill_viridis_c(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Fill Viridis (Continuous) via cmap mapping."""
    if "cmap_name" not in spec:
        spec["cmap_name"] = "viridis"
    return p + scale_fill_cmap(**spec)


@register_plot_component("scale_color_discrete")
def handle_color_discrete(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Color Discrete component wrapper."""
    return p + scale_color_discrete(**spec)


@register_plot_component("scale_fill_discrete")
def handle_fill_discrete(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Fill Discrete component wrapper."""
    return p + scale_fill_discrete(**spec)


@register_plot_component("scale_color_brewer")
def handle_color_brewer(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Color Brewer (Discrete) component wrapper."""
    return p + scale_color_brewer(**spec)


@register_plot_component("scale_fill_brewer")
def handle_fill_brewer(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Fill Brewer (Discrete) component wrapper."""
    return p + scale_fill_brewer(**spec)


@register_plot_component("scale_color_manual")
def handle_color_manual(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Color Manual component wrapper."""
    return p + scale_color_manual(**spec)


@register_plot_component("scale_fill_manual")
def handle_fill_manual(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Fill Manual component wrapper."""
    return p + scale_fill_manual(**spec)
