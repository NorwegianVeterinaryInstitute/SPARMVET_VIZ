# Implementation Plan Master: Dashboard Core & Plugin Validation

## Authority: @dasharch

## Source of Truth for SPARMVET_VIZ Architecture

## 1. Overview & Vision

Transition from "Scaffolding" to "Functional Prototype" by implementing missing transformer logic and validating it via the modular Shiny frontend. We utilize a **'Decorator-First'** development cycle to align the Python execution engine with the active YAML manifest logic verified in `./config/manifests/pipelines/`.

#### 🟢 Phase 19: Unified Manifest Standard & Hygiene (ADR-041) — COMPLETED 2026-04-20

- [x] **Formal ADR-041**: Registered the "Keyed Schema / Ordered Logic" hybrid standard.
- [x] **Standard Documentation**: Created `config/manifests/README.md` and updated `project_conventions.md`.
- [x] **Schema Normalization**: Converted legacy simple dicts and redundant fragments to **Rich Dictionary** standard.
- [x] **Wrangling Tiering**: Verified that all pipeline fragments adopt the `tier1`/`tier2` list structure.
- [x] **Fragment Flatness**: Stripped top-level anchoring keys from included files for recursive compatibility.

#### 🟢 Phase 20: Relational Manifest Stress Testing (COMPLETED 2026-03-07)

- [x] **Relational Audit**: Executed `debug_assembler.py` against the ST22 manifest.
- [x] **Resilience Hardening**: Fixed 'bool' attribute error in `DataAssembler` and `DataWrangler`.
- [x] **Contract Validation**: Unified Contract Guard projection to handle `original_name` mappings.
- [x] **Full Pipeline Pass**: Verified all 3 major assemblies materiality (Anchor, AR1, Summary).

---

**STATUS:** Manifest Structural Integrity Restored. 🏗️💎

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

### Phase 19: Unified Manifest Standard & Hygiene (ADR-041) ✅ COMPLETED 2026-04-20

**Objective:** Standardize manifest structures to resolve the disconnect between UI contract viewers and backend data engines.

- [x] **ADR-041 Registration:** Formally document the "Keyed-Schema & Ordered-Logic" standard.
- [x] **Rules Synchronization:** Update `rules_data_engine.md` and `rules_manifest_structure.md`.
- [x] **Project Conventions Update:** Document the "Adequate Dictionary" format and fragment flatness.
- [x] **Manifest README:** Create `config/manifests/README.md` for associated documentation.
- [x] **Structural Hygiene:**
  - [x] Move all `input_fields` and `output_fields` to Rich Dictionary format.
  - [x] Ensure all `wrangling` blocks use mandatory tier nesting (`tier1`, `tier2`) as sequential lists.
  - [x] Remove redundant top-level keys from included `.yaml` fragments.
- [x] **Engine Alignment**: Verified that `DataIngestor` and `DataWrangler` are compatible with the Keyed Dict / Sequential List hybrid.

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

## Phase 12: UI Orchestration & Aesthetics (ADR-027)

*IMPORTANT: The specific layout configurations, sandbox gating logic, and persona mappings are defined authoritatively in `[ui_implementation_contract.md](../../.agents/rules/ui_implementation_contract.md)`. This section serves only as an implementation tracker.*

### Phase 12-A: Comparison Theater & Persona Scaffolding (DONE)

- [x] **Comparison Theater Base**: Dual-column layout setup. [DONE]
- [x] **True 3-Column Navigation Shell (ADR-029a)**: Nested `layout_sidebar` structure with Left (Navigator), Center (Theater), and Right (Audit). [DONE]
- [x] **Dynamic Layout Grid**: Implement logic to shift between grid modes and handle maximized panes. [DONE]
- [x] **Analysis Theater Tabs**: Materialize manifest groups into dynamic tabsets with integrated controls. [DONE]
- [x] **Persona Reactivity Matrix Enforcement**: Link `app/src/ui.py` strictly to persona-based masking. [DONE]
- [x] **Visual vs Functional Pickers**: Connected schema pickers and column visibility controls. [DONE]

### Phase 12-B: Position-Aware Sandbox & Controls

- [ ] **Bifurcated Tier 3 (`t3_recipe`)**: Implement the distinction between `t3_recipe_prefill` (wide format exploration prior to blueprint steps) and `t3_recipe_complete` (final plot data including T2 blueprint).
- [ ] **Single Audit Stack**: Pre-fill with *Violet* properties, append *Yellow* properties. Position dictates execution order relative to the blueprint.
- [ ] **Validation & Revert Protocol**: Add `btn_revert` to wipe the user sandbox and reset to the unmodified T2 blueprint. Implement disable toggles and deletion warnings.
- [ ] **Comment Gatekeeper**: Tie `btn_apply` to validation of `comment_fields` across all active yellow/modified nodes.

### Phase 12-C: Headless UI Manifest Verification

- [ ] **Persona Gating Tests**: Implement headless test strategies (e.g., Shiny testing addons like `pytest-playwright`) to verify each persona's UI masking element by element, locking to one persona at a time per test suite.

### Phase 16: Gallery Taxonomy & Scaling (DONE 2026-04-19)

- [x] **Metadata indexing**: `gallery_index.json` pivot generation (ADR-037).
- [x] **UI Integration**: Split-pane viewer with isolated reactivity.
- [x] **Ergonomic Polish**: Promoted selector to top of sidebar, added Play-style Apply button.

## Phase 17: Contextual UI Masking & Focus Mode (DONE 2026-04-19)

- [x] **Contextual Masking (ADR-038)**: Implemented server-side reactive reification to hide Global Sidebar controls.
- [x] **Clone Post-Action**: Implemented automatic tab switching / Home signaling after recipe cloning.
- [x] **State Restoration**: Hardened session resume while in Gallery mode.

## Phase 18: Blueprint Architect — Bidirectional Lineage Navigation (ACTIVE)

Full design rationale in ADR-040 (`architecture_decisions.md`). Replaces the flat Interface (Fields) tab with a Bidirectional Lineage Rail + 3-column contract viewer.

### Phase 18-A: Field Materialization & Context Map ✅ COMPLETED 2026-04-20

- [x] `_build_sibling_map()` — file-path index with role, schema_id, siblings, ingredients.
- [x] `_build_schema_registry()` — schema-ID index capturing `!include` refs and inline YAML.
- [x] `_build_lineage_chain()` — ordered Rail node list for any selected component.
- [x] `_load_fields_file()` — ADR-014-aware field file reader.
- [x] `_component_ctx_map`, `_includes_map`, `_schema_registry` reactive values.
- [x] `normalize_manifest_fields.py` moved to `app/assets/` with importable API; `btn_normalize_fields` handler.
- [x] `_parse_fields_safe` handles rich `{col: {type, label}}` dict format.

### Phase 18-B: Lineage Rail UI ✅ COMPLETED 2026-04-20

- [x] `_build_lineage_chain()` helper — walks backward then forward through sibling map.
- [x] `active_lineage_chain` reactive populated on every component load.
- [x] `lineage_rail_ui` renders clickable `<button>` chain with role icons and active highlighting.
- [x] JS Rail node clicks set hidden `lineage_node_rel` input → `handle_lineage_node_click` effect.
- [x] **Rail node click full load**: `handle_lineage_node_click` triggers `btn_import_manifest` via `ui.js_eval`. Rail fully navigable.
- [ ] **Plot spec chain enrichment**: Prepend assembly node to plot_spec chain using `target_dataset`. *(DEFERRED)*
- [ ] **Branch selector**: One assembly → N plots; show branch tabs on Rail. *(DEFERRED)*

### Phase 18-B-fixes: Live Testing Fixes ✅ COMPLETED 2026-04-20 (Session 2)

- [x] **Sidebar display labels**: `_update_dataset_pipelines` shows `"{schema_id} — {role}"` instead of raw filenames.
- [x] **Plot spec upstream resolution**: `target_dataset` lookup broadened — covers `data_schemas` entries, not only `assembly_manifests`.
- [x] **Live View plot preview**: `active_manifest_path` reactive added; `architect_active_plot` uses full `ConfigManager` config; `active_viz_id` set on plot_spec load.
- [x] **TubeMap node click → full load**: `_sync_selector_from_node_click` fires `btn_import_manifest` via `ui.js_eval`.

### Phase 18-C: 3-Column Interface Panel ✅ COMPLETED 2026-04-20

- [x] Tab-3 rewritten: hidden `lineage_node_rel` input + `lineage_rail_ui` header + 3-column `layout_columns([4,4,4])`.
- [x] 7 new render outputs: `lineage_rail_ui`, `upstream_label_ui`, `lineage_upstream_ui`, `component_label_ui`, `lineage_component_ui`, `downstream_label_ui`, `lineage_downstream_ui`.
- [x] `_handle_manifest_import` full role dispatch: `input_fields`, `output_fields`, `wrangling`, `assembly`, `plot_spec`.
- [x] `wrangle_studio.define_server()` call extended with `get_schema_registry` and `get_includes_map` lambdas.

### Phase 18-D: Per-Plot Wrangling Support *(PENDING)*

- [ ] `pre_plot_wrangling` optional key in plot block (`!include` path).
- [ ] Lineage Rail shows intermediate node between assembly output and plot spec.
- [ ] "➕ Add plot wrangling" affordance when slot is absent.

### Phase 18-E: Reverse Navigation — Field Gap Analysis *(PENDING)*

- [ ] Enter desired field name → walk lineage backwards → show earliest insertion point.
- [ ] Highlight which `output_fields` and `final_contract` files need updating to carry the field forward.

### Phase 18-F: Full Interactive TubeMap (ADR-039) *(DEFERRED)*

- [ ] Clickable Mermaid/SVG DAG nodes driving the Lineage Rail.
- [ ] Action Registry parity (175+ actions).
- [ ] Visual Forking: select node → initiate new branch → produce YAML additions.

---

## Phase 21: Unified Home Theater (ADR-043 / ADR-044) — PLANNED 2026-04-23

**Objective:** Eliminate the redundant "Analysis Theater / Viz" nav mode, merge all results functionality into a single unified **Home** mode, implement persona-gated tier controls, context-reactive left sidebar filters, and right sidebar suppression for lower personas.

**Governing ADRs:** ADR-043 (Unified Home Theater), ADR-044 (Persona-Gated Audit Stack & Right Sidebar Visibility).

*IMPORTANT: All UI phases are gated by headless validation. No live UI testing until all headless checks pass (`ui_manifest_integration_testing.md`).*

### Phase 21-A: Nav & Routing Simplification

- [ ] **[server.py]** Remove `"Viz"` / `"Analysis Theater"` branch from `dynamic_tabs()` routing.
- [ ] **[server.py]** Remove `"Analysis Theater"` nav item from `sidebar_nav_ui()`.
- [ ] **[server.py]** Remove `theater_state` reactive and all `state == "plot"` / `state == "table"` / `state == "split"` branches.
- [ ] **[server.py]** Remove `btn_max_plot`, `btn_max_table`, `btn_reset_theater` action buttons and their handlers.
- [ ] **[server.py]** Remove `is_triple` / `triple_tier_mode` flag and the triple-tier layout branch.

### Phase 21-B: Manifest-Driven Tab Structure (Home)

- [ ] **[server.py]** Rebuild `dynamic_tabs()` so Home renders **exclusively** from `analysis_groups` in the active manifest — no hardcoded tabs.
- [ ] **[server.py]** Remove the hardcoded "Inspector" tab.
- [ ] **[server.py]** Wrap each group's `navset_underline` plot sub-tabs inside a `ui.accordion` / `ui.accordion_panel` (collapsible, default expanded).
- [ ] **[server.py]** Track the **active sub-tab id** as a reactive value (`active_home_subtab`); expose via `ui.navset_underline(..., id=...)` and `input.<id>()`.

### Phase 21-C: Tier Toggle

- [ ] **[server.py]** Implement a `ui.input_radio_buttons("tier_toggle", ...)` strip rendering T1/T2 always; T3-Wrangle/T3-Plot only when persona ≥ `pipeline_exploration_advanced`.
- [ ] **[server.py]** Wire `tier_toggle` to control which plot output and data table are rendered in the center pane.
- [ ] **[server.py]** Remove `ref_tier_switch` and `view_toggle` inputs and their handlers.

### Phase 21-D: Collapsible Data Preview

- [ ] **[server.py]** Place the data preview table (T1/T2 or T3 sandbox) in a `ui.accordion_panel` below the plot accordion, default expanded.
- [ ] **[server.py]** Column picker for T3 sandbox: enforce `width: 100%`, `flex: 1 1 100%`; no multi-row wrapping.
- [ ] **[ui.py]** Add CSS rules to enforce column picker full-width layout.

### Phase 21-E: Comparison Mode (Separate Toggle, Persona-Gated)

- [ ] **[server.py]** Implement `ui.input_switch("comparison_mode", ...)` visible only for ≥ `pipeline_exploration_advanced`.
- [ ] **[server.py]** When ON: render 2-column layout (T2 reference left, T3 active right) for both plot and data accordions.
- [ ] **[server.py]** When OFF: single-pane, driven by Tier Toggle only.
- [ ] **[server.py]** Remove old `is_comparison` logic and `comparison_mode_toggle_ui` render.

### Phase 21-F: Context-Reactive Left Sidebar Filters

- [ ] **[server.py]** Read `active_home_subtab` reactive to determine the active `plot_spec` from `analysis_groups`.
- [ ] **[server.py]** Extract aesthetic column names (`x`, `y`, `color`, `fill`, `facet`, `group`) from the active `plot_spec`.
- [ ] **[server.py]** Regenerate left panel filter widgets scoped to those columns only; update on every sub-tab change.
- [ ] **[server.py]** Ensure filter regeneration does NOT reset Tier Toggle or Comparison Mode state.

### Phase 21-G: Persona-Gated Right Sidebar Suppression (ADR-044)

- [ ] **[server.py]** For `pipeline_static` and `pipeline_exploration_simple`: programmatically exclude the right sidebar layout element (not CSS hide — exclude from `layout_sidebar` so theater fills full width).
- [ ] **[server.py]** For ≥ `pipeline_exploration_advanced`: render full audit stack (T2 Violet blueprint nodes + T3 Yellow sandbox nodes + `btn_apply` + `btn_revert`).
- [ ] **[server.py]** Ensure T3 recipe always silently pre-fills from T2 for all personas.

### Phase 21-H: Headless Verification & @verify Gate

- [ ] **[HEADLESS]** Create `debug_home_theater.py` — verifies manifest tab generation, tier toggle rendering stubs, filter scoping, and right sidebar suppression logic for all 5 personas. Materialize report to `tmpAI/`.
- [ ] **[@verify]** Promote validated artifact to `tmp/` and halt for user review.
