# Live-UI Test Checklist — Current Dashboard

**Owner:** @evezeyl
**Branch baseline:** `dev` (Phase 26 + session fixes + T3 data / compare / flicker fixes — 2026-05-02)
**Replaces:** `tasks_test_22J.md` (Phase 22-J scoped, stale after Phase 24–25 refactors)
**Purpose:** Walk the running app systematically. Every section is a discrete scenario. Check boxes as you go; note symptoms when something fails — don't try to fix inline.

---

## 0. Pre-flight

- [x] `git status` shows clean working tree (or only scratch files).
- [x] `git log --oneline -1` shows a Phase 25 commit at HEAD.
- [ ] App starts: `./.venv/bin/python app/src/main.py` — UI loads without Python traceback in terminal.
- [x] No red error banners in the browser on first load.
- [x] Check terminal for `DEBUG: Rendering sidebar_nav_ui for Persona: <name>` — confirm the expected persona loaded.

---

## 1. Persona gating — what appears per persona

Test each persona by changing the `persona_id` in the active config YAML (or selecting in the UI if manifest selector is visible).

### 1a. `pipeline-static`
- [x] Left sidebar: **no** manifest selector, **no** T3 mode toggle, no right sidebar audit panel.
- [x] Tier toggle shows only T1 / T2 (no T3).
- [x] No "Gallery" or "Blueprint Architect" nav items in sidebar.
- [x] No "Session Management" or "Single Graph Export" accordion panels.
- [x] Filter panel is **absent** — not shown at all (`interactivity_enabled: false` gates the accordion out entirely).

### 1b. `pipeline-exploration-simple`
- [x] Left sidebar shows Filters accordion (interactive) but no T3 tier.
- [x] Right sidebar audit panel absent.
- [x] No developer-only panels (Test Lab, Blueprint Architect).
- [x] Gallery NOT visible.

### 1c. `project-independent`
- [x] Manifest selector accordion **visible**.
- [x] Gallery nav item visible.
- [x] Blueprint Architect (Wrangle Studio) nav item Not visible (persona updated).
- [x] T3 tier present in tier toggle.
- [x] Right sidebar aqudit panel visible with "Pipeline Audit" header.
- [x] Session Management accordion visible.
- [x] Single Graph Export accordion visible (if `export_graph_enabled: true`).
- [x] "Test Lab" nav item **NOT** visible (developer_mode_enabled: false).

### 1d. `developer`
- [x] All of the above PLUS "Test Lab" nav item visible.
- [x] Blueprint Architect visible.

---

## 2. Left sidebar — accordion panels

Using `project-independent` or `developer` persona throughout the following sections.

- [x] **Manifest Choice** accordion opens/collapses cleanly. Project selection dropdown shows available projects.
- [x] Changing project selection reloads plots in the center theater (may take a moment).
- [x] **Data Import** accordion shows the import UI (file upload or path selector depending on persona).
- [x] **Filters** accordion opens cleanly with the filter builder form.
- [x] **Global Project Export** accordion visible and contains export button.
- [x] **Single Graph Export** accordion visible (if enabled for persona).
- [x] **Session Management** accordion visible (if enabled).
- [x] Accordion open/close state is independent — opening one does not close others.
- [x] Persona name shown below nav pills: "Active: Project Independent User" (or equivalent). Ok - now defined by the persona config, we can have any Persona name. 

---

## 3. Center theater — tabs and plot rendering

- [x] Tabs at top of center panel correspond to analysis groups in the active manifest.
- [x] Clicking each tab loads its plots (no Python traceback in terminal).
- [x] Within a tab with multiple plots, sub-tabs navigate between individual plots.
- [x] Plot renders as a static image (plotnine via `@render.plot`).
- [ ] **Data Preview** accordion below the plot shows a table of ~100 rows from the active plot's dataset.
- [x] Data preview updates when you switch plot sub-tabs.
- [x] **Column selector absent for pipeline-static / pipeline-exploration-simple**: no "Visible columns (preview only)" or "Columns (drop unselected via audit)" control shown (`interactivity_enabled: false` — `home_col_selector_ui` returns empty div).
- [x] **Thin header strip** at top of center panel shows: dataset label (left) + tier toggle radio buttons (right).
- [x] Tier toggle shows T1 / T2 for pipeline personas; T1 / T2 / T3 for advanced personas.

---

## 4. Tier toggle behavior

### 4a. T1 → T2

- [x] Switch to T2. Plot and data preview update (if T2 transforms are defined in the manifest — otherwise visually identical to T1 is expected). [Year Distribution plot for test]
- [x] No flickering or duplicate renders in the terminal output.

### 4b. T1 / T2 → T3

- [x] Switch to T3. Plot header or data preview header updates to indicate T3 mode.
- [x] Left sidebar "Filters" panel **Apply button** label changes from `Apply (N)` to `➜ Audit (N)`.
- [x] Right sidebar shows "Pipeline Audit" card with "Tier 2 — Inherited" and "Tier 3 — My Adjustments" sections. [We modified the design but this is correct]

### 4c. Tier toggle stability

- [x] Toggling T1 → T3 → T1 does not change the active plot sub-tab.
- [ ] Switching panels (Home → Gallery → Home) does not reset the tier toggle. [But it reset which manifest I am looking AT - That should be better if it was going back to previous viewing state]
- [x] T2/T3 comparison mode toggle stays on the correct plot after switching. *(STATE-1/STATE-2 fixed 2026-05-02 — note if regression.)*

---

## 5. Filter panel (T1 / T2 mode)

### 5a. Basic filter — string column

- [x] In **Filters** accordion, select a **string** column (e.g. `species`, `country`).
- [x] Operator dropdown shows: `= equal`, `≠ not equal`, `∈ any of`, `∉ none of` (no `between`). *(`= equal` with multiple values auto-promotes to `∈ any of` at add-time — intentional, by design.)*
- [x] Enter a value. Click `+ Add`. A staged row appears below the form.
- [x] Click `Apply (1)`. Data preview updates to show only matching rows.
- [x] Plot updates to reflect the filter.
- [x] "Reset filters" clears the staged row and restores the unfiltered view.

### 5b. Basic filter — numeric column

- [x] Select a **numeric** column.
- [x] Operator dropdown includes `↔ between`.
- [x] Select `between` → form shows two numeric inputs (lo / hi), not a text box.
- [x] Inclusivity buttons show `≤ inclusive` and `< exclusive`. *(SOLVED: was "≤ ≤ inclusive" / "< < exclusive")*
- [x] Enter a range. Click `+ Add`. Staged row shows the range.
- [x] Click `Apply`. Data preview shows only rows within the range.
- [x] Switch back to a different operator (e.g. `>`). Form reverts to a single input.
- [x] Switch to a different column and back — operator resets to the first valid option for that column's type.
- [x] Int column shows integer default value (e.g. `2022` not `2022.0`), step = 1. *(SOLVED: col_min/max now typed as int for Int/UInt columns)*
- [x] Reset clears the value widget (selectize / text input). *(SOLVED: `update_selectize` + `update_text` called on reset)*
- [ ] **CONSIDER**: Filter choices (selectize options) are not updated after Apply — excluded values still appear in the picker. Updating choices from the filtered data is possible but means you can't add back a filter without Reset. Decide before implementing.

### 5b-extra: Trash button style
- [x] 🗑 in filter staged rows matches 🗑 in audit panel (same `btn-link` red style). *(SOLVED: aligned to `btn btn-sm btn-link p-0` / `color:#dc3545`)*

### 5c. Multiple staged rows

- [x] Add two filter rows (different columns). Both appear staged.
- [x] Click `Apply (2)`. Both filters apply (AND logic).
- [x] Remove one row with the 🗑 icon — count badge updates; clicking Apply again applies only the remaining row.

---

## 6. Filter panel (T3 mode) — staging to audit

- [x] Switch to T3 mode.
- [x] Build a filter on a **non-key column** (e.g. `species eq E. coli`). Click `+ Add`.
- [x] Click `➜ Audit (1)`.
- [x] **Propagation modal opens**. Header: "Add 1 filter/exclusion(s) — choose scope". Summary lists the column.
- [x] **No** ⚠️ Primary-key warning banner (since this is not a join key).
- [x] Pick **"This plot only"** → confirm.
- [x] Right sidebar "Tier 3 — My Adjustments" shows a pending node with yellow reason input.
- [x] Type a reason. `Apply` button transitions from "Apply ⛔" (no reason) to enabled "Apply".
- [x] Click Apply. Notification: "✅ T3 recipe applied — N node(s) across 1 plot stack(s)."
- [x] Plot and data preview reflect the filter.
- [x] Switch to another plot sub-tab → that plot is **unaffected** (per-plot scoping).

[Homogeneize css style of the button trash/bin with the trash/bin button from filters]
---

## 7. T3 audit — primary key column (silent conversion to exclusion)

- [x] In T3 mode, build a filter where **column = primary key** (e.g. `sample_id`).
- [x] Click `+ Add` then `➜ Audit (1)`.
- [x] Modal opens with a ⚠️ banner: "One or more nodes target a join key…"
- [x] Pick **"All plots"** → confirm.
- [x] Pending node in right sidebar shows icon **🚫 Exclusion** (not 🔍 Row Filter).
- [x] Node has ⚠️ Primary key warning banner.
- [x] Switch to another plot sub-tab → the same pending node appears there too.
- [x] Type a reason on one plot; click Apply. Both copies commit.
- [x] The excluded sample disappears from the data preview on every plot.

---

## 8. T3 audit — "All plots except" scoping

- [x] In T3, build a filter on the primary key column for a different sample.
- [x] In the propagation modal, pick **"All plots except…"**.
- [x] In the multiselect, pick one "QC plot" (any sub-tab).
- [x] Confirm. Pending nodes appear in every plot **except** the QC plot.
- [x] Switch to the QC plot → no pending node for this sample.
- [x] Apply. The QC plot still shows the sample; all others do not.

---

## 9. T3 audit — drop column

### 9a. Non-key column drop

- [x] In the Data Preview, open the "visible columns" multiselect and **deselect** a non-key column.
- [x] `➜ Audit drops (1)` button activates.
- [x] Click it → propagation modal with "Drop 1 column(s)" header; no PK warning banner.
- [x] Pick "This plot only" → confirm.
- [x] Pending `drop_column` node (✂️) in right sidebar.
- [x] Type reason, Apply. Column gone from data preview for this plot; other plots unaffected.

### 9b. Primary key column drop — blocked

- [x] Deselect the primary key column (e.g. `sample_id`).
- [x] Click `➜ Audit drops (N)`.
- [x] Notification: red error "Cannot drop join key column(s)…". No node added.
- [x] Re-select the column; count badge resets to 0.

---

## 10. T3 audit — node deletion

- [ ] After committing a node propagated to multiple plots, switch to any plot → click the 🗑 next to the node.
- [ ] Notification: "🗑 1 audit decision(s) deleted (N copy/copies across plots)."
- [ ] Switch to other plots → the node is gone everywhere.
- [ ] Data preview reverts (the filtered sample / column returns).

[A little hover on mouse or note for the user that tries to remove a primary key
and when there is a Row filter on primary key - My user are not familiar with what
a primary key is for - so simple term, explaining potential consequences ... and short. A more extended documentation on this is welcome - for my non compute science users]
---

## 11. Right sidebar — Blueprint Architect context

- [ ] Click **Blueprint Architect** in the nav pills.
- [ ] Center panel switches to the TubeMap diagram.
- [ ] Right sidebar header changes to **"Blueprint Surgeon"**.
- [ ] "No node selected" message shown until you click a TubeMap node.
- [ ] Click a node in the TubeMap → right sidebar shows "Focused: `<node_id>`" and logic stack step count.
- [ ] Click Home in nav pills → right sidebar reverts to "Pipeline Audit".

---

## 12. Gallery nav

- [ ] Click **Gallery** in nav pills (project-independent or developer persona).
- [ ] Center panel shows the gallery recipe browser.
- [ ] Left sidebar shows "Discovery Mode Active" message (no filter or project panels).
- [ ] Gallery sidebar on the left of the gallery (or within the panel) shows filter checkboxes for tags/categories.
- [ ] Clicking a gallery card loads the recipe preview on the right pane.
- [ ] Click Home → center panel returns to plots, left sidebar tools re-appear.

---

## 13. Comparison mode (project-independent / developer)

- [ ] In T3 mode, look for the **comparison mode toggle** below the tier toggle strip. *(Only appears for personas with `comparison_mode_enabled: true` in T3 mode.)*
- [ ] Toggle it on. Center panel shows two columns (reference vs. adjusted view), or the layout changes to show comparison.
- [ ] Toggle it off. Returns to single-panel view.
- [ ] *(Known issue AUDIT-4: Compare T2/T3 toggle may lose state on plot switch — note if that occurs.)*

---

## 14. Session management

- [ ] Open **Session Management** accordion in left sidebar.
- [ ] Commit at least 2 T3 nodes across different plots.
- [ ] Wait 2 minutes (ghost auto-save interval for developer/project-independent personas) OR use a manual save button if present.
- [ ] Close and restart the app.
- [ ] Session ghost should auto-restore, OR use **"Restore session"** button.
- [ ] All committed T3 nodes reappear in their per-plot panels.

---

## 15. Global Project Export

- [ ] Open **Global Project Export** accordion.
- [ ] Click the export button.
- [ ] A `.zip` bundle downloads (or a path is reported in the terminal).
- [ ] Bundle contains at minimum: the assembled data, a recipe/filter trace, and a plot export.
- [ ] *(EXPORT-2/EXPORT-3 selective export and Quarto report polish are open items — don't test those specifics here.)*

---

## 16. Single Graph Export

- [ ] Open **Single Graph Export** accordion.
- [ ] Pick a plot from the selector.
- [ ] Click export → PNG or SVG downloads for that single plot.

---

## 17. Regression checks

These are known open bugs — record whether they reproduce or seem fixed.

- [x] **STATE-1**: Plot flicker on T3 toggle / panel switch — fixed 2026-05-02 (per-plot cell handlers + CSS hide/show). Note if regression.
- [x] **STATE-2 / AUDIT-4**: Compare T2/T3 toggle wrong-plot-wins — fixed 2026-05-02, user-verified. Note if regression.
- [x] **UX-1**: Plot rendering slow — parquet cache fast path in place. Note if still sluggish.
- [ ] **UX-2**: "Visible columns" multiselect in Data Preview is narrower than the panel. Note if still present.
- [x] **BUG-PERF-1**: `materialize_tier1` skip-if-exists guard confirmed — only fires on cache miss. Note if repeated calls observed in terminal.

---

## 18. Edge cases

- [ ] Click Cancel in the propagation modal → no node added, no pending state left.
- [ ] Click `➜ Audit (0)` with 0 staged rows → should show a notification asking you to add rows first (or button should be disabled).
- [ ] Add 2 filters on the same column with different values → both become separate nodes, propagate independently.
- [ ] Schema-skip: author a filter on a column that exists in only some plots, propagate "All plots" → notification should mention skipped plots.

---

## 19. Data Import (IMPORT-1)

Using `project-independent` or `developer` persona (the **Data Import** accordion must be visible).

### 19a. Single file upload

- [ ] Open **Data Import** accordion in left sidebar.
- [ ] Click the file upload control and select a single TSV/CSV that matches a dataset schema (e.g. `metadata.tsv` for the `metadata` dataset ID).
- [ ] An **assignment table** appears: one row per uploaded file, with a dropdown showing available dataset IDs from the manifest.
- [ ] The correct dataset ID is pre-selected (or selectable). Click **Apply**.
- [ ] Terminal shows no Python traceback. A success notification appears.
- [ ] The plots reload with the new data (parquet cache busted — first load may be slightly slower).

### 19b. Validation error — wrong schema

- [ ] Upload a file that does NOT match any dataset schema (e.g. wrong column names).
- [ ] Per-file error block appears below the assignment row: shows which columns are missing, which have wrong type, etc.
- [ ] No data is written; the parquet cache is NOT busted.
- [ ] Re-upload the corrected file → assignment table resets; apply succeeds.

### 19c. Multi-file upload

- [ ] Hold **Ctrl/⌘** and select two files for two different datasets.
- [ ] Assignment table shows one row per file with independent dataset dropdowns.
- [ ] Assign each to the correct dataset ID. Click Apply.
- [ ] Both datasets reload; plots that depend on each one update independently.

### 19d. Duplicate dataset assignment

- [ ] Upload two files but assign both to the same dataset ID.
- [ ] Expect either a validation error or the second assignment overwrites the first — note observed behavior.

---

## 20. Integer axis breaks (`breaks_integer: true`)

Test with the `year_distribution` plot (uses `scale_x_continuous` with `breaks_integer: true`).

- [ ] Navigate to the plot that shows year on the x-axis (e.g. "Year Distribution" in the test manifest).
- [ ] X-axis labels are whole integers (`2018`, `2019`, …) — no decimals (`2019.0`).
- [ ] Toggle T1 → T2 → T1: axis labels remain integers throughout.
- [ ] No Python traceback in terminal related to `MaxNLocator` or `breaks`.

---

## 21. Filter widget types and reset behavior

### 21a. Integer column widget

- [ ] In Filters accordion, select a column typed `Int64` or `Int32` (e.g. `year`).
- [ ] Operator `= equal`: value input shows integer step (1), default value is a whole number (e.g. `2022` not `2022.0`).
- [ ] Operator `↔ between`: lo/hi inputs both show integer values and step = 1.

### 21b. Float column widget

- [ ] Select a column typed `Float64`.
- [ ] Operator `= equal`: value input shows decimal default (e.g. `0.95`).
- [ ] Operator `↔ between`: lo/hi inputs show float values.

### 21c. Reset clears value widget

- [ ] Add a filter row (string column with selectize, or text input). Click `+ Add`.
- [ ] Click **Reset filters**.
- [ ] The value input (selectize or text box) is cleared — no stale value remains from before. *(SOLVED: `update_selectize` + `update_text` called on reset)*

### 21d. `between` inclusivity labels

- [ ] Select a numeric column, choose `↔ between`.
- [ ] Radio buttons show `≤ inclusive` and `< exclusive` (single symbol each — not `≤ ≤ inclusive`). *(SOLVED)*

---

## What to do when something fails

1. Note the **section number** and what you saw vs. what was expected.
2. Screenshot the affected panel + terminal output if possible.
3. Don't try to fix it inline — add a `[ ] BUG: <description>` note below the failed item and continue.
4. Known open bugs (STATE-1, STATE-2, AUDIT-4, BUG-PERF-1) are already tracked — confirm reproduction or mark as not-seen.

---

## Known deferred / not tested here

- **PROP-2/PROP-3**: Filter inventory panel and TubeMap blast-radius view — not implemented.
- **UX-NOTIF-1**: Toast notifications → notification log panel — not implemented.
- **22-J-10**: Aesthetic propagation (color/shape/fill) — no authoring path yet.
- **THEATER-1**: Collapse/minimize plot panel — not implemented.
- **EXPORT-SGE-7 / IMPORT-1 multi-assign edge cases**: Dataset-to-plot mapping when datasets share field names — design decided (Option B assignment table) but not exhaustively tested.
- **Playwright automated UI tests**: 2 tests skipped (`test_reactive_audit_gate`, `test_persona_switch_reactivity`) — stale premises, see `test_reactive_shell.py`.

---

**Reference docs:**
- `docs/user_guide/audit_pipeline.qmd` — user-facing audit walkthrough
- `.antigravity/knowledge/architecture_decisions.md` — ADR-049 (per-plot scoping), ADR-052 (right sidebar gating), ADR-053 (flag-only persona gating)
- `.antigravity/tasks/tasks.md` — open bug list
- `.antigravity/tasks/archives/tasks_archive_phase25.md` — Phase 25 completed items
