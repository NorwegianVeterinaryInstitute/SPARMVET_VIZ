# Modular Boundaries & Development Rules

This document outlines the **"Clear Lines" Policy** and development standards for the SPARMVET Orchestration layer.

## 1. Modular Boundaries & Reusability
The system is built on a collection of independent, reusable libraries located in `./libs/`. These libraries are designed to be standalone tools that focus on single domains (Ingestion, Transformation, Visualization).

### The "Clear Lines" Policy
To maintain architectural integrity and prevent circular dependencies, we enforce a unidirectional data flow:

**Data Flow: `Ingestor` ──▶ `Orchestrator/App` ──▶ `Transformer/Wrangler`**

*   **Ingestion (`libs/ingestion`)**: Responsible for reading raw data from files or sources into LazyFrames.
*   **Transformation (`libs/transformer`)**: Responsible for applying manifest-driven rules to LazyFrames.
*   **Orchestration (`app/` or `assets/scripts/`)**: The "Thinker". It coordinates the logic, joins datasets, and handles the handoff between Ingestion and Transformation.

### NO Cross-Library Imports
It is strictly **PROHIBITED** for libraries in `./libs/` to depend on each other.
- ❌ `transformer` must NOT import `ingestion`.
- ❌ `ingestion` must NOT import `transformer`.
- ✅ Both may import from `utils` (shared constants and config loaders).

---

## 2. Import Strategy: Package-First Authority
We use **Editable Mode** installations to treat our local libraries as first-class Python packages.

*   **Standard Import**: Always use `import ingestion` or `from transformer.data_wrangler import DataWrangler`.
*   **No Path Hacking**: The use of `sys.path.append` or `sys.path.insert` to find internal modules is forbidden.
*   **Directory Integrity**: The internal `src/` structure of each library must be respected (mapped via `pyproject.toml`) to maintain local testability for `pytest`.

---

## 3. The Manifest Data Contract (ADR-013)
The primary defense against code breakage is the **Manifest Contract**.

1.  **input_fields**: What we expect.
2.  **wrangling**: What we do.
3.  **output_fields**: What we promise to return.

**The Final Guard**: The processing engine must implement a final `.select()` using the `output_fields` keys. This ensures that even if an upstream source adds experimental columns, they are never exposed to the orchestration layer unless explicitly added to the contract.

---

## 4. Execution Authority
All work MUST occur within the root virtual environment:
```bash
./.venv/bin/python assets/scripts/wrangle_debug.py --manifest ...
```
This ensures all Editable Mode packages are correctly resolved and maintained across different development sessions.
