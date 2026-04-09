# Implementation Plan Master: Dashboard Core & Plugin Validation

# Authority: @dasharch

# Source of Truth for SPARMVET_VIZ Architecture

## 1. Overview & Vision

Transition from "Scaffolding" to "Functional Prototype" by implementing missing transformer logic and validating it via the modular Shiny frontend. We utilize a **'Decorator-First'** development cycle to align the Python execution engine with the active YAML manifest logic verified in `./config/manifests/pipelines/`.

## 2. Architectural Principles

- **Decorator-First:** Explicit decorator patterns for both Wrangling actions (`@register_action`) and Plotting factories (`@register_plot`).
- **YAML Data Contract:** Pursue **YAML-ONLY** validation. Phase out JSON schema dependencies for the core manifest logic.
- **Polars-First:** Mandatory use of **Polars LazyFrames** for all heavy lifting. Materialize only at the Presentation or Export layers.
- **Tidy Data Consistency:** Use **Plotnine** for the Presentation Layer to ensure seamless handoff from Polars-transformed dataframes.

## 3. Environment & Modular Standards

- **Root .venv:** All execution MUST occur within the root `.venv/` directory.
- **Modular package architecture:**
  - Each subdirectory in `libs/` (e.g., `libs/transformer`, `libs/viz_factory`) MUST be an independent package with its own `pyproject.toml`.
  - Installation in the root `.venv` MUST use the `-e` (editable) flag to maintain modularity and live-syncing of code changes.
- **CLI-argparse for Testing:** Every library in `libs/` must include a CLI-compatible test script. Hardcoded paths inside test logic are forbidden. Use `argparse` to handle data inputs (TSV), configuration manifests (YAML), and output destinations.

## 4. Technical Roadmap

### Phase A: 'Decorator-First' Logic (DONE)

- [x] Verify status of decorator-based plugin system.
- [x] Implement missing decorator-based actions (drop_duplicates, summarize).
- [x] Update ResFinder_wrangling.yaml.

### Phase B: Dynamic Plot Factory (DONE)

- [x] Implement `@register_plot(factory_id)` decorator in `libs/viz_factory/src/registry.py`.
- [x] Refactor `base.py` to replace Plotly placeholders with Plotnine templates.
- [x] Prototype Polars-to-Plotnine handoff. (ADR-010) [DONE]

### Phase 3: Atomic Layer Optimization (DONE)

- [x] **Decorator Expansion:** Implement `regex_extract`, `drop_columns`, `round_numeric`, and `filter_range`.
- [x] **M2 (Layer 1 Verification):** Universal Runner (`wrangler_debug.py`) and Automated Suite (`test_decorator_suite.py`) verified against 17 atomic actions. [COMPLETED] 🚀
- [x] **Universal Runner Callability:** Confirm `wrangler_debug.py` can be imported as a library by the Orchestrator.
- [x] **Lazy Processing Audit:** Ensure atomic actions do not trigger premature Polars collection.

### Phase 4: The Assembly Factory (DONE)

- [x] **DataAssembler Core:** Implement Layer 2 orchestrator script.
- [x] **Multi-Source Loop:** Call the Wrangler for all datasets defined in the manifest.
- [x] **Cross-Dataset Joins:** Execute Polars `.join()` logic using manifest-defined `join_on`.
- [x] **Final Stage Wrangling:** Support a global wrangling pass across the joined LazyFrame.
- [x] **Relational Decorators:** Registered `join` and `join_filter` in the unified registry.

### Phase 5: Architectural Guardrails & Integration (DONE)

- [x] Implement **`libs/utils/src/data_executor.py`** to center the `.collect()` logic for the Orchestrator. [DONE]
- [x] Finalize YAML-only validation logic. [DONE]
- [x] Implement responsive UI adjustments for premium branding.

### Phase 6: Viz Factory Components [DONE]

- [x] Initialize library and `@register_plot_component` registry.
- [x] Implement core `geoms/`, `facets/`, `coords/`, `positions/` subdirectories.
- [x] Fully implement and verify `scales/` and `themes/` components with verification PNGs (35 components/86% verified).
- [x] Create `bulk_test_runner.py` for automated manifest-to-PNG generation/verification.
- [x] Resolve failed verifications (scale_color_cmap, facet_labeller, stat_ecdf, stat_function).
- [x] Implement "Filter vs. Anchor" reactivity logic (ADR-024).

### Phase 7: Orchestration Guardrails (DONE)

- [x] Implement **`libs/utils/src/data_executor.py`** to center the `.collect()` logic for the Orchestrator.
- [x] Finalize YAML-only validation logic.
- [x] Implement responsive UI adjustments for premium branding.

### Phase 8: Frontend Scaffolding (UI Heartbeat)

- [ ] **Asset Integration:** Use `create_test_deployment.py` to bind synthetic ST22 dummy data.
- [ ] **UI Implementation (`app/src/ui.py`):** Sidebar for dataset/manifest selection.
- [ ] **Server Implementation (`app/src/server.py`):** Connect `help_registry_server`; call `DataWrangler`.

### Phase 9: The Artist (Visual Pipeline Builder SDK) (DONE)

- [x] **Registry Initialization:** Established `@register_plot_component` in `libs/viz_factory`.
- [x] **Standardization:** Applied Violet Law (Documentation Only) to all libraries and ADR-013 to test manifests.
- [x] **Modular SDK:** Confirmed `generator_utils` autonomy.
- [ ] **Visual Builder GUI:** Ensure the SDK is UI-agnostic to support future Shiny-based manifest builders.
- [ ] **Aqua Suite:** Implement the 'Aqua' relational data generator.

### Phase 10: The Persistence & Tiering Layer (DONE)

- [x] **Implementation of ADR-024:** Integrate `pl.sink_parquet` into `DataAssembler`. [DONE]
- [x] **Checkpoint Logic:** Add a "Short-Circuit" to the Transformer to detect existing Parquet anchors. [DONE]
- [x] **Tier 2 Summarizer:** Implement `@register_action("summarize")` using `group_by().agg()` to reduce row counts before VizFactory hand-off. [DONE]
- [x] **Performance Validation:** Target < 5s render time for 200k-row filtered views. [VERIFIED]

## 5. Governing Authority (Authority Matrix)

This implementation plan is governed by the authoritative rulebooks and architectural decisions located in the project root. Refer to these files for the "How" and "Why" of any component implementation:

- **Verification & Testing Protocol**: [.agents/rules/rules_verification_testing.md](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/.agents/rules/rules_verification_testing.md)
- **Architectural Decisions (ADR)**: [.antigravity/knowledge/architecture_decisions.md](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/.antigravity/knowledge/architecture_decisions.md)
- **Data Engine Standards**: [.agents/rules/rules_data_engine.md](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/.agents/rules/rules_data_engine.md)
- **Workspace Master Index**: [./.agents/rules/workspace_standard.md](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/workspace_standard.md)

---

### Phase 11: UI Persona & Reactive Integration (ADR-026/ADR-024)

### Phase 11-A: Pipeline Demo Implementation (DONE)

- [x] **UI Bootloader**: Implement `ui_config.yaml` for Persona masking. [DONE]
- [x] **Dual-View Scaffolding**: Create `ui.navset_tab` with Tab A (Tier 2 Reference) and Tab B (Tier 3 Active). [DONE]
- [x] **Tier 3 Sidebar Connector**: Link Shiny inputs to `VizFactory` filters using Predicate Pushdown. [DONE]
- [x] **Annotation Modal**: Implement mandatory 'User Note' popup on data exclusion. [DONE]
- [x] **Export Engine**: Automate '.zip' bundle (Plot + Data + Audit Log + YAML Recipe). [DONE]

### Phase 11-B: Developer Studio (DEFERRED)

- [ ] **Branching Logic**: 'New Branch' from Tier 1 Anchor with YAML persistence.
- [ ] **Pre-Flight Validator**: Data Contract compatibility check (Green/Yellow/Red).
- [ ] **Ghost Manifest**: Silent UI auto-save to `tmp/last_state.yaml`.

### Phase 11-C: UI Shell & Module Integration

- [ ] **Persona Bootloader**: Implement `app/src/bootloader.py` to toggle features via `config/ui/<persona>.yaml`.
- [ ] **Library Hook-up**: Absolute imports of `libs/` packages into `app/modules/` (ADR-011).
- [ ] **Shell Layout**: Build the 3-zone layout (Navigation, Theater, Audit Stack) and allow for side by side plot capabilities (toogle).
- [ ] **Aesthetic Polish**: Apply Light Grey (#f8f9fa) sidebars and light-colored help tooltips.

### Phase 11-D: Dynamic Discovery & Interaction

- [ ] **Discovery Engine:** Implement manifest-to-tab and Polars-schema-to-filter logic.
- [ ] **Interactivity:** Build the column-picker and collapsible sidebars.

### Phase 11-E: Ingestion, Persistence & Gallery

- [ ] **External Ingestion:** Build the YAML upload and External Data joining helper.
- [ ] **Ghost Saving:** Implement automatic background manifest versioning.
- [ ] **Gallery Content:** Initialize `assets/gallery_data/` with credit/license templates.
- [ ] **Gallery Engine**: Browser for `assets/gallery_data/`. Python code location : `libs/viz_gallery` with "One-Click Clone" logic.
- [ ] **Recipe Pre-filling Engine**: Ensure Tier 3 inherits Tier 2's logic as editable nodes.
- [ ] **Exclusion Modal (Tier 1/3)**: Implement "Brush-to-Table" coordinate lookup to Anchor data.

### Phase 11-E: Component Granularity & Interactivity

- [ ] **Dynamic Column Picker:** Build the "Show/Hide" logic for the Tier 3 data tables. Tier 3 table must have the option to show the branching from Tier 1 with and without Tier 2 logic (toggle switch). Tier 1 and Tier 2 tables should be read only. Tier 1 and Tier 2 tables should be scrollable BUT immutable.
- [ ] **Dual-Plot Grid:** Implement the `layout_columns` toggle to show Tier1 vs Tier 2 vs Tier 3 side-by-side.
- [ ] **Audit Node UI:** Create the interactive "Logic Nodes" in the Right Sidebar with color-coding and trash icons.
- [ ] **Outlier "Brush" Integration:** Map the Plotnine/Plotly selection event to a modal that displays the matching Tier 1 Anchor rows.
- [ ] **Export Bundler UI:** Create the "One-Click Export" dialog supporting the `.zip` export (Plot + Data + Audit + YAML) including all tiers data and tiers plots.

### Phase 11-F: Ingestion, Persistence & Developer Studio

- [ ] **DataConnector UI:** Implement the Excel-to-TSV upload helper using existing asset scripts.
- [ ] **Persistence Manager:** Build the logic for Locations 1 to 5 based on paths defined in `config/ui/<persona>.yaml`. Create a template config file (`config/ui/<template_persona>_template.yaml`). Use this template to create a new config file for each persona. (Location 1 for raw data location: `assets/test_data` Location 2 for manifests locations `assets/template_manifests/`, Location 3  `tmp/ui/parquet_data/` for curated data (Tier 1 and Tier 2), Location 4: `tmp/ui/user/` for tier 3 data, user auto-save, and session saves triggered by user save button) Create specific subdirectories for each user in Location 4. Location 5: `assets/gallery_data/` for gallery data and examples plots).
- [ ] **Ghost Manifest Logic:** Implement the "last 5 versions" auto-save in subdirectory of Location 4: `autosave`.
- [ ] **WrangleStudio "Design Studio"**:
  - [ ] **Drag-and-Drop Nodes:** Visual chaining of Transformer decorators.
  - [ ] **Synthetic Data Generator:** GUI for `create_test_data.py`.
  - [ ] **Gallery Submission:** Automate the creation of folder structure, credits, and licensing for new plots.

## Phase 12. UI Orchestration & Aesthetics (ADR-027)

- **Library Sovereignty**: The UI MUST NOT implement transformation or plotting logic. It MUST call `./libs/`.
- **Aesthetic Lock**: Side panels MUST be **#f8f9fa** (Light Grey). Tooltips MUST be light-colored (Yellow/Green).
- **Recipe Integrity**: Tier 3 views MUST "pre-fill" with the Tier 2 recipe list to allow user modification *before* aggregation.
- **Violet Law Boundary**: "Deep Violet" is strictly for `.qmd` documentation. Do not use it for general UI elements.

## Phase 13: UI - Session & Persistence Standards (ADR-031)

- **Automatic Save:** The UI MUST implement a debounced "Ghost Save" (eg. every 2 min or after any WrangleStudio change). Ghost save frequency must be read from `config/ui/<persona>.yaml`. In the template `config/ui/<template_persona>_template.yaml` define ghost save frequency at every 2 min.

- **Session Recovery:** Upon boot, the Bootloader checks for a `last_state.yaml` (Location 4 autosave subdirectory). If found, it prompts the user to "Restore Previous Session".
- **Import Normalization:** All raw imports (Excel/CSV) MUST be converted to TSV and validated against the `input_fields` contract before Tier 1 materialization.

## Phase 14: UI: Developer Mode & Gallery Submission

- **Submission Gate:** In Developer Mode, users can "Submit to Gallery." This triggers a script that:
  1. Anonymizes data (or confirms synthetic status).
  2. Generates the mandatory `LICENSE.md` and `README.md`.
  3. Bundles the asset into `assets/gallery_data/`.
