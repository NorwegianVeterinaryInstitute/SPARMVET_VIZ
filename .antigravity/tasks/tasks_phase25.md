# Phase 25 — Left Sidebar Restructure: Change Manifests

**ADR:** ADR-052
**Design document:** `EVE_WORK/daily/2026-05-01/persona_functionality_side_bars_v3_clean.csv`
**Refactor protocol:** `.antigravity/knowledge/refactor_protocol_phase24.md` (reused)
**Status:** IMPLEMENTED through 25-L (2026-05-01). Remaining: 25-M (ui_implementation_contract.md rewrite, Opus).

**Commit map (per substep):**

| Step | Commits |
|---|---|
| 25-A | 8f6e41c, a99e126 |
| 25-B | 5ac91a3 |
| 25-C | e792734, 65f48b8, 806a72b |
| 25-D | dff0092 |
| 25-E | b817506, fd6dea2 |
| 25-F | 29bf346 |
| 25-G | a92ae53 |
| 25-H | 4bc1e05 |

---

## Pre-flight (do ONCE before 25-A)

```bash
git tag pre-phase25-$(date +%Y%m%d)
PYTHONPATH=. ./.venv/bin/python -m pytest libs/ app/tests/ -q 2>&1 | tee .antigravity/baselines/phase25_pre.txt
python -c "from app.src.main import app; print('import OK')" >> .antigravity/baselines/phase25_pre.txt
PYTHONPATH=. SPARMVET_PERSONA=qa ./.venv/bin/python -m pytest app/tests/test_shiny_smoke.py -v >> .antigravity/baselines/phase25_pre.txt
```

Verify: 90/90 unit + import clean + 12/12 smoke before any edit.

---

## Model recommendation

| Steps | Recommended model | Reason |
|---|---|---|
| 25-A, 25-B, 25-C | Sonnet | Config, rename, mechanical gate additions, well-defined bug fixes |
| 25-D, 25-E, 25-F | Opus | New reactive components, new accordion panels, PersonaValidator, Quarto integration |
| 25-G, 25-H | Sonnet | Visual fix, smoke test update |

---

## Step ordering (risk-ordered, leaf-to-root)

| Step | Label | Risk | action type |
|---|---|---|---|
| 25-A | Config + renames | Low | CONFIG + RENAME_UI |
| 25-B | Persona template new fields + validator | Low-Med | NEW_FIELD + BUILD_NEW (pure module) |
| 25-C | Persona gating + bug fixes | Med | GATE + FIX_BUG |
| 25-D | Right sidebar layout fix | Med | LAYOUT_FIX |
| 25-E | Left sidebar restructure (move panels) | Med | RESTRUCTURE |
| 25-F | Data Import panel (new build) | High | BUILD_NEW |
| 25-G | Export restructure + Session export | Med-High | RESTRUCTURE + BUILD_NEW |
| 25-H | Single Graph Export | Med | BUILD_NEW |
| 25-I | Visual fixes | Low | VISUAL_FIX |
| 25-J | Smoke test coverage update | Low | TEST |

---

## 25-A — Config + Renames

**Risk:** Low — no logic changes, config and UI label only.

```
CHANGE MANIFEST — Step 25-A
Files touched:
  config/ui/templates/project-independent_template.yaml  — gallery_enabled: false → true
  app/handlers/home_theater.py                           — rename "Dev Studio" nav pill label → "Test Lab"
  EVE_WORK/notes/cheatsheat.md                           — update persona capability matrix row for project-independent
Names being CHANGED: nav pill label only ("Dev Studio" → "Test Lab")
Logic changes: NONE
Config changes: gallery_enabled for project-independent
Risk: Low — no reactive logic touched
```

**Commits:**
- Commit A1 `config: gallery for project-independent + Test Lab rename`
- Commit A2 `docs: update cheatsheet persona matrix`

---

## 25-B — Persona Template New Fields + PersonaValidator

**Risk:** Low-Med — new pure module (no Shiny), new YAML fields, no existing logic touched.

```
CHANGE MANIFEST — Step 25-B
New file: app/modules/persona_validator.py
  — PersonaValidator class
  — validate(template: dict, template_path: str) -> list[str] (returns error strings)
  — Rules: manifest_selector.visible=false → fixed_manifest must be non-null existing path
  — Rules: persona_id must match filename
  — Rules: all known flags present (warn on missing, use defaults)
Files modified:
  config/ui/templates/pipeline-static_template.yaml         — add manifest_selector + testing_mode sections
  config/ui/templates/pipeline-exploration-simple_template.yaml — same
  config/ui/templates/pipeline-exploration-advanced_template.yaml — same
  config/ui/templates/project-independent_template.yaml      — same
  config/ui/templates/developer_template.yaml                — same
  config/ui/templates/qa_template.yaml                       — same
  app/src/server.py                                          — call PersonaValidator before define_server()
New tests: app/tests/test_persona_validator.py
Risk: Low — pure module, no Shiny, no reactive changes
```

**New YAML fields per template:**
```yaml
# pipeline-static, pipeline-exploration-simple:
manifest_selector:
  visible: false
  fixed_manifest: null  # operator MUST fill this for their deployment

testing_mode: false

# All others:
manifest_selector:
  visible: true
  fixed_manifest: null

testing_mode: true
```

**Commits:**
- Commit B1 `feat(25-B): PersonaValidator module + template new fields`
- Commit B2 `test: persona_validator unit tests`

---

## 25-C — Persona Gating + Bug Fixes

**Risk:** Med — modifying existing reactive handlers. Run full gate after each sub-commit.

```
CHANGE MANIFEST — Step 25-C
Files touched:
  app/handlers/filter_and_audit_handlers.py
    — sidebar_filters: add interactivity_enabled gate + static message for pipeline-static + disclaimer for simple
    — filter_controls_ui: hide Apply/Audit + Reset buttons when interactivity_enabled=false
    — filter_rows_ui: hide Remove row button when interactivity_enabled=false
  app/handlers/export_handlers.py
    — system_tools_ui: add bootloader.is_enabled('export_bundle_enabled') gate
  app/handlers/session_handlers.py
    — session_management_ui: replace hardcoded advanced_personas set with
      bootloader.is_enabled('session_management_enabled')  [PERSONA-1 fix]
  app/handlers/home_theater.py
    — sidebar_nav_ui: fix Gallery always-visible bug (gallery_enabled gate was broken)
    — right_sidebar_content_ui comparison toggle: add bootloader.is_enabled('comparison_mode_enabled')
      instead of hardcoded persona name check
Bug IDs fixed: PERSONA-1, GALLERY-BUG
Risk: Med — reactive gate changes; run smoke suite after each sub-commit
```

**Commits:**
- Commit C1 `fix(25-C): interactivity_enabled gate on filter form + buttons`
- Commit C2 `fix(25-C): export_bundle_enabled gate + PERSONA-1 session fix + Gallery bug`
- Commit C3 `fix(25-C): comparison_mode_enabled flag gate (replaces hardcoded set)`

---

## 25-D — Right Sidebar Layout Fix

**Risk:** Med — structural layout change in ui.py; verify center column expands for pipeline personas.

```
CHANGE MANIFEST — Step 25-D
File touched: app/src/ui.py
  — Read os.getenv("SPARMVET_PERSONA", "developer") at layout build time
  — If persona ∈ {"pipeline-static", "pipeline-exploration-simple"}:
      omit ui.sidebar(position="right") from ui.layout_sidebar(...)
  — Else: include as before
Bug ID fixed: LAYOUT-BUG
Risk: Med — structural; confirm with smoke test run under SPARMVET_PERSONA=pipeline-static
```

**Commits:**
- Commit D1 `fix(25-D): exclude right sidebar from layout for pipeline personas`

**Extra verification:** Run smoke with `SPARMVET_PERSONA=pipeline-static` and confirm center column fills width.

---

## 25-E — Left Sidebar Accordion Restructure (move panels)

**Risk:** Med — moves existing UI slots between accordion panels, no new reactive logic.

```
CHANGE MANIFEST — Step 25-E
Files touched:
  app/handlers/home_theater.py (sidebar_tools_ui)
    — Rename "Project Navigator" accordion panel → "Manifest Choice"
    — Split "System Tools" accordion into three panels:
        "Global Project Export" (was Export Bundle sub-section)
        "Session Management"    (was System Tools — Session sub-section)
    — Move Data Ingestion slots OUT of sidebar_tools_ui
      (they will be in Data Import panel — Step 25-F)
  app/handlers/export_handlers.py (system_tools_ui)
    — Remove Session Management slot (now in session_handlers)
    — Remove Data Ingestion slots (moving to Data Import)
    — Rename panel label + bundle name field + quality selector labels
    — Add plot format selector (PNG/SVG/PDF radio)
Names being MOVED: session_management_ui output slot, data ingestion slots
Names being KEPT: export_bundle_download, export_audit_report_ui, system_tools_ui (renamed)
Risk: Med — accordion restructure; smoke suite verifies sidebar renders
```

**Commits:**
- Commit E1 `refactor(25-E): split System Tools into Global Project Export + Session Management panels`
- Commit E2 `refactor(25-E): move data ingestion slots out of system_tools_ui`

---

## 25-F — Data Import Panel (New Build)

**Risk:** High — new accordion panel with conditional rendering based on testing_mode + persona.

```
CHANGE MANIFEST — Step 25-F
New output: data_import_ui (in home_theater.py or new data_import_handlers.py)
  — For pipeline-static + pipeline-exploration-simple (testing_mode=false, production):
      SHOW(RO): read-only display of configured/injected data path(s)
  — For exploration personas (testing_mode=true by default):
      Active file/directory selector pre-filled from manifest default data paths
      User can override (to test with different data)
  — Metadata TSV replacement slot (gate: metadata_ingestion_enabled)
  — Multi-file/Excel ingestion slot (gate: data_ingestion_enabled)
      Requires data-type-to-manifest mapping UI
  Add to sidebar_tools_ui accordion: new "Data Import" panel calling output_ui("data_import_ui")
Risk: High — new reactive component; new bootloader API needed to read manifest default data paths
Pre-condition: PersonaValidator (25-B) must be in place
```

**Commits:**
- Commit F1 `feat(25-F): data_import_ui shell + read-only display for pipeline personas`
- Commit F2 `feat(25-F): active data selector for exploration personas + testing_mode awareness`
- Commit F3 `feat(25-F): metadata + multi-file ingestion slots with gate`

---

## 25-G — Export Restructure + Session Export

**Risk:** Med-High — Quarto server-side render is new; session export is new download handler.

```
CHANGE MANIFEST — Step 25-G
Files touched:
  app/handlers/export_handlers.py
    — Consolidate export_audit_report_ui: replace two buttons with format selector
      (HTML / PDF / DOCX) + single "Export Audit Report" button
    — Add server-side Quarto render call for HTML/PDF/DOCX
    — Add export_audit_docx_quarto download handler
  app/handlers/session_handlers.py
    — Add session_export_download handler: zips _sessions/{session_key}/ → bytes
    — Add "Export Session (.zip)" download button to session_management_ui
Risk: Med-High — Quarto subprocess call is new; test with all three formats
```

**Commits:**
- Commit G1 `feat(25-G): consolidated audit report format selector + Quarto render`
- Commit G2 `feat(25-G): session export (.zip) download button + handler`

---

## 25-H — Single Graph Export

**Risk:** Med — new download handler, gated by export_graph_enabled.

```
CHANGE MANIFEST — Step 25-H
New output: single_graph_export_ui (in export_handlers.py or new handler)
  — Plot format selector (PNG/SVG/PDF)
  — "Export Active Graph" download button
  — Download produces: plot file + active plot's data slice (T3-filtered) +
    relevant manifest section + committed T3 nodes for this plot
  — Gate: bootloader.is_enabled('export_graph_enabled')
  Add to sidebar_tools_ui accordion: new "Single Graph Export" panel
Risk: Med — new download handler; reuses existing viz_factory.render() call
```

**Commits:**
- Commit H1 `feat(25-H): Single Graph Export panel + download handler`

---

## 25-I — Visual Fixes

**Risk:** Low — CSS/label changes only.

```
CHANGE MANIFEST — Step 25-I
Files touched:
  app/handlers/filter_and_audit_handlers.py
    — Replace ✕ with 🗑 on filter row remove button
  app/handlers/home_theater.py (or audit stack renderer)
    — Right sidebar active plot header: add fw-bold + style="background:#fffde7;"
    — Add 4-6px bottom margin before first audit node
Risk: Low — visual only, no reactive logic
```

**Commits:**
- Commit I1 `style(25-I): filter row trash icon + right sidebar header styling`

---

## 25-J — Smoke Test Coverage Update

**Risk:** Low — new test selectors for new sidebar panels.

```
CHANGE MANIFEST — Step 25-J
File touched: app/tests/test_shiny_smoke.py
  — Add selectors for new panels: #nav_accordion, "Manifest Choice", "Data Import",
    "Global Project Export", "Session Management"
  — Add test: data_import_panel_visible_for_exploration_personas
  — Add test: manifest_choice_hidden_for_pipeline_static
  — Update existing sidebar selectors if IDs changed in 25-E
Risk: Low — test additions only
```

**Commits:**
- Commit J1 `test(25-J): smoke coverage for Phase 25 new sidebar panels`

---

## 25-K — ADR-052 Follow-ups (audit_report_enabled + Quarto-only)

**Risk:** Low — adds one feature flag and replaces Pandoc fallback with native Quarto.
**Status:** IMPLEMENTED 2026-05-01 (commit `5f4c491`).

```
CHANGE MANIFEST — Step 25-K
Files touched:
  config/ui/templates/*.yaml (×6)             — add audit_report_enabled flag
  app/handlers/export_handlers.py             — bootloader.is_enabled gate;
                                                 Quarto-only download handler
  app/modules/exporter.py                     — render_audit_report(fmt=...)
                                                 calls quarto render --to <fmt>;
                                                 pandoc_convert + pandoc_available
                                                 helpers removed
Bug IDs fixed: ADR-052-FOLLOWUP-1, ADR-052-FOLLOWUP-2
Risk: Low — replaces an already-failing path; qa now sees the audit panel
```

---

## 25-L — PersonaManager Dependency-Cascade Enforcement

**Risk:** Med — touches the bootloader path that every gate consults.
**Recommended model:** Sonnet, no extended thinking.

```
CHANGE MANIFEST — Step 25-L
Files touched:
  app/src/bootloader.py
    — _load_persona_config: after reading the YAML, apply the dependency
      cascade documented in rules_persona_feature_flags.md §107–127:
        if interactivity_enabled is False:
            comparison_mode_enabled = False
            session_management_enabled = False
            export_graph_enabled = False
            audit_report_enabled = False
        if import_helper_enabled is False:
            data_ingestion_enabled = False
        deployment-profile override: data_ingestion_enabled may be force-False
      Log a WARNING for each flag that was set True in the template and is
      forced False by the cascade.
  app/modules/persona_validator.py
    — Add a Rule 5: warn when a child flag is True but its master gate is False
      (PersonaValidator catches the same family of misconfigurations at startup).
  app/tests/test_persona_validator.py
    — Add unit tests for the cascade rule: each forced override and warning.
  .agents/rules/rules_persona_feature_flags.md
    — Tighten §107–127 prose so it reflects the actual implementation
      (currently it's a forward-looking spec).
Bug IDs fixed: PERSONA-CASCADE-1
Risk: Med — every is_enabled call sees the cascade; full smoke after each
       sub-commit.
```

**Commits (planned):**
- Commit L1 `feat(25-L): bootloader dependency-cascade for persona flags`
- Commit L2 `test(25-L): PersonaValidator rule 5 + bootloader cascade tests`

---

## 25-M — `ui_implementation_contract.md` Rewrite

**Risk:** Low (docs only) — but high cognitive load; needs careful side-by-side review.
**Recommended model:** Opus, MEDIUM effort.
**Trigger:** After 25-I + 25-J close (let smoke contract stabilise first), or
sooner if the design drifts further from the contract during 25-L.

```
CHANGE MANIFEST — Step 25-M
File touched: .agents/rules/ui_implementation_contract.md
Sections to rewrite (current vs Phase 25):
  §7.1  Session Save / Import — point at Session Management panel; document
        the header-level Export Active Session (.zip) button and the
        per-session Restore + Delete (per-session Export removed in 25-G).
  §7.2  Export Results Bundle — keep core flow; relocate to Global Project
        Export panel; document plot_format selector (PNG/SVG/PDF).
  §7.3  Export Active Graph — un-defer (now Phase 25-H); document the .zip
        bundle (plot + data + manifest fragment + t3_recipe.json + README).
  §9    Metadata Ingestion — relocate to Data Import panel; gate stays
        metadata_ingestion_enabled.
  §10   Data Ingestion + Excel Converter — relocate to Data Import panel;
        gate stays data_ingestion_enabled (multi-file uploader).
  §11   Panel → sidebar content map — replace with Phase 25-E accordion
        structure (Manifest Choice / Data Import / Filters / Global Project
        Export / Single Graph Export / Session Management).
  §12f  Audit Report — single format selector + one button (HTML/PDF/DOCX),
        Quarto-only render (no Pandoc).
  §15.5 Persona-name underscore form (pipeline_exploration_advanced) →
        hyphen form everywhere.
  Cross-refs — replace all "System Tools", "Project Navigator", "Dev Studio"
        terminology with current panel and nav-pill names.
Risk: Low — documentation only; no code touched.
```

**Commits (planned):**
- Commit M1 `docs(25-M): align ui_implementation_contract.md with Phase 25 architecture`

---

## Verification gate (identical to Phase 24 — run after EVERY commit)

```bash
# 1. Core unit tests
PYTHONPATH=. ./.venv/bin/python -m pytest app/tests/test_filter_operators.py libs/connector/tests/ libs/viz_factory/tests/test_deco2_components.py -q

# 2. App import
python -c "from app.src.main import app; print('OK')"

# 3. Playwright smoke (qa persona)
PYTHONPATH=. SPARMVET_PERSONA=qa ./.venv/bin/python -m pytest app/tests/test_shiny_smoke.py -v

# 4. For pipeline-persona layout fix (25-D): additional run
PYTHONPATH=. SPARMVET_PERSONA=pipeline-static ./.venv/bin/python -m pytest app/tests/test_shiny_smoke.py -v
```

## Halt-and-ask conditions (same as Phase 24)

- Any gate fails twice on same step → stop, post blocker report
- New reactive.Value needed that isn't in define_server's current surface
- Quarto subprocess integration breaks import clean → stop
- LoC delta > 5% between moved code and source deletions
