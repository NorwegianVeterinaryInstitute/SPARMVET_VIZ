# Visualization Factory (Artist Pillar)

## Purpose
The architectural "Artist Pillar" responsible for translating tidy, standardized relational data into high-performance, publication-quality `Plotnine` (Grammar of Graphics) visualizations. It abstracts the complexities of the plotting library behind a declarative, data-agnostic manifest structure.

## Key Components
- `VizFactory (viz_factory.py)`: The primary orchestrator that initializes `ggplot` with a `mapping` block and iteratively pipes registered `layers`.
- `ActionRegistry (registry.py)`: The central mapping of string-based YAML action names (e.g., `"geom_boxplot"`) to their atomic Python component registrations.
- `Geoms Core (geoms/core.py)`: Implements individual `geom_*` wrappers including `geom_point`, `geom_boxplot`, and `geom_histogram`.
- `Themes Core (themes/core.py)`: Implements standard Plotnine themes (`theme_minimal`, `theme_bw`) for application-wide consistency.

## I/O Summary
- **Input**: A standardized Polars `LazyFrame` or `DataFrame`, a manifest dictionary, and a specific `plot_id`.
- **Method**: `render(df, manifest, plot_id)`
- **Output**: A standalone `plotnine` object ready for the Shiny Server (Orchestrator).

## Data Hand-off (ADR-010)
To maximize performance and memory efficiency, the `VizFactory (viz_factory.py)` performs a terminal `.collect().to_pandas()` strictly at the moment of `ggplot()` initialization, ensuring that only the final, filtered results are materialized for the Plotnine engine.

## Module Structure (src/)
The library is organized into functional subdirectories reflecting the Grammar of Graphics:
- `geoms/`: Geometric marks and statistical transforms.
- `scales/`: Aesthetic mappings and color scales.
- `themes/`: Non-data ink and visual appearance.
- `facets/`: Sub-plotting layouts.
- `coords/`: Coordinate systems.
- `positions/`: Overlap handling.
- `guides/`: Legend and axis title management.

## Installation (Editable Mode)
This library MUST be installed in editable mode:
```bash
pip install -e libs/viz_factory
```

## Debug Runner
Use the local CLI runner to verify plot generation:
```bash
.venv/bin/python libs/viz_factory/tests/debug_viz.py --output [PATH]
```
