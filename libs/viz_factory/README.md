# Visualization Factory (Artist Pillar)

## Purpose
The architectural "Artist Pillar" responsible for translating tidy, standardized relational data into high-performance, publication-quality Plotnine (Grammar of Graphics) visualizations. It abstracts the complexities of the plotting library behind a declarative, data-agnostic manifest structure.

## Key Components
- `VizFactory (viz_factory.py)`: The primary orchestrator that initializes `ggplot` with a `mapping` block and iteratively pipes registered `layers`.
- `ActionRegistry (registry.py)`: The central mapping of string-based YAML action names (e.g., `"geom_boxplot"`) to their atomic Python component registrations.
- `Geoms Core (geoms/core.py)`: Implements individual `geom_*` wrappers (boxplots, histograms, etc.) using the `@register_plot_component` decorator.

## I/O Summary
- **Input**: A standardized Polars `LazyFrame`, a manifest dictionary, and a specific `plot_id`.
- **Output**: A standalone `plotnine` object ready for the Shiny Server (Orchestrator).

## Data Hand-off (ADR-010)
To maximize performance and memory efficiency, the `VizFactory (viz_factory.py)` accepts `pl.LazyFrame`s. It performs a terminal `.collect().to_pandas()` strictly at the moment of initialization, ensuring that only the final, filtered results are materialized for the Plotnine engine.

## Data-Agnostic Mapping Rules
All plots derive their structure from a standardized `mapping` block in the manifest:
1. `x`: Defines the primary axis or category.
2. `y`: Defines the measured value (optional for histograms).
3. `fill`/`color`/`shape`: Defines groups or aesthetics.
4. `layers`: A sequential list of dictionaries detailing the `geoms`, `scales`, and `themes` to be applied.

## Installation (Editable Mode)
This library MUST be installed in editable mode for development sync:
```bash
pip install -e libs/viz_factory
```

## Debug Runner
Use the local CLI runner to verify plot generation:
```bash
.venv/bin/python libs/viz_factory/tests/debug_viz.py --data [TSV] --plot_id [ID] --output [PATH]
```
