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

> **Numbering note (2026-04-30):** Phase 11-B and Phases 13–15 are absent from this plan. These are historical gaps — the work was done but tracked directly in git commits and ADRs rather than this document. The plan numbering is non-sequential by design at those points, not missing work.

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

---

## Phase 22: Server Decomposition (ADR-045) — COMPLETED 2026-04-23

**Objective:** Split the 2,362-line `app/src/server.py` monolith into a thin orchestrator (228 lines) plus five focused Shiny handler modules (`app/handlers/`) and a pure manifest introspection module (`app/modules/manifest_navigator.py`). **Zero behaviour change** — structural refactor only.

**Governing ADR:** ADR-045. **Completed:** 2026-04-23.

### Phase 22-A: Create `app/modules/manifest_navigator.py`

- [x] Created `app/modules/manifest_navigator.py` (~280 lines).
- [x] Moved 5 pure functions, renamed to public API (dropped `_` prefix): `build_sibling_map`, `build_schema_registry`, `build_lineage_chain`, `load_fields_file`, `resolve_fields_for_schema`.
- [x] Module docstring references ADR-045 and lists full public API.
- [x] `blueprint_handlers.py` imports from `manifest_navigator`; `server.py` no longer needs these imports.
- [x] Import check passed.

### Phase 22-B: Create `app/handlers/` directory and `__init__.py`

- [x] Created `app/handlers/__init__.py` with package docstring listing all 5 handler modules and Two-Category Law constraints.

### Phase 22-C: Extract `app/handlers/gallery_handlers.py`

- [x] Created with `define_server(input, output, session, *, bootloader, wrangle_studio, safe_input)`.
- [x] All gallery handlers moved: `_sync_family_all`, `_sync_pattern_all`, `_sync_difficulty_all`, `_init_gallery_selector`, `handle_gallery_clone`, `_gallery_active_metadata`, `gallery_preview_img`, `gallery_static_data`, `gallery_yaml_preview`, `gallery_md_content`, `_update_gallery_options`, `gallery_browser_anchor`.
- [x] Delegation call added to `server.py`.

### Phase 22-D: Extract `app/handlers/ingestion_handlers.py`

- [x] Created with `define_server(input, output, session, *, bootloader, current_persona, safe_input)`.
- [x] Handlers moved: `handle_ingest`, `update_persona_context`.

### Phase 22-E: Extract `app/handlers/audit_stack.py`

- [x] Created with `define_server(input, output, session, *, wrangle_studio, recipe_pending, snapshot_recipe, active_cfg, active_collection_id)`.
- [x] Handlers moved: `handle_apply`, `track_recipe_changes`, `recipe_pending_badge_ui`, `audit_nodes_tier2`, `audit_nodes_tier3`.

### Phase 22-F: Extract `app/handlers/blueprint_handlers.py`

- [x] Created with full keyword-only dependency injection signature.
- [x] All Phase 18 Shiny wiring moved; imports updated to use `manifest_navigator`.
- [x] `_includes_map`, `_component_ctx_map`, `_schema_registry` injected as `reactive.Value` instances from `server.py`.

### Phase 22-G: Extract `app/handlers/home_theater.py`

- [x] Created with `define_server(input, output, session, *, bootloader, wrangle_studio, dev_studio, orchestrator, viz_factory, gallery_viewer, current_persona, anchor_path, tier1_anchor, tier_reference, tier3_leaf, active_cfg, active_collection_id, safe_input)`.
- [x] All Home Theater handlers moved: `dynamic_tabs`, `sidebar_nav_ui`, `sidebar_tools_ui`, `right_sidebar_content_ui`, `system_tools_ui`, `sidebar_filters`, `plot_reference`, `table_reference`, `plot_leaf`, `table_leaf`, `handle_plot_brush`, `comparison_mode_toggle_ui`.

### Phase 22-H: Slim `server.py` to orchestrator only

- [x] Final `server.py`: 228 lines — shared state, shared calcs, shared utils, 5 delegation calls only.
- [x] `render` removed from shiny imports (no `@render.*` in server.py).

### Phase 22-I: @verify Gate

- [x] [HEADLESS] Import check passed.
- [x] [LIVE] Smoke test — no major regressions detected (user confirmed).
- [x] [@verify] Complete.

### Phase 22-J: Per-Plot T3 Audit Scoping & Join-Key Propagation ✅ COMPLETED 2026-04-25

- [x] `t3_recipe_by_plot: dict[plot_subtab_id, list[RecipeNode]]` replaces flat `t3_recipe` — per-plot stacks.
- [x] Propagation modal: 3-option scope dialog ("This plot only / All plots / All plots except…") at T3 promotion.
- [x] PK-touching nodes show ⚠️ warning banner in modal and on audit card.
- [x] Linked-id deletion: 🗑 delete removes a node and all copies sharing the same `id` across every plot stack.
- [x] Join-key propagation: orchestrator `per_ingredient_cast`/`base_cast` normalisation (Categorical ≠ String fix).
- [x] Live-UI verification checklist written: `tasks_test_22J.md`. Awaiting user sign-off.

### Phase 18-F: Full Interactive TubeMap (ADR-039) *(DEFERRED)*

- [ ] Clickable Mermaid/SVG DAG nodes driving the Lineage Rail.
- [ ] Action Registry parity (175+ actions).
- [ ] Visual Forking: select node → initiate new branch → produce YAML additions.

---

## Phase 21: Unified Home Theater (ADR-043 / ADR-044) ✅ COMPLETED 2026-04-30

**Objective:** Eliminate the redundant "Analysis Theater / Viz" nav mode, merge all results functionality into a single unified **Home** mode, implement persona-gated tier controls, context-reactive left sidebar filters, and right sidebar suppression for lower personas.

**Governing ADRs:** ADR-043 (Unified Home Theater), ADR-044 (Persona-Gated Audit Stack & Right Sidebar Visibility), ADR-047 (Export Bundle).

### Phase 21-A: Nav & Routing Simplification ✅ COMPLETED 2026-04-23

- [x] Removed `"Viz"` / `"Analysis Theater"` branch and nav item.
- [x] Removed `theater_state`, `btn_max_*`, `is_triple`/`triple_tier_mode`.

### Phase 21-B: Manifest-Driven Tab Structure ✅ COMPLETED 2026-04-23

- [x] Home renders exclusively from `analysis_groups` — no hardcoded tabs.
- [x] `active_home_subtab` reactive; `_track_active_home_subtab` effect.
- [x] Dynamic `@render.plot` handlers registered at init for all `plot_group_{p_id}`.

### Phase 21-C: Tier Toggle ✅ COMPLETED 2026-04-23

- [x] `tier_toggle` radio (T1/T2 always; T3 persona-gated advanced+).
- [x] `_track_tier_toggle` effect syncs input → `tier_toggle` reactive.Value.
- [x] `ref_tier_switch` and `view_toggle` removed.

### Phase 21-D: Home Layout Redesign & Collapsible Data Preview ✅ COMPLETED 2026-04-23

- [x] Thin header strip (dataset label + tier toggle). Groups as `navset_pill`. Plots in `navset_card_tab`. Data preview in independent accordion below.
- [x] `home_data_preview` scoped to active plot dataset. Column selector (`home_col_selector_ui`) above DataGrid.
- [x] `data_preview_section` always mounted in DOM (before no-groups early return).
- [x] No-groups fallback wraps top-level plots in synthetic `navset_card_tab`.
- [x] Tier toggle uses `selected="T1"` (static) to prevent `dynamic_tabs` DOM re-render on tier change.

### Phase 21-E: Comparison Mode ✅ COMPLETED 2026-04-30

- [x] `comparison_mode_toggle_ui` fixed: persona IDs use hyphens; tier gate (`tier_toggle != "T3"` early return); label "⚖ Compare T2 vs T3".
- [x] `ui.output_ui("comparison_mode_toggle_ui")` placed in `theater_header` inside `dynamic_tabs` (was defined but never mounted).
- [x] `_make_cmp_baseline_handler(p_id)` factory registered for all plot IDs — renders `plot_group_{p_id}_cmp_base` with T1 data, no T3 audit nodes.
- [x] `dynamic_tabs` reads `comparison_mode` input: 2-column layout (T2 baseline left / T3 adjusted right) when ON in T3 tier.

### Phase 21-F: Context-Reactive Filters + Column Selection ✅ COMPLETED 2026-04-23

- [x] Filter recipe builder UI: `_pending_filters` + `applied_filters` reactive.Values.
- [x] Shell stability pattern: `sidebar_filters` reads only `current_persona`; child outputs (`filter_rows_ui`, `filter_form_ui`, `filter_controls_ui`, `filter_t3_btn_ui`) independent.
- [x] `_apply_filter_rows` helper: auto-promotes eq/ne→in/not_in for list values; casts column to Utf8 for set ops; coerces scalar to numeric dtype.
- [x] `applied_filters` → plot handlers and `home_data_preview` (predicate pushdown).
- [x] `not_in` op added to VizFactory predicate pushdown.
- [x] Column selector (`selectize`) above DataGrid, preview-only.
- [ ] 21-F-5 (T3 Apply to recipe) — UI stub present; serialization deferred.
- [ ] 21-F-7 (add `scale_x_discrete` to manifests) — deferred to user.

### Phase 21-G: Persona-Gated Right Sidebar Suppression ✅ COMPLETED 2026-04-30

- [x] `hidden_personas = {"pipeline-static", "pipeline-exploration-simple"}` in `right_sidebar_content_ui`.
- [x] Returns `ui.div()` for suppressed personas — sidebar slot empty, theater expands to full width.
- [x] Full audit stack visible for ≥ `pipeline-exploration-advanced`.

### Phase 21-H: Headless Verification & @verify Gate ✅ COMPLETED 2026-04-30

- [x] `app/tests/debug_home_theater.py` created — 10 sections, 76/76 checks PASS.
- [x] Covers: persona feature flags, manifest tab structure, tier choices, sidebar suppression, comparison mode gating, PK extraction, session provenance SHA256, ghost round-trip, filter recipe schema, bootloader locations.
- [x] Output artifact: `tmpAI/home_theater_verify/results.json`.

### Phase 21-I: Export Results Bundle ✅ COMPLETED 2026-04-23

**Governing ADR:** ADR-047.

- [x] `system_tools_ui`: user-name field, preset radio (web/publication), filter warning, download button.
- [x] `@render.download export_bundle_download`: async generator yielding zip bytes.
- [x] Bundle: `plots/` (SVG/PNG), `data/` (T1+T2 always; T3 for advanced+T3), `recipes/`, `FILTERS.txt` (No Trace No Export), `report.qmd` (Quarto source), `README.txt`.
- [ ] Ghost save to `user_sessions` — deferred.
- [ ] Per-plot checkbox selection — deferred (all plots always exported).

---

## Phase 24: `home_theater.py` Decomposition (ADR-051) — DESIGNED 2026-04-30, Implementation Pending

**Objective:** Split `app/handlers/home_theater.py` (2,547 lines as of 2026-04-30) into a thin coordinator plus three focused handler modules, following the same ADR-045 decomposition pattern used for `server.py`. **Gate status (2026-04-30):** Phase 22-J live-UI test §1 (core per-plot scoping) PASSED — gate effectively MET. Remaining test items (§3–15) are blocked on the AUDIT-1 ADR-049 amendment and DEMO-3/4 operand casting bugs, not on 22-J wiring. ST22 Lineage 2 still pending but is independent.

**Governing ADR:** ADR-051. **Triggered by:** Post-Phase-21 growth past the 2,362-line threshold that triggered ADR-045.

### Proposed File Map

| File | Owns | Est. Lines |
|---|---|---|
| `app/handlers/home_theater.py` (slimmed) | Module helpers, `define_server` signature, shared local state, `dynamic_tabs`, per-plot handler registration, reactive state effects (`_track_tier_toggle`, `_sync_session_provenance`, `_track_active_home_subtab`), `home_data_preview`, `home_col_selector_ui`, `sidebar_nav_ui`, `sidebar_tools_ui`, `right_sidebar_content_ui`, plot/table renders (`plot_reference`, `table_reference`, `plot_leaf`, `table_leaf`, `plot_leaf_brush`, `comparison_mode_toggle_ui`) | ~900 |
| `app/handlers/t3_audit_handlers.py` (new) | `col_drop_audit_btn_ui`, all filter recipe builder effects (`_filter_add_row`, `_filter_apply`, `_filter_reset`, `_col_drop_to_audit`), propagation modal builder, `_handle_propagation_confirm`, `_make_remove_handler` factory | ~450 |
| `app/handlers/session_handlers.py` (new) | `session_management_ui`, `_handle_session_import`, `_handle_session_actions` (restore + delete dynamic handlers) | ~400 |
| `app/handlers/export_handlers.py` (new) | `system_tools_ui`, `export_bundle_download`, `export_audit_report_html`, `export_audit_report_docx`, all export helper functions | ~510 |
| `app/modules/t3_recipe_engine.py` (new) | Pure functions extracted from inside `define_server`: `apply_filter_rows(lf, filters)`, `extract_t3_filter_rows(home_state, plot_id)`, `extract_t3_drop_columns(home_state, plot_id)`. These are used by both `home_theater.py` plot renders and `t3_audit_handlers.py` — the Two-Category Law requires them in a module (no Shiny imports). | ~120 |

### Key Architectural Decisions for Phase 24

1. **Shared reactive state**: `applied_filters`, `_pending_filters`, and `_propagation_scratch` are currently defined inside `home_theater.define_server()`. They must be passed by reference as keyword arguments to `t3_audit_handlers.define_server(...)` and `export_handlers.define_server(...)`. Do NOT promote them to `server.py` — they are Home-scoped, not global.

2. **`define_server` contract for each new handler**: `(input, output, session, *, ...)` with only keyword-only arguments after the Shiny trio. Each new handler calls `define_server(...)` internally called by `home_theater.define_server(...)` — NOT by `server.py` directly (ADR-045 only adds one delegation level; Phase 24 nests sub-delegation within the Home theater tier).

3. **Pure helper extraction**: `_apply_filter_rows`, `_t3_filter_rows`, `_t3_drop_columns` are currently closures inside `define_server`. They must be refactored to receive `home_state` and `safe_input` as explicit parameters and moved to `t3_recipe_engine.py`.

4. **`sidebar_filters` stays in `home_theater.py`**: It renders the filter-builder UI but does not own any reactive effects — those move to `t3_audit_handlers.py`. The split is at the UI/effect boundary.

### Phase 24-A: Extract `app/modules/t3_recipe_engine.py`

- [ ] Define `apply_filter_rows(lf, filter_list)` — pure LazyFrame predicate application.
- [ ] Define `extract_t3_filter_rows(t3_recipe_by_plot, plot_id)` — returns active `filter_row` nodes for a plot as filter-list dicts.
- [ ] Define `extract_t3_drop_columns(t3_recipe_by_plot, plot_id)` — returns active `drop_column` node column names.
- [ ] Add `@deps` block. Import check from a headless script.

### Phase 24-B: Extract `app/handlers/t3_audit_handlers.py`

- [ ] `define_server(input, output, session, *, applied_filters, _pending_filters, _propagation_scratch, home_state, active_cfg, active_home_subtab, tier_toggle, session_manager, safe_input, bootloader)`.
- [ ] Move: `col_drop_audit_btn_ui`, filter effects, propagation modal, `_make_remove_handler`.
- [ ] Replace internal helpers with calls to `t3_recipe_engine` functions.

### Phase 24-C: Extract `app/handlers/session_handlers.py`

- [ ] `define_server(input, output, session, *, session_manager, home_state, current_persona, safe_input, bootloader, orchestrator, active_cfg, tier_toggle, applied_filters)`.
- [ ] Move: `session_management_ui`, `_handle_session_import`, `_handle_session_actions`.

### Phase 24-D: Extract `app/handlers/export_handlers.py`

- [ ] `define_server(input, output, session, *, applied_filters, home_state, session_manager, bootloader, current_persona, active_cfg, tier_toggle, active_home_subtab, safe_input, viz_factory, tier1_anchor, tier_reference, tier3_leaf)`.
- [ ] Move: `system_tools_ui`, `export_bundle_download`, all audit report downloads.

### Phase 24-E: Slim `home_theater.py` + @verify Gate

- [ ] Wire sub-delegation calls inside `home_theater.define_server()` to all three new handlers.
- [ ] Remove moved code. Update imports.
- [ ] Headless import check. Live smoke test. `@verify` complete.

---

### Phase 23: Scientific Audit Hardening (ACTIVE 2026-04-23)

**Objective**: Institutionalize the development-phase audit requirements: mandatory Tier 1 visibility, biological typing standards, and precision renaming.

- [x] **ADR-046**: Formalize the Scientific Audit Protocol (Tier 1 visibility, retention policy). [DONE]
- [x] **Rulebook Sync**: Update `rules_data_engine.md` and `rules_manifest_structure.md` with whitelisting and typing laws. [DONE]
- [ ] **Ingestor Diagnostics**: Implement non-breaking warnings for missing manifest columns in `DataIngestor`.
- [ ] **Audit Materialization**: Standardize the `debug_wrangler.py` and `debug_assembler.py` output paths to a unified `tmp/{date}/{lineage}/` folder structure.
- [ ] **Lineage 2 (Plasmids)**: Apply new renaming precision standards (`predicted_phenotype`) and verify via Tier 1 audit.
