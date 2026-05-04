# Utils Library

## Purpose

Provides shared utilities, bridges, and configuration loaders utilized across the application layers. It enforces the separation of concerns by acting as the neutral third-party logic resolver for files outside the core analytic pipeline.

## Key Components

- `ConfigManager (config_loader.py)`: Recursively reads, validates, and dispatches YAML configuration files from `config/` to the relevant layers. Acts as the explicit "Bridge" between YAML rules and Python execution. Supports `!include` tags for modular manifests.
- `HashingUtility (hashing.py)`: Provides deterministic SHA-256 fingerprinting for manifests and metadata-embedded hash retrieval for Parquet anchors.
- `GalleryManager (gallery_manager.py)`: Logic layer for result preservation. Handles folder-based persistence for analysis bundles (CSV, PNG, YAML) in the `assets/gallery_data/` registry.

## I/O Summary

- **Input**: Directory paths, user-uploaded metadata paths, and raw `.yaml` configuration files.
- **Output**: Parsed, validated, and merged Python configuration dictionaries.

## Local CLI Runners / Tests

- Execute underlying loader checks via native `pytest`.

## Installation (Editable Mode)

According to the workspace standard, this library must be installed locally via:

```bash
pip install -e ./libs/utils
```

---

## Legacy Notes (Development Guardrails)

*Gatekeeper: Runtime Validation vs Development Validation*

1. **Runtime Validation (The "User" Guardrail):**
When the user fetches data, the Ingestion Layer performs a Structural Check against the `required_columns` obtained via `ConfigManager (config_loader.py)`. If they don't match, the Ingestion Layer raises a `SpeciesMismatchError` so the UI can notify the user gracefully.

2. **Development Validation (The "Developer" Guardrail):**
A Meta-Schema (`config/templates/species_schema.yaml`) guards against bad deployments. The `ConfigManager (config_loader.py)` checks every YAML file in `manifests/` against the Meta-Schema before boot, rejecting any malformed dictionaries.

### Good vs Bad Flow

- Bad Flow: Visualization calls Ingestion to get config.
- Good Flow: Ingestion calls Utils for config; Visualization also calls Utils for config. (Neutral resolution).
