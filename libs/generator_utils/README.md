# Generator SDK

## Purpose

The architectural engine responsible for bootstrapping new pipelines and generating high-integrity synthetic data. It acts as a headless precursor to the Visual Pipeline Designer, converting raw Excel/TSV files into structured datasets and manifests.

## Key Components

- `XlsxExtractor (extractor.py)`: Extracts and normalizes multi-sheet `.xlsx` workbooks to standardized `.tsv` formats for ingestion.
- `ManifestBootstrapper (bootstrapper.py)`: Infers data schemas from raw files to scaffold baseline YAML manifests (`input_fields`, `output_fields`).
- `KeyReconciler (key_reconciler.py)`: Logic for identifying and aligning primary keys across disparate and noisy datasets.
- `AquaSynthesizer (aqua_synthesizer.py)` - [SDK Core]: Generates high-integrity relational synthetic test data based on Ground Truth statistical sampling.
- `SDKDebugger (test_sdk.py)` - [Orchestrator]: Automated validation for synthesizer and extractor logic.
- `ReconcileDebugger (debug_reconciler.py)` - [Dev Tool]: Interactive CLI for fuzzy key matching audit and suggested regex generation.
- `AmbiguityDebugger (debug_ambiguity.py)` - [Dev Tool]: Specialized CLI for identifying fuzzy match collisions and materializing conflict reports.

## I/O Summary

- **Input**: Raw Excel workbooks, TSVs, or predefined Reference Manifests.
- **Output**: Standardized `.tsv` files, bootstrapped `.yaml` manifests, and relational Synthetic "Fake" Datasets.

## Local CLI Runners

Located primarily in `assets/scripts/` to rapidly parse and scaffold test data:

```bash
python3 assets/scripts/create_test_data.py --data_file ...
python3 assets/scripts/create_manifest.py --data_dir ...
```

## Installation (Editable Mode)

According to the workspace standard, this library must be installed locally via:

```bash
pip install -e ./libs/generator_utils
```
