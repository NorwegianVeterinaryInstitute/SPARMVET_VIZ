import polars as pl
from plotnine import ggplot, aes
from typing import Dict, Any, List
# Explicit imports to ensure registration occurs
from viz_factory.registry import get_component
from utils.errors import VisualizationError
import difflib


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
        """
        # Ensure it's a LazyFrame for consistent ADR-010 handling
        if isinstance(df, pl.DataFrame):
            df = df.lazy()

        raw_plot_config = manifest.get('plots', {}).get(plot_id)
        if not raw_plot_config:
            raise KeyError(f"Plot ID '{plot_id}' not found in manifest.")

        # 1. Standardize Manifest (Handle factory_id and flat aesthetics)
        plot_config = self._standardize_config(
            raw_plot_config, manifest.get('plot_defaults', {}))

        # 2. Validate Aesthetics (ADR-034)
        mapping_spec = plot_config.get('mapping', {})
        all_cols = df.columns
        for aesthetic, col_name in mapping_spec.items():
            if col_name not in all_cols:
                matches = difflib.get_close_matches(
                    col_name, all_cols, n=1, cutoff=0.6)
                tip = f"Ensure column '{col_name}' exists in the current dataset."
                if matches:
                    tip += f" Hint: Did you mean '{matches[0]}'?"
                raise VisualizationError(
                    f"Aesthetic '{aesthetic}' references unknown column '{col_name}'.",
                    tip=tip
                )

        # Initialize mapping (Agnostic Mapping)
        mapping = aes(**mapping_spec)

        # 2. Tier 3: Apply UI-driven Filters (Predicate Pushdown)
        ui_filters = plot_config.get('filters', [])
        if ui_filters:
            print(
                f"  └── 🍃 Tier 3 (The Leaf): Applying {len(ui_filters)} UI filters...")
            for f in ui_filters:
                col = f.get("column")
                op = f.get("op", "eq")
                val = f.get("value")

                if op == "eq":
                    df = df.filter(pl.col(col) == val)
                elif op == "ne":
                    df = df.filter(pl.col(col) != val)
                elif op == "gt":
                    df = df.filter(pl.col(col) > val)
                elif op == "ge":
                    df = df.filter(pl.col(col) >= val)
                elif op == "lt":
                    df = df.filter(pl.col(col) < val)
                elif op == "le":
                    df = df.filter(pl.col(col) <= val)
                elif op == "in":
                    if isinstance(val, list):
                        df = df.filter(pl.col(col).is_in(val))
                    else:
                        df = df.filter(pl.col(col) == val)

        # 3. Instantiate the ggplot object & ADR-010: Hand-off to Pandas strictly at init.
        # We materialise here after all UI/Leaf filters are pushed down.
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
        # Theme: Manifest defaults or fallback
        if not any(l.startswith("theme_") or l.startswith("element_") for l in applied_layers):
            theme_name = plot_config.get('theme', _DEFAULT_THEME)
            try:
                theme_func = get_component(theme_name)
                p = theme_func(p, {})
                print(f"Applied default theme: {theme_name}")
            except:
                from plotnine import theme_bw
                p = p + theme_bw()
                print(f"Applied fallback theme: theme_bw")

        # Coord default: coord_cartesian
        if not any(l.startswith("coord_") for l in applied_layers):
            from plotnine import coord_cartesian
            p = p + coord_cartesian()
            print(f"Applied default layer: {_DEFAULT_COORD}")

        # Facet: Handle flat 'facet_by' or default
        if not any(l.startswith("facet_") for l in applied_layers):
            facet_col = plot_config.get('facet_by')
            if facet_col:
                from plotnine import facet_wrap
                p = p + facet_wrap(f"~{facet_col}")
                print(f"Applied facet_wrap: ~{facet_col}")
            else:
                from plotnine import facet_null
                p = p + facet_null()
                print(f"Applied default layer: {_DEFAULT_FACET}")

        # Labels (Title)
        title = plot_config.get('title')
        if title:
            from plotnine import labs
            p = p + labs(title=title)

        return p

    def _standardize_config(self, plot_config: Dict[str, Any], manifest_defaults: Dict[str, Any]) -> Dict[str, Any]:
        """ Standardizes high-level or legacy manifests into the mapping/layers spec. """
        import copy
        config = copy.deepcopy(plot_config)

        # Merge manifest-level defaults
        for k, v in manifest_defaults.items():
            if k not in config:
                config[k] = v

        # 1. Promote flat aesthetics to mapping if mapping is missing
        if 'mapping' not in config:
            mapping = {}
            # List of aesthetics to extract from top level
            possible_aes = ['x', 'y', 'color', 'fill',
                            'size', 'alpha', 'shape', 'label']
            for aes_key in possible_aes:
                if aes_key in config:
                    mapping[aes_key] = config[aes_key]

            if mapping:
                config['mapping'] = mapping

        # 2. Handle factory_id translation
        factory_id = config.get('factory_id')
        if factory_id and not config.get('layers'):
            layers = []
            if factory_id == "heatmap_logic":
                # Heatmaps use 'fill' for tiles in plotnine, but manifests often say 'color'
                if 'mapping' in config and 'color' in config['mapping']:
                    config['mapping']['fill'] = config['mapping']['color']
                layers.append({"name": "geom_tile", "params": {
                              "color": "white", "size": 0.1}})

            elif factory_id == "bar_logic":
                if 'mapping' in config and 'y' in config['mapping']:
                    layers.append({"name": "geom_col", "params": {}})
                else:
                    layers.append({"name": "geom_bar", "params": {}})

            elif factory_id == "scatter_logic":
                layers.append({"name": "geom_point", "params": {}})

            if layers:
                config['layers'] = layers

        return config
