# Viz Factory (Artist Pillar)

## Purpose
The `VizFactory` library provides a high-level, declarative interface for generating data-agnostic visualizations. It decouples the analytical pipeline from visual rendering by using a YAML-based manifest system.

## I/O
- **Input**: `pl.LazyFrame` (Polars) and a Dictionary (Manifest) following the SPARMVET visualization spec.
- **Output**: A `ggplot` object (Plotnine) ready for rendering or export.

## Key Components (Violet Standard)
- **VizFactory (viz_factory.py)**: The central orchestration class that parses manifests and layers aesthetics.
- **GeomFactory (geoms/core.py)**: Registry and handlers for geometric layers (Point, Line, Bar, etc.).
- **ScaleFactory (scales/core.py)**: Registry and handlers for visual scales (Axes, Colors, Sizes, etc.).
- **ThemeFactory (themes/)**: Manages visual styling presets and custom theme element overrides.
- **FacetFactory (facets/)**: Orchestrates multi-panel layouts (wrap, grid, null).
- **CoordFactory (coords/)**: Handles spatial coordinate systems and transformations.
- **PositionFactory (positions/)**: Adjusts overlapping geometries (stack, dodge, jitter).
- **GuideFactory (guides/)**: Controls legend and colorbar appearance (legend, colorbar, none).
- **Stat Implementation**: As per the Grammar of Graphics, statistical transformations (e.g., `stat_bin`, `stat_count`) are integrated directly into the **Geom Layer** (`geoms/`) to simplify the manifest and ensure data-agnostic logic.
- **ActionRegistry (registry.py)**: Decorator-based system for component discovery and extension.

## Usage
Refer to the [Visualisation Factory Workflow](../../docs/workflows/visualisation_factory.qmd) for detailed implementation and usage examples.
