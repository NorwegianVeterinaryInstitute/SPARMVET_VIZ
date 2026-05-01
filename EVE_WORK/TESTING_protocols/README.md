# SPARMVET_VIZ — Manual Testing Protocols

## How to use

Each CSV is a standalone test template for one module or concern.
For each test session, copy the file to `EVE_WORK/daily/<date>/` and fill in
the `pass`, `observed`, and `tester_notes` columns as you go.

## Files

| File | What it covers |
|---|---|
| `protocol_01_persona_masking.csv` | Left sidebar + right sidebar visibility per persona — run after any UI gating change |
| `protocol_02_home_filters.csv` | Filter pipeline: add row / apply / reset / operator types / dtype handling |
| `protocol_03_audit_pipeline.csv` | T3 audit: per-plot scoping, propagation modal, drop-column, linked-id delete |
| `protocol_04_export.csv` | Export bundle, audit report (HTML/PDF/DOCX), session import/export |
| `protocol_05_blueprint_architect.csv` | Blueprint Architect mode: manifest selector, TubeMap, live plot/table preview |
| `protocol_06_gallery.csv` | Gallery mode: search/filter, asset rendering, YAML transplant to sandbox |
| `protocol_07_data_assembly.csv` | Project load, data assembly, cache invalidation (manifest change / data change) |

## Columns

| Column | Who fills it | Values |
|---|---|---|
| `test_id` | pre-filled | e.g. P01-003 |
| `module` | pre-filled | Home / Gallery / Blueprint / Export / Assembly |
| `section` | pre-filled | logical group within module |
| `scenario` | pre-filled | short name |
| `persona_required` | pre-filled | which persona(s) to use |
| `precondition` | pre-filled | what must be set up first |
| `action` | pre-filled | what to do |
| `expected_result` | pre-filled | what should happen |
| `pass` | **TESTER** | Y / N / SKIP |
| `observed` | **TESTER** | brief description of what actually happened |
| `date` | **TESTER** | YYYY-MM-DD |
| `tester_notes` | **TESTER** | bugs, questions, follow-ups |

## Severity convention (use in tester_notes)

- `[BLOCKER]` — app crash or data loss
- `[BUG]` — wrong behaviour, reproducible
- `[VISUAL]` — cosmetic only
- `[QUESTION]` — unclear spec, needs design decision
- `[SKIP-DEFERRED]` — feature not yet built (known)
