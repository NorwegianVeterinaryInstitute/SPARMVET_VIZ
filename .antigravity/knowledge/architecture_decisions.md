# Architecture Decisions (SPARMVET_VIZ)

# Last Updated: 2026-04-09 by @dasharch
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

## ADR 003: "Thin" Shiny Frontend & Project-Agnostic Mandate

**Status:** IMPLEMENTED (April 9, 2026)
**Context:** Heavy data processing (Polars) should not slow down the UI rendering, and the system must be applicable to any project schema.
**Decision:** The Shiny App (`app/src/ui.py` and `server.py`) acts solely as an **Orchestrator**.

- **Rule:** No raw data wrangling or complex plotting logic allowed inside the `server.py` reactive blocks; all logic must be deferred to `libs/`.
- **Agnostic Mandate:** The system MUST NOT assume domain-specific column names (e.g., 'species', 'sample_id'). All UI elements and logic chains must derive their structure from manifest introspection (**ADR-004**) or Polars schema discovery (**ADR-029b**).

## ADR 004: YAML-Only Configuration & Registry Recognition

**Status:** ENFORCED
**Context:** The "Four-Pillar Strategy" originally mentioned JSON Schema, but the current code architecture is strictly **YAML-driven**.
**Decision:** All metadata schemas, wrangling rules, and data contracts will be managed via **YAML manifests**.

- **Registry Recognition**: The system 'recognizes' novel wrangling functions via the `@register_action(name)` decorator. These functions are automatically discovered by the `DataWrangler` at runtime through the centralized Python registry.
- **Mapping**: The YAML `action` key acts as the look-up token. There is no intermediate JSON schema; the YAML is parsed directly into Python dictionaries for processing.
- **Manifest Schema:** The YAML `wrangling` block for any action should prefer the key `columns: []` to allow batch processing.

## ADR 005: Universal Wrangler Runner

- **Agnostic Logic:** `libs/transformer/tests/debug_wrangler.py` must not contain decorator-specific hardcoding.
- **Dynamic Dispatch:** It must initialize the `DataWrangler`, parse the provided `--manifest`, and apply whatever rules are defined therein to the `--data` TSV.
- **CLI Standard:** It must always support `--data`, `--manifest`, and `--output` arguments via `argparse` to ensure manual reproducibility.

## ADR 006: Asset-Driven Prototyping Strategy

**Status:** DEPRECATED (Moved to ADR-032)
**Context:** For the "Walking Skeleton" to be interactive without real Galaxy data, we required a robust synthetic data layer.
**Decision:** Use the `./assets/` layer to drive the prototype lifecycle.
**Note:** This strategy has been superseded by the "Library Autonomy" logic in ADR-032.

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

## ADR 024: Tiered Wrangling & Data Lifecycle (ADR-024 Refinement)

**Status:** IMPLEMENTED (April 10, 2026)
**Context:** Plotnine's 22-minute render time for >200k rows necessitates a data reduction strategy. Users require "instant" UI filtering without re-running heavy Layer 1/2 joins.
**Decision:** Implement a three-tier tree lifecycle and a two-tier nested wrangling structure within the `DataWrangler (data_wrangler.py)`.

### 1. The 3-Tier Tree Lifecycle

- **Tier 1 (The Trunk):** Relational Anchor. The fully assembled Tidy Table (Layer 1 + Layer 2). Persisted as `tmp/session_anchor.parquet`.
- **Tier 2 (The Branch):** Plot-Specific Anchor. A filtered, summarized, or reshaped branch optimized for a functional group of plots. Persisted as `tmp/branch_*.parquet`.
- **Tier 3 (The Leaf):** Interactive UI View. Transient LazyFrames derived from Tier 1 or Tier 2 via Predicate Pushdown.

### 2. Nested Wrangling Structure (YAML)

All `wrangling` blocks in YAML manifests MUST use nested tier keys to separate logic:

- **`tier1` (Tidy/Relational):** Logic applied to wide data (Join, Clean, Rename, Filter). This produces the "Filterable Trunk".
- **`tier2` (Plot-Prep):** Visual-specific transformations (Unpivot/Long-format, Summarize, Aggregate).

**Identity Logic (Missing Keys):**

- If a manifest is missing `tier2`, it is treated as an **Identity Transformation** for that tier (Tier 1 output is passed through unchanged).
- The `DataWrangler` uses `_resolve_tier()` to extract the correct sequence, ensuring structural homogeneity.
- **Mandate:** Flat list wrangling is deprecated; all new manifests must adopt the nested structure.

## ADR 025: The Gallery & Recipe Pattern (Visual Cookbook)

**Status:** PROPOSED --- Target: Next Session
**Context:** Users without deep ggplot2 knowledge need a way to discover, understand, and adapt plot manifests for their own AMR datasets. Static documentation is insufficient --- examples must be executable and inspectable.
**Decision:** Implement a **Visual Gallery** where each registered VizFactory component is documented as a 3-part **Recipe**:

1. **Representative Data Header** --- A TSV snippet (first N rows) showing the expected data shape.
2. **YAML Manifest** --- The exact manifest used to produce the plot (copy-paste ready).
3. **Resulting Image** --- The rendered plot PNG.

**Implementation Rules:**

- **Gallery Flag**: The `bulk_debug_viz_factory_layers.py` runner SHALL support a `--gallery` flag. When set, it writes a `gallery_report.md` to the output dir containing all three recipe parts per component.
- **Premiere Example**: The Triple-Source Integration (Metadata/Phenotypes/Genotypes) plots from Phase 9 serve as the premier end-to-end gallery entry, demonstrating real AMR data.
- **Data Safety**: Gallery data headers are generated from test TSV files only. Real patient data MUST NOT appear in gallery output.
- **Documentation Target**: `docs/appendix/viz_factory_rationale.qmd` hosts the User-as-Artist philosophy linking to the gallery.

**Benefit:** Enables a self-service "copy, modify, render" workflow for end users, directly supporting the SPARMVET_VIZ mission of accessible AMR data visualisation.

**Low-Level Coding Design Note:** This pattern is explicitly designed to support **Low-Level Coding** --- a practice where domain scientists (veterinary epidemiologists, microbiologists) interact with the system at the YAML abstraction layer rather than the Python layer. The YAML manifest *is* the code. A user who can edit a text file can produce a custom AMR visualisation. The Gallery provides the examples needed to make this self-teaching.

## ADR 026: Reactive State, Persona Logic & Reporting

**Status:** ENFORCED (April 7, 2026)
**Context:** Decoupling production rigidity from developer flexibility while maintaining sub-5s responsiveness for 200k+ rows.
**Decision:**

- **Persona Isolation**: Use `config/ui/templates/ui_persona_template.yaml` to toggle feature visibility (e.g., masking 'Developer Mode', 'Interactability', 'Gallery'). UI Personas MUST ONLY control functional masking and rendering, NOT system paths.
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

- **Central Theater (Center):** Vertical Layout: Top 60% Plot / Bottom 40% Data Table (adjustable). Maximize/Minimize controls for each component.
- **Comparison Theater (APPROVED — Phase 12-A):** Optional dual-column layout activated by a `comparison_mode` toggle. Gated by `comparison_mode_enabled` in `config/ui/<persona>_template.yaml`.

  **Left Column — Reference Sandbox (`#f8f9fa` recessed):**
  - `plot_reference`: Tier 2 reference plot — **immutable**, never affected by user filters.
  - `ref_tier_switch` toggle: `Tier 1 (wide)` ↔ `Tier 2 (viz-transformed)` — affects reference table only.
  - `table_reference`: Read-only exploration table. User may filter/column-pick for visual inspection (e.g., "which samples are from France, 2002?") but NO writes are persisted. Label: `"⚠️ Inspection only — changes here are not saved"`.

  **Right Column — Active Pane (theater white `#ffffff`):**
  - `plot_leaf`: Tier 3 plot, recalculated only on explicit **▶ Apply** click.
  - `view_toggle`: `Wide (Tier 1)` ↔ `Long/Aggregated (Tier 3')` — switches the interactive table view; hints at filter stage.
  - `table_leaf`: Wide-format Tier 1 data with column picker and interactive row filters.
  - **▶ Apply Button**: Explicit trigger for `tier3_leaf()` recalculation. Prevents constant UI re-rendering on large datasets.

  **Position-Aware Recipe Pipeline (The Core Rule):**
  Tier 3 = Tier 1 fork with Tier 2 steps pre-filled in the right Audit Panel.
  The **position** of each step relative to inherited Tier 2 nodes determines its transform stage:
  - Steps placed **ABOVE** Tier 2 nodes → applied to wide Tier 1 data (pre-transform filtering).
  - Steps placed **BELOW** Tier 2 nodes → applied after viz transforms (post-transform selection).
  - Removing an inherited Tier 2 step triggers a `ui.modal` warning: "This may break the plot render."

- **Right Sidebar (Audit Stack):** Logic Color-Coding differentiates Inherited Tier 2 steps (Light violet background `#f3e5f5`) from User-added Tier 3 steps (Light Yellow background `#fffde7`). User steps must include a mandatory comment field. Each step has a trash icon (Remove). Removing Tier 2 steps requires warning + confirmation. Restore button (**Reset Sync**) is blue (`#0d6efd`) and resets Tier 3 state to match Tier 2. Centered header alignment is mandatory for all sidebar categories.

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

## ADR 031: Data Tier, Session Persistence & Path Authority

**Status:** IMPLEMENTED (April 9, 2026)
**Context:** Need a configurable, reliable way to handle session recovery and multi-location data storage.
**Decision:** Implement a **Path Authority Strategy** strictly managed via `config/connectors/`.

- **Connector Authority Rule:** System connection paths (Locations 1-5), Script Agency paths, and Runtime Environments MUST be defined in dedicated connector configurations (e.g., `config/connectors/local/local_connector.yaml`), entirely decoupled from UI logic.
- **Location 1 (Raw/Ingestion):** Path to raw external data assets.
- **Location 2 (Manifests):** Path to pipeline definitions.
- **Location 3 (Tiers 1 & 2):** Curated Parquet Anchors & Views (`session_anchor.parquet`).
- **Location 4 (User & Tiers 3):** User-accessible directory for session states, active UI leaf interaction, and ghost saves.
- **Location 5 (Gallery):** Assets gallery for cloned/submitted recipes (`assets/gallery_data/`).

## ADR 032: Library Autonomy & Script Internalization

**Status:** IMPLEMENTED (April 9, 2026)
**Decision:** All core utility scripts (Synthetic Data Generation, Excel Parsing) MUST reside within their respective library `src/` directories to ensure package self-sufficiency (**ADR-011**).

- **Migration**: Deprecated `assets/scripts/` in favor of library-internal modules (e.g., `generator_utils.aqua_synthesizer`).
- **Discovery**: The UI consumes these scripts via `bootloader.get_script_path()`, ensuring path autonomy.
- **Rule**: Deletion of the `assets/scripts/` directory is mandatory once migration is verified to prevent logic fragmentation.

## ADR 033: Educational Gallery & Structured Metadata

**Status:** IMPLEMENTED (April 18, 2026)
**Context:** Users need more than just technical recipes; they need context on *how* and *why* to use specific visualizations.
**Decision:** Implement an "Educational Gallery" extension that pairs technical manifests with structured markdown metadata.

- **Split-Pane Viewer:** The Gallery Browser MUST utilize a 50/50 split layout.
  - **Left Pane (Technical):** Displays the plot, Tier 1/2 data samples, and the raw YAML recipe.
  - **Right Pane (Educational):** Displays a nicely formatted (shiny::markdown) description derived from an associated `.md` file.
- **Mandatory Metadata Template:** Every submission to the public gallery MUST include a description file with the following mandatory sections:
  1. **Suitability:** When most suited for use.
  2. **Data Schema (Tier 1):** Required data types (categorical vs numeric).
  3. **Transformation Logic (Tier 2):** Description of essential reshapes.
  4. **Interpretations:** Assumptions, known limitations, and comments.
- **Governance:** High-density analysis "Theaters" focus on discovery, while the Gallery focuses on "Visual Literacy."
- **Visual Polish**: Centering of the Guidance pane content using `mx-auto` and `text-center` is required for all recipes.

## ADR 034: Unified Diagnostic Layer & Aesthetic Error Handling

**Status:** IMPLEMENTED (April 10, 2026)
**Context:** Silent failures in large Polars pipelines lead to user frustration and "Black Box" analytical profiles.
**Decision:** Implement a system-wide diagnostic layer that traps common failures and suggests human-readable fixes.

- **The SPARMVET_Error Pattern**: Implement a central `SPARMVET_Error` class in `libs/utils`. Libraries (Ingestion, Transformer, VizFactory) MUST raise specific subclasses containing a `tip` attribute.
- **Visual Feedback**: The UI catches these errors and renders them inside a **Soft Note Modal** (`#fff9c4`).
- **Heuristic Suggestions**: When a 'Missing Column' error occurs, the Transformer must use string similarity (e.g. Levenshtein) to suggest the closest match from the existing schema to help catch typos immediately.
- **Fail-Fast Viz**: The VizFactory must pre-validate manifest aesthetics against the incoming dataset columns before attempting (ggplot) plotnine construction to prevent crashing the render reactive.

## ADR-035: Gallery Taxonomy & Visual Discovery System

**Status:** IMPLEMENTED (April 18, 2026)
**Context:**  As the Gallery grows, users require a structured way to discover recipes beyond simple folder browsing. ADR-033 established the split-pane view, but not the classification of plots.
**Decision:**  Implement a formal taxonomy based on "Families" and "Difficulty":

- **Families**: Distribution, Correlation, Comparison, Ranking, Evolution, Part-to-Whole.
- **Difficulty**: [Simple], [Intermediate], [Advanced].
- **Data Pattern**: Explicit labeling of numeric and categorical dimensions.
- **Metadata Integration**: These fields are mandatory in `recipe_meta.md` and drive the real-time UI filtering.
**Aesthetic Constraint**: Taxonomy sidebar headers must be bold, underlined, and scaled (1.2rem) for hierarchical clarity.

## ADR-036: Persistent UI Integrity (ID Sanitation Pivot)

**Status:** IMPLEMENTED (April 18, 2026)
**Context:** Switching between heavy-state modules (e.g., Wrangle Studio vs. Theater) can lead to 'ghost' elements (stale headers or metrics) if the DOM is not forcefully cleared by the reactive engine.
**Decision:** Implement a **Dynamic ID Pivot** for main orchestration containers.

- **Rule**: The ID of the primary `navset_card_tab` MUST be derived from the active sidebar selection (e.g., `id=f"central_theater_tabs_{sidebar_name}"`).
- **Effect**: This forces Shiny to treat each module's theater as a distinct DOM entity, ensuring all previous module artifacts are flushed upon context switch.

## ADR-038: Contextual Sidebar Masking (Focus Mode)

**Status:** PROPOSED (April 19, 2026)
**Context:** Global UI controls (Project Loader, Session management) clutter the interface during specialized tasks like Gallery browsing where those controls are redundant.

- **Decision**: Implement a **Focus Mode** pattern via server-side reactive reification.
- **Reactive Masking**: Global Sidebar tools (Project Navigator, Filters, Session) are moved from a static `ui.py` definition to a reactive `@render.ui` in `server.py`.
- **Benefit**: This physically removes the headers and accordion panels from the DOM when the "Gallery" tab is active, ensuring zero visual clutter.
- **Natural Interface**: The UI is reconfigured to provide a persistent Global Navigation header (Home/Gallery) while task-specific tools exist as transient reactive overlays.

## ADR-039: The Blueprint Architect Workflow & TubeMap

**Status:** PROPOSED (April 19, 2026)
**Context:** Manifest-driven development requires a "multiscale" environment—switching between project-wide lineage (Macro) and component-level transformations (Micro). Fragmented UI tabs prevent a cohesive "Design → Verify" loop.
**Decision:** Implement the **Blueprint Architect** as a Tri-Pane "Flight Deck" with a DAG-driven project context.

- **The TubeMap Navigation (Map-First):** The central theater features a top-aligned, collapsible **Interactive Map** (Mermaid/SVG). This graph visualizes the entire manifest lineage (Tier 1 → Tier 2 → Assembly → Plot).
- **Contextual Focus:** Clicking a node (station) in the map dynamically focuses the entire UI on that component's state.
- **The Architectural Stack (Right Sidebar):** The Right Sidebar is reconfigured as the **Active Blueprint Stack**. It displays the atomic logic steps (Wrangling) for the station currently selected in the Map.
- **Stacked Live Preview (The Live Viewer):** The primary theater panel displays a **Vertical Stack** (Plot over Data Table). This provides a single-view verification of how logic changes affect the visual and data outcomes simultaneously.
- **Branching & Forking:** The Map View enables "Visual Forking"—selecting a node and initiating a new branch directly in the DAG, producing corresponding YAML additions to the manifest.

**Benefit:** Creates a unified development environment that minimizes context switching and provides immediate visual feedback on architectural changes.

## ADR-041: Unified Manifest Standard (Keyed-Schema & Ordered-Logic)

**Status:** ENFORCED (April 20, 2026)
**Context:** Ambiguity between List-of-Dicts and Dictionary formats for manifest components led to inconsistent structural integrity and potential backend performance penalties.
**Decision:** Standardize on a hybrid model that respects the functional requirements of each manifest layer:

1. **Field Definitions (`input_fields`, `output_fields`):**
   - **Format:** Mandatory **Rich Dictionary** (`slug: {original_name, type, label}`).
   - **Rationale:** High-performance $O(1)$ lookup is essential for Ingestion and Column Mapping. Dictionary format aligns natively with Polars `.schema()`.
   - **Constraint:** Key names (slugs) must be unique within the manifest context.

2. **Wrangling Blocks (`tier1`, `tier2`):**
   - **Format:** Mandatory **Sequential List** of action dictionaries.
   - **Rationale:** Order of operations is foundational to data pipelining. Actions must be processed deterministically in the user-defined sequence.

3. **Fragment Packaging:**
   - **Standard:** Included YAML fragments (`!include`) MUST be "Flat". Redundant top-level anchoring keys (e.g., repeating `input_fields:` inside the included file) are strictly prohibited.
   - **Rationale:** Supports the `ConfigManager` auto-unnesting logic and prevents deep-key nesting in memory.

**Benefit:** Resolves the architectural disconnect between the UI contract viewer and the Backend data engines, ensuring both high performance and high integrity.

---

## ADR-040: Bidirectional Lineage Navigation & Blueprint Interface Fields

**Status:** PARTIALLY IMPLEMENTED (April 20, 2026 — Phases 18-A, 18-B, 18-C + live-testing fixes complete; 18-D/E/F pending)
**Context:** Phase 18 work on the Blueprint Architect Interface (Fields) tab revealed that a flat "view one component's fields" model cannot represent the real manifest topology: multi-ingredient assemblies (many Tier 1 → one Tier 2), per-plot wrangling steps, and branching outputs. More importantly, the most natural scientific workflow is **reverse lineage** — starting from a desired plot output and tracing backwards to find where a missing field must be added or computed.

**Decision:** Extend the Blueprint Architect with a **Bidirectional Lineage Rail** and a **3-column contract viewer** replacing the current flat Interface (Fields) tab.

### Core Concepts

**1. Two TubeMap levels (tabs within the existing accordion):**

- **Tab A — Project Overview (existing):** Full project DAG showing all Tier 1 datasets, assemblies, and plots. Provides macro context.
- **Tab B — Component Lineage Rail (new):** When a node is selected in Tab A, this renders only the linear chain for that node — from raw source to the terminal plot, showing the exact path that data travels. If the project branches (one assembly → N plots), the Rail shows one branch at a time, with a branch selector.

**2. 3-column Interface panel (replaces flat tab-3 Fields):**
When any node on the Lineage Rail is selected:

- **Left — Upstream Contract:** Fields arriving at this node. For Tier 1 wrangling: input_fields. For assembly: one collapsible accordion per ingredient showing each dataset's output_fields. For a plot: the parent assembly's final_contract.
- **Center — Active Component:** The component's own definition (wrangling recipe, plot spec, or field schema). Editable. The logic stack / raw YAML lives here.
- **Right — Downstream Contract:** Fields leaving this node. For Tier 1 wrangling: output_fields. For assembly: final_contract. For a plot: "Plot terminal — no output schema."

**3. Bidirectional workflow:**

- **Forward (build):** Source → wrangle → assemble → plot. Select a component, see what comes in, edit the recipe, see what goes out.
- **Reverse (design):** Start at a plot node. The left panel shows what fields are available from the assembly. If a needed field is missing, click backwards along the Rail to the assembly → then to the relevant Tier 1 wrangling → add the `mutate` step there → the field propagates forward. The Rail makes the gap immediately visible.

**4. Per-plot wrangling (new manifest concept):**
Some plots require dataset-specific transformations after the assembly (wide/long format pivots, aggregations, filters). These are represented as an optional `pre_plot_wrangling` key in the plot block:

```yaml
plots:
  mlst_bar:
    target_dataset: MLST_with_metadata
    pre_plot_wrangling: !include 'plots/mlst_bar_wrangling.yaml'  # optional
    spec: !include 'plots/mlst_bar.yaml'
```

This keeps plot-specific transformations explicit and traceable. In the Lineage Rail, this appears as an intermediate node between the assembly output and the plot spec. If absent, the slot shows an "➕ Add plot wrangling" affordance.

**5. Assembly branching representation:**
When an assembly recipe joins N ingredients, the Upstream Contract panel shows an accordion — one section per ingredient — each displaying that dataset's output_fields. This is honest: there is no single unified input schema; the inputs are the individual outputs of N Tier 1 pipelines. The final_contract represents the merged, curated output that all downstream plots consume.

### Technical Foundation (IMPLEMENTED as of 2026-04-20)

#### Module-level helpers in `server.py`

| Helper | Key | Value | Purpose |
| :--- | :--- | :--- | :--- |
| `_build_sibling_map(manifest_path_str)` | `rel_path` (str) | `{role, schema_id, schema_type, siblings, ingredients}` | File-path index. Assembly wrangling files get `role="assembly"`. Only file-path strings registered as keys (inline dicts are unhashable). |
| `_build_schema_registry(manifest_path_str, includes_map)` | `schema_id` (str) | `{schema_type, input_fields, wrangling, output_fields, recipe, ingredients, target_dataset, group_id, source, info}` | Schema-ID index capturing both `!include` rel-paths (str) and inline YAML content (`{"inline": val}`). |
| `_build_lineage_chain(selected_rel, ctx_map)` | — | `list[{rel, schema_id, role, label, is_active}]` | Walks backward then forward from selected node to produce an ordered chain for the Rail. |
| `_load_fields_file(abs_path)` | — | `list` | Reads field files; unwraps ADR-014 single-key wrapper if present. |
| `_slot(block, key)` | — | `str \| {"inline": val} \| None` | Distinguishes `!include` marker, inline content, and absent/empty. |

#### Reactive values in `server.py`

- `_includes_map: reactive.Value` — `{rel_path: abs_path_str}` for all `!include` files in active manifest.
- `_component_ctx_map: reactive.Value` — `{rel_path: {...}}` built by `_build_sibling_map` on manifest selection.
- `_schema_registry: reactive.Value` — `{schema_id: {...}}` built by `_build_schema_registry` on manifest selection.

#### Reactive state in `WrangleStudio.__init__`

```python
self.active_component_info  = reactive.Value({})   # {role, schema_id, schema_type, ingredients, wrangling}
self.active_upstream        = reactive.Value([])    # [] | list[fields] | list[{id, fields}] (assembly)
self.active_downstream      = reactive.Value([])    # [] | list[fields]
self.active_lineage_chain   = reactive.Value([])    # ordered Rail nodes
self.active_manifest_path   = reactive.Value("")    # master manifest path — set on every import
self.active_viz_id          = reactive.Value(None)  # plot schema_id — set only when role=="plot_spec"
```

#### Role dispatch in `_handle_manifest_import` Mode A

| `role` | `active_upstream` | `active_downstream` |
| :--- | :--- | :--- |
| `input_fields` | `[]` | fields from file |
| `output_fields` | fields from file | `[]` |
| `wrangling` | sibling `input_fields` file | sibling `output_fields` file |
| `assembly` | per-ingredient accordion (schema_id → output_fields via ctx_map) | assembly `output_fields` |
| `plot_spec` | parent `output_fields` resolved via `target_dataset` — searches assembly first, then data_schemas | `[]` (terminal) |

**Key constraint on `plot_spec` upstream resolution:** `target_dataset` in plot spec files typically names a **data schema** (e.g. `"FastP"`), not an assembly. The lookup in `_handle_manifest_import` tries three passes: (1) assembly `output_fields`, (2) any `output_fields` for matching `schema_id`, (3) `input_fields` fallback.

#### Lineage Rail UI (`lineage_rail_ui` output)

Renders a `<button>` per chain node with role icon, label, role tag. Active node: bold border + filled background. JS `onclick` sets a hidden `<input id="lineage_node_rel">` and dispatches a `change` event → `handle_lineage_node_click` effect → `ui.update_select` + `ui.js_eval` to click `btn_import_manifest` programmatically. TubeMap node clicks (`_sync_selector_from_node_click`) use the same JS pattern.

#### Sidebar display labels

`_update_dataset_pipelines` builds display labels as `"{schema_id} — {role}"` (from `_component_ctx_map`) instead of raw filenames. Fallback to `abs_path.name` when the rel_path is not in the sibling map.

#### Live View plot preview

`architect_active_plot` uses `ConfigManager(active_manifest_path.get()).raw_config` for the full resolved manifest config, not `yaml.safe_load(active_raw_yaml)` (which is the component file fragment). `active_viz_id` is set to `schema_id` when a `plot_spec` is loaded.

### Implementation Phases

- **Phase 18-A:** ✅ Field materialization, context map, role-aware loading, normalize button, `_build_sibling_map`, `_build_schema_registry`. *(COMPLETED 2026-04-20)*
- **Phase 18-B:** ✅ `_build_lineage_chain`, Rail UI rendering, chain populated on component load, Rail click → full component load via `ui.js_eval`. *(COMPLETED 2026-04-20)*
- **Phase 18-B-fixes:** ✅ Sidebar labels, plot_spec upstream resolution, Live View wiring, TubeMap click wiring. *(COMPLETED 2026-04-20 Session 2)*
- **Phase 18-C:** ✅ 3-column panel with `lineage_rail_ui`, upstream/component/downstream cards, dynamic headers. *(COMPLETED 2026-04-20)*
- **Phase 18-D:** ✅ `pre_plot_wrangling` support — optional key in plot block; Rail node between assembly and plot. *(COMPLETED 2026-04-20)*
- **Phase 18-E:** Reverse navigation — Field Gap Analysis tool. *(PENDING)*
- **Phase 18-F:** ✅ Full clickable TubeMap driving Rail navigation. *(COMPLETED 2026-04-20)*
  - `BlueprintMapper.generate_mermaid()`: plot nodes (in subgraphs) now tracked in `_clickable` and get `click` directives — they were previously missed.
  - `_sync_selector_from_node_click`: TubeMap node ID (`safe_schema_id`) resolved to best `rel_path` via `_component_ctx_map`, using role priority (assembly > wrangling > plot_spec > plot_wrangling > output_fields > input_fields). Previously tried to use schema_id directly as selector value → nothing loaded.
- **Phase 18-G:** ✅ Full inline manifest reactivity + Assembly Live Data + TubeMap zoom/pan. *(COMPLETED 2026-04-20 Session 5)*
  - See ADR-040-G below.

### Phase 18-G Detail (Session 5, 2026-04-20)

#### Bug: Assembly node "unable to find column 'category'" error

**Root cause:** `processed_data_surgical` in `wrangle_studio.py` called `apply_logic(lf)` unconditionally on the materialized parquet. For an `assembly` node, the parquet IS the final assembled output; re-running the assembly recipe (which starts with `filter_eq column: category` on the pre-unpivot data) against the already-assembled columns caused the column-not-found error.

**Fix:** `processed_data_surgical` now only calls `apply_logic` when `active_component_info.role` ∈ `{"wrangling", "plot_wrangling"}`. For all other roles (`assembly`, `plot_spec`, `output_fields`, `input_fields`) the parquet is served as-is.

#### Bug: Assembly node never materialised / Live Data Glimpse empty

**Root cause:** The `assembly` role handler in Mode A (`_handle_manifest_import`) set `active_upstream`/`active_downstream` but never called `orchestrator.materialize_tier1` or set `active_anchor_path`.

**Fix:** Added the same materialise-and-set-anchor block to the `assembly` handler that `plot_spec` already had.

#### Bug: Mode B (inline manifests) missing all reactive state

**Root cause:** Mode B (fallback path for inline manifests — no `!include` files) only set `logic_stack` and `active_fields`. All other reactive values (`active_component_info`, `active_upstream`, `active_downstream`, lineage chain, TubeMap highlight, `active_manifest_path`, assembly materialisation) were never set. This made clicking TubeMap nodes partially update the UI (logic stack changed) but left fields/contracts/TubeMap highlight blank.

**Fix:** Mode B now mirrors Mode A fully:
- Detects role from `_component_ctx_map` (which has inline entries since Phase 18-F)
- For `assembly` role: builds `ing_items` from inline `output_fields` dicts of each ingredient; materialises via `orchestrator.materialize_tier1`; sets `active_anchor_path`
- For all other roles: passes rich field dicts (not just key lists) to `active_upstream`/`active_downstream` so `_fields_table` renders type info
- Sets `active_component_info`, lineage chain, TubeMap highlight for all roles

#### Enhancement: TubeMap zoom/pan (`app/src/ui.py`, `app/modules/wrangle_studio.py`)

**Library added:** `svg-pan-zoom@3.6.1` (CDN).

**Integration:**
- `initTubeMapPanZoom()` defined globally in `ui.py`; called via `shiny:visualchange` event (300ms after mermaid re-render) and via inline `<script>` tag injected with each `blueprint_tubemap_ui` render
- Pan/zoom initialised on the `<svg>` produced by Mermaid; instance stored in `svg._panZoomInstance` to avoid double-init
- Toolbar: `＋ Zoom In` / `－ Zoom Out` / `⊡ Fit` buttons above viewport; each calls `_panZoomInstance.zoomIn/Out/fit/center()` inline
- Viewport: 300 px fixed height, `overflow: hidden` (pan replaces scroll)

**Known limitation:** `svg-pan-zoom` + Mermaid's `securityLevel:'loose'` both manipulate the SVG. Click handlers survive because they are on `<g>` nodes that pan-zoom does not replace — only the viewport transform changes. However, if the accordion is expanded after first render and the SVG dimensions were 0×0 at init time, `fit()` may need the 100ms settle timeout. The `setTimeout(pz.fit, 100)` handles this.

#### Open issue: TubeMap library replacement (tracked separately)

The current Mermaid.js + svg-pan-zoom stack works but has limitations:
- Graph is generated as a flat LR DAG; no hierarchical lane-based layout
- Compact "GitHub-style" commit graph is not achievable with Mermaid
- Re-render on every Shiny reactive change causes visible flicker
- Node shapes are limited; no swimlane or layered grouping without subgraphs

**Desired properties for a replacement library:**
1. **Compact, lane-based DAG** — GitHub-style commit graph where each schema type (Source / Wrangling / Assembly / Plot) occupies a horizontal lane
2. **Interactive** — click events surfaced to JS, programmatic node highlight
3. **Pan + zoom built-in** — no secondary library needed
4. **Works inside Shiny** — can be initialised from a JS string (not file-based), re-rendered reactively without full page reload
5. **Lightweight** — no heavy framework dependency (React, Vue, etc.)

**Candidate libraries to evaluate:**
- **`vis-network`** (visjs.org) — force-directed + hierarchical layout, full click API, CDN-available, ~1MB. Best fit for hierarchical DAG. `hierarchical: {direction: "LR", sortMethod: "directed"}`
- **`d3-dag`** (github.com/erikbrinkman/d3-dag) — proper DAG layout algorithms (Sugiyama), renders as SVG via D3. Most control, most work.
- **`ELK.js`** (Eclipse Layout Kernel JS) — industry-grade DAG layouter; Mermaid 10 can use it as a layout backend (`layout: elk`) which keeps click callbacks. May be the lowest-effort upgrade.
- **`Cytoscape.js`** — full graph library, pan/zoom/click built-in, `dagre` layout plugin for DAG. CDN-available.

**Recommended path:** Try `mermaid + elk` first (config change only: `layout: elk`, `elk.algorithm: 'layered'`). If layout quality is still insufficient, migrate to `vis-network` with `hierarchical` mode — it requires wrapping the Mermaid DSL in a JS node/edge array but the `BlueprintMapper` already has that data structure internally.

**Benefit:** The Blueprint Architect becomes a full bidirectional manifest development environment. A scientist can start from a visualization goal and work backwards to the data transformation needed, or build forward from raw source to plot — both workflows using the same graph, the same contracts, and the same editing tools.

## ADR-042: YAML 'on' Resilience & Key Purging (bool/startswith)

**Status:** IMPLEMENTED (2026-03-07)
**Context:** YAML's reserved word `on` automatically parses to boolean `True` in many loaders. This caused attribute errors (`'bool' object has no attribute 'startswith'`) in the `DataAssembler` and `DataWrangler` when iterating over rule keys or purging internal metadata (`__` prefixed keys).
**Decision:** Implement defensive type checks and explicit boolean-key handling in all key-iteration loops.

- **Resilience:** The `DataAssembler` now uses `isinstance(k, str)` before calling `startswith("__")`.
- **Selector Handling:** Both `DataAssembler` and `DataWrangler` now explicitly check for `rule.get(True)` when resolving column selectors like `on`, `source`, or `columns`.
- **Hygiene:** Manifests SHOULD quote `"on"`, but the codebase MUST handle unquoted variants to ensure stability across diverse YAML loaders and human error.
