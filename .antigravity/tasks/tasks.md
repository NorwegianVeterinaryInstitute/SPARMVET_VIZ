# Tasks (SOLE SOURCE OF TRUTH)

**Workspace ID:** SPARMVET_VIZ
**Last Updated:** 2026-05-01 (Phase 24 IMPLEMENTED — home_theater.py 2,853 → 1,278 lines, ADR-051 closed; Phase 25 left-sidebar restructure queued) by @dasharch

## 🟣 Completed Phases — Archived

> Status: COMPLETED. Phases 16, 17, 18-A through 18-D, 18-B-fixes, 18-C, 18-F (stress tests), 21-A, 21-B, 22, 24 are done.
> Detailed history: [./.antigravity/tasks/archives/tasks_archive_2026-04-10.md], [./.antigravity/tasks/archives/tasks_archive_2026-04-14.md], [./.antigravity/logs/audit_2026-04-18.md], [./.antigravity/logs/audit_2026-04-23.md], [./.antigravity/logs/audit_2026-05-01.md].
> Phase 24 (`home_theater.py` decomposition, ADR-051) executed 2026-04-30 → 2026-05-01 across commits `89bb5ef`, `890b609`, `f540cbf`, `d50197e`, `4c38f26`, `18dbd46`, `f0f7d92`, `2393e50`, `0b50fbd`. Per-step change manifests in [./.antigravity/tasks/tasks_phase24.md].
> Phase 22 sub-phases 22-A through 22-F: IMPLEMENTED. Individual sub-task checkboxes were written prospectively and never ticked; all implementation is in place. Phase 24 decomposed the handlers into their permanent locations (`session_handlers.py`, `export_handlers.py`, `t3_recipe_engine.py`). Remaining open items (22-G-4, 22-J verification, bugs) are tracked below.

---

## 🟢 Phase 25: Left Sidebar Restructure — DESIGNED (ready to implement)

**Status:** DESIGNED 2026-05-01 (co-design session with @evezeyl). ADR-052 written. All scope questions answered. tasks_phase25.md written with 10 substeps. Pre-flight checklist ready.

**Objective:** Fix persona-gating bugs, restructure the left sidebar accordion into named panels (Manifest Choice / Data Import / Filters / Global Project Export / Session Management / Single Graph Export), add two new persona template fields (`manifest_selector`, `testing_mode`), fix the right sidebar layout bug, and add a PersonaValidator.

**ADR:** ADR-052 — see `.antigravity/knowledge/architecture_decisions.md`
**Design document:** `EVE_WORK/daily/2026-05-01/persona_functionality_side_bars_v3_clean.csv`
**Per-step change manifests:** `.antigravity/tasks/tasks_phase25.md`
**Refactor protocol:** `.antigravity/knowledge/refactor_protocol_phase24.md` (reused)

**Pre-flight (do once before 25-A):**
- [ ] `git tag pre-phase25-$(date +%Y%m%d)`
- [ ] `PYTHONPATH=. ./.venv/bin/python -m pytest libs/ app/tests/ -q 2>&1 | tee .antigravity/baselines/phase25_pre.txt`
- [ ] `python -c "from app.src.main import app; print('import OK')" >> .antigravity/baselines/phase25_pre.txt`
- [ ] `PYTHONPATH=. SPARMVET_PERSONA=qa ./.venv/bin/python -m pytest app/tests/test_shiny_smoke.py -v >> .antigravity/baselines/phase25_pre.txt`

**Substeps (model recommendation in brackets):**

- [x] **25-A** [Sonnet] — Config + renames: gallery_enabled for project-independent, Test Lab rename
- [x] **25-B** [Sonnet] — Persona template new fields (`manifest_selector`, `testing_mode`) + PersonaValidator pure module
- [x] **25-C** [Sonnet] — Persona gating fixes: `interactivity_enabled` gate on filter form, PERSONA-1 fix, Gallery bug, `comparison_mode_enabled` gate
- [x] **25-D** [Sonnet] — Right sidebar layout fix (Option A): exclude container from `ui.py` for pipeline personas
- [x] **25-E** [Sonnet] — Accordion restructure: rename panels, move session + data ingestion slots, add plot format selector
- [ ] **25-F** [Opus] — Data Import panel (new build): testing_mode-aware selector, pipeline-static read-only path display
- [ ] **25-G** [Opus] — Export restructure: consolidated audit report format selector + Quarto render + session export .zip
- [ ] **25-H** [Opus] — Single Graph Export (un-deferred from Phase 22): plot + data slice + manifest section
- [ ] **25-I** [Sonnet] — Visual fixes: filter row 🗑 icon, right sidebar header bold + yellow background
- [ ] **25-J** [Sonnet] — Smoke test coverage update for new sidebar panels

**Hard rules (Phase 24 protocol applies):**
1. Persona IDs use HYPHENS — never underscores.
2. Shared `reactive.Value` instances stay in `home_theater.define_server()` — pass as kwargs.
3. ADR-045 Two-Category Law: `app/modules/` = pure, `app/handlers/` = Shiny-only.
4. Playwright smoke gate mandatory after every commit.
5. `bootloader.is_enabled(...)` is the persona-flag interface — never hard-code persona name sets.

---

## 🟡 Phase 22: Session Management, T3 Audit Trace & Publication Finisher

**Objective:** Implement the full session identity system (§12d), T3 audit recipe (§12a–c), ghost save (§12d), Home module state object (§13), and export audit report (§12f) as specified in `ui_implementation_contract.md §12–13` and `rules_ui_dashboard.md`.

**Governing docs:** `ui_implementation_contract.md §12–13`, `rules_ui_dashboard.md §1–4`.

---

### Phase 22-A through 22-F — IMPLEMENTED ✅

> All implementation complete. Sub-task checkboxes were written prospectively and never ticked off.
> Current file locations (after Phase 24 decomposition):
> - `app/modules/session_manager.py` — SessionManager, RecipeNode, make_recipe_node, ghost R/W
> - `app/handlers/session_handlers.py` — session panel UI, import/export/delete
> - `app/handlers/export_handlers.py` — export bundle, audit report
> - `app/modules/exporter.py` — generate_methods_text, render_audit_report
> - `app/handlers/gallery_handlers.py` — "Send to T3" transplant
> - `app/src/server.py` — home_state schema (t3_recipe_by_plot, primary_keys, orphaned_t3_nodes)

---

### Phase 22-G: Headless Verification & @verify Gate

- [x] **22-G-1**: `app/tests/test_session_manager.py` — 26/26 PASSED (2026-04-25).
- [x] **22-G-2**: `app/tests/debug_session_flow.py` — 15/15 PASSED. Artifacts in `tmp/session_test/`.
- [x] **22-G-3**: Import check passes: `from app.src.main import app` — OK.
- [ ] **22-G-4**: [@verify] Manual review of session ghost files in `tmp/UI_TEST/user/_sessions/` — pending user test in live UI.

---

### Phase 22-H: Live-UI Bug Fixes (2026-04-25, after first user test)

**Context:** Found in the first interactive test of Phase 22 by @evezeyl. These are gaps that the unit tests and debug flow could not catch because they cover only the SessionManager module in isolation, not the wired Shiny reactive graph or persona name plumbing.

#### Bugs found and fixed

- [x] **22-H-1**: Right sidebar T3 audit panel rendered nothing.
  - **Root cause**: `audit_stack_tools_ui` output slot was referenced in the right sidebar but no `@render.ui` function with that name existed anywhere. The slot rendered silently empty. There were also no Add buttons to create RecipeNodes.
  - **Fix**: Added full `audit_stack_tools_ui` render in `app/handlers/audit_stack.py` with three Add buttons (`t3_add_filter`, `t3_add_exclusion`, `t3_add_drop`) plus gatekeeper-aware Apply, and three matching `@reactive.Effect` handlers that append empty RecipeNodes to `_pending_t3_nodes`.

- [x] **22-H-2**: Persona-gated UI never showed (or always showed) for advanced personas.
  - **Root cause**: Code-side persona sets were written with underscores (`pipeline_exploration_advanced`, `project_independent`) but real persona IDs from the templates use hyphens (`pipeline-exploration-advanced`, `project-independent`). Affected: gallery "Send to T3" button, session management panel, export audit report panel, T3 tier toggle option, right-sidebar suppression for simple personas.
  - **Fix**: Replaced underscore literals with hyphenated literals in:
    - `app/handlers/gallery_handlers.py` — `_T3_PERSONAS`
    - `app/handlers/home_theater.py` — `hidden_personas` (right-sidebar gate), `advanced_personas` (export panel), `advanced_personas` (session management panel), tier-choices block (line ~411)
  - **Lesson**: Persona IDs are user-data; never hard-code variants. Future work should centralise persona constants in one module.

- [x] **22-H-3**: Left-panel filters (My Adjustments) had no path into the T3 audit recipe.
  - **Root cause**: `filter_t3_btn_ui` rendered an "Apply to recipe" button (`input.filter_apply_recipe`) but no `@reactive.Effect` listened for it. The button was decorative.
  - **Fix**: Added `_filter_apply_recipe` handler in `app/handlers/home_theater.py`. Reads `_pending_filters`, converts each row to a `filter_row` RecipeNode (column/op/value pre-filled, reason empty), appends to `_pending_t3_nodes`. Gatekeeper enforces reason before Apply.

- [x] **22-H-4**: No detection of source-data file changes — tiers never re-derived after the user edited a metadata TSV.
  - **Root cause**: `data_batch_hash` field existed in the `home_state` schema but was never populated. `restore_t1t2()` was implemented in SessionManager but never called from the orchestrator/home_theater assembly path. The session_key therefore could not change when input files changed.
  - **Fix (2 parts)**:
    1. Added `DataOrchestrator.get_source_files(project_id) -> dict[str, Path]` in `app/modules/orchestrator.py`. Mirrors the ingestor's path-resolution logic (manifest `source.path` block first, legacy `data_dir` glob fallback). Returns only files that exist on disk.
    2. Added `_sync_session_provenance` `@reactive.Effect` in `app/handlers/home_theater.py`. Watches `input.project_id`. Hashes manifest + all source files via `SessionManager.compute_manifest_sha256` / `compute_data_batch_hash`. Compares to stored values in `home_state`. If `data_batch_hash` changed, shows a warning notification and writes the new hashes back to `home_state`.

- [x] **22-H-5**: Shiny client errors `output 'dynamic_tabs' is recalculating, but the output is in an unexpected state of: 'idle'` (and similar for `running`/`invalidated` states).
  - **Root cause**: My initial implementation of 22-H-4 placed `home_state.set(...)` *inside* the `@render.ui dynamic_tabs` function. Writing a `reactive.Value` during a render invalidates downstream readers immediately, even though the render has not completed. Shiny's client/server state machine then sees illegal transitions and emits these warnings.
  - **Fix**: Removed all `home_state.set` and hash computation from the `dynamic_tabs` render body. Moved them to a standalone `@reactive.Effect` (`_sync_session_provenance`) that runs as a side-effect and only writes to `home_state` when values actually changed (cheap idempotent guard).
  - **Lesson (durable)**: Never call `reactive.Value.set()` inside a `@render.*` function. State writes belong in `@reactive.Effect`. This is a generalisation of ADR-045's Two-Category Law and should be considered alongside it.

#### Files changed in 22-H

- `app/handlers/audit_stack.py` — added `audit_stack_tools_ui` render + 3 Add-node effects.
- `app/handlers/home_theater.py` — added `_filter_apply_recipe` effect, added `_sync_session_provenance` effect, fixed 4 persona-name literals (underscore → hyphen).
- `app/handlers/gallery_handlers.py` — fixed `_T3_PERSONAS` literal.
- `app/modules/orchestrator.py` — added `get_source_files(project_id)` method.

#### Verification status

- [x] Import check: `python -c "from app.src.main import app"` passes.
- [ ] [@verify] Live-UI test by user: confirm right-sidebar T3 panel renders Add buttons; "Apply to recipe" from left panel creates RecipeNodes; editing a source TSV triggers the "Source data files have changed" warning.

---

### Phase 22-I: T3 UX Simplification & Audit Polish (2026-04-25, second user-test pass)

**Context:** Second live-UI session with @evezeyl uncovered both bugs and a major UX simplification. The original design had two separate Apply buttons (left-panel "Apply" for transient view filters + "Apply to recipe" for T3 audit), and a right-sidebar tools bar with Add buttons for filter/exclude/drop. The user proposed collapsing this: in T3 mode, the left panel is the only authoring surface and its single Apply button promotes rows directly into the audit pipeline. Right sidebar becomes audit-trail only (plus Apply with gatekeeper).

#### Bugs found and fixed

- [x] **22-I-1**: Reason text input destroyed mid-typing every keystroke.
  - **Root cause**: `_sync_t3_reasons` was a `@reactive.Effect` with no event guard. It read every `input.t3_reason_<id>`, then read `home_state`, then wrote `home_state` if any reason changed. Each keystroke → effect re-fires → `home_state.set` → `audit_nodes_tier3` re-renders → reason input destroyed and re-mounted with new value, losing focus and possibly characters.
  - **Fix**: Removed the always-firing Effect. Reasons are now pulled from live inputs ONLY at `btn_apply` click time inside `handle_apply` (and read non-mutating by `_nodes_with_live_reasons()` for gatekeeper visibility on the Apply button). Input stays mounted during typing.

- [x] **22-I-2**: Apply button stayed "Apply ⛔" even after reason was typed.
  - **Root cause**: Gatekeeper read from `home_state.t3_recipe[*].reason`, which is empty until commit. With 22-I-1's no-eager-sync model, the button never sees the live text.
  - **Fix**: Added `_nodes_with_live_reasons()` helper that returns a non-mutating overlay merging live `input.t3_reason_<id>` values into the node list. `audit_stack_tools_ui` and `btn_apply_ui` use it before calling `gatekeeper_blocked()`. Button label flips live as the user types.

- [x] **22-I-3**: Shiny rejected `t3_reason_<uuid>` input IDs — `'… is not a valid id'`.
  - **Root cause**: `make_recipe_node` used `str(uuid.uuid4())` (hyphenated). Shiny input IDs allow only `[A-Za-z0-9_]`.
  - **Fix**: Two layers. `make_recipe_node` now uses `uuid.uuid4().hex` (32 hex chars, no hyphens). Added `_safe_input_suffix(node_id)` in `audit_stack.py` that replaces non-alnum chars with `_`, applied at all input-ID build sites — handles legacy ghost files with hyphenated UUIDs.

- [x] **22-I-4**: Left-panel filter rows weren't being re-applied; the same filter could be sent to T3 multiple times.
  - **Root cause**: Initial 22-H-3 wired "Apply to recipe" without clearing `_pending_filters`/`applied_filters`. Plot view also relied on `applied_filters` so we couldn't clear naively.
  - **Fix**: Added `_t3_filter_rows()` helper in `home_theater.py` that extracts active `filter_row` RecipeNodes and converts them to the `_apply_filter_rows`-compatible format. Both `home_data_preview` and the plot spec injection now use `applied_filters + _t3_filter_rows()`. With T3 nodes driving the plot, both filter lists are cleared on T3 promotion — left-panel rows disappear, plot stays filtered via the audit pipeline.

- [x] **22-I-5**: Audit summary line was unreadable / didn't show the filter content.
  - **Root cause**: `_params_summary` printed raw op codes (`eq`, `in`) and stringified lists (`[a, b]`); rendered in 0.75em grey text barely visible against the yellow card.
  - **Fix**: Operators now render as readable symbols (`=`, `≠`, `>`, `∈`, `∉`); list values format as `{a, b, c}` with truncation; the summary line itself is now monospace, larger, on a pale-yellow background, dark text.

- [x] **22-I-6**: Column drop selectize "snapped back" — deselecting a column appeared briefly then reverted.
  - **Root cause**: `home_col_selector_ui` mounted `input_selectize("preview_col_selector")` AND read its value to compute the audit-button count. Reading the input made the render reactive on its own input → every click → re-render → selectize rebuilt with `selected=cols` → user's deselection wiped.
  - **Fix**: Split into two outputs — `home_col_selector_ui` (mounts the selectize, depends only on schema) and `col_drop_audit_btn_ui` (reads the input, renders only the button). Codified as **Rule R4** in §14 of `ui_implementation_contract.md`.

#### UX simplification — single-Apply T3 flow (designed with @evezeyl)

Old flow (kept failing the "where do I click?" test):
1. Left panel: `+ Add` row → `Apply` (commits applied_filters) → `Apply to recipe` (separate orange button) → right sidebar shows pending node → type reason → right `Apply` button → committed.
2. Right sidebar had Add buttons for filter/exclude/drop AND the apply button.

New flow (Phase 22-I):
1. Left panel in T3 mode: `+ Add` row → `➜ Audit (N)` (orange, replaces "Apply") promotes rows directly to pending T3 nodes; left list clears.
2. Column selector in T3 mode: deselect column(s) → `➜ Audit drops (N)` (orange) creates `drop_column` RecipeNodes.
3. Right sidebar: audit-trail only — no Add buttons. Type reason in the yellow box on each pending node. Bottom `Apply` enables when gatekeeper passes → commits to `t3_recipe` + ghost-saves.
4. T1/T2 mode unchanged: left `Apply` is blue and commits transient `applied_filters` as before.

**Permanent delete (22-I-7)**: ✕ "deactivate" button replaced with 🗑 "delete" — removes the node from `t3_recipe`/`_pending_t3_nodes` entirely. The `active: False` schema field stays for legacy ghost compatibility but is no longer settable from the UI. Tracked via `_last_delete_clicks` dict for idempotent click-counting.

**T3 column drops in data path (22-I-8)**: Added `_t3_drop_columns()` helper. Both `home_data_preview` and the plot data path now drop committed columns via `lf.drop(...)`. Committed-dropped columns are also excluded from the column-selector choices — can't be re-dropped.

#### Files changed in 22-I

- `app/handlers/audit_stack.py` — removed Add buttons + handlers + `_sync_t3_reasons` Effect; added `_safe_input_suffix`, `_nodes_with_live_reasons`, `_handle_delete`; reworked `audit_stack_tools_ui` to be apply-only; reason sync moved into `handle_apply`. Improved `_params_summary` and audit-card visual styling.
- `app/handlers/home_theater.py` — `_filter_apply` now branches on `tier_toggle` (T3: build pending RecipeNodes + clear staging; T1/T2: legacy `applied_filters`). Removed `filter_t3_btn_ui` + `_filter_apply_recipe`. Added `_t3_drop_columns` helper, `col_drop_audit_btn_ui`, `_col_drop_to_audit` Effect. Split `home_col_selector_ui` to mount selectize without reading its own input. Apply button label flips to "➜ Audit (N)" in orange in T3 mode.
- `app/modules/session_manager.py` — `make_recipe_node` uses `uuid.uuid4().hex` (Shiny-safe IDs).
- `app/src/server.py` — added `t3_apply_count: 0` to `home_state` schema (used to clear left-panel filters on T3 commit).
- `.agents/rules/ui_implementation_contract.md` — added **Rule R4** to §14: "Don't read an input inside the render that mounts it."

#### Verification status

- [x] Import check: `python -c "from app.src.main import app"` passes after every fix.
- [x] [@verify] Live-UI confirmed by @evezeyl 2026-04-25:
  - Filter row → "➜ Audit (N)" → audit node appears with readable summary, reason input stable while typing.
  - Apply button activates the moment the reason field is non-empty.
  - Apply commits the node, clears left-panel staging, plot stays filtered.
  - Column deselection holds, "➜ Audit drops (N)" updates count live, audit drops apply to data.
  - 🗑 deletes nodes permanently.

#### Known follow-ups (not in this phase)

- Filter operator/value semantics have edge cases ("some bugs detected in the filters themselves but we will fix that later"). Defer to a focused filter-correctness pass.
- Right-sidebar Add buttons removed; `exclusion_row` is now reached automatically via primary-key conversion in Phase 22-J. Aesthetic and dev_raw_yaml sourcing reviewed in 22-J.

---

### Phase 22-J: Per-Plot Audit Scoping & Join-Key Propagation (2026-04-25, IMPLEMENTED — pending live-UI verification)

**Objective:** Replace flat `t3_recipe` with per-plot stacks. Propagation dialog at promotion time. Primary-key drop blocked. Primary-key filter → silent `exclusion_row` conversion + persistent warning flag through to the export report. Three propagation choices: this plot only / all plots / all plots except (multiselect). Linked-id deletion.

**Governing decisions** (settled with @evezeyl in design conversation 2026-04-25):

| ID | Decision | Rationale |
|---|---|---|
| 22-J-D1 | Per-plot stacks: `t3_recipe_by_plot: {plot_subtab_id: [nodes]}` | Audit decisions are rarely truly "global"; the flat list created confusion when switching plots. |
| 22-J-D2 | Linked propagation via shared `id` | "Apply to all" creates N copies sharing one id. Delete one → delete all. Edits propagate. |
| 22-J-D3 | Primary keys = union of all assembly join keys (`on`/`left_on`/`right_on`) | Covers true PKs and secondary/accessory keys (e.g. long-format Resfinder gene_id). |
| 22-J-D4 | Drop-column on join key: BLOCKED absolutely. No persona override. | T3 is for analytical adjustments, not output anonymization. |
| 22-J-D5 | Filter on join key: silent convert to `exclusion_row` | Audit reads honestly: "Excluded sample S2" not "filtered to ¬S2". |
| 22-J-D6 | Filter on non-key column whose effect removes a sample → stays `filter_row` | Semantically different — "value condition not met" ≠ "deliberate exclusion". |
| 22-J-D7 | `primary_key_warning: bool` on every node touching a PK | Persists in ghost; renders as banner on audit card and as marker in export report. |
| 22-J-D8 | Propagation dialog: 3 options — this/all/all-except (multiselect) | Captures Case A (S2 excluded everywhere except QC plot) directly. |
| 22-J-D9 | Skip propagation to plots whose schema lacks the column | Audit accurately reflects which plots actually had the column. Show notification. |
| 22-J-D10 | Ghost backward-compat: legacy flat `t3_recipe` → orphaned bucket on restore | Notification + "Orphaned" section in audit panels for user re-targeting. |
| 22-J-D11 | New-plot inheritance: NO automatic | Adding a plot later does not inherit prior "all plots" propagations. Explicit re-propagation only. |
| 22-J-D12 | Aesthetic propagation: dialog for color/shape/fill; alpha per-plot only | Color/shape often want homogeneity; alpha is a per-plot adjustment. No PK warning ever on aesthetics. |
| 22-J-D13 | No "re-include" node type | Undo = delete the audit node. Data reappears because recipe no longer removes it. |

**Design references:**
- `.agents/rules/ui_implementation_contract.md` §12g (technical spec — RecipeNode schema additions, propagation dialog, ghost format, primary-key detection).
- `docs/user_guide/audit_pipeline.qmd` (user-facing explanation — three use cases, why per-plot, why exclusion vs filter on PK).

#### Sub-tasks

- [x] **22-J-1**: `home_state.primary_keys` populated by `extract_primary_keys()` in `_sync_session_provenance`. Recomputes on manifest change. Idempotent guard prevents loops.
- [x] **22-J-2**: `home_state.t3_recipe_by_plot: dict[str, list]` replaces flat `t3_recipe`. `session_manager.write_t3_ghost` accepts `t3_recipe_by_plot=` kwarg, bumps `schema_version=2`, also writes a flattened legacy `t3_recipe` field for bw compat. `list_t3_ghosts` lifts pre-22-J flat lists into `__legacy__` bucket.
- [x] **22-J-3**: `RecipeNode` TypedDict gains `primary_key_warning: bool`. `make_recipe_node()` accepts `primary_key_warning` and `node_id` (for propagation copies sharing an id). All 26 unit tests pass.
- [x] **22-J-4**: `_active_plot_t3_nodes(plot_id)`, `_t3_filter_rows(plot_id)`, `_t3_drop_columns(plot_id)` read per-plot. Plot handlers pass `f"subtab_{p_id}"` explicitly so re-renders during plot iteration use the right stack. Default reads `home_state.active_plot_subtab` (which is now mirrored from `_track_active_home_subtab`).
- [x] **22-J-5**: `_filter_apply` in T3 mode: detects PK-targeted rows, silently converts to `exclusion_row` with negated op (`eq`→`ne`, `in`→`not_in`), stamps `primary_key_warning=true`, opens propagation modal via `_open_propagation_modal()`. Final expansion happens in `_handle_propagation_confirm`.
- [x] **22-J-6**: `_col_drop_to_audit`: blocks PK columns with a notification listing them; non-PK drops open the propagation modal.
- [x] **22-J-7**: `ui.modal` with three radio choices + multiselect for "All except…". `_propagation_scratch` holds nodes between handlers. `_handle_propagation_confirm` resolves choice → list of target plot ids → emits one RecipeNode copy per plot (all sharing `id`). Skips plots whose schema lacks the column via `_plot_has_column()`; reports skipped plots in the notification.
- [x] **22-J-8**: `audit_nodes_tier3` filters to active plot only; "Applied to N plots" badge counts unique `plot_scope`s per `id`. PK-warning yellow banner: "⚠️ Primary key — Primary ID/Key alignment". Orphan section appended when `__legacy__` bucket is non-empty.
- [x] **22-J-9**: `_handle_delete` collects all known node ids across every per-plot stack + pending; clicked ids delete every copy with that id everywhere. Reports both "decisions deleted" (unique ids) and "copies deleted" (physical removals).
- [ ] **22-J-10**: Aesthetic propagation (color/shape/fill) — design honoured but not yet wired in UI; deferred (no `aesthetic_override` authoring path exists today aside from gallery clones).
- [x] **22-J-11**: `generate_methods_text` dedupes propagated nodes by `id`, lists every target scope on one line, prepends `⚠️ [Primary key affected]` for PK-warning nodes. Marker carries through to HTML/PDF/DOCX.
- [x] **22-J-12**: All 26 SessionManager unit tests pass. Debug flow 15/15 pass (tests use legacy flat-list API which remains backward-compatible — both flat and per-plot ghosts roundtrip correctly).
- [ ] **22-J-13**: Live-UI verification by user — pending. See `tasks_test_22J.md` checklist.

#### Verification status

- [x] Design documented (`§12g` of `ui_implementation_contract.md`, `docs/user_guide/audit_pipeline.qmd`).
- [x] Implementation: 12 of 13 sub-tasks complete; 22-J-10 (aesthetic propagation UI) deferred until an aesthetic authoring surface exists.
- [x] Tests: 26/26 unit tests + 15/15 debug flow + import check `from app.src.main import app` all pass at HEAD `94bb917`.
- [ ] [@verify] Live-UI by @evezeyl — see `.antigravity/tasks/tasks_test_22J.md` for the structured test checklist.

#### Files changed in 22-J

- `app/modules/session_manager.py` — `extract_primary_keys()` helper, `make_recipe_node()` extended (primary_key_warning, node_id), ghost format v2 with backward-compat read.
- `app/handlers/home_theater.py` — `_active_plot_t3_nodes/_t3_filter_rows/_t3_drop_columns` per-plot helpers; `_all_plot_subtab_ids/_plot_label/_plot_has_column` helpers; `_open_propagation_modal/_handle_propagation_confirm`; `_filter_apply` and `_col_drop_to_audit` rewired for PK + propagation; `_track_active_home_subtab` mirrors to home_state; `_sync_session_provenance` populates `primary_keys`; ghost-restore reads `t3_recipe_by_plot`.
- `app/handlers/audit_stack.py` — `audit_nodes_tier3` filters to active plot, renders PK banner + propagation badge + orphan section; `_nodes_with_live_reasons` reads per-plot + linked-id reason fan-out; `handle_apply` commits pending nodes into `t3_recipe_by_plot[plot_scope]`; `_handle_delete` is linked across all stacks.
- `app/modules/exporter.py` — `generate_methods_text` dedupes propagated nodes, lists scopes, prepends PK marker; `render_audit_report` flattens `t3_recipe_by_plot` for Methods.
- `app/src/server.py` — `home_state` schema includes `t3_recipe_by_plot`, `primary_keys`, `orphaned_t3_nodes`.

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

### Phase 21-E: Comparison Mode — COMPLETED 2026-04-30
- [x] `comparison_mode_toggle_ui` fixed: underscore→hyphen persona IDs; only shows for advanced+ personas AND when tier==T3.
- [x] Toggle placed in `theater_header` strip (via `ui.output_ui("comparison_mode_toggle_ui")`).
- [x] `_make_cmp_baseline_handler(p_id)` registered for every plot ID: renders `plot_group_{p_id}_cmp_base` using raw T1 data with NO T3 audit nodes applied.
- [x] `dynamic_tabs` reads `input.comparison_mode`: when ON + T3, each plot tab shows 2-column layout — grey "T2 — Baseline" badge left, amber "T3 — My adjustments" badge right.
- [x] Old `is_comparison` was already removed in a prior phase. `comparison_mode_toggle_ui` retained (now correctly wired).
- [x] Import check passes.

> **Note:** Full T2-vs-T3 visual diff requires a manifest with T2 assembly transforms + active T3 audit nodes. With current ST22 data, comparison shows T1 baseline (no T2 transforms applied) vs T3 filtered view when audit nodes are committed.

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

### Phase 21-G: Persona-Gated Right Sidebar Suppression — COMPLETED (verified 2026-04-30)
- [x] `right_sidebar_content_ui` already returns `ui.div()` for `{"pipeline-static", "pipeline-exploration-simple"}`.
- [x] Advanced personas get full audit stack: T2 violet nodes (`audit_nodes_tier2`) + T3 yellow nodes (`audit_nodes_tier3`) + Apply button with gatekeeper (`audit_stack_tools_ui`).
- [x] `btn_revert` concept superseded by per-node 🗑 delete in Phase 22-I — no revert needed.
- [x] T3 pre-fills from T2: out of scope for current ST22 data (no T2 transforms declared); architecture is in place via `tier_reference` calc.

### Phase 21-H: Headless Verification & @verify Gate — COMPLETED 2026-04-30
- [x] `app/tests/debug_home_theater.py` — 76/76 PASSED. Covers: persona feature flags (22 checks), manifest analysis_groups → tab structure (20 checks), tier choices per persona (5 checks), right sidebar suppression (6 checks), comparison mode gating (5 checks), primary key extraction (2 checks), session provenance sha256 (2 checks), ghost round-trip t3_recipe_by_plot (6 checks), filter recipe node schema (5 checks), bootloader location resolution (3 checks).
- [x] Report artifact written to `tmpAI/home_theater_verify/results.json`.
- [ ] [@verify] User review of artifacts — pending.

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

### Phase 23-A: Directory Rename & Bootloader Extension ✅ COMPLETED 2026-04-30
- [x] Renamed `config/connectors/` → `config/deployment/`; `local_connector.yaml` → `local_profile.yaml`. Added `deployment_type: filesystem` to local profile.
- [x] Extended `bootloader.py` with 4-level `_resolve_profile_path()` (ADR-048 §4). New attributes: `deployment_level`, `deployment_type`, `deployment_name`, `default_manifest`, `default_persona`, `project_root`.
- [x] `default_persona` from profile overrides `SPARMVET_PERSONA` env var (unless explicit persona arg passed to `__init__`).
- [x] Startup log: `[Bootloader] Profile resolved at level N (label): path`.
- [x] Validation: `_validate_profile()` raises `ValueError` for missing location keys; `SPARMVET_PROFILE` pointing to missing file raises `FileNotFoundError` immediately.
- [x] `get_location()` updated: if `project_root` is set in profile, relative location paths resolve under it.
- [x] Resolution chain documented in `project_conventions.md §4` and in `bootloader.py` module header.
- [x] All callers unchanged (same public API). Import check + full app import: clean.

### Phase 23-B: Connector Library (`libs/connector/`) ✅ COMPLETED 2026-04-30
- [x] `base.py`: `BaseConnector` ABC — `resolve_paths()`, `fetch_data()`, `get_manifest_path()`, `get_default_persona()`.
- [x] `filesystem.py`: `FilesystemConnector` — resolves locations; `project_root`-aware; no-op `fetch_data()`.
- [x] `galaxy.py`: `GalaxyConnector` — extends Filesystem; fallback to `_GALAXY_JOB_HOME_DIR` env var when `project_root` absent.
- [x] `irida.py`: `IridaConnector` — resolves paths via `irida.local_cache`; `fetch_data()` validates token + irida block, raises `NotImplementedError` (Phase 23-D stub).
- [x] `__init__.py`: exports all four classes + `get_connector(profile)` factory.
- [x] `tests/test_connectors.py`: 31 tests, all passing. Covers all connectors, factory, error branches.

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
- [x] Update `docs/workflows/connector.qmd` to reference ADR-048 and new schema. (2026-04-30) — removed stale "rename pending" section, fixed level-4 path, updated component table with real paths, updated dev fallback snippet.

---

## 🔧 2026-04-24 Repository Hygiene (from @dasharch workspace review)

*Verified by manual codebase inspection. Gemini agent findings were correct on all four items.*

### H-1: Fix broken cross-references in `architecture_decisions.md` — DONE
- [x] ADR-014: Replaced `"Section 12 of the Workspace Standard"` → `rules_data_engine.md §4` (Identity Transformations / Manifest Data Contract).
- [x] ADR-016: Replaced `"Section 13, Workspace Standard"` → `rules_runtime_environment.md §4` ("Clear Lines"). Section 14 → `rules_runtime_environment.md §1 & §5` (venv enforcement).

### H-2: Resolve `assets/scripts/` vs ADR-032 contradiction — RESOLVED
**Decision (2026-04-24):** `assets/scripts/` is the designated home for **user-facing helper scripts** (manifest creation, manifest validation, data verification, deployment debugging). ADR-032's deletion mandate applies only to scripts that were duplicating library-internal logic during early prototyping. Library test/debug runners belong inside their `libs/` packages. Cross-library dev utilities with no clear owner may go in `libs/utils/`.
- [x] ADR-032 scope clarification written in `architecture_decisions.md`.
- [x] Audit `assets/scripts/` contents: all 12 scripts are user-facing helpers or dev utilities. `materialize_manifest_plots.py` is an intentional shim (documented). `SF_create_manifest.py` is a simpler schema-only variant of `create_manifest.py` — kept. No scripts need moving. (2026-04-30)

### H-3: `connectors/` → `deployment/` terminology alignment
Already tracked under Phase 23-A. No new action — verified as duplicate.

### H-4: `home_theater.py` size watch — ESCALATED (2547 lines as of 2026-04-30)
Phase 21 is now stable. The file has grown from 1,562 → 2,547 lines — past the 2,362-line threshold that triggered the ADR-045 decomposition of `server.py`. Active design task added as ARCH-1 below.


---

## 🔧 2026-04-30 Documentation & Technical Debt (from @dasharch full project audit)

*Source: `EVE_WORK/daily/2026-04-30/Project_full_audit.md`. All 6 issues verified by agent.*

### DOC-1: Sync `implementation_plan_master.md` to current state — DONE 2026-04-30
- [x] Mark Phase 21-E as **COMPLETED 2026-04-30** (was: DEFERRED).
- [x] Mark Phase 21-G as **COMPLETED 2026-04-30** (was: PENDING).
- [x] Mark Phase 21-H as **COMPLETED 2026-04-30** (was: PENDING).
- [x] Add Phase 22-J (Per-Plot Audit Scoping & Join-Key Propagation) as a completed sub-phase under Phase 22.
- [x] Add a note under Phase 11 explaining the 11-B / 13–15 numbering gaps (historical non-sequential phases, not missing work).

### DOC-2: Fix ADR-040 header status contradiction — DONE 2026-04-30
- [x] Updated ADR-040 status line: `PARTIALLY IMPLEMENTED (18-D/E/F pending)` → `PARTIALLY IMPLEMENTED (18-A through 18-D, 18-B-fixes, 18-C, 18-F complete; 18-E pending)`.

### DOC-3: Mark ADR-029a as superseded — DONE 2026-04-30
- [x] Added SUPERSEDED banner at top of ADR-029a section.
- [x] Added inline note listing removed state variables and pointing to ADR-043.

### BUG-1: Fix `build_dep_graph.py` code-block parsing flaw — DONE 2026-04-30
- [x] Added `re.sub(r"```.*?```", "", content, flags=re.DOTALL)` pre-processing step before `@deps` regex in `scan_file()`.
- [x] Re-ran script: `workspace_standard.md` no longer listed as providing `action:cast` or mirroring `orchestrator.py`. Graph: 89 nodes, 151 edges — clean.

### ARCH-1: Design Phase 24 — `home_theater.py` decomposition — DONE 2026-04-30
- [x] Phase 24 design entry written in `implementation_plan_master.md` (24-A through 24-E sub-phases).
- [x] ADR-051 written in `architecture_decisions.md`: boundary rule, new file map, shared state protocol, pre-condition gates.
- [x] Proposed split: `t3_audit_handlers.py` (~450 lines), `session_handlers.py` (~400 lines), `export_handlers.py` (~510 lines), `t3_recipe_engine.py` module (~120 lines). `home_theater.py` → ~900 lines.
- [x] Implementation gated on Phase 22-J live-UI test + ST22 Lineage 2 sign-off.

---

# User needs to test

- [ ] change metadata year to have serval years - Verify sorting function in the columns
---

## 🔴 2026-04-30 Live UI Test Findings (Phase 22-J + general UX)

*Source: `EVE_WORK/daily/2026-04-30/UI_user_test.md`. Captured during the 22-J live-UI test pass. Items prefixed **DEMO** are blockers for the Monday demo.*

### CRITICAL (Monday demo blockers — fix one-by-one with commits between)

- [ ] **DEMO-1**: Manifest `1_test_data_ST22_dummy` — Virulence Variants plot fails with `Render error: 'rotation'`. Likely a layer/aesthetic kwarg the manifest schema doesn't recognise.
- [ ] **DEMO-2**: Manifest `1_test_data_ST22_dummy` — Assembly quality dotplot fails with `Render error: Aesthetic x references unknown column metric`. Same root cause family as the figshare plots: probably wrong `target_dataset` or column doesn't survive the assembly.
- [ ] **DEMO-3**: Filter on numeric/float column fails — `Render error: cannot compare string with numeric type f64`. Tested via AMR heatmap, identity column. Filter UI sends string operands; engine never casts. Surfaced in 22-J test §2. Fix in filter operand coercion path (preferable to manifest typing — the engine should adapt to manifest dtypes, not the other way around). *(was TYPE-1)*
- [ ] **DEMO-4**: Year filter on MLST bar plot fails — string vs numeric ambiguity. Years are stored as strings (categorical) in the manifest but a year filter UI naturally invites numeric ops. Decide: keep years as categorical strings + restrict UI ops to `eq`/`in`, OR cast to int and emit numeric ops. Same root family as DEMO-3 (operand coercion). *(was TYPE-2)*

### Test-data integrity (Monday demo)

- [x] **DATA-1** (resolved 2026-04-30, commit `4133159`): `1_test_data_ST22_dummy` — Quast/FastP/Bracken/Quality_metrics had a different sample_id set (Set A) than metadata/Summary/MLST/ResFinder (Set B). All 42 rows aligned in identical row order, so a row-by-row substitution mapped Set A → Set B canonical ids. Quast↔metadata join now produces 0 nulls (was 42/42 null). Follow-up: add an ingestion-time integrity warning when a left join produces ≥X% null right-side rows (defensive, won't recur for this dataset).

### Filter / Audit semantics — ADR amendment needed

- [ ] **AUDIT-1 (ADR-049 amendment)**: Re-decision needed on PK-column behaviour. ADR-049 specified silent conversion of PK-column filter → `exclusion_row`. Live testing surfaced that this conflicts with user mental model. New proposed semantics:
  - **Filter on PK column** → ALLOWED, but show a non-blocking warning ("⚠️ filtering on a join key — make sure this is what you want")
  - **Drop PK column** → BLOCKED (unchanged from current)
  - **Both filter and drop** → display the PK warning banner in the modal/audit panel
  
  Action: amend ADR-049 first (text change with rationale + the 2026-04-30 user-test reference), then implement. This unblocks 22-J test sections 3, 4, 5.
- [ ] **AUDIT-2**: Filter–audit mapping correctness — UI says "exact France" → audit shows "country: any of [France]". Verify the operator translation is faithful (`==` vs `in`, single-value semantic equivalence).
- [ ] **AUDIT-3**: Filter propagation between plots is not dispatching to all plots. Design discussion needed: should propagation trace back to the root data source (so it applies wherever the column appears)? When a plot's underlying dataset doesn't have the column, surface a warning rather than silently skipping. Touches ADR-049 §propagation.
- [ ] **AUDIT-4**: Compare T2/T3 toggle does not hold state — switching back from another plot loses the toggle. Reactive scoping bug.

### Filter widget UX (follow-up to DEMO-3/DEMO-4)

- [x] **UX-FILTER-1** (2026-04-30, commits `f08b88f` + `61e86a8` + `f4b1a91`): dtype-aware filter widgets implemented. Numeric columns: `ui.input_numeric` for scalar ops, two `ui.input_numeric` (min/max) for the new `between` op. Discrete columns: existing selectize multi-pick. Native types pass through without string coercion (defensive coercion still in place but logs a warning if it fires).

### Filter propagation transparency

#### CRITICAL — needed for safe usage

- [ ] **PROP-1**: Add a clear warning in the propagation modal **before** confirming, listing per-target plot whether the column **exists** in that plot's data. Three states per target plot:
  - ✅ column present → filter will apply
  - ⚠️ column absent → filter will NOT apply (silently skipped — user must verify)
  - ❌ column type mismatch → filter will fail at render time
  
  Today this is a silent skip (D9 schema-skip). Make it explicit at *authoring* time so users don't get surprised by an unfiltered plot they thought they had filtered. Wording: "This filter will apply to N of M selected plots. The other M-N do not contain column X — verify that's intended." **User mental-model note**: encourage the "apply one filter at a time and verify the effect before stacking" workflow — propagation magnifies mistakes if applied in batches.

- [ ] **PROP-4**: Documentation — write a section in `docs/user_guide/audit_pipeline.qmd` (or the persona guide) explaining: (a) propagation rules (column-presence semantics), (b) the recommended one-at-a-time review workflow, (c) advice to use the `reason:` field as the persistent audit trail. Include screenshots once PROP-1 is in.

#### ENHANCEMENT FEATURES (not blocking — future iterations)

- [ ] **PROP-2** (enhancement): "Filter inventory" summary panel (or expand the audit panel) showing the **current effective filter set per plot**. Helps users keep track when they've authored several filters across different scopes. Tooltip per filter: "applied to: plot_A, plot_B; not applicable to: plot_C (column missing)".

- [ ] **PROP-3** (enhancement, exploratory): **Propagation TubeMap** — a small graph visualisation showing, for the active filter/audit node, which plots/datasets it propagates to. Nodes coloured ✅/⚠️/❌ per the same column-presence states as PROP-1. Reuses the existing TubeMap aesthetic from the Blueprint Architect. Lets users see at a glance the blast radius of an edit. Significant scope — own design pass + ADR.

### Notification persistence

- [ ] **UX-NOTIF-1**: Toast notifications disappear too fast — user can't review what was applied to which plots. Per `EVE_WORK/daily/2026-04-30/UI_user_test.md`. Three concrete design options (pick one):

  **Option A — Bell button (simplest, recommended).** A small `🔔 Alerts (N)` button in the right sidebar header. Click → opens a popover listing the last 20 notifications (timestamped, latest first). Badge count shows unread count; clicking the bell marks all read. Click outside → closes. **Why it's good**: zero new screen real estate, familiar pattern (every email/Slack uses it), one click to review.

  **Option B — Permanent footer strip.** A 1-line strip at the bottom of the right sidebar showing the last notification + a "Show history" link → expands to last 20. **Tradeoff**: takes vertical space always, even when empty.

  **Option C — Hover annotations on filter rows.** Each audit/filter row gets a small ⓘ icon. Hover → tooltip shows "Applied to plots A, B; skipped on C (col missing)". **Tradeoff**: per-row only — doesn't capture cross-plot warnings or session-wide events. Best as a complement to A, not a replacement.

  **Recommendation**: implement **A**. Simple, contained, scales to many alerts without UI clutter. PROP-2 (filter inventory) merges naturally as a tab inside the bell popover ("Alerts" + "Filters" tabs). Does NOT replace toasts — toasts still pop for immediate feedback; bell archives them.

  Implementation sketch: `notification_log = reactive.Value([])`. Every `ui.notification_show()` call also appends to the log (a wrapper helper `_notify_and_log(...)`). Bell popover renders `notification_log[-20:]`. Persists to T3 ghost so reload restores history.

### Persona feature-flag wiring — architectural gap

- [x] **PERSONA-1a** (2026-04-30, partial): Refactored unambiguous gates in `sidebar_nav_ui` (Blueprint, Dev Studio, Gallery) to consult `bootloader.is_enabled(flag_name)` instead of hardcoded persona names. Flag matrix in `rules_persona_feature_flags.md` is the source of truth. User-visible behaviour unchanged (matches `persona_traceability_matrix.md` exactly).

- [ ] **PERSONA-1b** (doc-drift, deferred): Three sources disagree on whether `pipeline-exploration-simple` should see **Comparison Mode** and **Session Management**:

  | Source | Comparison for simple | Session Mgmt for simple |
  |---|---|---|
  | Old hardcoded code (until 2026-04-30) | ❌ hidden | ❌ hidden |
  | `persona_traceability_matrix.md` | ❌ hidden | ✅ visible |
  | `rules_persona_feature_flags.md` matrix + actual templates | ✅ visible | ✅ visible |

  Switching these two gates to `bootloader.is_enabled()` would flip them ON for `simple` (matching the templates+rules but contradicting the persona matrix and old code). Held off — kept persona-name gates with `# TODO PERSONA-1 doc-drift` comments in code.

  **Decision needed (post-demo)**: Pick the truth (likely the persona matrix is right — Comparison Mode is "T2 baseline vs T3 adjusted" and `simple` only has filter-level T3 access, not adjustment authoring). Then either:
  - Update the templates: set `comparison_mode_enabled: false` in `pipeline-exploration-simple_template.yaml`, then refactor the code to flag-based.
  - Or update the persona matrix to match the templates, then the code refactor is straightforward.

  Other gates checked and intentionally kept persona-name:
  - **Right sidebar visibility** (line ~1162): explicitly persona-name per `rules_persona_feature_flags.md` Group B note ("Not flag-controlled. Suppressed structurally"). Comment added.
  - **Audit report export** (line ~1617): no dedicated flag; tied to right-sidebar visibility. Comment added.

### Export — UX & correctness (2026-04-30 user test)

*Source: `EVE_WORK/daily/2026-04-30/UI_user_test.md`. Two real bugs were found and fixed below; the rest are UX work.*

- [x] **EXPORT-BUG-1** (fixed 2026-04-30): persona-id underscore-vs-hyphen bug in export_bundle_download made `is_advanced` always False → **T3 data silently skipped from every export** for every persona. Same bug family as the sidebar_nav fix.
- [x] **EXPORT-BUG-2** (fixed 2026-04-30): cross-project manifest leak. `proj_dir.rglob("*.yaml")` on the manifests/pipelines/ parent scooped up every other project's manifest + their include fragments into the bundle. Fixed: now copies only the active manifest + its `{proj_id}/` includes subdirectory.

- [ ] **EXPORT-2** (UX): Selective export — let the user pick what to include in the bundle. Checkboxes (or accordion of toggles) in the export panel, e.g.:
  - [x] Plots (always)
  - [ ] T1 / T2 / T3 data tiers (per-tier checkboxes)
  - [ ] Recipes (manifest YAML + includes)
  - [ ] Filter trace (FILTERS.txt)
  - [ ] Quarto report (.qmd)
  - [ ] README

  Today everything is bundled unconditionally. Should depend on the System Tools restructure (TOOLS-1) so the export UI has room to breathe.

- [ ] **EXPORT-3** (UX): The exported HTML report (Quarto-rendered .qmd) is "horrible" per user. Needs design polish — typography, plot placement, methods section formatting, table-of-contents, navigation. Reuse styling from the in-app theme. Probably a Quarto template rather than the current inline .qmd lines list.

- [ ] **EXPORT-1**: Implement **Export Active Graph** (single-plot quick export). Designed and persona-gated since Phase 22 (`export_graph_enabled` flag in `rules_persona_feature_flags.md`, persona matrix in `persona_traceability_matrix.md`) but the UI button + handler were never wired. Cheatsheet's "Export graph" column refers to this feature.

  **Spec**: button in the active plot's header (or right-sidebar tools) → downloads a small ZIP `{plot_id}_{ts}.zip` containing:
  - `plot.png` (or .svg/.pdf per user choice — same DPI selector as bundle)
  - `recipe.yaml` — the plot's spec fragment + active filters as a self-contained mini-manifest

  **Persona gate**: hidden for `pipeline-static` and `pipeline-exploration-simple`; visible for `pipeline-exploration-advanced`, `project-independent`, `developer` (matches matrix).

  **Why it matters**: complement to the bundle. Bundle = "publish my whole session" (reproducibility). Active graph = "send this one figure to a colleague" (quick re-use). Today users have to extract from the bundle, which is overkill for one plot.

  Not blocking for Monday demo (bundle covers the publication case).

### Theater — layout

- [ ] **THEATER-1** (UX): Collapse / minimize plot panel. Today plots take a fixed slot in the center; users can't shrink one to focus on data preview, audit panel, or another plot. Add a small ▼/▲ caret in each plot's card header that toggles the plot to a 1-line collapsed state. Per-plot, persisted in `home_state` so reload restores. Bonus: a "collapse all" / "expand all" button at the group level.

### Plot-data state preservation (2026-04-30 user test)

- [ ] **STATE-1**: Active plot data flickers / changes when toggling between **T3 mode on/off** and when switching panels (Home → Blueprint Architect → Home). User expectation: T3 mode toggle should NOT change which plot is active or its rendered data — only what filters/audit nodes are applied. Same for panel-mode switches. Reactive scoping bug — likely a `home_state.active_plot_subtab` write inside a render function, or a tier-toggle effect that re-renders plot defs from scratch instead of preserving them. Investigation: trace `tier_toggle.set()` chains and any `home_state.set({**state, "active_plot_subtab": ...})` writes.

- [ ] **STATE-2** (links to AUDIT-4, confirmed broken in user test): **Compare T2/T3 toggle** does not hold — clicking it pushes the user to a different plot. Likely the same reactive-scoping bug as STATE-1 (toggle write triggers a re-render that resets the active subtab). Fix together.

### Test data: Tier-divergence coverage

- [x] **DATA-2** (2026-04-30): `MLST_with_metadata` in `1_test_data_ST22_dummy.yaml` now has visible tier2 transforms — adds an `era` derived column AND filters to `year ≥ 2023`. Toggling T1↔T2 in the UI for any plot reading this assembly will show:
  - T1: full row count, no `era` column
  - T2: filtered row count + new `era` column
  - T3: T2 baseline + user's audit nodes
  
  Cache invalidated. Used by AUDIT-4 / STATE-2 verification. Could be extended later if more T2 coverage needed.

### Test harness persona

- [x] **PERSONA-2** (2026-04-30): Added `config/ui/templates/qa_template.yaml` — a deterministic test-harness persona with all flags ON and `ghost_save.enabled: false` (auto-saves break test determinism). Launch with `SPARMVET_PERSONA=qa`. Added to cheatsheet + persona_traceability_matrix. Foundation for future automated UI testing (Playwright/Selenium) — gives CI a stable reference persona without flag-flipping.

### Playwright headless smoke tests

- [x] **PLAYWRIGHT-1** (2026-04-30): Added full Playwright smoke test infrastructure for Home Theater verification.
  - `app/tests/conftest.py` — `shiny_app` module-scoped fixture via `shiny.pytest.create_app_fixture`
  - `app/tests/test_shiny_smoke.py` — 12 tests across T1 (startup), T2 (persona masking), T3 (filter pipeline), T4 (data preview)
  - `pyproject.toml` — added `[project.optional-dependencies] test` with `pytest>=9.0.0`, `playwright>=1.50.0`, `pytest-playwright>=0.7.0`
  - Gate: 10/12 pass with `SPARMVET_PERSONA=qa`; 2 persona-skip tests require non-developer launch personas
  - Documented in `rules_ui_dashboard.md §6` — mandatory verification gate for all Home Theater changes
  - Pre-existing broken tests NOT regressed: `test_reactive_shell.py` failures due to `#persona_selector` not rendered

### Library imports — defensive

- [x] **DEPS-1** (2026-04-30, commit `3cc8490`): `jinja2` was missing — pandas `DataFrame.style` is used by some Shiny render path (gallery breaks with `Import Jinja2 failed`). Added to top-level `pyproject.toml`. Also surfaced `pyarrow` was only in `libs/transformer/pyproject.toml` despite being needed at meta level — promoted.

### UX / polish

- [ ] **UX-1**: Plot rendering feels slow — likely related to BUG-PERF-1 below (every render re-materialises). Will improve once cache fast-path lands.
- [ ] **UX-2**: Data Preview — "visible columns" multiselect is narrower than the panel; wraps over many lines. Set CSS width to fill the panel.
- [ ] **UX-3**: Right sidebar `My Adjustments — <plot_id>` header — make more visible (bold, yellow background) and add spacing between applied adjustments.
- [ ] **UX-4**: Rename "Audit" button → "Send to Audit" (both center panel and left sidebar). Clearer two-step semantic: stage row → send to audit pipeline.
- [ ] **UX-5**: Homogenise delete UI — Pipeline Audit uses 🗑 trash icon; left-panel filter rows use ✕ cross. Switch filter rows to 🗑 for consistency.

### Performance / Architecture

- [ ] **BUG-PERF-1**: `materialize_tier1` fires on every project switch and every render — `sink_parquet` has no skip-if-exists guard, and `home_theater.py:545` doesn't consult `SessionManager.restore_t1t2()` for the fast path. Phase 22-A integration gap. Fix: home theater render path consults SessionManager first; if status is `fast_path`, use cached parquet path; only call `materialize_tier1` on `reassemble` / `new_session`. Diagnostic logs already in place (Orchestrator START/DONE + SessionManager status).

### Decorator audit (carried over)

- [x] **DECO-1** (2026-04-30): Programmatic decorator audit done. Full report: `.antigravity/logs/decorator_audit_2026-04-30.md`.
  - **Bottom line**: no breaking changes. polars 1.39.3 → 1.40.1 is API-compatible. plotnine 0.15.3 unchanged. Project ≈ 88% coverage of plotnine plot-component API.
  - Confirmed clean: no `melt` / `with_column` / `groupby` (polars-side) in project; `LazyFrame.columns` already migrated to `collect_schema().names()`; `is_between(closed=...)` uses correct string values.
  - Real gaps surface as **DECO-2** below.

- [x] **DECO-2** (2026-04-30, commit `3a3437a` + tests/docs in next commit):
  - `scale_color_brewer` / `scale_fill_brewer` — were ALREADY registered (audit script over-reported British-spelling aliases as gaps)
  - `scale_color_gradient` family — already registered
  - `scale_color_distiller` / `scale_fill_distiller` — already registered
  - `scale_color_cmap` / `_cmap_d` (+ fill) — already registered
  - **NEW**: `xlab` / `ylab` / `ggtitle` / `annotate` — added to themes/core.py
  - **NEW**: `scale_alpha[_manual]`, `scale_size[_manual|_area]`, `scale_shape[_manual]`, `scale_linetype[_manual]` — added to scales/core.py
  - **NEW**: `scale_color_hue` / `scale_fill_hue` / `scale_color_continuous` / `scale_fill_continuous` — added to scales/core.py
  - 17 components added, all registered, all smoke-tested via pytest (`libs/viz_factory/tests/test_deco2_components.py` — 38 cases) and integrity-suite test manifests in `libs/viz_factory/tests/test_data/`. README + visualisation_factory.qmd updated.

### Left Sidebar restructure — SUPERSEDED by Phase 25

> NAV-1..6 and TOOLS-1..5 superseded by Phase 25 (ADR-052) accordion redesign.
> See `tasks_phase25.md` for current implementation plan.

---

**STATUS (2026-05-01):** Phase 21 complete. Phase 22 fully implemented (22-A..F done; 22-G..J verified except 22-J-10 deferred + 22-J-13 structured test pending). Phase 23-A + 23-B complete. Phase 24 complete (ADR-051). **Phase 25 DESIGNED (ADR-052) — ready to implement.** See `tasks_phase25.md` for per-step change manifests. Pre-flight + 25-A/B/C next. Open bugs carried forward: DEMO-1..4, AUDIT-1..4, STATE-1..2.
**Archive Pointer:** [./.antigravity/tasks/archives/tasks_archive_2026-04-10.md]
