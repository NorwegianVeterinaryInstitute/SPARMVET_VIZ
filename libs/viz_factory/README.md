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
- **ThemeFactory (themes/core.py)**: Registry and handlers for visual themes (minimal, bw, classic, etc.).
- **FacetFactory (facets/core.py)**: Registry and handlers for multi-panel layout logic (wrap, grid).
- **ActionRegistry (registry.py)**: Decorator-based system for component discovery and extension.

## Usage
Refer to the [Visualisation Factory Workflow](../../docs/workflows/visualisation_factory.qmd) for detailed implementation and usage examples.
