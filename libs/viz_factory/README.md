# Viz Factory (Artist Pillar)

## Purpose

The `VizFactory` library provides a high-level, declarative interface for generating data-agnostic visualizations. It decouples the analytical pipeline from visual rendering by using a YAML-based manifest system.

## I/O

- **Input**: `pl.LazyFrame` (Polars) and a Dictionary (Manifest) following the SPARMVET visualization spec.
- **Output**: A `ggplot` object (Plotnine) ready for rendering or export.

## Architectural Features

- **Comparison Theater Support**: Native compatibility with dual-pane layout for side-by-side reference vs. active analysis.
- **Gated Reactivity**: Optimized for throttled recalculation via the `btn_apply` mechanism in the App Layer, ensuring performance on high-density datasets.

## Documentation
>
> [!IMPORTANT]
> This README is a high-level summary. For exhaustive component deep-dives, usage tutorials, and the testing rationale, you MUST refer to the official [Viz Factory Dev-to-User Guide](../../docs/workflows/visualisation_factory.qmd).

## Key Components (Violet Standard)

- **VizFactory (viz_factory.py)**: Central orchestration class that handles manifest parsing and ggplot composition.
- **GeomFactory (geoms/core.py)**: Registry for geometric layers (Point, Line, Bar). Supports mapping aesthetics to plotnine geoms.
- **ScaleFactory (scales/core.py)**: Handles visual scaling, axis naming, and color transformation rules.
- **ThemeFactory (themes/core.py)**: Manages stylistic presets and visual contrast settings.
- **FacetFactory (facets/core.py)**: Orchestrates layout partitioning (Wrap, Grid).
- **IntegritySuite (viz_factory_integrity_suite.py)** - [Orchestrator]: Programmatically audits every plot component for 1:1:1 evidence.
- **VisualisationRunner (debug_runner.py)** - [Dev Tool]: High-performance CLI for rendering isolated components and verifying manifest mappings.
- **Audit (debug_audit.py)** - [Validator]: Scans for Ghost Tasks (Tasks marked [x] but missing logic).
- **Distiller (debug_distiller.py)** - [Component Debugger]: Isolated test for Color Distiller palettes and scaling.
- **Sync (debug_bulk_sync.py)** - [Developer Utility]: Logic tool to auto-reflect library test results into the central task tracker.
- **ActionRegistry (registry.py)**: Decorator-based system for the dynamic extension of plot components.

## Local CLI Runners

For Artist Pillar verification, use the local debugging runners to render components and verify 1:1:1 integrity:

**Full Suite Audit (The Automated Gate):**

```bash
./.venv/bin/python libs/viz_factory/tests/viz_factory_integrity_suite.py --output_dir tmp/viz_factory/
```

**Single Component Render:**

```bash
./.venv/bin/python libs/viz_factory/tests/debug_runner.py --manifest [YAML_TRIPLET] --output_dir tmp/viz_factory/
```

Refer to the [Visualisation Factory Workflow](../../docs/workflows/visualisation_factory.qmd) for detailed implementation and usage examples.
