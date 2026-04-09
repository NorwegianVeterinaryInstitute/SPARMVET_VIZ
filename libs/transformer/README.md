# Transformer Library

## Purpose

The central engine for data wrangling and Phase 4 relational assembly. It enforces the ADR-013 data contracts by cleaning raw data and joining disparate sources into a single, tidy Polars DataFrame ready for visualization.

## Documentation
>
> [!IMPORTANT]
> This README is a high-level summary. For exhaustive deep-dives, architectural ADRs, and the full gallery of actions, you MUST refer to the official [Transformer Dev-to-User Guide](../../docs/workflows/wrangling.qmd).

## Key Components

- `DataWrangler (data_wrangler.py)`: Executes atomic cleaning actions against single datasets using declarative YAML pipelines.
- `DataAssembler (data_assembler.py)`: Orchestrates multi-source relational joins vertically. Includes ADR-024 Tier 1 Short-Circuit logic.
- `ActionRegistry (registry.py)`: Dictionary of allowed Python functions mapping to yaml actions.
- `MetadataValidator (metadata_validator.py)`: Validates user-uploaded metadata against contracts to prepare for joining.
- `IntegritySuite (transformer_integrity_suite.py)`: Master validation tool for programmatic action discovery and 1:1:1 verification.
- **Action Sub-Packages (ADR-024)**:
  - `Reshapinger (reshaping/core.py)`: Structural transformations (Pivot, Unpivot, Explode, Split).
  - `Cleaner (cleaning/core.py)`: Atomic cleaning (Rename, Replace, Nulls, Selection, Sanitization).
  - `Expressionist (cleaning/expressions.py)`: Pattern-based extraction (Regex) and atomic logic (Cast, Coalesce, Label_If).
  - `Categorizer (cleaning/advanced.py)`: Complex lookup mapping.
  - `Joiner (relational/joins.py)`: Relational assembly logic.
  - `Summarizer (performance/aggregation.py)`: Pre-visualization data collapsing for Tier 2.
- `Anchor (persistence/anchor.py)`: Tier 1 disk materialization tools (`sink_parquet`).
- **Reactive State (Tier 3)**: Transient views generated via Predicate Pushdown. Supports a "Memory Array" toggle to include/exclude Tier 2 steps on-the-fly.
- **Path Authority**: Persistence locations (Tiers 1-3) are determined by `config/connectors`, decoupling hardware from the UI.

## I/O Summary

- **Input**: Raw `pl.LazyFrame`s from the Ingestion layer, and YAML Manifest `spec` dictionaries.
- **Output**: Cleaned, joined, and contract-enforced `pl.LazyFrame`s matching the `output_fields` specification.

## Local CLI Runners

For Phase 1 & Phase 4 verification, use the local debugging runners to execute declarative YAML manifests and verify output TSVs:

```bash
.venv/bin/python libs/transformer/tests/debug_wrangler.py --data [INPUT] --manifest [YAML] --output [OUT]
.venv/bin/python libs/transformer/tests/debug_assembler.py --manifest [YAML] --output [OUT]
```

## Installation (Editable Mode)

According to the workspace standard, this library must be installed locally via:

```bash
pip install -e ./libs/transformer
```
