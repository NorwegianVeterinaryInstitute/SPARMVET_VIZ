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

### Phase 21-F: Context-Reactive Left Sidebar Filters
- [ ] Read `active_home_subtab` → extract active `plot_spec` aesthetics → regenerate filter widgets scoped to those columns only.
- [ ] Ensure filter regeneration does NOT reset Tier Toggle or Comparison Mode.

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

## 🟡 Deferred / Backlog

### Phase 18 Deferred Items
- [ ] **Plot spec chain enrichment** (18-B): Prepend assembly wrangling node to plot_spec chain using `target_dataset`.
- [ ] **Branch selector** (18-B / 18-F): When one assembly → N plots, show branch tabs.
- [ ] **Interactive TubeMap** (18-F / ADR-039): Full Mermaid/SVG DAG with clickable nodes.
- [ ] **Action Registry Parity** (18-F): Map complete `@register_action` library to Blueprint Architect.
- [ ] **Visual Forking** (18-F): Select a node, initiate a new branch (YAML additions).

### Phase 20: Relational Manifest Tooling
- [ ] **Field Gap Analysis tool**: Field name → walk lineage backwards to earliest insertion point.
- [ ] **Forward propagation hint**: Show which output_fields / final_contract files need updating.

### Deferred VizFactory / Scale Fixes
- [ ] Retest & fix `scale_x_timedelta`, `scale_y_timedelta` (dtype mismatch). *(decorators commented out in scales/core.py)*
- [ ] Retest & fix `geom_map` (requires spatial data). *(decorator commented out in geoms/core.py)*
- [ ] Automatic label size / orientation / spacing adjustment for plots.

### Gallery & UI
- [ ] **Taxonomy Data Audit**: Verify/correct tags in `assets/gallery_data/*/recipe_manifest.yaml`.
- [ ] Gallery thumbnails for faster visual scanning.
- [ ] Gallery: Test "Clone to Sandbox" functionality (requires more advanced wrangling modes).

### Technical Debt
- [ ] **Unified Materialization**: Standardize `debug_wrangler.py` and `debug_assembler.py` to auto-create dated `tmp/{date}/{lineage}/` subfolders.
- [ ] **Renaming Precision Audit**: Scan existing manifests for generic `phenotype` or `source` columns; refactor to `predicted_phenotype` or descriptive equivalent.
- [ ] Workspace hygiene: remove temporary tests from `tmp/` and dispose of unique scripts.

---

**STATUS:** Phase 21-C/D done. Layout = navset_pill groups + independent accordions (plots + data preview). Phase 21-E next. 🧱🔗
**Archive Pointer:** [./.antigravity/tasks/archives/tasks_archive_2026-04-10.md]
