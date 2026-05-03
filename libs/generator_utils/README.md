# Generator SDK

# Authority: ADR-011, ADR-032

## Purpose

The architectural engine responsible for bootstrapping new pipelines and generating high-integrity synthetic data. It acts as a headless precursor to the Visual Pipeline Designer, converting raw Excel/TSV files into structured datasets and manifests.

**Standard:** Fully Project-Agnostic and Schema-Aware (**ADR-003**).

## Key Components

### Core Engine (src/)

- `AquaSynthesizer (aqua_synthesizer.py)`: [SDK Core] Generates high-integrity relational synthetic test data based on Ground Truth statistical sampling. Supports real-data anonymization and schema-driven "Quick Generate" modes.
- `XlsxExtractor (extractor.py)`: Extracts and normalizes multi-sheet `.xlsx` workbooks into standardized `.tsv` formats for ingestion.
- `ManifestBootstrapper (bootstrapper.py)`: Infers data schemas from raw files to scaffold baseline YAML manifests (`input_fields`, `output_fields`).
- `KeyReconciler (reconciler.py)`: Logic for identifying and aligning primary keys across disparate and noisy datasets.

### Developer Tools & Debuggers (tests/)

- `SDKDebugger (test_sdk.py)`: [Orchestrator] Automated validation for synthesizer and extractor logic.
- `AmbiguityDebugger (debug_ambiguity.py)`: [Dev Tool] Specialized CLI for identifying fuzzy match collisions and materializing conflict reports.
- `ReconcileDebugger (debug_reconciler.py)`: [Dev Tool] Interactive CLI for fuzzy key matching audit and suggested regex generation.

## I/O Summary

- **Input**: Raw Excel/TSV files or predefined Schema Manifests (Location 2).
- **Output**: Standardized `.tsv` files, bootstrapped `.yaml` manifests, and Project-Agnostic Synthetic Recordsets.

## Execution Authority (ADR-031)

Internal scripts are resolved via the `Bootloader (app/src/bootloader.py)` using keys defined in the connector configuration.

```bash
# Example CLI Usage for AquaSynthesizer
./.venv/bin/python libs/generator_utils/src/generator_utils/aqua_synthesizer.py --generate_only [HEADERS]
```

## Installation (Editable Mode)

```bash
pip install -e ./libs/generator_utils
```
