# Architecture Decisions (SPARMVET_VIZ)
# Last Updated: 2026-03-26 by @dasharch

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

## ADR 009: Multi-Source Ingestion
**Status:** PROPOSED
**Context:** Multi-species dashboards require combining core analytical data (e.g., ResFinder, MLST) with metadata and other additional datasets.
**Decision:** Implement a **Multi-Source Ingestion** strategy.
- **Rule:** Additional datasets MUST share the same 'wrangling' decorator logic as core data and metadata to ensure consistency across the pipeline.
- **Rule:** Joins between datasets MUST be explicitly defined by a `join_on` key in the manifest.
- **Primary Key Rule:** The field referenced by `join_on` MUST be defined in the fields manifest with `is_primary_key: true`.
- **Implementation:** The `DataWrangler` or an Orchestrator must loop through all defined sources, apply respective wrangling rules, and perform Polars-based joins before handing off to the visualization factory.

## ADR 010: Polars as the Universal Engine
**Status:** ENFORCED
**Context:** To maintain scalability, the entire transformation chain must remain in **Polars**.
**Decision:** **Polars** is the mandatory library for all Wrangling, Ingestion, and Selection logic. 
- **Legacy Rule**: No Pandas calls allowed in `libs/transformer/` or `libs/ingestion/`. 
- **Hand-off Rule**: Conversion to Pandas is only permitted at the final moment inside the `viz_factory` for Plotnine compatibility.

## ADR 011: Modular Monorepo & Independent Package Management
**Status:** ENFORCED
**Context:** The project is a monorepo where each subdirectory in `libs/` and the main `app/` are designed to be independent Python packages. 
**Decision:** Each library MUST maintain its own `pyproject.toml`. 
- **Path Mapping:** 
  - `./libs/transformer`
  - `./libs/viz_factory`
  - `./app`
  - `./libs/utils`
- **Installation Rule:** The global `.venv` at the root will install these libraries in 'editable mode' (`pip install -e ./libs/transformer`). 
-   **Integrity Rule:** No symlinks. Each module must define its own dependencies, ensuring that if extracted, it could function as a standalone library.
-   **Dependency Rule:** Legacy requirements (`requirements.txt`, `requires.txt`) are strictly **FORBIDDEN**; the `pyproject.toml` file is the sole source of truth for module dependencies.

## ADR 012: Staged Data Assembly
**Status:** PROPOSED
**Context:** Multi-source data ingestion and complex joins can lead to monolithic, hard-to-maintain code if handled within a single class.
**Decision:** Adopt a **Staged Pipeline** approach.
- **Layer 1: Atomic Cleaning (The Wrangler):** The `DataWrangler` remains atomic. Its sole responsibility is "One Input -> One Cleaned Output". It follows declarative rules for a single dataset and MUST NOT contain join logic.
- **Layer 2: Orchestrated Assembly (The Assembler):** A dedicated `DataAssembler` or Orchestrator component is responsible for coordinating multiple Wrangler instances.
- **Responsibilities of Layer 2:**
    - Looping through defined datasets in the manifest.
    - Executing Layer 1 cleaning for each.
    - Performing Polars-based joins across cleaned datasets using `join_on`.
    - Applying final cross-dataset wrangling rules (e.g., calculated fields across joined tables).
- **Benefit:** Decouples cleaning logic from assembly logic, enabling independent testing and reuse of atomic wrangling actions.


## ADR 013: Dual-Validation Manifests
**Status:** ENFORCED
**Context:** To maintain robust data lineage between raw ingestion and final presentation, we must track schema state at two distinct points.
**Decision:** Manifests MUST explicitly define two schema states:
- **`input_fields`**: Defines the raw incoming schema (Raw/Ingestion). Used for validation before any wrangling occurs.
- **`output_fields`**: Defines the final consumed schema post-wrangling. This acts as the "Published Contract" for the Viz Factory and Orchestrator.
**Wrangling Rule:** The `wrangling` block remains the operational bridge between these two states.
- **`input_fields`** -> **`wrangling`** -> **`output_fields`**.


## ADR 014: Identity Logic for Wrangling
**Status:** ENFORCED
**Context:** Some reference datasets (e.g., APEC Virulence) should be imported "as-is" without transformations or column filtering.
**Decision:** The `DataWrangler` and Universal Runner MUST support **Identity Transformations**.
- **Rule:** If the `wrangling` block is missing or an empty list `[]`, the pipeline bypasses all atomic actions.
- **Rule:** If the `output_fields` block is missing or an empty list `[]`, the pipeline retains all columns from the `input_fields`.
- **Benefit:** Reduces manifest boilerplate for reference data and ensures the system remains robust when dealing with "straight-through" data ingestion.

- **Implementation:** Codified in **Section 12** of the [Workspace Standard](../rules/workspace_standard.md).
- **The Contract Guard:** The `output_fields` block is a strict Polars `.select()` contract, protecting the `DataAssembler` from Column Drift.

## ADR 015: Flexible Source Resolution (Manifest-First)
**Status:** IMPLEMENTED
**Context:** Multi-source ingestion required explicit path resolution.
**Decision:** Mandatory use of `source` blocks in yaml manifests.
- **Rule:** Every dataset entry must contain a `source` dictionary with `type` and `path`.
- **Implementation:** Prototyped in `DataIngestor` and finalized via `wrangle_debug.py`.
- **Reference:** See **Section 12** of the [Workspace Standard](../rules/workspace_standard.md).


## ADR 016: Package-First Authority (Editable Mode)
**Status:** IMPLEMENTED
**Context:** Fragmented library imports required a standard, reusable interface.
**Decision:** Core libraries are installed in **Editable Mode** to enable clean package communication.
- **Enforcement:** The **"Clear Lines" Policy** (Section 13, Workspace Standard) prohibits cross-library imports (e.g., `transformer` → `ingestion`).
- **Standard:** All execution locked to root `.venv` (Section 14, Workspace Standard).
- **Execution:** Validated via `assets/scripts/wrangle_debug.py` acting as an orchestration layer.

## ADR 018: Unified Transformer Model (Shared Registry)
**Status:** IMPLEMENTED
**Context:** The expansion from atomic cleaning (Layer 1) to multi-source assembly (Layer 2) required consistent transformation logic across both stages without code duplication.
**Decision:** The `DataWrangler` and `DataAssembler` must share the same central registry for actions.
- **Standard:** Both classes pull from `AVAILABLE_WRANGLING_ACTIONS` populated via the `@register_action` decorator.
- **Homogeneity:** Any atomic decorator (e.g., `strip_whitespace`, `split_column`) is natively available as an operation within an assembly recipe.
- **Benefit:** Simplifies library maintenance and ensures that "Wrangling" is treated as a single unified discipline across all pipeline layers.

## ADR 019: Decorator-Based Plot Component Registry
**Status:** PROPOSED
**Context:** The Viz Factory requires a modular way to build plots without a monolithic plotting script.
**Decision:** Implement a **Decorator Pattern** (`@register_plot_component`).
- **Registry Heart:** `libs/viz_factory/src/registry.py`.
- **Categories:** Components are registered by type: `geoms`, `scales`, `themes`, `facets`, and `coords`.
- **Benefits:** Allows the UI to dynamically list available "Plot Layers" for user selection.

## ADR 020: Data-Agnostic Plotting Manifest
**Status:** PROPOSED
**Context:** Plots must be reusable across different datasets (e.g., boxplots for different species).
**Decision:** Use a **Dictionary-of-Plots** where each plot contains a **List-of-Layers**.
- **Mapping Block:** Defines data-agnostic aesthetics (`x`, `y`, `fill`, `color`).
- **Layers Block:** An ordered list of dictionaries defining the plot construction.
- **Example:** A `geom_boxplot` layer is a dictionary of parameters passed to the registered function.

## ADR 021: Reactive State Management (Anchor vs. Filter)
**Status:** PROPOSED
**Context:** Users need to explore data by filtering without losing the "Master" view.
**Decision:** Implement a dual-state hand-off between the Transformer and the Viz Factory.
- **The Anchor:** The `Master Tidy Table` remains the unmodified source of truth.
- **The Filtered View:** A temporary LazyFrame created by the Transformer for exploration.
- **Reactivity:** The Viz Factory re-renders the *same* manifest against whichever state is active (Unmodified vs. Filtered).