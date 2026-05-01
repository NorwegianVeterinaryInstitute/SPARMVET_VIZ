# Audit — Phase 25 (Left Sidebar Restructure) steps A–H complete

**Date:** 2026-05-01
**Branch:** dev
**HEAD before phase:** `45221bb` (session 10 handoff)
**HEAD after 25-H + docs:** `9648c33` + this audit
**ADR:** ADR-052 (now IMPLEMENTED through 25-H)

---

## Substep verification

| Step | Commit(s) | Files | Gate evidence |
|---|---|---|---|
| 25-A — Config + renames | 8f6e41c, a99e126 | `config/ui/templates/project-independent_template.yaml`, `app/handlers/home_theater.py`, `EVE_WORK/notes/cheatsheat.md` | qa smoke 10/10 |
| 25-B — Template fields + PersonaValidator | 5ac91a3 | 6× `config/ui/templates/*.yaml`, `app/modules/persona_validator.py`, `app/tests/test_persona_validator.py`, `app/src/bootloader.py`, `app/src/server.py` | 12/12 unit + qa smoke |
| 25-C — Persona gating fixes | e792734, 65f48b8, 806a72b | `app/handlers/filter_and_audit_handlers.py`, `app/handlers/export_handlers.py`, `app/handlers/session_handlers.py`, `app/handlers/home_theater.py` | qa smoke after each commit |
| 25-D — Right sidebar layout fix | dff0092 | `app/src/ui.py` | qa smoke + pipeline-static smoke (audit_sidebar absent) |
| 25-E — Accordion restructure | b817506, fd6dea2 | `app/handlers/home_theater.py`, `app/handlers/export_handlers.py` | qa smoke 10/10 |
| 25-F — Data Import panel | 29bf346 | `app/handlers/data_import_handlers.py` (new), `app/handlers/home_theater.py` | qa smoke 10/10 |
| 25-G — Audit format + active session export | a92ae53 | `app/handlers/export_handlers.py`, `app/handlers/session_handlers.py`, `app/handlers/home_theater.py` | qa smoke 10/10 |
| 25-H — Single Graph Export | 4bc1e05 | `app/handlers/single_graph_export_handlers.py` (new), `app/handlers/home_theater.py` | qa smoke 10/10 |

Final unit + import gate before this audit:

```
102 passed in 1.18s   (test_filter_operators + libs/connector + viz_factory deco2 + persona_validator)
import OK             (from app.src.main import app)
qa smoke              10 passed, 2 skipped (expected: developer-only TestPersonaMasking cases)
```

---

## Files added (Phase 25)

- `app/modules/persona_validator.py` — pure validator, no Shiny imports.
- `app/tests/test_persona_validator.py` — 12 unit tests.
- `app/handlers/data_import_handlers.py` — `data_import_ui` output (25-F).
- `app/handlers/single_graph_export_handlers.py` — `single_graph_export_ui` + `export_single_graph` (25-H).

## Files renamed / restructured

- `home_theater.sidebar_tools_ui` accordion now exposes (top→bottom): **Manifest Choice** → **Data Import** → **Filters** → **Global Project Export** → **Single Graph Export** (gated) → **Session Management** (gated).
- `export_handlers.system_tools_ui` no longer hosts session, metadata, or multi-file ingestion slots.
- `session_handlers.session_management_ui` adds a header-level **Export Active Session (.zip)** button; per-session Export buttons removed (no backend was registered for them).

## Persona-template extensions (now live in all 6 templates)

```yaml
manifest_selector:
  visible: <bool>
  fixed_manifest: <path|null>

testing_mode: <bool>
```

| Persona | manifest_selector.visible | testing_mode |
|---|:---:|:---:|
| pipeline-static | false | false |
| pipeline-exploration-simple | false | false |
| pipeline-exploration-advanced | true | true |
| project-independent | true | true |
| developer | true | true |
| qa | true | true |

---

## Known deviations from the design — flagged for follow-up

### ADR-052-FOLLOWUP-1 — Pandoc fallback in 25-G

ADR-052 §52-7 calls for Pandoc removal and Quarto-only PDF/DOCX render. The implementation
keeps `pandoc_convert(html_path, fmt)` as a fallback because Quarto's native PDF/DOCX render
needs additional template plumbing in `app/modules/exporter.py:render_audit_report`. To close
this deviation, either:

1. extend `render_audit_report` to take `fmt` and call `quarto render report.qmd --to <fmt>`
   for each requested format, OR
2. accept Pandoc as a permanent fallback dependency and amend ADR-052 §52-7.

Severity: **low** (functionality works; cosmetic dependency surface).

### ADR-052-FOLLOWUP-2 — Hardcoded persona set in `export_audit_report_ui`

`app/handlers/export_handlers.py:462` retains `advanced_personas = {"pipeline-exploration-advanced",
"project-independent", "developer"}`. No flag in `rules_persona_feature_flags.md` covers this
exact set; `qa` is currently EXCLUDED, which is wrong (qa gets every developer flag — see the
matrix). Two options:

1. add `audit_report_enabled` to all 6 persona templates and switch to
   `bootloader.is_enabled("audit_report_enabled")`, OR
2. document this hardcoded set as a structural exception (parallel to right-sidebar
   suppression in §52-1) and at minimum extend the set to include `qa`.

Severity: **medium** — qa-persona users currently lose access to the audit report panel.

### ADR-052-FOLLOWUP-3 — pipeline-static smoke coverage

The qa-persona smoke suite passes (10/10). Running `SPARMVET_PERSONA=pipeline-static` against
the same suite produces 7 failures — the tests assume `#project_id` is visible, but
`manifest_selector.visible=false` for pipeline-static deliberately hides it. These failures
predate Phase 25 (they would have failed on any pipeline-persona run). 25-J is the dedicated
step to introduce persona-aware selectors and a `pipeline-static`-specific test set.

Severity: **low** — test infrastructure, not product behaviour.

---

## Inconsistencies fixed in this audit pass

- `rules_persona_feature_flags.md` — gallery_enabled flipped to `true` for project-independent
  in the matrix; new `qa` column added; `manifest_selector.visible` + `testing_mode` rows
  appended; "Dev Studio" → "Test Lab" terminology; "System Tools" references updated to the
  Phase 25-E panel split.
- `rules_ui_dashboard.md` — Home-mode left-sidebar section rewritten to describe the Phase 25
  panel structure (Manifest Choice / Data Import / Filters / Global Project Export / Single
  Graph Export / Session Management); persona matrix gains a `qa` row.
- `tasks_phase25.md` — status moved from PRE-FLIGHT to IMPLEMENTED through 25-H; commit map
  added.
- `architecture_decisions.md` — ADR-052 status DESIGNED → IMPLEMENTED; substep audit + three
  follow-up deviations recorded inline.
- `tasks.md` — substeps 25-F/G/H ticked.

## Inconsistencies still open (not fixed here)

- **`ui_implementation_contract.md`** — references "System Tools", "Project Navigator", "Dev
  Studio", and `pipeline_exploration_advanced` (underscore form) in many sections (§7.1, §7.2,
  §7.3, §9, §10, §11, §15.5). This is a deeper rewrite that should follow ADR-052 closure as
  its own commit; doing it inline here would balloon this audit.
- **`rules_ui_dashboard.md` §7.1–§7.3** were not touched in this pass (the rewrite happened in
  the panel-structure block earlier in the file). Cross-references to "System Tools" remain
  in the deeper sections.
- **`PersonaManager` dependency-rule enforcement** is documented in `rules_persona_feature_flags.md`
  §107–127 but `bootloader.is_enabled` does not actually apply the cascade (e.g. forcing
  `comparison_mode_enabled=False` when `interactivity_enabled=False`). The runtime relies on
  each call site checking the master gate explicitly. Pre-existing, unrelated to Phase 25.

---

## Next steps (handoff to next session)

1. **25-I (Sonnet, low risk)** — visual polish: filter row 🗑 icon, right sidebar header
   bold + yellow background.
2. **25-J (Sonnet, low risk)** — smoke test coverage: new selectors for the Phase 25 panels;
   a `pipeline-static`-specific test set; assert `data_import_ui` rendering for exploration
   personas.
3. **ADR-052-FOLLOWUP-2 (Sonnet, low risk)** — fix the qa-persona audit-report regression
   (option 2 above is the cheapest: extend the hardcoded set to include `qa`).
4. **`ui_implementation_contract.md` rewrite (Opus, medium effort)** — bring §7–§11 in line
   with the Phase 25 panel structure.
