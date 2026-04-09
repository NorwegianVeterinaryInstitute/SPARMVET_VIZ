# Ingestion Library

## Purpose

The architectural "Gatekeeper." It reads raw input formats (TSV, VCF) and applies defensive programming checks to ensure the data strictly conforms to the established `input_fields` manifest contracts before any logic is applied.

## Key Components

- `DataIngestor (data_ingestor.py)`: Handles file I/O operations and evaluates schema integrity on load.

## I/O Summary

- **Input**: Raw UI uploads or files fetched via the `Connector` layer (using paths resolved from `config/connectors/`).
- **Output**: Schema-validated raw `pl.LazyFrame`s ready for the Transformer layer. Rejects non-conforming files immediately.

## Installation (Editable Mode)

According to the workspace standard, this library must be installed locally via:

```bash
pip install -e ./libs/ingestion
```
