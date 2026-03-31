# Transformer Library

## Purpose
The central engine for data wrangling and Phase 4 relational assembly. It enforces the ADR-013 data contracts by cleaning raw data and joining disparate sources into a single, tidy Polars DataFrame ready for visualization.

## Key Components
- `DataWrangler (data_wrangler.py)`: Executes atomic cleaning actions against single datasets using declarative YAML pipelines.
- `DataAssembler (data_assembler.py)`: Orchestrates multi-source relational joins vertically.
- `ActionRegistry (registry.py)`: Dictionary of allowed Python functions mapping to yaml actions.
- `MetadataValidator (metadata_validator.py)`: Validates user-uploaded metadata against contracts to prepare for joining.
- **Action Sub-Packages (ADR-024)**:
    - `Reshapinger (reshaping/core.py)`: Structural transformations (Pivot, Unpivot, Explode, Split).
    - `Cleaner (cleaning/core.py)`: Atomic cleaning (Rename, Cast, Replace, Nulls, Selection).
    - `Expressionist (cleaning/expressions.py)`: Pattern-based extractions (Regex).
    - `Categorizer (cleaning/advanced.py)`: Complex lookup mapping.
    - `Joiner (relational/joins.py)`: Relational assembly logic.
    - `Summarizer (performance/aggregation.py)`: Pre-visualization data collapsing.
    - `Persistor (persistence/)`: Disk materialization tools (Parquet).

## I/O Summary
- **Input**: Raw `pl.LazyFrame`s from the Ingestion layer, and YAML Manifest `spec` dictionaries.
- **Output**: Cleaned, joined, and contract-enforced `pl.LazyFrame`s matching the `output_fields` specification.

## Local CLI Runners
For Phase 1 & Phase 4 verification, use the local debugging runners to execute declarative YAML manifests and verify output TSVs:
```bash
.venv/bin/python libs/transformer/tests/wrangler_debug.py --data [INPUT] --manifest [YAML] --output [OUT]
.venv/bin/python libs/transformer/tests/assembler_debug.py --meta [META] --mlst [MLST]
```

## Installation (Editable Mode)
According to the workspace standard, this library must be installed locally via:
```bash
pip install -e ./libs/transformer
```
