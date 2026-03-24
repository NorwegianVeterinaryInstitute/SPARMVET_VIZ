# Architecture Decisions (SPARMVET_VIZ)
# Last Updated: 2026-03-21 by @dasharch

## ADR 001: Decorator-Based Action Registry
**Status:** IMPLEMENTED
**Context:** The Transformer module required a way to execute declarative YAML-based wrangling rules without a monolithic `registry.py`.
**Decision:** Implement a **Decorator Pattern** (`@register_action`). 
- **Registry Heart:** `libs/transformer/src/actions/base.py` defines the decorator and the `AVAILABLE_WRANGLING_ACTIONS` dictionary.
- **Auto-Load Strategy:** `libs/transformer/src/actions/__init__.py` imports `core` and `advanced` sub-packages to trigger the registration of all actions at system startup.
- **Benefits:** Decouples core logic from the execution engine, simplifies adding new bio-math functions, and enables automated introspection for the "In-App Help" pillar.
- **Multi-Column Support:** All registered actions MUST support a `columns` argument that accepts either a single string or a List[str].
- **Polars Implementation:** Actions must use `pl.col(columns)` to enable parallel execution across the target list.

## ADR 002: Tidy Data Contract (Long Format)
**Status:** ENFORCED
**Context:** Multi-species dashboards with variable gene counts (AMR) require a data format that remains stable even if species columns change.
**Decision:** All pipelines **MUST** produce Tidy (Long Format) CSV/TSV data (e.g., `Sample | Gene_Name | Result`).
- **Transformer Implementation:** Actions like `split_and_explode` and `derive_categories` are designed specifically to operate on or produce long-format Polars LazyFrames.

## ADR 003: "Thin" Shiny Frontend
**Status:** IMPLEMENTED
**Context:** Heavy data processing (Polars) should not slow down the UI rendering.
**Decision:** The Shiny App (`app/src/ui.py` and `server.py`) acts solely as an **Orchestrator**.
- **Rule:** No raw data wrangling or complex plotting logic allowed inside the `server.py` reactive blocks; all logic must be deferred to `libs/`.

## ADR 004: YAML-Only Configuration & Registry Recognition
**Status:** ENFORCED
**Context:** The "Four-Pillar Strategy" originally mentioned JSON Schema, but the current code architecture is strictly **YAML-driven**.
**Decision:** All metadata schemas, wrangling rules, and data contracts will be managed via **YAML manifests**.
- **Registry Recognition**: The system 'recognizes' novel wrangling functions via the `@register_action(name)` decorator. These functions are automatically discovered by the `DataWrangler` at runtime through the centralized Python registry. 
- **Mapping**: The YAML `action` key acts as the look-up token. There is no intermediate JSON schema; the YAML is parsed directly into Python dictionaries for processing.
- **Manifest Schema:** The YAML `wrangling` block for any action should prefer the key `columns: []` to allow batch processing.


## ADR 005: Universal Wrangler Runner
- **Agnostic Logic:** `libs/transformer/tests/test_wrangler.py` must not contain decorator-specific hardcoding. 
- **Dynamic Dispatch:** It must initialize the `DataWrangler`, parse the provided `--manifest`, and apply whatever rules are defined therein to the `--data` TSV.
- **CLI Standard:** It must always support `--data`, `--manifest`, and `--output` arguments via `argparse` to ensure manual reproducibility.

## ADR 006: Asset-Driven Prototyping Strategy
**Status:** ENFORCED
**Context:** For the "Walking Skeleton" to be interactive without real Galaxy data, we require a robust synthetic data layer.
**Decision:** Use the `./assets/` layer to drive the prototype lifecycle.
- **Data Generation**: `create_test_data.py` generates synthetic `.tsv` files based on real pipeline schemas (ResFinder, metadata).
- **Deployment Provisioning**: `create_test_deployment.py` generates deployment YAMLs in `config/deployments/test_deployments/`. These files act as the configuration anchor, binding synthetic TSV files to active YAML manifests.
- **Logic Integration**: The `DataWrangler` and `DataIngestor` consume these synthetic assets, allowing full end-to-end testing of the wrangling registry without external dependencies.
- **Source of Truth**: The directories `config/manifests/species/` and `templates/` are now considered **LEGACY** and replaced by the modular `config/manifests/pipelines/` structure.

## ADR 007: Minimal Dataset & Manual UI Deferral
**Status:** ENFORCED
**Context:** To achieve a functional prototype by March 21st, we must reduce implementation debt.
**Decision:** Adopt a **'Minimal Dataset'** strategy and defer automated UI complexity.
- **Minimal Dataset**: We assume input TSVs follow the YAML contract perfectly for Phase A/B. Malformed data handling is moved to Phase C.
- **Manual UI Deferral**: The dashboard will initially support manual file loading and sidebar selection of synthetic assets, avoiding the immediate need for the BioBlend/Galaxy API Mode B.
- **Pillar 4 Shift**: Formal JSON Schema validation is deferred in favor of direct YAML manifest interpretation.

## ADR 008: Visualisation Library - Plotnine Primary
**Status:** ENFORCED
**Context:** Previous ADR prioritized Plotly. After re-evaluating the "Artist" pillar, Plotnine is chosen for consistency with the Tidy data logic.
**Decision:** **Plotnine** is the primary visualization engine for the Prototype.
- **Plotly Status**: Moved to **[DEFERRED]** list.
- **Implementation**: Factory functions will return `ggplot` objects. Interactivity is sacrificed for Phase 1 to ensure standard "walking skeleton" data-visual flow.

## ADR 009: Polars as the Universal Engine
**Status:** ENFORCED
**Context:** To maintain scalability, the entire transformation chain must remain in **Polars**.
**Decision:** **Polars** is the mandatory library for all Wrangling, Ingestion, and Selection logic. 
- **Legacy Rule**: No Pandas calls allowed in `libs/transformer/` or `libs/ingestion/`. 
- **Hand-off Rule**: Conversion to Pandas is only permitted at the final moment inside the `viz_factory` for Plotnine compatibility.

## ADR 010: Modular Monorepo & Independent Package Management
**Status:** ENFORCED
**Context:** The project is a monorepo where each subdirectory in `libs/` and the main `app/` are designed to be independent Python packages. 
**Decision:** Each library MUST maintain its own `pyproject.toml`. 
- **Path Mapping:** 
  - `./libs/transformer`
  - `./libs/viz_factory`
  - `./app`
  - `./libs/utils`
- **Installation Rule:** The global `.venv` at the root will install these libraries in 'editable mode' (`pip install -e ./libs/transformer`). 
- **Integrity Rule:** No symlinks. Each module must define its own dependencies, ensuring that if extracted, it could function as a standalone library.
- **Dependency Rule:** Legacy requirements (`requirements.txt`, `requires.txt`) are strictly **FORBIDDEN**; the `pyproject.toml` file is the sole source of truth for module dependencies.
