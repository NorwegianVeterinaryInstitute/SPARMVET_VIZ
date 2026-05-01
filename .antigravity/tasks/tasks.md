# Tasks (SOLE SOURCE OF TRUTH)

**Workspace ID:** SPARMVET_VIZ
**Last Updated:** 2026-05-01 (Phase 25 fully done; suite 87 passed / 5 skipped / 0 failed) by @dasharch

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
| Doc/Hygiene H-1..4, DOC-1..3, BUG-1, ARCH-1 | Cross-ref fixes, ADR updates, dep graph fix, Phase 24 design | 2026-04-30 | [tasks_archive_phase24.md](archives/tasks_archive_phase24.md) |

**Commit anchors (Phase 24):** `89bb5ef`, `890b609`, `f540cbf`, `d50197e`, `4c38f26`, `18dbd46`, `f0f7d92`, `2393e50`, `0b50fbd`
**Commit anchors (Phase 25):** `294814e`, `9b66656`, `72726df`, `45591ac`, `95b48ac`, `dc4464c`, `320f6bf`

---

## 🔵 Phase 23: Multi-System Deployment Architecture (ADR-048) — PARTIAL

**Completed:** 23-A (deployment profile, bootloader extension), 23-B (connector library — 31 tests).
**ADR:** ADR-048. **Design doc:** `docs/deployment/deployment_guide.qmd`.

### Phase 23-C: Galaxy Tool Wrapper Templates
- [ ] Template Galaxy XML wrapper (`tool_amr_pipeline.xml`) — one per pipeline.
- [ ] Bundle profile YAMLs inside Docker image (`/profiles/`).
- [ ] Document Galaxy admin setup steps in `docs/deployment/`.

### Phase 23-D: IRIDA Integration
- [ ] IRIDA plugin/iframe launch mechanism — confirm env var injection method.
- [ ] `IridaConnector.fetch_data()` — download samples, metadata, analysis results via REST API.
- [ ] Optional: result POST-back to IRIDA project.
- [ ] Document IRIDA admin setup steps in `docs/deployment/`.

### Phase 23-E: Documentation
- [ ] Per-system admin quick-start guides (Galaxy / IRIDA / server / local).

---

## 🟡 Phase 22 — Open Items

### 22-G-4: Session ghost manual verification
- [ ] [@verify] Manual review of session ghost files in `tmp/UI_TEST/user/_sessions/` — pending user test in live UI.

### 22-J: Open / Deferred
- [ ] **22-J-10**: Aesthetic propagation (color/shape/fill) — no aesthetic authoring path exists today. Deferred until gallery-clone or wrangling surface supports aesthetic overrides.
- [ ] **22-J-13**: Live-UI verification by user — see `.antigravity/tasks/tasks_test_22J.md` checklist. Blocked on AUDIT-1 (ADR-049 amendment), DEMO-3, DEMO-4.

---

## 🟡 Active Lineage Build: ST22 Sequential Development

> **Convention:** All debug outputs routed to `tmp/YYYY-MM-DD/<lineage_id>/`. Bioscientist persona governs YAML; @dasharch governs Python.

- [x] **Lineage 1 (AMR Profile)**: Materialized (T1/T2/Plots). Verified Integer Year and Predicted Phenotype.
- [ ] **Lineage 2 (Plasmid Dynamics)**:
    - [ ] Create `2_test_data_ST22_dummy/input_fields/plasmid_data.yaml`
    - [ ] Implement Tier 1 filtering (e.g., min identity/overlap for PlasmidFinder)
    - [ ] Assemble with metadata and AMR results.
    - [ ] Verify via Tier 1 audit artifacts.

---

# User needs to test

- [ ] Change metadata year to have several years — verify sorting function in the columns.

---

## 🔴 Open Bugs (2026-04-30 live-UI test)

*Source: `EVE_WORK/daily/2026-04-30/UI_user_test.md`. Items prefixed **DEMO** are blockers for the Monday demo (2026-05-04).*

### CRITICAL (Monday demo blockers)

- [ ] **DEMO-1**: `1_test_data_ST22_dummy` — Virulence Variants plot fails: `Render error: 'rotation'`. Likely an unrecognised layer/aesthetic kwarg.
- [ ] **DEMO-2**: `1_test_data_ST22_dummy` — Assembly quality dotplot fails: `Render error: Aesthetic x references unknown column metric`. Wrong `target_dataset` or column lost in assembly.
- [ ] **DEMO-3**: Filter on numeric/float column fails — `cannot compare string with numeric type f64`. Filter UI sends string operands; engine doesn't cast. Fix in filter operand coercion path.
- [ ] **DEMO-4**: Year filter on MLST bar plot fails — string vs numeric ambiguity. Decide: keep years as categorical strings + restrict UI ops to `eq`/`in`, OR cast to int. Same root family as DEMO-3.

### Filter / Audit semantics — ADR amendment needed

- [ ] **AUDIT-1 (ADR-049 amendment)**: Re-decision on PK-column filter behaviour. Current: silent convert to `exclusion_row`. Proposed: ALLOW filter on PK column with a non-blocking warning; keep DROP blocked. Amend ADR-049 first, then implement. Unblocks 22-J test §3, 4, 5.
- [ ] **AUDIT-2**: Filter–audit mapping correctness — UI "exact France" → audit shows "country: any of [France]". Verify `==` vs `in` single-value semantic equivalence.
- [ ] **AUDIT-3**: Filter propagation doesn't dispatch to all plots. Design question: trace back to root data source? Surface warning when column missing rather than silent skip. Touches ADR-049 §propagation.
- [ ] **AUDIT-4**: Compare T2/T3 toggle loses state on plot switch. Reactive scoping bug (links to STATE-2).

### Filter propagation transparency

- [ ] **PROP-1** *(CRITICAL for safe usage)*: In the propagation modal, list per-target plot whether the column **exists**: ✅ present / ⚠️ absent (silent skip) / ❌ type mismatch. Show "This filter will apply to N of M selected plots." Wording note: encourage one-at-a-time verify workflow.
- [ ] **PROP-4**: Document propagation rules in `docs/user_guide/audit_pipeline.qmd` — column-presence semantics, one-at-a-time review workflow, reason field as audit trail. Include screenshots after PROP-1.
- [ ] **PROP-2** *(enhancement)*: "Filter inventory" summary panel — effective filter set per plot with per-filter tooltip listing applied/skipped plots.
- [ ] **PROP-3** *(enhancement, exploratory)*: Propagation TubeMap — small graph visualisation showing blast radius of an audit node. Nodes coloured ✅/⚠️/❌. Reuses Blueprint Architect TubeMap aesthetic. Significant scope — own design pass + ADR needed.

### Notification persistence

- [ ] **UX-NOTIF-1**: Toast notifications disappear too fast. **Recommended: Option A** — `🔔 Alerts (N)` button in right sidebar header, click → popover with last 20 notifications (timestamped). Badge for unread. Implementation sketch: `notification_log = reactive.Value([])`, all `ui.notification_show()` calls also append via `_notify_and_log()` wrapper; persists to T3 ghost.

### Persona feature-flag wiring

- [ ] **PERSONA-1b** (doc-drift, decision needed post-demo): Three sources disagree on Comparison Mode + Session Mgmt visibility for `pipeline-exploration-simple`. Current code keeps persona-name gates with `# TODO PERSONA-1` comments. Decision: pick the truth (likely persona matrix is right — simple has no T3 authoring, so comparison is N/A), update template OR matrix, then refactor to flag-based.

### Export

- [ ] **EXPORT-2** *(UX)*: Selective export — checkboxes for T1/T2/T3 data tiers, recipes, filter trace, Quarto report, README. Currently everything bundled unconditionally.
- [ ] **EXPORT-3** *(UX)*: Exported HTML report (Quarto-rendered) needs design polish — typography, plot placement, methods section, TOC, navigation. Quarto template approach preferred.

### Theater — layout

- [ ] **THEATER-1** *(UX)*: Collapse/minimize plot panel. ▼/▲ caret in each plot card header → toggles to 1-line collapsed state. Per-plot, persisted in `home_state`. Bonus: "collapse all / expand all" at group level.

### Plot-data state preservation

- [ ] **STATE-1**: Active plot data flickers when toggling T3 mode on/off and when switching panels (Home → Blueprint → Home). Tier toggle should not change which plot is active. Trace `tier_toggle.set()` chains and `home_state.set({**state, "active_plot_subtab": ...})` writes inside render functions.
- [ ] **STATE-2** (links to AUDIT-4): Compare T2/T3 toggle doesn't hold — clicking it switches to a different plot. Same reactive-scoping bug as STATE-1. Fix together.

### UX / polish

- [ ] **UX-1**: Plot rendering feels slow — see BUG-PERF-1 below.
- [ ] **UX-2**: Data Preview — "visible columns" multiselect narrower than panel; set CSS width to fill.
- [ ] **UX-4**: Rename "Audit" button → "Send to Audit" (both center panel and left sidebar).
- [ ] **UX-5**: Homogenise delete UI — Pipeline Audit uses 🗑; left-panel filter rows use ✕. Switch filter rows to 🗑.

### Performance

- [ ] **BUG-PERF-1**: `materialize_tier1` fires on every project switch and render — `sink_parquet` has no skip-if-exists guard. Fix: home theater render path consults SessionManager first; if status is `fast_path`, use cached parquet; only call `materialize_tier1` on `reassemble` / `new_session`.

---

## 🟡 Deferred / Backlog

### Phase 18 Deferred Items
- [ ] **Branch selector** (18-B/18-F): Lineage Rail stops at assembly level for one-assembly → N-plots divergence.
- [ ] **Action Registry Parity** (18-F): Expose 175+ `@register_action` entries in Blueprint Architect UI.
- [ ] **Visual Forking** (18-F): Select a node → initiate new branch → YAML additions.

### Phase 20: Relational Manifest Tooling
- [ ] **Field Gap Analysis tool**: Field name → walk lineage backwards to earliest insertion point.
- [ ] **Forward propagation hint**: Show which output_fields / final_contract files need updating.

### Deferred VizFactory / Scale Fixes
- [ ] Retest & fix `scale_x_timedelta`, `scale_y_timedelta` (dtype mismatch). *(decorators commented out in scales/core.py)*
- [ ] Retest & fix `geom_map` (requires spatial data). *(decorator commented out in geoms/core.py)*

### Blueprint Architect — Deferred Aesthetics & Debug
- [ ] **"Data: …" display** — top-left of analysis theater header; review display format.
- [ ] **TubeMap aesthetics** — tighter rail/tube look; rename 'ref' → 'Add' in nodes and legend.
- [ ] Full Blueprint Architect aesthetic/functional debug pass (field contracts, lineage rail, Zone C layout).

### Gallery & UI
- [ ] **Taxonomy Data Audit**: Verify/correct tags in `assets/gallery_data/*/recipe_manifest.yaml`.
- [ ] Gallery thumbnails for faster visual scanning.
- [ ] Gallery: Test "Clone to Sandbox" functionality.

### Technical Debt
- [ ] **Unified Materialization**: Standardize `debug_wrangler.py` / `debug_assembler.py` to auto-create dated `tmp/{date}/{lineage}/` subfolders.
- [ ] **Renaming Precision Audit**: Scan existing manifests for generic `phenotype` / `source` columns; refactor to descriptive equivalents.
- [ ] Workspace hygiene: remove temporary tests from `tmp/` and dispose of unique scripts.
- [ ] **`persona_selector` orphaned handler**: `ingestion_handlers.py:57` listens for `input.persona_selector` which is never rendered. Remove or re-wire if runtime persona switching is ever re-added.

### Phase 21 Deferred
- [ ] **21-F-7**: Add `scale_x_discrete` / `scale_y_discrete` to manifests where Year/ST columns should be treated as categorical. User updates manifests directly.
- [ ] **Phase 21 T2/T3 visual diff**: Full tier-switch user-testing deferred — no manifest with proper T2/T3 assembly available for ST22. Mechanism is wired; test when ST22 Lineage 2 is materialized.

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
