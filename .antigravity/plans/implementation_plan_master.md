# Implementation Plan Master: Dashboard Core & Plugin Validation

## Authority: @dasharch

## Source of Truth for SPARMVET_VIZ Architecture

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
- [x] **M2 (Layer 1 Verification):** Universal Runner (`wrangler_debug.py`) and Automated Suite (`debug_decorator_suite.py`) verified against 17 atomic actions. [COMPLETED] 🚀
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

### Phase 8: Frontend Scaffolding (UI Heartbeat) (DONE)

- [x] **Asset Integration:** Materialized via `Bootloader` (ADR-031).
- [x] **UI Implementation (`app/src/ui.py`):** Sidebar for project/manifest discovery.
- [x] **Server Implementation (`app/src/server.py`):** Orchestrator materialization.

### Phase 9: Triple-Source AMR Integration (DONE)

- [x] **fg_metadata/phenotypes/genotypes** migration and normalization. [DONE]
- [x] **3-Way Assembly**: figshare_integration.yaml. [DONE]
- [x] **Integration Plots**: Verified via 1:1:1 evidence loop. [DONE]

### Phase 9-B: The Artist (Visual Pipeline Builder SDK) (DONE)

- [x] **Registry Initialization:** Established `@register_plot_component` in `libs/viz_factory`.
- [x] **Modular SDK:** Confirmed `generator_utils` autonomy and `AquaSynthesizer` logic.
- [x] **Visual Builder Core:** Implemented `WrangleStudio` manual node stack. [DONE]

### Phase 10: The Persistence & Tiering Layer (DONE)

- [x] **Implementation of ADR-024:** Integrate `pl.sink_parquet` into `DataAssembler`. [DONE]
- [x] **Checkpoint Logic:** Add a "Short-Circuit" to the Transformer to detect existing Parquet anchors.
  - [x] **Automated Freshness Check:** Implemented `mtime` comparison between manifest directory and parquet to invalidate stale caches. [DONE] (Phase 14 refinement)
- [x] **Tier 2 Summarizer:** Implement `@register_action("summarize")` for row reduction. [DONE]

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
- [x] **Tier 3 Sidebar Connector**: Link Shiny inputs to `VizFactory` filters. [DONE]
- [ ] **Annotation Modal**: Implement mandatory 'User Note' popup. (ACTIVE)

### Phase 11-C: UI Shell & Module Integration (DONE)

- [x] **Persona Bootloader**: Implement `app/src/bootloader.py`.
- [x] **Library Hook-up**: Absolute imports of `libs/` packages into `app/modules/`.
- [x] **Shell Layout**: Build the 3-zone layout (Navigation, Theater, Audit Stack).

### Phase 11-D: Dynamic Discovery & Interaction (DONE)

- [x] **Discovery Engine:** Implement manifest-to-tab and Polars-schema-to-filter logic.
- [x] **Interactivity:** Build the column-picker and collapsible sidebars.

### Phase 11-E: Ingestion, Persistence & Gallery (ACTIVE)

- [x] **External Ingestion:** Build the YAML upload and Excel-to-TSV helper. [DONE]
- [x] **Ghost Saving:** Implement automatic background manifest versioning. [DONE]
- [ ] **Gallery Engine**: Build UI browser pointing to Connector Location 5.
- [x] **Join Preview Modal**: Implement PK validation check in WrangleStudio (ADR-012). [DONE]

### Phase 11-F: Ingestion, Persistence & Developer Studio (ACTIVE)

- [x] **Path Authority Engine:** [DONE]
- [x] **Library Internalization:** [DONE]
- [x] **WrangleStudio Core:** Visual chaining of Transformer nodes. [DONE]
- [x] **Synthetic Data GUI:** Wrapper for AquaSynthesizer. [DONE]
- [ ] **Outlier "Brush" Integration:** Map plot selection to Tier 1 Anchor data lookup.

## Phase 12. UI Orchestration & Aesthetics (ADR-027)

### Phase 12-A: Comparison Theater & Schema-First (ACTIVE)

- [x] **Comparison Theater**: Dual-column layout (Reference Sandbox + Active Pane). Position-aware recipe pipeline. Apply button. Persona-gated.
- [ ] **Universal Schema Discovery**: Refactor UI pickers to derive choices from active Polars LazyFrame schema.
- [ ] **Project-Agnostic Nomenclature**: Finalize label transition (Project/Record).
- [ ] **Dynamic Tab Generation**: Manifest-driven tab population for complex groups.

### Phase 12-B: The Data Safety Sandbox & Advanced Interactions

**Data Safety Sandbox (approved 2026-04-09):**

- [ ] **Position-Aware Recipe Engine**: Recipe steps tracked with stage metadata (`pre_transform` | `post_transform`) based on position relative to inherited Tier 2 nodes in the Audit Panel.
- [ ] **Immutable Reference Pane**: Left sandbox `table_reference` enforces read-only constraint at the server level — no reactive writes propagated from sandbox filters.
- [ ] **Apply Button Gate**: `btn_apply` as the sole trigger for `tier3_leaf()` recalculation. A `recipe_pending` reactive value tracks unsaved changes and enables/disables the button.

**Advanced Interactions:**

- [x] **Audit Node Interactive Trace**: Mandatory comments and remove icons. [DONE]
- [x] **Triple-Tier Grid Toggle**: Full Tier 1 | Tier 2 | Tier 3 side-by-side comparison. [DONE]
- [x] **Outlier "Brush" Integration**: [ADR-030] Map selection to Tier 1 lookup. [DONE]
- [x] **Gallery Engine Browser**: Real manifest ghost-loading from Location 5. [DONE]

- [ ] **Submission Gate:** Automate anonymization, README, and LICENSE generation.
- [ ] **Export Bundler UI:** One-click `.zip` export (Plot + Data + Audit + YAML).

### Phase 14-B: Educational Gallery Engine (ADR-033)

- [ ] **Recipe Meta Parser**: Multi-modal lookup for associated `.md` descriptions in assets/gallery_data/.
- [ ] **Split-Pane Viewer**: 50/50 Technical (Left) vs. Educational (Right) layout extension.
- [ ] **Visual Literacy Module**: Mandatory Template rendering (Suitability, Schema, Tier 2, interpretations).

### Phase 14-C: Diagnostic Layer & Safety (ADR-034) [ACTIVE]

- [ ] **Unified Error Registry**: Implement `SPARMVET_Error` hierarchy in `libs/utils`.
- [ ] **Column Similarity Engine**: Integrate `difflib` into `DataWrangler` for typo suggestions.
- [ ] **Viz Assertion Gate**: Pre-validate GGPlot aesthetics against Polars schema.
- [ ] **Soft Note UI**: Map library errors to `#fff9c4` notifications in `server.py`.

## Phase 15: Deferred & Future Scope

- [ ] **Plotly Interactivity:** [DEFERRED] Transition to native Plotly events for post-prototype exploration.
- [ ] **Mode B API Integration**: [DEFERRED] Live connector for BioBlend/Galaxy platform endpoints.
- [ ] **Decision Metadata Hash (ADR-024 Refinement)**: Embed manifest SHA-256 fingerprints in Parquet metadata to ensure 100% sync reliability (replaces timestamp heuristic). [FUTURE]
