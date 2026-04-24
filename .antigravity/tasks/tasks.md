# Tasks (SOLE SOURCE OF TRUTH)

**Workspace ID:** SPARMVET_VIZ
**Last Updated:** 2026-04-23 (Session 2) by @dasharch

## 🟣 Completed Phases — Archived

> Status: COMPLETED. Phases 16, 17, 18-A through 18-D, 18-B-fixes, 18-C, 18-F (stress tests), 21-A, 21-B, 22 are done.
> Detailed history: [./.antigravity/tasks/archives/tasks_archive_2026-04-10.md], [./.antigravity/tasks/archives/tasks_archive_2026-04-14.md], [./.antigravity/logs/audit_2026-04-18.md], [./.antigravity/logs/audit_2026-04-23.md]

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

**STATUS:** Phase 21-F done. Phase 21-I (Export Bundle) done. Phase 21-E (Comparison Mode) next. Phase 23 (Deployment Architecture) designed (ADR-048), implementation pending.
**Archive Pointer:** [./.antigravity/tasks/archives/tasks_archive_2026-04-10.md]
