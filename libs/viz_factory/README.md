# Visualization Factory

## Purpose
Generates high-performance, publication-quality Plotnine (Grammar of Graphics) plot objects independently of the data source. It operates purely on standardized Polars dataframes, applying visual defaults and properties passed dynamically from the configuration layer.

## Key Components
- `PlotFactory (plot_factory.py)`: The core engine that translates declarative UI/Plot specifications into reactive ggplot/Plotnine components.

## I/O Summary
- **Input**: Master Tidy Polars DataFrames and merged Plot Configuration dictionaries.
- **Output**: Static `plotnine` objects (or identical ggplot structures) ready for display within the Shiny `ui.py` layer.

## Installation (Editable Mode)
According to the workspace standard, this library must be installed locally via:
```bash
pip install -e ./libs/viz_factory
```
