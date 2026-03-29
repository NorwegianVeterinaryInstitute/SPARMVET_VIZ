import polars as pl
from plotnine import ggplot, aes
from typing import Dict, Any, List
# Explicit imports to ensure registration occurs
from viz_factory.registry import get_component


# --- Default Layer Policy ---
# These are injected silently if the manifest omits the relevant layer category.
# NOTE: No default geom is injected; every manifest MUST define at least one geom explicitly.
_DEFAULT_THEME = "theme_bw"
_DEFAULT_COORD = "coord_cartesian"
_DEFAULT_FACET = "facet_null"


class VizFactory:
    """
    Electronic Artist Pillar (VizFactory).
    Takes standardized Polars dataframes and applies declarative Plotnine layers.

    Default Injection Policy:
    - Theme: theme_bw (if no theme_ layer defined)
    - Coord: coord_cartesian (if no coord_ layer defined)
    - Facet: facet_null (if no facet_ layer defined)
    - Position/Stat: These are ggplot2 geom-level defaults (identity); no injection needed.
    """

    def render(self, df: Any, manifest: Dict[str, Any], plot_id: str):
        """
        Main entry point for rendering a single plot by ID from a manifest.
        Supports both Polars LazyFrame and DataFrame.

        manifest_dict follows the structure:
        {
           "plots": {
              "[plot_id]": {
                 "mapping": {"x": "column_a", "fill": "column_b"},
                 "layers": [
                    {"name": "geom_boxplot", "params": {"outlier_shape": "NA"}},
                    {"name": "theme_bw", "params": {}}
                 ]
              }
           }
        }
        """
        # Ensure it's a LazyFrame for consistent ADR-010 handling
        if isinstance(df, pl.DataFrame):
            df = df.lazy()
        plot_config = manifest.get('plots', {}).get(plot_id)
        if not plot_config:
            raise KeyError(f"Plot ID '{plot_id}' not found in manifest.")

        # 1. Initialize mapping (Agnostic Mapping)
        mapping_spec = plot_config.get('mapping', {})
        mapping = aes(**mapping_spec)

        # 2. Instantiate the ggplot object & ADR-010: Hand-off to Pandas strictly at init.
        p = ggplot(df.collect().to_pandas(), mapping)

        # 3. Apply Layers sequentially
        layers = plot_config.get('layers', [])
        applied_layers = []
        for layer_spec in layers:
            layer_name = layer_spec.get('name')
            layer_params = layer_spec.get('params', {})

            # Fetch the registered component
            component_func = get_component(layer_name)

            # Pipe the plot object through the component
            p = component_func(p, layer_params)
            applied_layers.append(layer_name)
            print(f"Applied layer: {layer_name}")

        # 4. Inject Defaults for missing layer categories
        # Coord default: coord_cartesian
        if not any(l.startswith("coord_") for l in applied_layers):
            from plotnine import coord_cartesian
            p = p + coord_cartesian()
            print(f"Applied default layer: {_DEFAULT_COORD}")

        # Facet default: facet_null
        if not any(l.startswith("facet_") for l in applied_layers):
            from plotnine import facet_null
            p = p + facet_null()
            print(f"Applied default layer: {_DEFAULT_FACET}")

        # Theme default: theme_bw
        if not any(l.startswith("theme_") or l.startswith("element_") for l in applied_layers):
            from plotnine import theme_bw
            p = p + theme_bw()
            print(f"Applied default layer: {_DEFAULT_THEME}")

        return p
