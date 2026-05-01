# Tasks (SOLE SOURCE OF TRUTH)

**Workspace ID:** SPARMVET_VIZ
**Last Updated:** 2026-05-01 (Phase 25 + demo fixes done; suite 87 passed / 5 skipped / 0 failed) by @dasharch

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
| DEMO-1..4 | Monday demo render/filter bugs — all fixed | 2026-04-30 | commits `55ab1c5` `33afa1b` `b91dfc9` `4c962e6` `8b4f3a4` |
| AUDIT-1 | Allow PK-column filters with warning (ADR-049 amended) | 2026-04-30 | commit `3c6195f` |
| PROP-1 | Per-plot column-presence preview in propagation modal | 2026-04-30 | commit `b4dcd10` |
| UX-5 / UX-3 | Filter row 🗑 icon + right sidebar header bold/yellow | 2026-05-01 | commit `294814e` |
| PERSONA-1b | Persona-name gate doc-drift — resolved by Phase 25-O flag refactor | 2026-05-01 | commit `7344951` |

**Phase 24 commits:** `89bb5ef` `890b609` `f540cbf` `d50197e` `4c38f26` `18dbd46` `f0f7d92` `2393e50` `0b50fbd`
**Phase 25 commits:** `294814e` `9b66656` `72726df` `45591ac` `95b48ac` `dc4464c` `320f6bf`

---

## 🔵 Phase 23: Multi-System Deployment (ADR-048) — PARTIAL

**Completed:** 23-A (deployment profile, bootloader extension), 23-B (connector library — 31 tests).

### Phase 23-C: Galaxy Tool Wrapper Templates
- [ ] Template Galaxy XML wrapper (`tool_amr_pipeline.xml`) — one per pipeline.
- [ ] Bundle profile YAMLs inside Docker image (`/profiles/`).
- [ ] Document Galaxy admin setup steps in `docs/deployment/`.

### Phase 23-D: IRIDA Integration
- [ ] IRIDA plugin/iframe launch mechanism — confirm env var injection method.
- [ ] `IridaConnector.fetch_data()` — download samples, metadata, analysis results via REST API.
- [ ] Document IRIDA admin setup steps in `docs/deployment/`.

### Phase 23-E: Documentation
- [ ] Per-system admin quick-start guides (Galaxy / IRIDA / server / local).

---

## 🟡 Phase 22 — Open Items

- [ ] **22-G-4** `[@verify]`: Manual review of session ghost files in `tmp/UI_TEST/user/_sessions/` — pending user test in live UI.
- [ ] **22-J-10**: Aesthetic propagation (color/shape/fill) — no authoring path exists. Deferred until gallery-clone or wrangling surface supports aesthetic overrides.
- [ ] **22-J-13**: Live-UI verification — see `tasks_test_22J.md`. Currently blocked on AUDIT-2/3 and PROP-4.

---

## 🟡 Active Lineage Build: ST22

- [x] **Lineage 1 (AMR Profile)**: Materialized. Verified Integer Year and Predicted Phenotype.
- [ ] **Lineage 2 (Plasmid Dynamics)**:
    - [ ] Create `2_test_data_ST22_dummy/input_fields/plasmid_data.yaml`
    - [ ] Implement Tier 1 filtering (min identity/overlap for PlasmidFinder)
    - [ ] Assemble with metadata and AMR results; verify via Tier 1 audit artifacts.

---

## 👤 User needs to test

- [ ] Change metadata year to have several years — verify sorting function in the columns.
- [ ] **Phase 21 T1/T2 visual diff**: Does toggling T1↔T2 show a visible difference? Use `MLST_with_metadata` assembly in `1_test_data_ST22_dummy` (has `era` derived column + `year ≥ 2023` filter in T2).
- [ ] Create a manifest with a real T1/T2 transform (e.g. wide → long pivot) to validate that tier switching renders the correct shape change.

---

## 🔴 Open Issues

### Filter / Audit semantics

- [ ] **AUDIT-2**: Filter–audit mapping correctness — UI "exact France" → audit shows "country: any of [France]". Verify `==` vs `in` single-value semantic equivalence in `_params_summary` / `filter_and_audit_handlers.py`.
- [ ] **AUDIT-3**: Filter propagation doesn't reach all plots in some cases. Trace: should propagation walk back to the root data source? Surface a warning when the column is missing in a target plot rather than silently skipping (D9 in ADR-049).
- [ ] **AUDIT-4**: Compare T2/T3 toggle loses state on plot switch. Reactive scoping bug — likely a reactive write on render, see also STATE-2.

### Filter propagation transparency

- [ ] **PROP-2** *(enhancement)*: "Filter inventory" panel — show the effective filter set per plot, with per-filter tooltip listing which plots are affected/skipped.
- [ ] **PROP-3** *(enhancement, large scope)*: Propagation TubeMap — graph visualisation of audit node blast radius, nodes coloured ✅/⚠️/❌. Own design pass + ADR needed before starting.
- [ ] **PROP-4**: Document propagation rules in `docs/user_guide/audit_pipeline.qmd` — column-presence semantics, one-at-a-time review workflow, reason field as audit trail.

### Notifications

- [ ] **UX-NOTIF-1**: Toast notifications disappear too fast. **Recommended: Option A** — `🔔 Alerts (N)` button in right sidebar header → popover with last 20 notifications (timestamped). Implementation: `notification_log = reactive.Value([])`, wrap all `ui.notification_show()` calls with `_notify_and_log()`, persist to T3 ghost.

### Export

- [ ] **EXPORT-2** *(UX)*: Selective export — per-tier checkboxes for T1/T2/T3 data, recipes, filter trace, Quarto report, README. Currently everything bundled unconditionally.
- [ ] **EXPORT-3** *(UX)*: Quarto-rendered HTML report needs design polish — typography, plot placement, methods section, TOC. Quarto template approach preferred.

### Theater / State

- [ ] **THEATER-1** *(UX)*: Collapse/minimize plot panel. ▼/▲ caret in plot card header → 1-line collapsed state. Per-plot, persisted in `home_state`.
- [ ] **STATE-1**: Active plot flickers when toggling T3 mode and when switching panels (Home → Blueprint → Home). Trace `tier_toggle.set()` chains and `home_state.set(...)` writes inside render functions.
- [ ] **STATE-2** (links to AUDIT-4): Compare T2/T3 toggle switches to a different plot. Same reactive-scoping root as STATE-1 — fix together.

### UX / polish

- [ ] **UX-1**: Plot rendering is slow — dependent on BUG-PERF-1.
- [ ] **UX-2**: Data Preview "visible columns" multiselect narrower than panel. Set CSS width to fill the panel on the selectize container.
- [ ] **UX-4**: Rename button label "➜ Audit (N)" → "➜ Send to Audit (N)" for clarity (both center panel and left sidebar).

### Performance

- [ ] **BUG-PERF-1**: `materialize_tier1` fires on every render — `sink_parquet` has no skip-if-exists guard. Fix: consult `SessionManager.status` first; use cached parquet on `fast_path`; only rematerialise on `reassemble` / `new_session`.

---

### VizFactory — Deferred Scale / Geom Fixes
- [x] `scale_x_timedelta` / `scale_y_timedelta` — **DONE** (2026-05-01): worked fine in plotnine 0.15.3; handlers uncommented and smoke-tested (42/42 pass).
- [ ] `geom_map` — still deferred; requires spatial data (GeoDataFrame). Import works in plotnine 0.15.3 but no test data available. Uncomment when spatial manifests are introduced.
- [ ] **21-F-7**: Add `scale_x_discrete` / `scale_y_discrete` to manifests where Year/ST columns are categorical. User-facing manifest edit.


## 🟡 Deferred / Backlog



### Gallery & UI
- [ ] **Taxonomy Data Audit**: Verify/correct tags in `assets/gallery_data/*/recipe_manifest.yaml`.
- [ ] Gallery thumbnails for faster visual scanning.
- [ ] Gallery: Test "Clone to Sandbox" functionality.

### Technical Debt
- [ ] **Unified Materialization**: `debug_wrangler.py` / `debug_assembler.py` — add auto-create of dated `tmp/{date}/{lineage}/` subfolders.
- [ ] **`persona_selector` orphaned handler**: `ingestion_handlers.py:57` listens for `input.persona_selector` which is never rendered. Remove or re-wire if runtime persona switching is re-added.

### Phase 20: Relational Manifest Tooling
- [ ] **Field Gap Analysis tool**: Field name → walk lineage backwards to earliest insertion point.
- [ ] **Forward propagation hint**: Show which output_fields / final_contract files need updating.

### Blueprint Architect — Deferred
- [ ] **TubeMap aesthetics** — tighter rail/tube look; rename 'ref' → 'Add' in nodes and legend.
- [ ] Full Blueprint Architect debug pass (field contracts, lineage rail, Zone C layout).
- [ ] **Action Registry Parity** (18-F): Expose 175+ `@register_action` entries in Blueprint Architect UI.
- [ ] **Visual Forking** (18-F): Select a node → initiate new branch → YAML additions.

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
