# Tasks (SOLE SOURCE OF TRUTH)

**Workspace ID:** SPARMVET_VIZ
**Last Updated:** 2026-05-03 (UI colour harmonisation + revert) by @dasharch

---

## 🟣 Completed Phases — Archived

| Phase | Description | Completed | Archive |
|---|---|---|---|
| Phases 16–18, 21-A–B | Nav/routing, manifest-driven tabs, tier toggle, layout | 2026-04-23 | [tasks_archive_2026-04-10.md](archives/tasks_archive_2026-04-10.md) |
| Phase 21-C–I, IU-1–7 | Comparison mode, filters, right sidebar, export bundle, VizFactory | 2026-04-23–30 | [tasks_archive_2026-04-14.md](archives/tasks_archive_2026-04-14.md) |
| Phase 22 (A–J) | Session mgmt, T3 audit, per-plot scoping, propagation | 2026-04-25 | bugs/open items below |
| Phase 23-A/B | Deployment profile, connector library | 2026-04-30 | [tasks_archive_phase24.md](archives/tasks_archive_phase24.md) |
| Phase 24 | `home_theater.py` decomposition (ADR-051) | 2026-05-01 | [tasks_archive_phase24.md](archives/tasks_archive_phase24.md) |
| Phase 25 (A–O) | Left sidebar restructure, persona flag gating, ADR-052+053 | 2026-05-01 | [tasks_archive_phase25.md](archives/tasks_archive_phase25.md) |
| Phase 26 CSS | UI harmonisation: view banners, button colours, Gallery sidebar refactor, sidebar toggle, modal radio spacing | 2026-05-02 | ADR-056, ADR-057 |
| DEMO-1..4 | Monday demo render/filter bugs — all fixed | 2026-04-30 | commits `55ab1c5` `33afa1b` `b91dfc9` `4c962e6` `8b4f3a4` |
| AUDIT-1 | Allow PK-column filters with warning (ADR-049 amended) | 2026-04-30 | commit `3c6195f` |
| PROP-1 | Per-plot column-presence preview in propagation modal | 2026-04-30 | commit `b4dcd10` |
| UX-3/5 | Filter row 🗑 icon + right sidebar header bold/yellow | 2026-05-01 | commit `294814e` |
| UX-4 | "➜ Send to Audit (N)" rename in T3 mode | 2026-05-02 | `filter_and_audit_handlers.py` |
| UX-2 | Data preview selectize width — covered by `.column-picker-container` CSS | 2026-05-02 | `theme.css` Phase 26 |
| PERSONA-1b | Persona-name gate doc-drift | 2026-05-01 | commit `7344951` |
| STARTUP-SORT | Duplicate `sort` registration warning on startup | 2026-05-02 | commit `130f4f5` |
| SESSION-1 | Session reimport fails (no assembly.json) | 2026-05-02 | `session_manager.py`, `home_theater.py` |
| EXPORT-SGE-1/5/6 | Single graph export: plot/data filenames + README hashes | 2026-05-02 | `single_graph_export_handlers.py` |
| EXPORT-SGE-3 | Apply button vestigial — confirmed absent, closed | 2026-05-02 | no code change |
| UX-FONT-1 | `default_font_family: "Liberation Sans"` in test manifests | 2026-05-02 | `1/2_test_data_ST22_dummy`, `stress_test_master` |
| persona_selector orphan | Removed dead `update_persona_context` handler | 2026-05-02 | `ingestion_handlers.py` |
| VizFactory timedelta | `scale_x/y_timedelta` — works in plotnine 0.15.3, smoke-tested | 2026-05-01 | 42/42 pass |
| STATE-T2 (render) | Plot render handlers (`_group_plot_handler`, `_cmp_baseline_handler`) always served T1 — now use `_resolve_active_lf` | 2026-05-02 | `home_theater.py` |
| FLICKER-CMP-SWITCH | Compare switch DOM flicker — CSS hide/show instead of DOM insert/remove | 2026-05-02 | `home_theater.py` `comparison_mode_toggle_ui` |
| FLICKER-CMP-TABS | T2/T3 compare toggle rebuilt all subtabs — per-plot `plot_cell_{p_id}` handlers isolate layout | 2026-05-02 | `home_theater.py` `_make_plot_cell_handler` |
| AUDIT-COLLECTION | Pipeline Audit "Collection:" always showed first manifest collection — fixed via `_active_target_ds()` | 2026-05-02 | `audit_stack.py` |
| EXPORT-ZIP-STRUCT | Global export ZIP flat layout → folder-per-dataset with README mapping table | 2026-05-02 | `export_handlers.py` |
| YEAR-CAST-INT | Year column Float64 (from TSV) → Int64 via `cast` wrangling step; bad axis breaks eliminated | 2026-05-02 | `1_test_data_ST22_dummy.yaml` wrangling |
| VIZ-BREAKS-INT | `breaks_integer: true` param on `scale_x/y_continuous` → `MaxNLocator(integer=True)` | 2026-05-02 | `viz_factory/scales/core.py` |
| STATE-1 | Plot flicker on T3 toggle / panel switch — per-plot cell handlers + CSS hide/show | 2026-05-02 | `home_theater.py` |
| STATE-2 | Compare toggle wrong-plot-wins — resolved by per-plot cell handler isolation, user-verified | 2026-05-02 | `home_theater.py` |
| BUG-PERF-1 | `materialize_tier1` skip-if-exists guard present at call site (`out_path.exists()`) | 2026-05-02 | `home_theater.py:199` |
| UX-1 | Plot rendering slow — resolved with parquet cache fast path | 2026-05-02 | `home_theater.py` |

**Phase 24 commits:** `89bb5ef` `890b609` `f540cbf` `d50197e` `4c38f26` `18dbd46` `f0f7d92` `2393e50` `0b50fbd`
**Phase 25 commits:** `294814e` `9b66656` `72726df` `45591ac` `95b48ac` `dc4464c` `320f6bf`

| CSS-TOGGLE | Sidebar toggle `position:fixed` broke re-open when both sidebars collapsed — removed, defer to bslib positioning | 2026-05-03 | `theme.css` §4 — ADR-062 |
| GALLERY-ICONS | Double icons on Recipe/Gallery Taxonomy accordion panels — removed `icon=` kwarg | 2026-05-03 | `gallery_viewer.py` |
| GALLERY-SELECTALL | "Select all" alignment + spacing fixed; `.gallery-select-all-row` CSS class scopes margin override | 2026-05-03 | `gallery_viewer.py`, `theme.css` §13 |
| GALLERY-PIVOT | `gallery_handlers.py` sync handlers now read choices from pivot (same source as `build_sidebar_ui`) | 2026-05-03 | `gallery_handlers.py` |
| GALLERY-PANES | Both Gallery theater panes (Preview + Guidance) are now collapsible accordions | 2026-05-03 | `gallery_viewer.py`, `theme.css` §14 — ADR-061 |
| GALLERY-META | All 13 `recipe_meta.md` files + template migrated to standard `## Name` / `> tags` / `### sections` format | 2026-05-03 | `assets/gallery_data/*/recipe_meta.md` — ADR-061 |
| CSS-SECTION17 | §17 "Educational Guidance Pane Content" added; all `.gallery-md-pane` rules consolidated | 2026-05-03 | `theme.css` §17 — ADR-061 |
| GALLERY-RECIPES-13 | 13 new gallery recipes added + VizFactory format normalized (name: key, global mapping, per-recipe bugs) | 2026-05-03 | `assets/gallery_data/*/` — ADR-063 |
| GALLERY-TAXONOMY-6 | 6-axis taxonomy: added `geom`/`show`/`sample_size` across all 34 manifests, sidebar filters, pivot index, handlers | 2026-05-03 | `gallery_manager.py`, `gallery_viewer.py`, `gallery_handlers.py` — ADR-063 |
| GALLERY-TAXONOMY-CHEAT | `TAXONOMY_CHEATSHEET.md` created — icon→axis map, allowed values, tag strip format, manifest info block template | 2026-05-03 | `assets/gallery_data/TAXONOMY_CHEATSHEET.md` |
| GALLERY-PREVIEWS | `generate_previews.py` created; all 34 `preview_plot.png` regenerated | 2026-05-03 | `libs/viz_gallery/assets/generate_previews.py` |
| GALLERY-META-6AXIS | All 34 `recipe_meta.md` tag strips extended with 3 new fields (⚙️ geom · 🎯 show · 📏 sample_size) | 2026-05-03 | `assets/gallery_data/*/recipe_meta.md` |
| CSS-ACCORDION-HARM | §18/18b accordion harmonization: bold text, no grey border, `border-radius: 8px; overflow: hidden` on accordion-items; Bootstrap collapse cards styled; TubeMap normalized | 2026-05-03 | `theme.css` §18/18b — ADR-064 |
| HOME-PLOT-COLLAPSE | Home Main Plot Card (`home_plots_body_accordion`) + Data Preview (`acc_home_data`) now collapsible via bslib accordion; Data Preview title unified (icon + font) | 2026-05-03 | `home_theater.py`, `theme.css` §18b — ADR-064 |
| BLUEPRINT-WORK-COLLAPSE | Blueprint Work Area accordion (`blueprint_workarea_accordion`) — bslib accordion; Bootstrap Glimpse/Plot Preview cards styled and rounded | 2026-05-03 | `wrangle_studio.py`, `theme.css` §18b — ADR-064 |
| REVERT-ADR064-COLLAPSE | Reverted structural accordion changes from ADR-064 (commits bdf8723→729b2af) that broke `#central_theater_tabs` and introduced rogue Plot Preview card — restored `home_theater.py` + `wrangle_studio.py` to bdf8723, then removed Plot Preview Bootstrap collapse card from wrangle_studio | 2026-05-03 | `git checkout bdf8723 -- …` — preserves ADR-064 CSS §18; Python only reverted |
| CSS-BLUE-HARM | Comprehensive `#345beb` colour harmonisation across all 4 views: nav pills inactive, theater tab links, TubeMap accordion text, audit sidebar bg/text, session delete button style, gallery preview/guidance headers, view title banner text, card headers | 2026-05-03 | `theme.css` §3/§5/§6/§9/§12/§14/§16/§17/§18 — ADR-065 |
| CSS-BLUE-FIXES | Final 4 CSS colour fixes: `#audit_sidebar .card` full rounding (was `8px 8px 0 0`), `#audit_sidebar h6` `#345beb` (Active Logic Stack), guidance expanded state `#345beb`, Live Data Glimpse button `#345beb` | 2026-05-03 | `theme.css` §5/§16/§17/§18 — ADR-065 |
| UI-STYLE-GUIDE | Created `docs/reference/ui_style_guide.qmd` — developer CSS customisation reference: per-view element→selector→default→modifiable table, colour tokens, typography scale, CSS section index, hard constraints callout, known dead rules | 2026-05-03 | `docs/reference/ui_style_guide.qmd`, registered in `docs/_quarto.yml` |

---

## 🟡 Active Lineage Build: ST22

- [x] **Lineage 1 (AMR Profile)**: Materialized. Verified Integer Year and Predicted Phenotype.
- [ ] **Lineage 2 (Plasmid Dynamics)** `[@user]`:
    - [ ] Create `2_test_data_ST22_dummy/input_fields/plasmid_data.yaml`
    - [ ] Implement Tier 1 filtering (min identity/overlap for PlasmidFinder)
    - [ ] Assemble with metadata and AMR results; verify via Tier 1 audit artifacts.

---

## 👤 User needs to test

- [x] **Phase 21 T1/T2 visual diff**: Verified 2026-05-02 — T1↔T2 toggle works, earlier years disappear in T2. T2/T3 comparison mode also confirmed working.
- [x] **22-G-4**: Session ghost files verified 2026-05-02. Sessions `7f265b1d7b27` and `b98f603ac5f7` both have `assembly.json` written by the SESSION-1 fix. Old pre-fix sessions still present but will import via T3-ghost fallback. No cleanup needed.


---

## 🔴 Open Issues

### Bugs

- [x] **STATE-T2**: Plot render handlers (`_group_plot_handler`, `_cmp_baseline_handler`) had inline data resolution that always served T1 — ignored `tier_toggle`. Fixed 2026-05-02: both now use `_resolve_active_lf` (T1 or T2 per toggle) and `_resolve_t1_lf` (baseline always T1).
- [x] **STATE-1**: Flicker on T3 toggle and panel switch — resolved 2026-05-02 via per-plot `plot_cell_{p_id}` handlers (layout isolated from `dynamic_tabs`) + CSS hide/show for compare switch. `home_state` remains monolithic but observable flicker is gone; split-state refactor deferred to BUG-PERF-1 scope if needed.
- [x] **STATE-2**: Compare T2/T3 toggle wrong-plot-wins — resolved 2026-05-02; user-verified no longer reproduces after per-plot cell handler isolation.
- [x] **BUG-PERF-1**: `materialize_tier1` skip-if-exists guard confirmed present in `home_theater.py:199` — `if out_path.exists(): return pl.scan_parquet(out_path)`. Only rematerializes on cache miss.

### Filter / Audit

- [x] **AUDIT-2**: Filter display mismatch — resolved. Promotion `eq`→`in` happens at Add-time (`filter_and_audit_handlers.py:373`); staged row immediately renders with `∈` via `_op_label(op)`; `_params_summary` in audit panel uses the same symbol table. Display is consistent end-to-end.
- [x] **AUDIT-3**: Propagation skip is NOT silent — confirmed. Modal preview shows `⚠️ N skip (col missing)` before confirm; post-confirm notification explicitly lists each skipped plot + column (`filter_and_audit_handlers.py:772`). ADR-049 D9 implemented.
- [x] **AUDIT-4**: Compare T2/T3 toggle loses state on plot switch — resolved with STATE-2 (per-plot cell handlers), user-verified.
- [x] **PROP-4**: Propagation rules documented in `docs/user_guide/audit_pipeline.qmd` — one-at-a-time workflow (8-step sequence), writing good reasons section, column-presence semantics already covered in propagation preview section.

### Export

- [x] **EXPORT-TIERS**: Both global and single graph export were only exporting T1 data — T2 wrangling was a stub (`t2_equals_t1 = True`). Fixed 2026-05-02: both now export `_T1_data.tsv` always, `_T2_data.tsv` when tier2 recipe steps exist, `_T3_data.tsv` when T3 nodes committed.
- [x] **EXPORT-SGE-2**: `full_recipe.yaml` added to single graph export bundle — T1/T2 assembly + T3 nodes + plot spec. `!include` confirmed resolved in `raw_config` (custom SafeLoader constructor). `manifest_fragment.yaml` and `t3_recipe.json` kept for backwards compat.
- [x] **EXPORT-SGE-4**: Multi-file upload hint added — "Hold Ctrl/⌘ Cmd to select multiple files". Native `multiple=True` already in place; dynamic "Add another" loop not needed.
- [x] **EXPORT-SGE-7**: Dataset-to-plot mapping when multiple source files uploaded — resolved by IMPORT-1. The assignment table (filename → dataset dropdown per manifest) is the implementation; same Option B design. 2026-05-02.

### Session / Import

- [x] **IMPORT-1**: Data Import — implemented 2026-05-02. Assignment table (filename → dataset dropdown), per-file `MetadataValidator` validation with `.tip` fuzzy suggestions surfaced inline, writes to `source.path` or `raw_data_dir/{ds_id}`, busts parquet cache + `bootloader` LF cache, `data_refresh_trigger` invalidates plot renders. MetadataValidator dtype map audited and fixed (numeric→Float64, date→Date, character→Utf8) before implementation.

- [ ] **INGEST-SANITIZE-1**: Ghost sanitization logic (`libs/ingestion/`) is partially implemented — the sanitizer class exists but is not wired into the main ingestion pipeline. `IngestorOrchestrator` calls raw loaders directly; sanitization is only triggered in isolated debug runners. Wire `DataSanitizer` into `IngestorOrchestrator.run()` before T1 materialisation so ghost values (empty strings, whitespace-only, sentinel nulls) are stripped on every ingestion. See audit §1A (audit_final_exhaustive_2026-05-03.md).

### UX

- [x] **UX-1**: Plot rendering slow — resolved with BUG-PERF-1 (parquet cache hit on fast path).
- [x] **UX-NOTIF-1**: Toast notifications disappear too fast — implemented 2026-05-02. `notification_log = reactive.Value([])` in `server.py`; `app/handlers/notification_utils.py` provides `make_notifier(notification_log)` factory; `_notify` wrapper replaces `ui.notification_show` in 6 user-facing handlers (filter_and_audit, audit_stack, session, export, data_import, sge); right sidebar shows `🔔 Alerts (N)` accordion (newest-first, last 20, type-colored). T3 ghost persistence deferred.
- [ ] **THEATER-1**: Collapse/minimize plot panel — ▼/▲ caret in plot card header → 1-line collapsed state. Per-plot, persisted in `home_state`.

---

## 🟡 Deferred / Backlog

### Gallery — USER:

- [ ] Gallery: Re-verify "Clone to Sandbox" after ADR-057 sidebar refactor. Decide how. *(Deferred — Gallery needs dedicated work sprint before tackling clone flow.)*

### Multi-System Deployment (Phase 23 C–E)

Phases 23-A/B done. 23-C/D/E deferred — not active sprint.

- [ ] **23-C**: Galaxy XML wrapper templates; bundle profile YAMLs in Docker; Galaxy admin docs.
- [ ] **23-D**: IRIDA plugin/iframe launch + `IridaConnector.fetch_data()`; IRIDA admin docs.
- [ ] **23-E**: Per-system quick-start guides (Galaxy / IRIDA / server / local).

### Filter / Propagation (enhancements)

- [ ] **PROP-2**: "Filter inventory" panel — effective filter set per plot with per-filter tooltip (affected/skipped plots).
- [ ] **PROP-3**: Propagation TubeMap — graph viz of audit blast radius, nodes ✅/⚠️/❌. Needs own design pass + ADR.
- [ ] **22-J-10**: Aesthetic propagation (color/shape/fill) — deferred until gallery-clone or wrangling surface supports aesthetic overrides.

### Export (enhancements)

- [ ] **EXPORT-2**: Selective export — per-tier checkboxes (T1/T2/T3 data, recipes, filter trace, Quarto report, README).
- [ ] **EXPORT-3**: Quarto HTML report — typography, plot placement, methods section, TOC polish.
- [ ] **EXPORT-4**: Global export — per-plot height/width control before bundling.
- [ ] **EXPORT-TUBEMAP**: Embed static tube map SVG in global export Quarto report — shows T1→T2 lineage visually. Requires a headless/static render path for `BlueprintMapper.generate_cy_elements()` output (currently only rendered inside Shiny Blueprint reactive context). Depends on Blueprint Architect being stable.

### Gallery & UI

- [ ] **GALLERY-MAP** `[investigation]`: Map chart types (choropleth, hexbin map, bubble map, cartogram). Currently blocked — `geom_map`/spatial layer requires GeoDataFrame support not yet in VizFactory. Needs: spatial manifest format + geopandas integration design. Deferred 2026-05-03.
- [ ] **GALLERY-FLOW** `[investigation]`: Flow / network chart types (Chord diagram, Sankey, network graph, arc diagram, edge bundling). Currently blocked — plotnine has no native support; would require ggplot2-equivalent (networkD3, ggalluvial) or a separate render path. Needs feasibility study: can VizFactory grow a "non-plotnine renderer" hook, or does this need a new library slot? Deferred 2026-05-03.
- [ ] **Taxonomy Data Audit** `[@user]`: Verify/correct tags in `assets/gallery_data/*/recipe_manifest.yaml`.
- [ ] Gallery thumbnails for faster visual scanning.
- [ ] **UX-GALLEXP-1**: Gallery Explorer right sidebar — functionality TBD (currently static help text).
- [ ] **UX-DEVINSP-1**: Test Lab right sidebar + left sidebar redesign — functionality TBD.
- [ ] **UX-CSS-DEMO** `[@user]`: Review `assets/demo/demo_vetinst.css` after default theme finalised.
- [ ] **UX-NOTIF-2**: Persist `notification_log` to the T3 ghost so alerts survive a page refresh. Implementation: on each `_notify` call in `audit_stack.py` (which already has `session_manager`), append to the T3 ghost's `notification_log` list. On session restore, reload into `notification_log` reactive. Linked to UX-NOTIF-1 (ADR-060).
- [ ] **THEATER-1**: Collapse/minimize plot panel — ▼/▲ caret in plot card header → 1-line collapsed state. Per-plot, persisted in `home_state`.

### VizFactory

- [ ] `geom_map` — deferred; requires spatial data (GeoDataFrame). Uncomment when spatial manifests introduced.
- [ ] **21-F-7**: Add `scale_x_discrete` / `scale_y_discrete` to manifests where Year/ST columns are categorical.

### Technical Debt

- [ ] **Unified Materialization**: `debug_wrangler.py` / `debug_assembler.py` — auto-create dated `tmp/{date}/{lineage}/` subfolders.
- [ ] **T3 lf threading**: When new T3 node types (rename, derive, pivot) are added, thread them through `_apply_t3_to_lf`. Design in `.antigravity/tasks/design_sge_lineage_t3.md`.

### Blueprint Architect

- [ ] **TubeMap aesthetics** — tighter rail/tube look; rename 'ref' → 'Add' in nodes and legend.
- [ ] Full Blueprint Architect debug pass (field contracts, lineage rail, Zone C layout).
- [ ] **Action Registry Parity** (18-F): Expose 175+ `@register_action` entries in UI.
- [ ] **Visual Forking** (18-F): Select node → initiate new branch → YAML additions.
- [ ] **Field Gap Analysis tool**: Field name → walk lineage to earliest insertion point.
- [ ] **Forward propagation hint**: Show which output_fields / final_contract files need updating.
- [ ] **UX-NOTIF-3**: Project-load notification for Blueprint Architect manifest reload. When a manifest is imported/saved via Blueprint and reloaded into the active project, `input.project_id` does not change — so the current `_notify_project_loaded` effect does not fire. Hook a notification into `blueprint_handlers.py` after a successful manifest import (`btn_import_manifest` path). Low priority; tackle during Blueprint debug pass.

---

**Archive Pointers:**
- [tasks_archive_2026-04-10.md](archives/tasks_archive_2026-04-10.md)
- [tasks_archive_2026-04-14.md](archives/tasks_archive_2026-04-14.md)
- [tasks_archive_phase14.md](archives/tasks_archive_phase14.md)
- [tasks_archive_phase24.md](archives/tasks_archive_phase24.md)
- [tasks_archive_phase25.md](archives/tasks_archive_phase25.md)
- [tasks_archive_documentation.md](archives/tasks_archive_documentation.md)
- [tasks_archive_infrastructure.md](archives/tasks_archive_infrastructure.md)
- [tasks_archive_integration_qa.md](archives/tasks_archive_integration_qa.md)
- [tasks_archive_viz_factory.md](archives/tasks_archive_viz_factory.md)
- [tasks_test_ui_current.md](tasks_test_ui_current.md) — current UI test checklist
