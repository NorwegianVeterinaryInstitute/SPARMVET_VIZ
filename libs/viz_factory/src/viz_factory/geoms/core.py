from typing import Dict, Any
from plotnine import (
    geom_point, geom_line, geom_bar, geom_col, geom_boxplot, geom_violin,
    geom_histogram, geom_smooth, geom_density, geom_errorbar, geom_pointrange,
    geom_tile, geom_raster, geom_text, geom_label, geom_jitter, geom_step,
    stat_count, stat_bin, stat_summary, stat_boxplot, stat_ydensity,
    stat_smooth, stat_density, stat_qq, stat_ecdf, stat_unique, stat_function,
    ggplot, labs
)
from viz_factory.registry import register_plot_component


@register_plot_component("geom_boxplot")
def handle_boxplot(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Boxplot component wrapper."""
    return p + geom_boxplot(**spec)


@register_plot_component("geom_violin")
def handle_violin(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Violin (Density) component wrapper."""
    return p + geom_violin(**spec)


@register_plot_component("geom_point")
def handle_point(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Point (Scatter) component wrapper."""
    return p + geom_point(**spec)


@register_plot_component("geom_line")
def handle_line(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Line (Connected points) component wrapper."""
    return p + geom_line(**spec)


@register_plot_component("geom_bar")
def handle_bar(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Bar (count) component wrapper."""
    return p + geom_bar(**spec)


@register_plot_component("geom_col")
def handle_col(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Column (identity) component wrapper."""
    return p + geom_col(**spec)


@register_plot_component("geom_histogram")
def handle_histogram(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Histogram component wrapper."""
    return p + geom_histogram(**spec)


@register_plot_component("geom_smooth")
def handle_smooth(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Smooth (Regression) component wrapper."""
    return p + geom_smooth(**spec)


@register_plot_component("geom_density")
def handle_density(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Density component wrapper."""
    return p + geom_density(**spec)


@register_plot_component("geom_errorbar")
def handle_errorbar(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Errorbar component wrapper."""
    return p + geom_errorbar(**spec)


@register_plot_component("geom_pointrange")
def handle_pointrange(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Pointrange component wrapper."""
    return p + geom_pointrange(**spec)


@register_plot_component("geom_tile")
def handle_tile(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Tile (Heatmap) component wrapper."""
    return p + geom_tile(**spec)


@register_plot_component("geom_raster")
def handle_raster(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Raster (Heatmap) component wrapper."""
    return p + geom_raster(**spec)


@register_plot_component("geom_text")
def handle_text(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Text (Annotation) component wrapper."""
    return p + geom_text(**spec)


@register_plot_component("geom_label")
def handle_label(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Label (Annotation) component wrapper."""
    return p + geom_label(**spec)


@register_plot_component("geom_jitter")
def handle_jitter(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Jitter component wrapper."""
    return p + geom_jitter(**spec)


@register_plot_component("geom_step")
def handle_step(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Step plot component wrapper (useful for ECDF and staircases)."""
    return p + geom_step(**spec)


@register_plot_component("geom_segment")
def handle_segment(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Segment component wrapper (useful for Lollipop charts)."""
    from plotnine import geom_segment
    return p + geom_segment(**spec)

# --- Statistical Components ---


@register_plot_component("stat_count")
def handle_stat_count(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    return p + stat_count(**spec)


@register_plot_component("stat_bin")
def handle_stat_bin(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    return p + stat_bin(**spec)


@register_plot_component("stat_identity")
def handle_stat_identity(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    # Most geoms default to stat_identity already
    return p


@register_plot_component("stat_summary")
def handle_stat_summary(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    return p + stat_summary(**spec)


@register_plot_component("stat_boxplot")
def handle_stat_boxplot(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    return p + stat_boxplot(**spec)


@register_plot_component("stat_ydensity")
def handle_stat_ydensity(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    return p + stat_ydensity(**spec)


@register_plot_component("stat_smooth")
def handle_stat_smooth(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    return p + stat_smooth(**spec)


@register_plot_component("stat_density")
def handle_stat_density(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    return p + stat_density(**spec)


@register_plot_component("stat_qq")
def handle_stat_qq(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    return p + stat_qq(**spec)


@register_plot_component("stat_ecdf")
def handle_stat_ecdf(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    return p + stat_ecdf(**spec)


@register_plot_component("stat_unique")
def handle_stat_unique(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    return p + stat_unique(**spec)


@register_plot_component("stat_function")
def handle_stat_function(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Statistical function layer. 'fun' must be a callable; string lambdas are evaluated."""
    spec = dict(spec)
    fun = spec.get("fun")
    if isinstance(fun, str):
        try:
            # Safe for developer-controlled manifests only
            spec["fun"] = eval(fun)
        except Exception as e:
            print(
                f"Warning: stat_function could not evaluate 'fun' string: {e}")
            return p
    return p + stat_function(**spec)


@register_plot_component("labs")
def handle_labs(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Label component (title, x, y, custom scales)."""
    return p + labs(**spec)
