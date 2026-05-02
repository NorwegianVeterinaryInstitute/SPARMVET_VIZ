# Tasks (SOLE SOURCE OF TRUTH)

**Workspace ID:** SPARMVET_VIZ
**Last Updated:** 2026-05-02 (triage pass) by @dasharch

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

**Phase 24 commits:** `89bb5ef` `890b609` `f540cbf` `d50197e` `4c38f26` `18dbd46` `f0f7d92` `2393e50` `0b50fbd`
**Phase 25 commits:** `294814e` `9b66656` `72726df` `45591ac` `95b48ac` `dc4464c` `320f6bf`

---

## 🟡 Active Lineage Build: ST22

- [x] **Lineage 1 (AMR Profile)**: Materialized. Verified Integer Year and Predicted Phenotype.
- [ ] **Lineage 2 (Plasmid Dynamics)** `[@user]`:
    - [ ] Create `2_test_data_ST22_dummy/input_fields/plasmid_data.yaml`
    - [ ] Implement Tier 1 filtering (min identity/overlap for PlasmidFinder)
    - [ ] Assemble with metadata and AMR results; verify via Tier 1 audit artifacts.

---

## 👤 User needs to test

- [ ] **Phase 21 T1/T2 visual diff** `[@user]`: Root cause fixed 2026-05-02 — `_resolve_active_lf` was always serving T1 parquet regardless of tier toggle. Now applies `DataWrangler.run_tier2()` on top when T2 is selected. Retest: open `year_distribution` plot in `1_test_data_ST22_dummy`, toggle T1↔T2 — earlier years should disappear in T2.
- [x] **22-G-4**: Session ghost files verified 2026-05-02. Sessions `7f265b1d7b27` and `b98f603ac5f7` both have `assembly.json` written by the SESSION-1 fix. Old pre-fix sessions still present but will import via T3-ghost fallback. No cleanup needed.


---

## 🔴 Open Issues

### Bugs

- [x] **STATE-T2**: Plot render handlers (`_group_plot_handler`, `_cmp_baseline_handler`) had inline data resolution that always served T1 — ignored `tier_toggle`. Fixed 2026-05-02: both now use `_resolve_active_lf` (T1 or T2 per toggle) and `_resolve_t1_lf` (baseline always T1).
- [ ] **STATE-1**: Active plot flickers when toggling T3 mode or switching panels (Home → Blueprint → Home). Root: `home_state` is monolithic — any write (session hashes, subtab tracking) causes ALL plot handlers to re-render. Fix: isolate plot renders from non-data `home_state` fields via `reactive.isolate()` or split `home_state`.
- [ ] **STATE-2**: Compare T2/T3 toggle switches to wrong plot + jumps back to previous state. Root: `_track_active_home_subtab` iterates all group subtab inputs; comparison mode changes UI structure so a different subtab wins. Needs live tracing to confirm exact priority logic bug. (links to AUDIT-4)
- [ ] **BUG-PERF-1**: `materialize_tier1` fires on every render — `sink_parquet` has no skip-if-exists guard. Fix: consult `SessionManager.status` first; use cached parquet on `fast_path`; only rematerialise on `reassemble` / `new_session`.

### Filter / Audit

- [ ] **AUDIT-2**: Filter display mismatch — UI "= exact France" → audit shows "∈ any of [France]". Root cause: `eq` op with single scalar is promoted to `in` in the commit path. Decide: normalise display to always show `in` form, or preserve original op in the T3 ghost. Investigate `_apply_filter_rows` + `_params_summary` path.
- [ ] **AUDIT-3**: Filter propagation silently skips plots when the column is missing. Should surface a per-plot warning rather than silent skip (ADR-049 D9). Trace propagation walk — should it also walk back to root data source?
- [ ] **AUDIT-4**: Compare T2/T3 toggle loses state on plot switch — linked to STATE-2.
- [ ] **PROP-4** `[@user]`: Document propagation rules in `docs/user_guide/audit_pipeline.qmd` — column-presence semantics, one-at-a-time review workflow, reason field as audit trail.

### Export

- [x] **EXPORT-TIERS**: Both global and single graph export were only exporting T1 data — T2 wrangling was a stub (`t2_equals_t1 = True`). Fixed 2026-05-02: both now export `_T1_data.tsv` always, `_T2_data.tsv` when tier2 recipe steps exist, `_T3_data.tsv` when T3 nodes committed.
- [ ] **EXPORT-SGE-2**: Single graph export — include full lineage recipe YAML (T1/T2 assembly + T3 nodes). Design written in `.antigravity/tasks/design_sge_lineage_t3.md`. Pending decision on `!include` resolution in `active_cfg().raw_config`.
- [ ] **EXPORT-SGE-4** `[@user]`: Multi-file upload UX — users may not know how to select multiple files. Consider "Add another file" loop or instructions.
- [ ] **EXPORT-SGE-7**: Dataset-to-plot mapping when multiple source files uploaded — define and document. Linked to SGE-2 design.

### Session / Import

- [ ] **IMPORT-1**: Data Import accordion — upload does not trigger reingestion → transform → new viz. Needs "Apply" button appearing after file selected; triggers full orchestrator pipeline; notifies on completion.

### UX

- [ ] **UX-1**: Plot rendering slow — blocked on BUG-PERF-1.
- [ ] **UX-NOTIF-1**: Toast notifications disappear too fast. Recommended fix: `🔔 Alerts (N)` button in right sidebar → popover with last 20 timestamped notifications. Implementation: `notification_log = reactive.Value([])`, wrap `ui.notification_show()` calls with `_notify_and_log()`, persist to T3 ghost.
- [ ] **THEATER-1**: Collapse/minimize plot panel — ▼/▲ caret in plot card header → 1-line collapsed state. Per-plot, persisted in `home_state`.

---

## 🟡 Deferred / Backlog

### Galery - USER: 

- [ ] Gallery: Re-verify "Clone to Sandbox" after ADR-057 sidebar refactor. Decide how.

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

- [ ] **Taxonomy Data Audit** `[@user]`: Verify/correct tags in `assets/gallery_data/*/recipe_manifest.yaml`.
- [ ] Gallery thumbnails for faster visual scanning.
- [ ] **UX-GALLEXP-1**: Gallery Explorer right sidebar — functionality TBD (currently static help text).
- [ ] **UX-DEVINSP-1**: Test Lab right sidebar + left sidebar redesign — functionality TBD.
- [ ] **UX-CSS-DEMO** `[@user]`: Review `assets/demo/demo_vetinst.css` after default theme finalised.

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
