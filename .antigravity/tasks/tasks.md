# Tasks (SOLE SOURCE OF TRUTH)

**Workspace ID:** SPARMVET_VIZ
**Last Updated:** 2026-04-20 by @dasharch

## 🟣 Global Tiered Migration & Documentation Lock (COMPLETED)
>
> Status: COMPLETED. Detailed history moved to: [./.antigravity/tasks/archives/tasks_archive_2026-04-10.md]

## 🟢 2026-04-10 Session Progress (COMPLETED)
>
> Status: COMPLETED. Detailed history moved to: [./.antigravity/tasks/archives/tasks_archive_2026-04-10.md]

## 🟢 2026-04-18 Session: Layout stabilization, Hierarchical Navigation & Aesthetic polish (COMPLETED)
>
> Status: COMPLETED. Detailed history moved to: [./.antigravity/logs/audit_2026-04-18.md]

## 🟢 2026-04-18 Session (Cont.): Structural Repair & UI Integrity (COMPLETED)
>
> Status: COMPLETED. Detailed history available in: [./.antigravity/logs/audit_2026-04-18.md]

## 🟣 UI Infrastructure & Integrity (BASELINE LOCK)
>
> Status: COMPLETED. The Analysis Theater satisfies all forensic alignment and ID sanitation requirements.

## 🟢 Phase 16: Gallery Taxonomy & Scaling (COMPLETED 2026-04-19)

- [x] **Metadata Harmonization**: Extracted taxonomy from `recipe_meta.md` into YAML `info` blocks.
- [x] **Pivot-Index Engine**: Implemented `GalleryIndexer` and `gallery_index.json` structure (ADR-037).
- [x] **Governance Wrapper**: Implemented `libs/viz_gallery/assets/refresh_gallery.py` for audit & indexing.
- [x] **UI logic Activation**: Switched `server.py` to use high-performance Set Intersections for all gallery filtering.
- [x] **Ergonomic Polish**: Promoted selector to top of sidebar, added Play-style Apply button, and restored previews.
- [ ] **Taxonomy Data Audit**: [DEFERRED] Verify and correct the tags for the taxonomy classification (Family/Pattern/Difficulty) in gallery assets manifests (`assets/gallery_data/*/recipe_manifest.yaml`).

## 🟢 Phase 17: Contextual UI Masking & Focus Mode (COMPLETED 2026-04-19)

- [x] **Contextual Masking (ADR-038)**: Implemented server-side reactive reification in `server.py` to mask redundant tools.
- [x] **Global Nav Persistence**: Promoted Home/Gallery selector to a persistent header in the left sidebar.
- [x] **Seamless Switch signaling**: Implemented Home-tab focus mode when cloning from gallery.

## 🟢 Phase 18: Blueprint Architect — Bidirectional Lineage Navigation (ACTIVE)

**Objective**: Transform the Blueprint Architect into a full bidirectional manifest development environment. A scientist can start from a desired plot output and trace backwards to find where a missing field must be added (reverse lineage), or build forward from source to plot (forward lineage). Full design rationale in ADR-040.

### Phase 18-A: Field Materialization & Component Context Map (COMPLETED 2026-04-20)

- [x] Move `normalize_manifest_fields.py` to `app/assets/` with importable `normalize_file()` API.
- [x] Add `btn_normalize_fields` ("⚙️ Fix Format") button to Interface (Fields) tab in `wrangle_studio.py`.
- [x] Wire `btn_normalize_fields` handler in `server.py` — writes file in-place with `.bak` backup, reloads workspace.
- [x] Fix `_parse_fields_safe` to handle rich `{col: {type, label, ...}}` dict format.
- [x] Fix `_normalize_fields` to handle rich dict format (extracts `type`/`label` instead of `str(v)`).
- [x] Add `_build_sibling_map()` — parses master YAML without resolving `!include`; maps rel_path → `{role, schema_id, schema_type, siblings, ingredients}`. Assembly wrangling files get `role="assembly"`.
- [x] Add `_build_schema_registry()` — full schema-level structural index capturing both `!include` refs and inline content via `_slot()` helper.
- [x] Add `_load_fields_file()` helper — unwraps redundant wrapper keys (ADR-014 parity).
- [x] Add `_component_ctx_map`, `_includes_map`, `_schema_registry` reactive values; all populated on manifest selection.
- [x] Rewrite `_handle_manifest_import` role-aware dispatch: `input_fields` → left panel; `output_fields` → right panel; `wrangling` → both panels from siblings; `assembly` → multi-ingredient accordion upstream; `plot_spec` → parent assembly final_contract upstream.
- [x] Wire `get_schema_registry` and `get_includes_map` into `wrangle_studio.define_server()` call.

### Phase 18-B: Lineage Rail UI (Component Chain View) — COMPLETED 2026-04-20

- [x] **`_build_lineage_chain()`**: Walks sibling map bidirectionally; produces ordered `[{rel, schema_id, role, label, is_active}]` chain. Verified headless for all 5 role types.
- [x] **`active_lineage_chain` reactive**: Populated in `_handle_manifest_import` after every role dispatch.
- [x] **`lineage_rail_ui` clickable render**: Horizontal `<button>` chain with role icons (📥⚙️🔗📤📊), role-coloured borders, active node highlighted. JS `onclick` sets hidden `lineage_node_rel` input.
- [x] **`handle_lineage_node_click` effect**: Receives Rail node clicks via `@reactive.event(input.lineage_node_rel)`, updates pipeline selector, shows notification.
- [x] **Rail click → full component load**: `handle_lineage_node_click` triggers `btn_import_manifest` via `ui.js_eval` — Rail is fully navigable.
- [ ] **Plot spec chain enrichment**: Prepend assembly wrangling node to plot_spec chain using `target_dataset` from file content. *(DEFERRED)*
- [ ] **Branch selector**: When one assembly → N plots, show branch tabs so user can select downstream path. *(DEFERRED to 18-F)*

### Phase 18-B-fixes: Live Testing Bug Fixes — COMPLETED 2026-04-20

- [x] **Sidebar selector labels**: `_update_dataset_pipelines` now shows `"{schema_id} — {role}"` display labels instead of raw filenames.
- [x] **Plot spec upstream contract**: `_handle_manifest_import` broadened `target_dataset` lookup to cover `data_schemas` entries (not only `assembly_manifests`) — fixes empty Upstream Contract when `target_dataset` is a source dataset.
- [x] **Live View plot preview**: `active_manifest_path` reactive added; `_handle_manifest_import` sets `active_viz_id` + `active_manifest_path` when loading a plot spec; `architect_active_plot` uses full `ConfigManager` config instead of component fragment.
- [x] **TubeMap node click → full load**: `_sync_selector_from_node_click` now fires `btn_import_manifest` via `ui.js_eval` after updating the selector.

### Phase 18-C: 3-Column Interface Panel (COMPLETED 2026-04-20)

- [x] **Lineage Rail header**: `lineage_rail_ui` — horizontal context bar with role badge, schema_id, schema_type.
- [x] **Left — Upstream Contract**: `lineage_upstream_ui` — input_fields table; assembly multi-ingredient accordion; plot → parent assembly final_contract.
- [x] **Center — Active Component**: `lineage_component_ui` — schema_id, role, schema_type, ingredients, inline wrangling indicator.
- [x] **Right — Downstream Contract**: `lineage_downstream_ui` — output_fields table; plot → empty (terminal).
- [x] Dynamic column headers: `upstream_label_ui`, `component_label_ui`, `downstream_label_ui`.

### Phase 18-D: Per-Plot Wrangling Support (COMPLETED 2026-04-20)

- [x] **Manifest key `pre_plot_wrangling`**: Supported `!include` in plot block; registered as `plot_wrangling` role.
- [x] **Lineage Rail node**: Added 🔧 icon (orange) for plot wrangling intermediate node.
- [x] **"➕ Add plot wrangling" affordance**: UI shows button when slot is absent; linked badge when present.

### Phase 20: Relational Manifest Stress Testing & stabilization

- [ ] **Field Gap Analysis tool**: Enter a desired field name → the tool walks the lineage backwards and shows which pipeline step is the earliest point where the field can be added or computed.
- [ ] **Forward propagation hint**: After identifying the insertion point, highlight which output_fields and final_contract files need to be updated to carry the field forward to the plot.

### Phase 18-F: Interactive TubeMap Engine (ADR-039, original scope)

- [ ] **Interactive TubeMap (ADR-039)**: Full Mermaid/SVG DAG with clickable nodes driving the Lineage Rail.
- [ ] **Action Registry Parity**: Map the complete `@register_action` library (175+ actions) to the Architect.
- [ ] **Visual Forking**: Select a node and initiate a new branch, producing YAML additions to the manifest.
- [x] **Stress Test Loop**: Executed `debug_assembler.py` against the large ST22 manifest.
- [x] **Key Purge Resilience**: Fixed 'bool' attribute error in `DataAssembler` to handle unquoted YAML 'on'.
- [x] **Defensive Recoding**: Added casting in `recode_values` for non-string columns.
- [x] **Contract Guard Smarts**: Updated `debug_assembler.py` to auto-resolve `original_name` mappings.
- [x] **Pipeline Pass**: Verified all 3 major ST22 assemblies (Anchor, AR1, Summary) materialize successfully.

## 🟢 Phase 22: Server Decomposition (ADR-045) — COMPLETED 2026-04-23

**Objective:** Split `server.py` (~2,362 lines) into a thin orchestrator + `app/handlers/` modules + `app/modules/manifest_navigator.py`. Zero behaviour change. Must complete before Phase 21-B to keep new Home Theater code in its correct location.
**Full task breakdown:** `implementation_plan_master.md` Phase 22.

### Phase 22-A: `app/modules/manifest_navigator.py`
- [x] Create file; move 5 pure functions from `server.py`; rename to drop `_` prefix (public API).
- [x] Update `server.py` imports.
- [x] Verify: `python -c "from app.modules.manifest_navigator import build_sibling_map; print('OK')"`.

### Phase 22-B: `app/handlers/__init__.py`
- [x] Create empty `__init__.py`.

### Phase 22-C: `app/handlers/gallery_handlers.py`
- [x] Move all gallery `@reactive.Effect`/`@render.*` blocks; add `define_server()` delegation in `server.py`.

### Phase 22-D: `app/handlers/ingestion_handlers.py`
- [x] Move `handle_ingest`, `update_persona_context`; add delegation.

### Phase 22-E: `app/handlers/audit_stack.py`
- [x] Move audit nodes, `handle_apply`, `track_recipe_changes`, `recipe_pending_badge_ui`; add delegation.

### Phase 22-F: `app/handlers/blueprint_handlers.py`
- [x] Move all Phase 18 Shiny wiring; update internal imports to use `manifest_navigator`; add delegation.

### Phase 22-G: `app/handlers/home_theater.py`
- [x] Move `dynamic_tabs`, sidebar/filter/plot/table handlers; add delegation.

### Phase 22-H: Slim `server.py`
- [x] Confirmed 228 lines (thin orchestrator only — shared state, calcs, utils, 5 delegations).

### Phase 22-I: @verify Gate
- [x] [HEADLESS] Import check passed.
- [x] [LIVE] UI smoke test — no major regressions detected.
- [x] [@verify] Complete.

## 🟡 Phase 21: Unified Home Theater (ADR-043 / ADR-044) — NEXT SESSION

**Objective:** Eliminate the "Analysis Theater / Viz" nav mode; merge into a unified Home; implement Tier Toggle, context-reactive filters, collapsible layout, Comparison Mode, and persona-gated right sidebar suppression.
**Governing ADRs:** ADR-043, ADR-044. **Full task breakdown:** `implementation_plan_master.md` Phase 21.

### Phase 21-A: Nav & Routing Simplification
- [ ] Remove `"Viz"` branch from `dynamic_tabs()` in `server.py`.
- [ ] Remove `"Analysis Theater"` nav item from `sidebar_nav_ui()`.
- [ ] Remove `theater_state`, `btn_max_plot`, `btn_max_table`, `btn_reset_theater`, `is_triple` / `triple_tier_mode`.

### Phase 21-B: Manifest-Driven Tab Structure
- [ ] Rebuild Home to render exclusively from `analysis_groups` — no hardcoded tabs, no Inspector tab.
- [ ] Wrap each group's plot sub-tabs (`navset_underline`) in a collapsible `ui.accordion_panel` (default expanded).
- [ ] Track `active_home_subtab` as a reactive value.

### Phase 21-C: Tier Toggle
- [ ] Implement `tier_toggle` radio-button strip: T1/T2 always; T3-Wrangle/T3-Plot persona-gated.
- [ ] Wire to control plot output and data table rendered in center pane.
- [ ] Remove `ref_tier_switch` and `view_toggle`.

### Phase 21-D: Collapsible Data Preview
- [ ] Place data preview table in a `ui.accordion_panel` below plot accordion (default expanded).
- [ ] Column picker: `width: 100%`, `flex: 1 1 100%`, no multi-row wrapping (CSS update in `ui.py`).

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

## 🟡 NEXT SESSION (deferred)

## 🟡 2d NEXT SESSION: Relational Pipeline Stress Testing & Gallery Submission

- [ ] **Relational Row-Explosion Audit**: Stress test the Tier 2 Join logic using the ST22 manifest to ensure no unintended Cartesian products across curiosity branches.
  - [x] [HEADLESS] Create `debug_relational_audit.py` to stress test ST22 joins and verify relational integrity.
  - [x] [HEADLESS] Materialize Tier 2 results to `tmp/Manifest_test/ST22_audit/`.
  - [x] [HEADLESS] Validate row counts (Input Anchor vs Joined Result) and output `df.glimpse()`.
- [x] **Gallery Submission Pipeline**: Implement the reactive backend for `btn_gallery_open_submission` to allow for formal result preservation.
  - [x] [HEADLESS] Implement `GalleryManager` for folder-based persistence (libs/viz_gallery).
  - [x] [HEADLESS] Create `@verify` debugger (debug_gallery_submission.py) and materialize to tmp/.
  - [x] [UI] Bind backend to `server.py` and enforce Gatekeeper constraints.
- [x] **UI Performance Benchmark**: Optimize the reactive `is_feature_enabled` helper to ensure zero-latency persona switching during live sessions.
  - [x] [HEADLESS] Create `debug_ui_performance.py` to target persona switching latency and YAML IO overhead.
  - [x] [HEADLESS] Implement template caching in `Bootloader (bootloader.py)` to eliminate redundant disk reads.
  - [x] [HEADLESS] Verify latency reduction and materialize benchmark report to `tmp/ui_perf_audit.txt`.

## 🟢 Phase 3 (REFINED)

- [x] **Advanced Error Handling:** Malformed Data gatekeeping (ADR-034).
  - [x] [HEADLESS] Implement `MetadataValidator (metadata_validator.py)`.
  - [x] [HEADLESS] Integrate schema validation loop in `DataOrchestrator`.
  - [x] [HEADLESS] Verify typo-correction suggestions via `debug_phase3_refinements.py`.
- [x] **Decision Metadata Hash:** (ADR-024 refinement) Embed SHA-256 fingerprints in Parquet branch metadata.
  - [x] [HEADLESS] Implement deterministic recipe hashing in `utils.hashing`.
  - [x] [HEADLESS] Update `DataAssembler` to verify logic integrity before short-circuiting.
  - [x] [HEADLESS] Embed fingerprints in Parquet metadata via `pyarrow`.
- [ ] **Plotly Interactivity:** [DEFERRED] move native interactivity to Post-Prototype phase.
- [ ] **Mode B API:** [DEFERRED] BioBlend/Galaxy dynamic connector.
- [x] **Automated Element & Decorator Audit (Master Suite):**
  - [x] [HEADLESS] Create `ingestion_integrity_suite.py` (Verified 4/4 cases).
  - [x] [HEADLESS] Complete `transformer_integrity_suite.py` (Verified 37/37 actions).
  - [x] [HEADLESS] Run `viz_factory_integrity_suite.py` (Verified 123/125 components).

## 🟢 Phase 4: Artist Expansion (API Parity)

- [x] **Registry Expansion**: Achieved 1:1 parity with Plotnine 0.14.0 components (175 total registered).
  - [x] [HEADLESS] Implement 30+ missing geoms and stats (geoms/core.py).
  - [x] [HEADLESS] Implement math, date, and stroke scales (scales/core.py).
  - [x] [HEADLESS] Implement 3rd-party themes (538, Seaborn, XKCD, Tufte) (themes/core.py).
- [x] **Integrity Audit & Test Coverage**:
  - [x] [HEADLESS] Generate test manifests and TSV data for all 175 components.
  - [x] [HEADLESS] Verify 98.3% integrity coverage via `viz_factory_integrity_suite.py` (172/175 PASSED).
  - [ ] [HEADLESS] Retest & Fix deferred components: `scale_x_timedelta`, `scale_y_timedelta` (dtype mismatch), `geom_map` (requires spatial data). [DEFERRED] Decorators commented out in `scales/core.py` and `geoms/core.py`.
- [x] **Documentation Sync**:
  - [x] Updated `libs/viz_factory/README.md` with pass rates.
  - [x] Updated `docs/appendix/viz_factory_components.qmd` with gallery examples for all major component groups.
- [x] **Transformer completeness check**: Verified all primary Polars actions are implemented (Added `mutate` for arbitrary expressions).
- [ ] Workspace hygiene: remove temporary tests from tmp/ and dispose of unique scripts. [PENDING]
- [ ] Automatic adjustment labels size, orientation and space for plots [DEFERRED]

## 🟢 Phase 6: Analytical Engine Hardening (Polars Parity) (COMPLETED)

- [x] **Window & Sequential Logic**:
  - [x] Implement `window_agg` (Grouped Rolling Aggregations).
  - [x] Implement `shift` / `lag` (Time-series inter-row comparison).
  - [x] Implement `fill_nulls_direction` (Forward/Backward Fill).
- [x] **Temporal Intelligence**:
  - [x] Implement `date_extract` (Year, Month, Week splitting).
  - [x] Implement `date_truncate` & `date_offset`.
- [x] **List & Struct Engineering**:
  - [x] Implement `list_slice`, `list_join`, and `is_in` logic.
- [x] **Analytical Core**:
  - [x] Implement `sort` (Multi-key deterministic ordering).
  - [x] Implement `sample` (Percentage-based data reduction).
  - [x] Implement `cum_sum` / `cum_count` (Running totals).
  - [x] Implement `z_score` and `percentile` normalization.
- [x] **Exhaustive Parity (Final Tier)**:
  - [x] Implement `select_by_pattern` (Regex column selection).
  - [x] Implement `str_replace_regex` and `null_if`.
  - [x] Implement `value_counts` and `describe_stats` generators.
- [x] **Niche/Horizontal Logic**:
  - [x] Implement `horizontal_stats`, `any_horizontal`, `all_horizontal`.
  - [x] Implement `interpolate`.

# USER TESTING [DEFERRED]

- [ ] Gallery:_ Test The Clone to sandbox functionality (can only be done when more advanced in other modes for development wrangling)

# IMPROVEMENETS IDEAS [DEFERRED]

- [ ] Gallery thumbnails for finding faster the plots we want to look at ?

---

**STATUS:** UI Architectural Baseline Hardened. 🧱🔗
**Archive Pointer:** Detailed history for all tiered wrangling refactors is located in [./.antigravity/tasks/archives/tasks_archive_2026-04-10.md].
