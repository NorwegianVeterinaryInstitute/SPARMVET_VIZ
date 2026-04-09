# Ingestion Library

## Purpose

The architectural "Gatekeeper." It reads raw input formats (TSV, VCF) and applies defensive programming checks to ensure the data strictly conforms to the established `input_fields` manifest contracts before any logic is applied.

## Key Components

- `DataIngestor (ingestor.py)`: Architectural "Gatekeeper" that handles file I/O and enforces manifest schema contracts.
- `IngestionDebugger (debug_ingestor.py)` - [Validator]: Independent CLI tool for manual verification of ingestion rules against raw biological assets.

## I/O Summary

- **Input**: Raw UI uploads or files fetched via the `Connector` layer (using paths resolved from `Connector (local_connector.yaml)` per ADR-031).
- **Output**: Schema-validated raw `pl.LazyFrame`s ready for the Transformer layer. Rejects non-conforming files immediately.

## Installation (Editable Mode)

According to the workspace standard, this library must be installed locally via:

```bash
pip install -e ./libs/ingestion
```
