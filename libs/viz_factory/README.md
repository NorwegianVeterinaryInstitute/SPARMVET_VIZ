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
- **ThemeFactory (themes/core.py)**: Manages visual styling presets and custom theme element overrides.
- **FacetFactory (facets/core.py)**: Orchestrates multi-panel layouts (wrap, grid, null).
- **CoordFactory (coords/core.py)**: Handles spatial coordinate systems and transformations.
- **PositionFactory (positions/core.py)**: Adjusts overlapping geometries (stack, dodge, jitter).
- **GuideFactory (guides/core.py)**: Controls legend and colorbar appearance (legend, colorbar, none).
- **IntegritySuite (viz_factory_integrity_suite.py)**: Artist Integrity Suite for automated component discovery and 1:1:1 triplet verification.
- **ActionRegistry (registry.py)**: Decorator-based system for component discovery and extension.

## Usage
Refer to the [Visualisation Factory Workflow](../../docs/workflows/visualisation_factory.qmd) for detailed implementation and usage examples.
