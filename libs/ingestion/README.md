# Ingestion Library

# Authority: ADR-011, ADR-032

## Purpose

The architectural "Gatekeeper." It reads raw input formats (Excel, TSV) and applies defensive programming checks to ensure the data strictly conforms to the established `input_fields` manifest contracts.

## Key Components

- `ExcelHandler (excel_handler.py)`: [ADR-032] Authoritative normalization engine for extracting multiple sheets from Excel workbooks into standardized TSVs.
- `DataIngestor (ingestor.py)`: Architectural "Gatekeeper" that handles file I/O and enforces manifest schema contracts.
- `IngestionDebugger (debug_ingestor.py)`: [Validator] Independent CLI tool for manual verification of ingestion rules against raw assets.

## I/O Summary

- **Input**: Raw UI uploads or system files resolved via **Path Authority (ADR-031)**.
- **Output**: Schema-validated `pl.LazyFrame`s ready for the **Transformer (transformer)** layer. Rejects non-conforming files immediately.

## Installation (Editable Mode)

```bash
pip install -e ./libs/ingestion
```
