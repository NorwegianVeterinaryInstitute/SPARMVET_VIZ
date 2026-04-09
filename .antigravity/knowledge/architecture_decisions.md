# Architecture Decisions (SPARMVET_VIZ)

# Last Updated: 2026-03-29 by @dasharch
>
> all paths must be provided relative to the project root. Absolute paths or symlinks are not allowed.

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
- **Integrity Rule:** No symlinks. Each module must define its own dependencies, ensuring that if extracted, it could function as a standalone library.
- **Dependency Rule:** Legacy requirements (`requirements.txt`, `requires.txt`) are strictly **FORBIDDEN**; the `pyproject.toml` file is the sole source of truth for module dependencies.

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

- **Implementation:** Codified in **Section 12** of the [Workspace Standard](./.agents/rules/workspace_standard.md). #REVIEW there is no section 12. It likely has been moved to another rules file.
- **The Contract Guard:** The `output_fields` block is a strict Polars `.select()` contract, protecting the `DataAssembler` from Column Drift.

## ADR 015: Flexible Source Resolution (Manifest-First)

**Status:** IMPLEMENTED
**Context:** Multi-source ingestion required explicit path resolution.
**Decision:** Mandatory use of `source` blocks in yaml manifests.

- **Rule:** Every dataset entry must contain a `source` dictionary with `type` and `path`.
- **Implementation:** Prototyped in `DataIngestor` and finalized via `wrangle_debug.py`.
- **Reference:** See Section 3 (Manifest Data Contract) of the [Data Engine Protocol](./.agents/rules/rules_data_engine.md).

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

## ADR 022: The Violet Law (Documentation Standard)

**Status:** ENFORCED
**Context:** Consistent verbal and written communication is necessary when identifying core architectural classes and files.
**Decision:** All human-facing documentation (.qmd files) and library READMEs ("Key Components" lists) MUST format component references as `ComponentName (file_name.py)`.

- **Purpose:** Decouples technical context ambiguity by enforcing a "Who and Where" standard simultaneously for readers.
- **Strict Boundary:** This format is strictly DOCUMENTATION-ONLY. It MUST NOT be used for functional class names, variables, filenames, or high-level docstrings in the actual codebase logic.
- **Reference:** Workspace Rules `rules_aesthetic.md` (The Violet Law).

## ADR 023: Statistical Transformations (Stats) Delegation

**Status:** ENFORCED
**Context:** The `stat_*` layer logic in Plotnine often mimics or operates directly on geometric layers. Creating an entirely separate complex abstract registry mechanism for `stats` components would needlessly complicate the declarative YAML manifest structure.
**Decision:** All important standard statistical transformations (Stats) MUST be implemented and registered directly within the `geoms/` directory.

- **Benefit:** Simplifies the manifest structure by injecting stats logic as parameter arguments into existing geom factories (e.g. `geom_bar` handling `stat="count"`).
- **Compliance:** This explicitly preserves the ggplot2 (R) "Grammar of Graphics" while eliminating overhead from maintaining disjointed duplicate state.

## ADR-024: Tiered Data Lifecycle (Anchor vs. View)

**Status:** PROPOSED (March 31, 2026)
**Context:** Plotnine's 22-minute render time for >200k rows necessitates a data reduction strategy. Users require "instant" UI filtering without re-running heavy Layer 1/2 joins.
**Decision:** Implement a two-tier data management system within the Transformer library.

- **Tier 1 (The Anchor):** The fully assembled Tidy Table (Layer 1 + Layer 2). This is persisted to disk as a `.parquet` file in `tmp/session_anchor.parquet`.
- **Tier 2 (The View):** A temporary, filtered, or pre-aggregated LazyFrame derived from Tier 1 for rapid UI rendering.
- **Persistence Layer:** The `DataAssembler` shall use `pl.sink_parquet()` for Tier 1 and the UI shall use `pl.scan_parquet()` for Tier 2 to leverage Predicate Pushdown and memory efficiency.

## ADR 025: The Gallery & Recipe Pattern (Visual Cookbook)

**Status:** PROPOSED — Target: Next Session
**Context:** Users without deep ggplot2 knowledge need a way to discover, understand, and adapt plot manifests for their own AMR datasets. Static documentation is insufficient — examples must be executable and inspectable.
**Decision:** Implement a **Visual Gallery** where each registered VizFactory component is documented as a 3-part **Recipe**:

1. **Representative Data Header** — A TSV snippet (first N rows) showing the expected data shape.
2. **YAML Manifest** — The exact manifest used to produce the plot (copy-paste ready).
3. **Resulting Image** — The rendered plot PNG.

**Implementation Rules:**

- **Gallery Flag**: The `bulk_debug_viz_factory_layers.py` runner SHALL support a `--gallery` flag. When set, it writes a `gallery_report.md` to the output dir containing all three recipe parts per component.
- **Premiere Example**: The Triple-Source Integration (Metadata/Phenotypes/Genotypes) plots from Phase 9 serve as the premier end-to-end gallery entry, demonstrating real AMR data.
- **Data Safety**: Gallery data headers are generated from test TSV files only. Real patient data MUST NOT appear in gallery output.
- **Documentation Target**: `docs/appendix/viz_factory_rationale.qmd` hosts the User-as-Artist philosophy linking to the gallery.

**Benefit:** Enables a self-service "copy, modify, render" workflow for end users, directly supporting the SPARMVET_VIZ mission of accessible AMR data visualisation.

**Low-Level Coding Design Note:** This pattern is explicitly designed to support **Low-Level Coding** — a practice where domain scientists (veterinary epidemiologists, microbiologists) interact with the system at the YAML abstraction layer rather than the Python layer. The YAML manifest *is* the code. A user who can edit a text file can produce a custom AMR visualisation. The Gallery provides the examples needed to make this self-teaching.

## ADR 026: Reactive State, Persona Logic & Reporting

**Status:** ENFORCED (April 7, 2026)
**Context:** Decoupling production rigidity from developer flexibility while maintaining sub-5s responsiveness for 200k+ rows.
**Decision:**

- **Persona Isolation**: Use `ui_config.yaml` to toggle feature visibility (e.g., masking 'Branching' in Pipeline Mode).
- **The Identity Rule**: Tier 3 (Leaf) is initialized as an identity of Tier 2 (Branch). Sidebar filters modify the Leaf view via Predicate Pushdown ONLY.
- **Immutable Audit**: "No Trace, No Export" rule. Manual exclusions require a mandatory 'User Note'.
- **Persistence**: YAML is the authoritative format for all saved 'Recipes' to ensure human-readability and Git compatibility.

## ADR 027: Multi-Module UI Orchestration & Aesthetics

**Status:** PROPOSED (April 8, 2026)
**Context:** Need a scalable UI supporting different Personas (User/Developer) while adhering to the "Thin Frontend" rule.
**Decision:** Implement a 5-module UI stack where the frontend acts strictly as an **Orchestrator**.

- **Module Integration:**
  - **DataConnector**: Ingests via `libs/ingestion`.
  - **WrangleStudio**: Chains decorators from `libs/transformer`.
  - **VizViewer**: Renders side-by-side Tier 2/3 plots via `libs/viz_factory`.
  - **AuditEngine**: Immutable logging and "Recipe Pre-filling" logic.
  - **GalleryViewer**: Browser for `assets/gallery_data/`.
- **Aesthetic Constraints:** - **Sidebars**: Light Grey (#f8f9fa).
  - **Tooltips/Help**: Light Yellow (#fff9c4) or Light Green (#e8f5e9).
  - **Prohibition**: No "Deep Violet" themes in the UI (Documentation only).

## ADR 028: Gallery Content & Logic Separation

**Status:** PROPOSED (April 8, 2026)
**Context:** Need an expandable gallery with proper attribution and licensing.
**Decision:** Separate logic from data assets.

- **Logic Layer:** `libs/viz_gallery` (Standalone Python package).
- **Content Layer:** `assets/gallery_data/`.
- **Mandatory Assets:** Each example folder MUST contain: `example_data.tsv`, `recipe_manifest.yaml`, `preview_plot.png`, `LICENSE.md`, and `README.md` (for author credits).

### ADR 029a: Dashboard Theater & Panel Layout Specs

**Status:** PROPOSED (April 8, 2026)
**Context:** Need a high-density, interactive workspace for data exploration with specific "Theater" states.
**Decision:** Implement a Three-Column Shell with a multi-state Central Theater.
Implement a manifest-driven UI that discovers its own structure at runtime.

- **Dynamic Tab Discovery:** The `VizViewer (viz_factory.py)` MUST scan the active YAML manifest for all defined plot IDs and programmatically generate a corresponding tab for each.
- **Automatic Column Discovery:** The UI MUST introspect the incoming Polars LazyFrame (Tier 1/2) to identify all available columns.

- **Navigation Panel (Left):**  - Nested hierarchy: `Group (e.g., QC)` > `Plot Selection`. - Must include a `Global Export` toggle and a `Persona Selector`. It must be possible to deactivate Persona selector by UI configuration file `config/ui/<template_persona>_template.yaml`)

- **Central Theater (Center):** - **Vertical Layout:** Top 60% Plot / Bottom 40% Data Table (adjustable). Maximize/Minimize controls for each component.
- **Comparison Mode:** Support a horizontal grid `[Tier 1 | Tier 2 | Tier 3]` where plot Tier 3 updates reactively to the filters and selects while Tier 1 and Tier 2 does not.

- **Right Sidebar (Audit Stack):** Logic Color-Coding differentiates Inherited Tier 2 steps (Light violet background) from User-added Tier 3 steps (Light Yellow background). User steps must include a mandatory comment field. - **Interactive Nodes:** Each step added by the user must have a trash icon (Remove) and a mandatory comment field (hover to view reason). Option to remove Tier 2 steps must be configurable in `config/ui/<template_persona>_template.yaml`. If enabled (default in template), a warning (eg. This might break the plot render, original plot can be restored using <restore button>) and confirmation steps must been shown before deletion. Restore button should be placed at the top of the right sidebar.

## ADR 029b: Dynamic Discovery & Interaction Logic

**Status:** PROPOSED (April 8, 2026)
**Decision:** Implement manifest-driven discovery and standardized interactivity.

- **Dynamic Tabs:** `VizViewer` MUST programmatically generate tabs by scanning plot IDs in the active YAML manifest. It must be possible to specify plot tittle and subtitle in The active YAML manifest (but optional).
- **Auto-Discovery:** UI MUST introspect the Polars schema to identify all columns; all columns (except Primary Keys) must be hideable via a picker and include top-level filter boxes.
- **Persistence:** Sidebars are open by default but must be collapsible to allow 100% theater width.

## ADR 029c: Interaction & Visibility Logic

**Status:** PROPOSED (April 8, 2026)
**Decision:** Standardize how users hide/show data and outliers.

- **Table Interactivity:** - Every column (except the Primary Key) must be "Hideable" via a column-picker. Affect the Tier 3 (Leaf) view.
  - Search/Filter boxes at the top of every column directly affect the Tier 3 (Leaf) view.
- **Sidebar Persistence:** Sidebars must be "Collapsible" (Open by default on Desktop) to allow the Theater to occupy 100% of the width during visualization.

## ADR 030: Manifest & External Data Ingestion

**Status:** PROPOSED (April 8, 2026)
**Decision:** Expand `DataConnector (ingestor.py)` to handle custom user inputs beyond standard pipelines.

- **Manifest Upload:** Support uploading predefined YAML manifests to override default pipeline logic.
- **External Data Joins:** Allow adding "Additional Data" files. The UI MUST provide a joining helper that uses `libs/transformer` relational logic to verify Primary Key matching before merging. (eg.can reuse parts of scripts in .assets/scripts)

## ADR 031: Data Tier & Session Persistence

**Status:** PROPOSED (April 8, 2026)
**Context:** Need a configurable, reliable way to handle session recovery and multi-location data storage.
**Decision:** Implement a Three-Location Persistence strategy managed via `config/ui/paths.yaml`.

- **Location 1 (Tiers 1 & 2):** Configurable system path for heavy parquet anchors. Restricted access usually applies here.
- **Location 2 (Tier 3 & Sessions):** User-accessible directory for exports and imported data.
  - **Ghost Manifests:** Automatic background saving of the active recipe. The system must retain the last 5 versions in `tmp/sessions/` for emergency recovery.
- **Location 3 (Gallery):** Default local path of gallery data is `.assets/gallery_data/`. The gallery logic layer path is `libs/viz_gallery` (Standalone Python package). It is designed to be syncable with a Git repository.

## ADR 032: Asset Script Integration (UI-Bridge)

**Status:** PROPOSED (April 8, 2026)
**Decision:**
The UI `DataConnector` and `WrangleStudio` must/can act as a wrapper for existing `assets/scripts/` (e.g., manifest creation, synthetic data generation) to ensure logic reuse. Any reused script needs to be moved to the appropriate libs directory before being re-used in the UI. Not functionality should be removed. However functionality can be added to the scripts to make them more user-friendly/reusable.

- **Import Helper:** When a user uploads Excel files, the UI invokes `assets/scripts/parse_pipeline_excel.py` or `SF_create_manifest.py` to normalize data to TSV. Move those scripts to appropriate library locations.
- **Synthetic Data:** The "Developer Studio" must provide a GUI for `assets/scripts/create_test_data.py` to allow one-click creation of mock datasets for testing.
