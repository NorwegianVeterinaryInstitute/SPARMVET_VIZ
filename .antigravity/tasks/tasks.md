# Tasks (SOLE SOURCE OF TRUTH)

**Workspace ID:** SPARMVET_VIZ
**Last Updated:** 2026-04-25 (Phase 22 complete + 22-H live-UI bugfixes applied) by @dasharch

## 🟣 Completed Phases — Archived

> Status: COMPLETED. Phases 16, 17, 18-A through 18-D, 18-B-fixes, 18-C, 18-F (stress tests), 21-A, 21-B, 22 are done.
> Detailed history: [./.antigravity/tasks/archives/tasks_archive_2026-04-10.md], [./.antigravity/tasks/archives/tasks_archive_2026-04-14.md], [./.antigravity/logs/audit_2026-04-18.md], [./.antigravity/logs/audit_2026-04-23.md]

---

## 🟡 Phase 22: Session Management, T3 Audit Trace & Publication Finisher

**Objective:** Implement the full session identity system (§12d), T3 audit recipe (§12a–c), ghost save (§12d), Home module state object (§13), and export audit report (§12f) as specified in `ui_implementation_contract.md §12–13` and `rules_ui_dashboard.md`.

**Governing docs:** `ui_implementation_contract.md §12–13`, `rules_ui_dashboard.md §1–4`.

---

### Phase 22-A: SessionManager — Session Identity & Ghost Save

**File:** `app/modules/session_manager.py` (new)

- [ ] **22-A-1**: `SessionManager.__init__`: accepts `location_4: Path`. Creates `_sessions/` subdirectory.
- [ ] **22-A-2**: `compute_manifest_sha256(manifest_path: Path) -> str`: SHA256 of manifest YAML file content.
- [ ] **22-A-3**: `compute_data_batch_hash(source_files: dict[str, Path]) -> str`: SHA256 of all per-file SHA256s concatenated in sorted key order.
- [ ] **22-A-4**: `compute_session_key(manifest_sha256: str, data_batch_hash: str) -> str`: `f"{manifest_sha256[:12]}:{data_batch_hash[:12]}"`.
- [ ] **22-A-5**: `session_dir(session_key: str) -> Path`: `_sessions/{session_key}/`, created on first access.
- [ ] **22-A-6**: `write_assembly_ghost(session_key, manifest_id, manifest_sha256, data_batch_hash, source_files, parquet_paths)`: writes `assembly.json` to session dir.
- [ ] **22-A-7**: `read_assembly_ghost(session_key) -> dict | None`: reads `assembly.json`; returns None if absent.
- [ ] **22-A-8**: `restore_t1t2(manifest_path, source_files) -> dict`: 6-step Prepped Chef logic — match session, validate hashes, return `{status, parquet_paths, session_key}`. Status: `"fast_path"`, `"reassemble"`, `"new_session"`, `"missing_source"`.
- [ ] **22-A-9**: `write_t3_ghost(session_key, manifest_id, manifest_sha256, data_batch_hash, tier_toggle, t3_recipe, t3_plot_overrides, label="") -> Path`: writes `t3_{timestamp}.json` to session dir; returns file path.
- [ ] **22-A-10**: `list_t3_ghosts(session_key) -> list[dict]`: returns all `t3_*.json` for a session, sorted newest-first; each entry includes `file`, `saved_at`, `label`, `manifest_sha256`, `data_batch_hash`.
- [ ] **22-A-11**: `list_all_sessions() -> list[dict]`: scans all `_sessions/*/assembly.json`; returns list with `session_key`, `manifest_id`, `assembled_at`, `t3_count` (number of T3 ghosts), latest `saved_at`.
- [ ] **22-A-12**: `export_session_zip(session_key) -> bytes`: zips `_sessions/{session_key}/` into in-memory bytes for download.
- [ ] **22-A-13**: `import_session_zip(zip_bytes: bytes) -> str`: unpacks zip into `_sessions/`; returns restored `session_key`.
- [ ] **22-A-14**: `delete_session(session_key)`: removes `_sessions/{session_key}/` entirely.
- [ ] **22-A-15**: Add `@deps` block. Write `libs/transformer/tests/` style test: `app/tests/test_session_manager.py` — unit tests for all methods using tmp paths.

---

### Phase 22-B: Home Module State Object

**Files:** `app/src/server.py`, `app/handlers/home_theater.py`

- [ ] **22-B-1**: Define `home_state = reactive.Value({...})` in `server.py` per §13 schema: `active_group_tab`, `active_plot_subtab`, `tier_toggle`, `accordion_plots_expanded`, `accordion_data_expanded`, `_pending_filters`, `applied_filters`, `t3_recipe`, `_pending_t3_nodes`, `t3_plot_overrides`, `manifest_sha256`, `assembly_timestamp`, `t3_ghost_file`, `t3_ghost_saved_at`.
- [ ] **22-B-2**: Remove standalone `applied_filters`, `_pending_filters`, `active_home_subtab`, `tier_toggle` `reactive.Value`s from `home_theater.py`; read/write via `home_state` instead.
- [ ] **22-B-3**: Pass `home_state` and `session_manager` into `define_server` in `home_theater.py`; update signature.
- [ ] **22-B-4**: Update `server.py` `define_home_theater_server` call with new kwargs.
- [ ] **22-B-5**: Panel independence: on panel switch away from Home, write navigation + T3 fields from `home_state` to T3 ghost (via `session_manager.write_t3_ghost`). On return to Home, state is already in `home_state` (no re-read needed — survives in memory).
- [ ] **22-B-6**: Import check: `python -c "from app.src.main import app"` passes with no errors.

---

### Phase 22-C: T3 Audit Recipe Nodes in Right Sidebar

**Files:** `app/handlers/audit_stack.py`, `app/handlers/home_theater.py`

- [ ] **22-C-1**: Define `RecipeNode` TypedDict (or plain dict schema) in `app/modules/session_manager.py`: fields `node_type`, `id`, `created_at`, `plot_scope`, `params`, `reason`, `active`.
- [ ] **22-C-2**: Replace `wrangle_studio.logic_stack` Yellow nodes in `audit_stack.py` with `home_state`'s `t3_recipe` list (committed RecipeNode dicts).
- [ ] **22-C-3**: Render Yellow nodes in right sidebar: each node shows `node_type` icon + `params` summary + `reason` text field (editable). Red border on empty reason.
- [ ] **22-C-4**: Gatekeeper: `btn_apply` locked (greyed, tooltip) when any `filter_row`, `exclusion_row`, `drop_column`, or `developer_raw_yaml` node has `reason == ""`. `aesthetic_override` never blocks.
- [ ] **22-C-5**: "Add filter row" button → appends a new `filter_row` RecipeNode to `_pending_t3_nodes` with empty reason. Existing `filter_add_row` effect refactored to write to T3 recipe instead of (or in addition to) `_pending_filters`.
- [ ] **22-C-6**: "Add exclusion" button (explicit row exclusion by value) → appends `exclusion_row` RecipeNode.
- [ ] **22-C-7**: "Drop column" button → appends `drop_column` RecipeNode (requires reason, mandatory).
- [ ] **22-C-8**: On `btn_apply`: move `_pending_t3_nodes` → `t3_recipe` (committed); trigger `session_manager.write_t3_ghost`.
- [ ] **22-C-9**: Node deactivation: "×" button sets `active: False` on node (not deletion). Node remains in list with strikethrough style.
- [ ] **22-C-10**: `drop_column` nodes applied to the working LazyFrame before plot render (physical column removal, not just preview hide).

---

### Phase 22-D: Left Sidebar — Session Management Panel

**File:** `app/handlers/home_theater.py` (system_tools_ui section)

- [ ] **22-D-1**: "Session Management" accordion panel in System Tools (≥ `pipeline_exploration_advanced`, `session_management_enabled`).
- [ ] **22-D-2**: Session list: `output_ui("session_list_ui")` — renders cards from `session_manager.list_all_sessions()`, grouped by `manifest_sha256[:12]`, sorted newest-first. Each card: manifest_id, short batch hash, label (editable inline), last saved, T3 ghost count.
- [ ] **22-D-3**: "Restore" button per card → opens T3 ghost picker modal: lists `session_manager.list_t3_ghosts(session_key)` newest-first + "Start fresh T3" option.
- [ ] **22-D-4**: Restore flow: run `session_manager.restore_t1t2()` → on `"fast_path"` load Parquet; on `"reassemble"` trigger orchestrator; on `"missing_source"` show blocking error notification. Then apply selected T3 ghost to `home_state`.
- [ ] **22-D-5**: Manifest/data hash mismatch warnings on T3 ghost restore (non-blocking `ui.notification_show`).
- [ ] **22-D-6**: `download_button("session_export_download")` → `session_manager.export_session_zip(session_key)`.
- [ ] **22-D-7**: `file_input("session_import_upload")` + import effect → `session_manager.import_session_zip(zip_bytes)` → refresh session list.
- [ ] **22-D-8**: "Delete session" button with confirmation dialog.

---

### Phase 22-E: Export Audit Report

**File:** `app/modules/exporter.py`, `app/handlers/home_theater.py`

- [ ] **22-E-1**: Quarto `.qmd` template in `app/assets/report_template.qmd`: front-matter block (manifest_id, manifest_sha256, t3_recipe_sha256, date), Study Context, Data Summary, Methods, Figures, Appendix (discarded nodes), Raw T3 Recipe.
- [ ] **22-E-2**: `generate_methods_text(t3_recipe: list[dict]) -> list[str]`: template-based plain English per node type (active nodes only). `active: False` nodes → Appendix text.
- [ ] **22-E-3**: `render_audit_report(home_state, session_key, output_path: Path)` in `exporter.py`: fills template, copies plot PNGs, calls `quarto render`.
- [ ] **22-E-4**: "Export Audit Report" button in System Tools (≥ `pipeline_exploration_advanced`) → `download_button` trigger → calls `render_audit_report`.
- [ ] **22-E-5**: Deactivated-node blocking warning dialog before export (if any `active: False` nodes exist).
- [ ] **22-E-6**: "Export PDF/DOCX" button → calls `pandoc` on rendered HTML; greyed with tooltip if `pandoc` not on PATH.
- [ ] **22-E-7**: `t3_recipe_sha256` computed as SHA256 of the serialized active-only T3 recipe YAML.

---

### Phase 22-F: Gallery → T3 Transplant (persona-gated)

**File:** `app/handlers/gallery_handlers.py`

- [ ] **22-F-1**: "Send to T3" button in gallery viewer: hidden for `pipeline_static` / `pipeline_exploration_simple`; visible for ≥ `pipeline_exploration_advanced`.
- [ ] **22-F-2**: Transplant effect: insert `developer_raw_yaml` RecipeNode into `home_state._pending_t3_nodes` with `gallery_source: {gallery_id, gallery_yaml_hash}`, `reason: ""`, targeting `home_state.active_plot_subtab`.
- [ ] **22-F-3**: On transplant, switch navigation back to Home panel and pre-focus the reason field of the new node.

---

### Phase 22-G: Headless Verification & @verify Gate

- [x] **22-G-1**: `app/tests/test_session_manager.py` — 26/26 PASSED (2026-04-25).
- [x] **22-G-2**: `app/tests/debug_session_flow.py` — 15/15 PASSED. Artifacts in `tmp/session_test/`.
- [x] **22-G-3**: Import check passes: `from app.src.main import app` — OK.
- [ ] **22-G-4**: [@verify] Manual review of session ghost files in `tmp/UI_TEST/user/_sessions/` — pending user test in live UI.

---

### Phase 22-H: Live-UI Bug Fixes (2026-04-25, after first user test)

**Context:** Found in the first interactive test of Phase 22 by @evezeyl. These are gaps that the unit tests and debug flow could not catch because they cover only the SessionManager module in isolation, not the wired Shiny reactive graph or persona name plumbing.

#### Bugs found and fixed

- [x] **22-H-1**: Right sidebar T3 audit panel rendered nothing.
  - **Root cause**: `audit_stack_tools_ui` output slot was referenced in the right sidebar but no `@render.ui` function with that name existed anywhere. The slot rendered silently empty. There were also no Add buttons to create RecipeNodes.
  - **Fix**: Added full `audit_stack_tools_ui` render in `app/handlers/audit_stack.py` with three Add buttons (`t3_add_filter`, `t3_add_exclusion`, `t3_add_drop`) plus gatekeeper-aware Apply, and three matching `@reactive.Effect` handlers that append empty RecipeNodes to `_pending_t3_nodes`.

- [x] **22-H-2**: Persona-gated UI never showed (or always showed) for advanced personas.
  - **Root cause**: Code-side persona sets were written with underscores (`pipeline_exploration_advanced`, `project_independent`) but real persona IDs from the templates use hyphens (`pipeline-exploration-advanced`, `project-independent`). Affected: gallery "Send to T3" button, session management panel, export audit report panel, T3 tier toggle option, right-sidebar suppression for simple personas.
  - **Fix**: Replaced underscore literals with hyphenated literals in:
    - `app/handlers/gallery_handlers.py` — `_T3_PERSONAS`
    - `app/handlers/home_theater.py` — `hidden_personas` (right-sidebar gate), `advanced_personas` (export panel), `advanced_personas` (session management panel), tier-choices block (line ~411)
  - **Lesson**: Persona IDs are user-data; never hard-code variants. Future work should centralise persona constants in one module.

- [x] **22-H-3**: Left-panel filters (My Adjustments) had no path into the T3 audit recipe.
  - **Root cause**: `filter_t3_btn_ui` rendered an "Apply to recipe" button (`input.filter_apply_recipe`) but no `@reactive.Effect` listened for it. The button was decorative.
  - **Fix**: Added `_filter_apply_recipe` handler in `app/handlers/home_theater.py`. Reads `_pending_filters`, converts each row to a `filter_row` RecipeNode (column/op/value pre-filled, reason empty), appends to `_pending_t3_nodes`. Gatekeeper enforces reason before Apply.

- [x] **22-H-4**: No detection of source-data file changes — tiers never re-derived after the user edited a metadata TSV.
  - **Root cause**: `data_batch_hash` field existed in the `home_state` schema but was never populated. `restore_t1t2()` was implemented in SessionManager but never called from the orchestrator/home_theater assembly path. The session_key therefore could not change when input files changed.
  - **Fix (2 parts)**:
    1. Added `DataOrchestrator.get_source_files(project_id) -> dict[str, Path]` in `app/modules/orchestrator.py`. Mirrors the ingestor's path-resolution logic (manifest `source.path` block first, legacy `data_dir` glob fallback). Returns only files that exist on disk.
    2. Added `_sync_session_provenance` `@reactive.Effect` in `app/handlers/home_theater.py`. Watches `input.project_id`. Hashes manifest + all source files via `SessionManager.compute_manifest_sha256` / `compute_data_batch_hash`. Compares to stored values in `home_state`. If `data_batch_hash` changed, shows a warning notification and writes the new hashes back to `home_state`.

- [x] **22-H-5**: Shiny client errors `output 'dynamic_tabs' is recalculating, but the output is in an unexpected state of: 'idle'` (and similar for `running`/`invalidated` states).
  - **Root cause**: My initial implementation of 22-H-4 placed `home_state.set(...)` *inside* the `@render.ui dynamic_tabs` function. Writing a `reactive.Value` during a render invalidates downstream readers immediately, even though the render has not completed. Shiny's client/server state machine then sees illegal transitions and emits these warnings.
  - **Fix**: Removed all `home_state.set` and hash computation from the `dynamic_tabs` render body. Moved them to a standalone `@reactive.Effect` (`_sync_session_provenance`) that runs as a side-effect and only writes to `home_state` when values actually changed (cheap idempotent guard).
  - **Lesson (durable)**: Never call `reactive.Value.set()` inside a `@render.*` function. State writes belong in `@reactive.Effect`. This is a generalisation of ADR-045's Two-Category Law and should be considered alongside it.

#### Files changed in 22-H

- `app/handlers/audit_stack.py` — added `audit_stack_tools_ui` render + 3 Add-node effects.
- `app/handlers/home_theater.py` — added `_filter_apply_recipe` effect, added `_sync_session_provenance` effect, fixed 4 persona-name literals (underscore → hyphen).
- `app/handlers/gallery_handlers.py` — fixed `_T3_PERSONAS` literal.
- `app/modules/orchestrator.py` — added `get_source_files(project_id)` method.

#### Verification status

- [x] Import check: `python -c "from app.src.main import app"` passes.
- [ ] [@verify] Live-UI test by user: confirm right-sidebar T3 panel renders Add buttons; "Apply to recipe" from left panel creates RecipeNodes; editing a source TSV triggers the "Source data files have changed" warning.

---

## 🟡 Phase 21: Unified Home Theater (ADR-043 / ADR-044) — IN PROGRESS

**Objective:** Eliminate the "Analysis Theater / Viz" nav mode; merge into a unified Home; implement Tier Toggle, context-reactive filters, collapsible layout, Comparison Mode, and persona-gated right sidebar suppression.
**Governing ADRs:** ADR-043, ADR-044.

### Phase 21-A: Nav & Routing Simplification — COMPLETED 2026-04-23
- [x] Removed `"Viz"` / `"Analysis Theater"` nav items from `home_theater.py`.
- [x] Removed `theater_state`, `btn_max_plot`, `btn_max_table`, `btn_reset_theater`, `is_triple` / `triple_tier_mode`.

### Phase 21-B: Manifest-Driven Tab Structure — COMPLETED 2026-04-23
- [x] Home renders exclusively from `analysis_groups` — no hardcoded tabs, no Inspector tab.
- [x] Each group's plot sub-tabs wrapped in collapsible `ui.accordion_panel` (default expanded).
- [x] `active_home_subtab` reactive added to `server.py`; tracked via `_track_active_home_subtab` in `home_theater.py`.
- [x] Dynamic `@render.plot` handlers registered at server init for all `plot_group_{p_id}`.
- [x] Plot handlers resolve `target_dataset` via `orchestrator.materialize_tier1`; fall back to `tier1_anchor`. Error-safe.
- [x] Import check passed.

### Phase 21-C: Tier Toggle — COMPLETED 2026-04-23
- [x] `tier_toggle` radio-button strip added to theater header: T1/T2 always; T3 persona-gated (advanced+).
- [x] `tier_reference` / `tier3_leaf` calcs in `server.py` now read `tier_toggle.get()` instead of dead `ref_tier_switch` / `view_toggle` inputs.
- [x] `_track_tier_toggle` effect in `home_theater.py` syncs input → `reactive.Value`.
- [x] `ref_tier_switch` and `view_toggle` removed.

### Phase 21-D: Home Layout Redesign & Collapsible Data Preview — COMPLETED 2026-04-23
- [x] Header: thin strip — `Data: <dataset_name>` left, tier radio right. No title, no persona/manifest text.
- [x] Tier labels: `Assembled` / `Analysis-ready` / `My adjustments` (T3 persona-gated).
- [x] Groups as `navset_pill` top strip (Option B). Each group = one `nav_panel`.
- [x] Plots: `navset_underline` inside a collapsible `accordion_panel` ("Plots"), open by default.
- [x] Data preview: `render.DataGrid` inside a separate collapsible `accordion_panel` ("Data Preview"), open by default — independent collapse from plots.
- [x] Data preview scoped to active plot's `target_dataset` at active tier. Falls back to first plot in first group.
- [x] `_track_active_home_subtab` updated to prioritise active group's subtab first.

### Phase 21-E: Comparison Mode
- [ ] Implement `comparison_mode` switch, persona-gated (≥ `pipeline_exploration_advanced`).
- [ ] When ON: 2-column layout (T2 reference left, T3 active right) for plots and data.
- [ ] Remove old `is_comparison` logic and `comparison_mode_toggle_ui`.

> **DEFERRED NOTE (2026-04-23):** Full tier-switch user-testing (T2/T3 data shift) deferred — no manifest with proper T2/T3 assembly is available for this project. The mechanism (tier_toggle reactive + tier_reference/tier3_leaf calcs) is wired; test when ST22 Lineage 2 is materialized.

### Phase 21-F: Context-Reactive Filters + Column Selection — IN PROGRESS

**Design decision (2026-04-23):** Two surfaces, clearly separated by purpose:

**Surface A — Left Sidebar Row Filters** (affect what data is plotted AND shown in preview):
- Scoped to columns present in the active plot's dataset (reactive to `active_home_subtab`).
- Multi-criteria per column: for categorical → multi-select checklist with "Select all/none" toggle; for numeric → range slider.
- Regeneration does NOT reset Tier Toggle.
- Filters expressed as `plot_config['filters']` list passed to VizFactory at render time (predicate pushdown already wired in VizFactory).

**Surface B — Data Preview Column Visibility** (preview only, does not affect plots):
- Lives inside the Data Preview accordion, above the DataGrid.
- Checkbox group: one checkbox per column, "Show all / Hide all" master toggle.
- Implemented as a client-side column visibility filter on the rendered DataGrid (subset columns before passing to `render.DataGrid`).
- T3 only: "Drop column from recipe" action (deferred — requires recipe mutation).

**Design decisions (2026-04-23):**
- Row filters use a **recipe builder** pattern: add N rows of {column, op, value}, Apply button pushes to `applied_filters` reactive → consumed by both plot handlers and data preview. Multiple rows on same column = AND logic (already supported by VizFactory predicate pushdown).
- **Type handling**: Year and similar columns stay `Int64` in data. Plot manifests use `scale_x_discrete` to declare categorical intent. Filter builder reads the active plot spec — if `scale_x_discrete`/`scale_y_discrete` present for that column → multi-select widget; otherwise → range slider. No data mutation, no `display_type` annotations. Coercion at filter time: values always matched against raw dtype.
- **T3 integration**: same filter list → serialized as recipe step when T3 active + advanced persona. Gate with persona check; design the data model now (`{column, op, value, dtype}`) to support both consumers.
- **Column selector**: `selectize` multi-select above DataGrid, preview-only, does not affect plots.
- **Auto-axis adjustment (VizFactory)**: label rotation/sizing is legitimate display-layer concern, stays in VizFactory. All data manipulation belongs in the recipe.

**Implementation tasks:**
- [x] **21-F-1**: Filter recipe builder UI in left sidebar. `_pending_filters` + `applied_filters` reactive.Values. Column select (scoped to active dataset, dtype-aware op set, discrete widget when `scale_x_discrete` present or non-numeric dtype). Add row / Remove row / Apply / Reset. *(home_theater.py `sidebar_filters` + effects)*
- [x] **21-F-2**: Wire `applied_filters` → plot handlers: injected into `synthetic_manifest["plots"][p_id]["filters"]` with dtype coercion at render time. *(home_theater.py `_make_group_plot_handler`)*
- [x] **21-F-3**: Wire `applied_filters` → `home_data_preview`: same predicate pushdown with dtype coercion. *(home_theater.py `home_data_preview`)*
- [x] **21-F-4**: Column selector (`selectize`) above DataGrid via `home_col_selector_ui`. Subsets preview DataFrame only. *(home_theater.py `home_col_selector_ui`)*
- [ ] **21-F-5**: T3 "Apply to recipe" button — UI stub present (persona-gated); serialization to recipe YAML step deferred.
- [x] **21-F-6**: `not_in` op support in VizFactory. *(viz_factory.py)*
- [ ] **21-F-7 (deferred)**: Add `scale_x_discrete` / `scale_y_discrete` to manifests where Year/ST columns should be treated as categorical. User will update manifests directly.

### Phase 21-G: Persona-Gated Right Sidebar Suppression
- [ ] For `pipeline_static` / `pipeline_exploration_simple`: exclude right sidebar layout element (not CSS-hide).
- [ ] For ≥ `pipeline_exploration_advanced`: render full audit stack (Violet T2 + Yellow T3 + `btn_apply` + `btn_revert`).
- [ ] Verify T3 recipe silently pre-fills from T2 for all personas.

### Phase 21-H: Headless Verification & @verify Gate
- [ ] [HEADLESS] Create `debug_home_theater.py` — verify tab generation, tier toggle stubs, filter scoping, sidebar suppression for all 5 personas. Output to `tmpAI/`.
- [ ] [@verify] Promote to `tmp/` and halt for user review.

---

## 🟡 Infrastructure Upgrades — IN PROGRESS (requested 2026-04-23)

### IU-1: VizFactory — position, labels, guides support — COMPLETED 2026-04-23
- [x] `factory_id` + explicit `layers`: base geom now prepended at position 0 so `position_dodge` and `labs` layers find it. *(viz_factory.py `_standardize_config`)*
- [x] Top-level `labels` block → `labs(**labels_block)` applied after layer loop.
- [x] Top-level `guides` block → `guides(fill=guide_legend(...))` with dict spec.
- [x] Verified: `_standardize_config` produces `[geom_bar, position_dodge, labs]` for `multi_resistance_*.yaml`.

### IU-2: DataAssembler — shorthand/unroll normalization — COMPLETED 2026-04-23
- [x] `DataAssembler._normalize_recipe()` pre-normalization pass added.
- [x] Handles `{join: {on: key}}`, `{select: [...]}`, `{mutate: {...}}` shorthand → canonical form.
- [x] Called at top of `assemble()` before hashing; existing ST22 canonical steps pass through unchanged.

### IU-3: Contract-Aware Materialization — COMPLETED 2026-04-23
- [x] `debug_gallery.py` already uses `scan_parquet` → types preserved end-to-end.
- [x] `debug_assembler.py` writes contracted Parquet (not TSV) for downstream consumption.
- [x] No active code path re-reads contracted TSV through ingestor; risk is theoretical. No change needed.

### IU-4: Ingestor Diagnostics — COMPLETED 2026-04-23
- [x] Non-breaking warnings in `DataIngestor` for columns in `input_fields` missing from source TSV. *(Verified at ingestor.py:92-94)*

### IU-5: @deps Project-Wide Annotation — COMPLETED 2026-04-23
- [x] Full project scan: 59 nodes, 112 edges in dependency graph. *(audit_2026-04-23.md, Session Blocks 5-6)*

### IU-7: VizFactory — Auto-adjust axis label orientation & size — COMPLETED 2026-04-23
- [x] `VizFactory._auto_adjust_axis_labels(p, df, x_col, y_col)` static method added.
- [x] X-axis (categorical only): skips numeric/datetime; 35° size 9 for >5 unique or >6-char; 45° size 8 for >8 unique or >12-char.
- [x] Y-axis (any dtype): size 8 for >12 unique or >12-char; size 7 for >20 unique or >20-char.
- [x] Both axes adjusted in a single `theme()` call. Applied automatically at end of `render()` unless manifest has explicit `element_text` layer.
- [x] Verified: long country X → 45°; numeric X → none; 13 AMR class Y → size 8; 25 numeric Y ticks → size 7.

### IU-6: Bioscientist Persona Hardening — COMPLETED 2026-04-23
- [x] §0-B Python Code Boundary decision table added.
- [x] §3-F Sequential Build Law added (step-gate protocol).
- [x] §4-B @dasharch Handoff Protocol added.
- [x] `project_conventions.md` added as mandatory read.
- [x] Silent Skip Warning, Float64 cause, dated output routing documented. *(audit_2026-04-23.md, Session Block 7)*

---

## 🟡 Active Lineage Build: ST22 Sequential Development

> **Convention:** All debug outputs routed to `tmp/YYYY-MM-DD/<lineage_id>/`. Bioscientist persona governs YAML; @dasharch governs Python.

- [x] **Lineage 1 (AMR Profile)**: Materialized (T1/T2/Plots). Verified Integer Year and Predicted Phenotype. [DONE]
- [ ] **Lineage 2 (Plasmid Dynamics)**:
    - [ ] Create `2_test_data_ST22_dummy/input_fields/plasmid_data.yaml`
    - [ ] Implement Tier 1 filtering (e.g., min identity/overlap for PlasmidFinder)
    - [ ] Assemble with metadata and AMR results.
    - [ ] Verify via Tier 1 audit artifacts.

---

## 🟡 Phase 21-I: Export Results Bundle — COMPLETED 2026-04-23

**Objective:** System Tools → Export zip bundle: all plots (SVG/high-DPI PNG), T1 datasets (TSV), YAML recipes, Quarto `.qmd` report, README.

- [x] `system_tools_ui`: user-name `input_text`, preset `input_radio_buttons` (web/publication), `download_button("export_bundle_download")`. Filter warning shown when `applied_filters` non-empty.
- [x] `@render.download export_bundle_download`: timestamped `YYYYMMDD_HHMMSS_<name>_results.zip` with:
  - `plots/` — SVG (web) or PNG ≥600 DPI (publication) per plot; error stub on failure
  - `data/` — T1+T2 TSVs always; T3 TSV only for advanced+ persona when tier_toggle=="T3"
  - `recipes/` — all YAML files from active project manifest directory
  - `FILTERS.txt` — "No Trace No Export" filter trace when `applied_filters` non-empty
  - `report.qmd` — Quarto source with metadata, optional filter table, figure includes, data refs
  - `README.txt` — bundle manifest (timestamp, project, persona, preset, counts)
- [x] `_export_bundle_filename()`: helper for reactive-safe filename generation.
- [ ] **Ghost save** (deferred): auto-save to `user_sessions` location in `local_connector.yaml`.
- [ ] **Plot selection** (deferred): currently exports all plots; per-plot checkbox selection deferred.

---

## 🟡 Deferred / Backlog

### Phase 18 Deferred Items
- [x] **Plot spec chain enrichment** (18-B): `manifest_navigator._resolve_target_dataset()` reads `target_dataset` from plot spec files; chain walk uses it. *(DONE — resolved by architecture)*
- [x] **Interactive TubeMap** (18-F / ADR-039): Cytoscape JSON DAG with clickable nodes fully wired in `blueprint_handlers.py` / `wrangle_studio.py`. *(DONE)*
- [ ] **Branch selector** (18-B / 18-F): Lineage Rail stops at assembly level for one-assembly → N-plots divergence. Genuinely deferred.
- [ ] **Action Registry Parity** (18-F): Expose 175+ `@register_action` entries in Blueprint Architect UI. Genuinely deferred.
- [ ] **Visual Forking** (18-F): Select a node → initiate new branch → YAML additions. Genuinely deferred.

### Phase 20: Relational Manifest Tooling
- [ ] **Field Gap Analysis tool**: Field name → walk lineage backwards to earliest insertion point. Genuinely deferred.
- [ ] **Forward propagation hint**: Show which output_fields / final_contract files need updating. Genuinely deferred.

### Deferred VizFactory / Scale Fixes
- [ ] Retest & fix `scale_x_timedelta`, `scale_y_timedelta` (dtype mismatch). *(decorators commented out in scales/core.py)*
- [ ] Retest & fix `geom_map` (requires spatial data). *(decorator commented out in geoms/core.py)*
- [x] Automatic label size / orientation / spacing adjustment for plots. *(DONE — see IU-7 below)*

### Blueprint Architect — Deferred Aesthetics & Debug
- [ ] **"Data: …" display** — top-left of analysis theater header shows raw dataset name; review display format and content.
- [ ] **TubeMap aesthetics** — tighter rail/tube look; rename 'ref' → 'Add' (Additional Dataset) in nodes and legend.
- [ ] Full Blueprint Architect aesthetic/functional debug pass (field contracts, lineage rail, Zone C layout).

### Gallery & UI
- [ ] **Taxonomy Data Audit**: Verify/correct tags in `assets/gallery_data/*/recipe_manifest.yaml`.
- [ ] Gallery thumbnails for faster visual scanning.
- [ ] Gallery: Test "Clone to Sandbox" functionality (requires more advanced wrangling modes).

### Technical Debt
- [ ] **Unified Materialization**: Standardize `debug_wrangler.py` and `debug_assembler.py` to auto-create dated `tmp/{date}/{lineage}/` subfolders.
- [ ] **Renaming Precision Audit**: Scan existing manifests for generic `phenotype` or `source` columns; refactor to `predicted_phenotype` or descriptive equivalent.
- [ ] Workspace hygiene: remove temporary tests from `tmp/` and dispose of unique scripts.

---

## 🔵 Phase 23: Multi-System Deployment Architecture (ADR-048) — DESIGNED, Implementation Pending

**Objective:** Enable the same Docker image to run across Galaxy, IRIDA, institutional servers, and local machines via a deployment profile YAML and a Bootloader resolution chain.

**Design decisions recorded:** ADR-048 (2026-04-24). User documentation written: `docs/deployment/deployment_guide.qmd`. Connector template updated: `config/connectors/templates/connector_template.yaml`.

### Phase 23-A: Directory Rename & Bootloader Extension
- [ ] Rename `config/connectors/` → `config/deployment/` (update Bootloader reference, update docs).
- [ ] Extend `bootloader.py`: add `SPARMVET_PROFILE` env var resolution chain (4 levels: env var → `~/.sparmvet/profile.yaml` → `/etc/sparmvet/profile.yaml` → dev fallback).
- [ ] Parse `default_manifest` and `default_persona` from profile and apply at startup.
- [ ] Startup log: which resolution level was matched.
- [ ] Validation: raise clear error if required fields missing or paths don't exist.

### Phase 23-B: Connector Library (`libs/connectors/`)
- [ ] `base.py`: Abstract `BaseConnector` interface (`resolve_paths`, `fetch_data`, `get_manifest_path`, `get_default_persona`).
- [ ] `filesystem.py`: `FilesystemConnector` — reads profile locations directly. No-op `fetch_data`.
- [ ] `irida.py`: `IridaConnector` — OAuth2 fetch via `SPARMVET_IRIDA_TOKEN` → local cache → paths like filesystem.
- [ ] `galaxy.py`: `GalaxyConnector` — thin wrapper over filesystem; maps Galaxy job dir env vars to locations.
- [ ] Unit tests for each connector against mock profiles.

### Phase 23-C: Galaxy Tool Wrapper Templates
- [ ] Template Galaxy XML wrapper (`tool_amr_pipeline.xml`) — one per pipeline.
- [ ] Bundle profile YAMLs inside Docker image (`/profiles/`).
- [ ] Document Galaxy admin setup steps in `docs/deployment/`.

### Phase 23-D: IRIDA Integration
- [ ] IRIDA plugin/iframe launch mechanism — confirm env var injection method.
- [ ] `IridaConnector.fetch_data()` — download samples, metadata, analysis results via REST API.
- [ ] Optional: result POST-back to IRIDA project.
- [ ] Document IRIDA admin setup steps in `docs/deployment/`.

### Phase 23-E: Documentation & Admin Guide
- [x] ADR-048 written.
- [x] `docs/deployment/deployment_guide.qmd` written (user-facing).
- [x] Connector template updated with new schema and inline comments.
- [ ] Per-system admin quick-start guides (Galaxy / IRIDA / server / local).
- [ ] Update `docs/workflows/connector.qmd` to reference ADR-048 and new schema.

---

## 🔧 2026-04-24 Repository Hygiene (from @dasharch workspace review)

*Verified by manual codebase inspection. Gemini agent findings were correct on all four items.*

### H-1: Fix broken cross-references in `architecture_decisions.md` — DONE
- [x] ADR-014: Replaced `"Section 12 of the Workspace Standard"` → `rules_data_engine.md §4` (Identity Transformations / Manifest Data Contract).
- [x] ADR-016: Replaced `"Section 13, Workspace Standard"` → `rules_runtime_environment.md §4` ("Clear Lines"). Section 14 → `rules_runtime_environment.md §1 & §5` (venv enforcement).

### H-2: Resolve `assets/scripts/` vs ADR-032 contradiction — RESOLVED
**Decision (2026-04-24):** `assets/scripts/` is the designated home for **user-facing helper scripts** (manifest creation, manifest validation, data verification, deployment debugging). ADR-032's deletion mandate applies only to scripts that were duplicating library-internal logic during early prototyping. Library test/debug runners belong inside their `libs/` packages. Cross-library dev utilities with no clear owner may go in `libs/utils/`.
- [x] ADR-032 scope clarification written in `architecture_decisions.md`.
- [ ] Audit `assets/scripts/` contents: confirm each script is user-facing or dev-helper (not duplicating a lib-internal runner). Move any that belong in a library or `libs/utils/`.

### H-3: `connectors/` → `deployment/` terminology alignment
Already tracked under Phase 23-A. No new action — verified as duplicate.

### H-4: `home_theater.py` size watch (1562 lines)
- [ ] Add a note to ADR-045 (Server Decomposition) that `home_theater.py` is approaching the size threshold that triggered the original `server.py` decomposition. Track as a future split candidate once Phase 21 stabilises. **No immediate action — flag for post-Phase-21 review.**


# User needs to test

- [ ] change metadata year to have serval years - Verify sorting function in the columns
---

**STATUS:** Phase 21-F done. Phase 21-I (Export Bundle) done. Phase 21-E (Comparison Mode) next. Phase 23 (Deployment Architecture) designed (ADR-048), implementation pending.
**Archive Pointer:** [./.antigravity/tasks/archives/tasks_archive_2026-04-10.md]
