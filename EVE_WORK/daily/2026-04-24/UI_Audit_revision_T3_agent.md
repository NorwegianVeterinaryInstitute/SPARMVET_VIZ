
---

## Analysis: Legacy vs. Current vs. Open Design Questions

Here is my review of the Gemini document against the current ADR/contract state, followed by the Tier 3 audit trace design.

---

### What is definitively LEGACY (superseded by later decisions)

| Gemini concept                                                | Why legacy                                                                                                                                                                                                                | What replaced it                              |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| **Tab A / Tab B** as the primary navigation metaphor          | Replaced by the **Tier Toggle** strip (T1/T2/T3-Wrangle/T3-Plot) + a single collapsible data accordion                                                                                                                    | ADR-043: Tier Toggle + Comparison Mode toggle |
| **"Developer Mode" vs. "Pipeline Mode"** as two hard modes    | Replaced by the **5-persona system** with feature flags. No binary mode switch — capabilities scale continuously                                                                                                          | ADR-041/ADR-043, persona templates            |
| **Bootloader reads `ui_config.yaml`** at startup              | ==Replaced by **ADR-048 Deployment Profile** (`config/connectors/local/`) + persona templates.== `ui_config.yaml` doesn't exist as described                                                                              | ADR-048 + persona feature flags               |
| ==**Synced brushing with plot selection → row highlight**==   | Not implemented yet. No grid↔plot sync described in contract                                                                                                                                                              | Phase 22+ (deferred)                          |
| ==**Annotation on plot brush** triggering a mandatory modal== | Partially superseded: the mandatory comment is now on the **Yellow Node** in the audit stack (§3 of contract), not a standalone modal per brush. The modal concept survives but is integrated into the node comment field | §3 Audit Gatekeeper                           |
| **Sidebar gains "Wrangling" tab in developer mode**           | Replaced: the right sidebar IS the audit/wrangling stack (visible for `pipeline_exploration_advanced`+). There is no separate "wrangling tab"                                                                             | Right Panel / Pipeline Audit                  |
| **"Ghost Manifest"** saving to `tmp/last_state.yaml`          | ==Refined: now `_autosave.json` in Location 4. Deferred Phase 22+==                                                                                                                                                       | §7.1 Ghost save                               |
| ==**Pandoc report generation**==                              | The concept survives but the format is now `report.qmd` (Quarto) in the export bundle, not a plain Pandoc `.txt`                                                                                                          | §7.2 Export Bundle                            |

---

### What is ACTIVE (implemented or formally decided)

- **3-tier data model** (T1 Anchor / T2 Branch / T3 Leaf) — fully formalized
- **No Trace, No Export** (mandatory comment on every Yellow node before Apply is enabled) — §3 contract
==- **Export bundle** (`.zip` with plots, T1/T2/T3 data, YAML recipes, `report.qmd`, `FILTERS.txt`, `README.txt`) — §7.2, Phase 21-I==
- **Session save/restore** (named `.json` in Location 4, multiple sessions) — designed in §7.1, deferred Phase 22+
- **Filter Recipe Builder** (left sidebar, row filters `{column, op, value}`) — Phase 21-F, implemented
- **Right sidebar = Pipeline Audit** (persona-gated, visible ≥ `pipeline_exploration_advanced`) — ADR-044
- **Gallery isolation boundary** — gallery serves pre-rendered assets only, no runtime Polars

---

### What is UNDECIDED / NOT YET FORMALLY SPECIFIED

Two things from your message are genuinely open:

1. **The full Tier 3 audit trace content and format** — what exactly gets recorded, how it is structured, what is mandatory
2. **Module state memory** — when switching Home ↔ Gallery, what state is recalled per module

---

### Tier 3 Audit Trace — Design Proposal

Based on your requirements (full transparency, mandatory reason, save to manifest/session, gallery recipe export, module state), here is what I think should be decided:

**What triggers an audit entry:**

| User action                                    | Entry type                            | Mandatory reason?                                                    |
| ---------------------------------------------- | ------------------------------------- | -------------------------------------------------------------------- |
| Filter row added (left sidebar Filter Builder) | `filter` node — Yellow                | No (filters are exploratory, lightweight)                            |
| Brush on T3 plot → row exclusion               | `exclusion` node — Yellow             | **YES** — blocks Apply until filled                                  |
| Column drop in T3 table                        | `drop_columns` node — Yellow          | **YES** — blocks Apply until filled                                  |
| Advanced filter in T3 table                    | `filter` node — Yellow                | **YES** — blocks Apply until filled                                  |
| Violet node modified (T2 blueprint changed)    | Modified `violet` node                | **YES** — blocks Apply, warns "blueprint change"                     |
| Node disabled (power-off icon)                 | Strikethrough + `disabled: true` flag | **YES** — reason required                                            |
| Revert (btn_revert)                            | Clears all Yellow nodes               | Records "Reverted to T2 blueprint" automatically, no reason required |

**What each entry contains:**

```yaml
- id: "node_20260424_143201_01"
  type: "exclusion"          # filter | exclusion | drop_columns | blueprint_override | disabled
  action: "filter_eq"        # wrangling action name
  params:                    # action parameters
    column: "sample_id"
    value: "S_LAB_042"
  reason: "Sample S_LAB_042 misidentified — instrument X failed on 2026-04-20. Confirmed by lab manager."
  timestamp: "2026-04-24T14:32:01"
  applied: true              # false = pending (not yet btn_apply pressed)
  tier: "T3"
  plot_context: "AMR_gene_distribution"   # which sub-tab was active
```

**What the "audit" sidebar shows:**

- Ordered list of Yellow nodes (most recent at top or bottom — to decide)
- Each node shows: action type + key params + reason field (editable inline) + disable/trash controls
- Color coding: Violet inherited, Yellow user-added
- **Apply button state** gated on: at least one pending node AND all Yellow/modified nodes have non-empty reason

**Saving the audit trace:**

Three paths for saving:

1. **Ghost save** — auto on every `btn_apply`, writes `_autosave.json` to Location 4 (Phase 22+)
2. **Session save** — explicit named save, includes full `t3_recipe` as the audit trace
3. **Export bundle** — `FILTERS.txt` covers row filters; the T3 YAML recipe in `recipes/` covers the full audit trace as a wrangling recipe. The `report.qmd` should render the audit nodes as a "Methods" table

**Open question on FILTERS.txt vs. T3 recipe:** Currently the contract has `FILTERS.txt` for filter trace and the YAML recipe for wrangling. For the audit trace, these should be **unified** — the T3 recipe IS the audit trace, and `FILTERS.txt` should be renamed/merged. The reason field in each node makes it a human-readable audit log too.

**Gallery → T3 recipe export:**

The Gemini document raised this: a gallery recipe should be exportable as T3 steps. The current contract says the gallery is read-only and "transplants" YAML into the T3 sandbox. This is already the right direction — the gallery recipe's `wrangling` block would be cloned as Yellow nodes into the T3 recipe.

Two things are undecided:

- Does transplanting from Gallery require reasons on the cloned nodes immediately, or can it be deferred until `btn_apply`?
- When the user switches Home → Gallery → Home, do the T3 nodes survive, and does the gallery know which sub-tab was active to offer context-relevant recipes?

**Module state memory** (Home ↔ Gallery transitions):

The contract says filters are preserved across panel switches but the filter UI is only mounted when Home is active (§11). The same logic should apply to T3 state: `t3_recipe` reactive value survives the panel switch, the last active sub-tab survives. This means:

- Gallery "Export to T3" always goes to the Home T3 sandbox for the **last-active plot sub-tab**
- Switching Home → Gallery → Home restores: active group tab, active plot sub-tab, tier toggle state, pending/applied filters, T3 recipe nodes

This is not yet formally specified — the contract says filter state is preserved but doesn't define the full Home module state object.

---

**What I recommend we formally decide and add to the contract:**

1. The full audit node schema (above)
2. Unify `FILTERS.txt` into the T3 recipe — filters are wrangling nodes too
3. Gallery transplant → Yellow nodes, reasons required before Apply (not at transplant time)
4. Define the Home module state object that survives panel switches (sub-tab, tier toggle, filters, T3 recipe)
5. Whether the audit sidebar (right panel) shows nodes chronologically or in execution order


Shall I draft these as a formal addition to `ui_implementation_contract.md` once we've agreed on the decisions above?


## Confirmed Decisions — Synthesis

**Audit trace completeness:** All T3 interactions are recorded — filter rows, selections/exclusions, any transformations added by the user. Every Yellow node requires a reason before Apply. The T3 recipe IS the audit trace — there is no separate `FILTERS.txt` for T3. The T3 YAML recipe covers the full sequence from start to end (all nodes, in execution order), and is the artifact that goes into the export.

**Node ordering in audit sidebar:** Most recent at top (display order), execution order is bottom-to-top reading (or the recipe is stored top-to-bottom in execution order and displayed reversed). Reverting order is trivial — just reverse the display list, the underlying recipe stays in execution order. Not a difficult change.

**Ghost saves — two distinct slots:**

- **T1/T2 ghost**: written once when data is first assembled, re-written only when new data or manifest change triggers a rebuild. This is an anchor, not a session file.
- **T3 ghost**: written on every `btn_apply` AND when switching away from a plot sub-tab (to prevent loss mid-edit). Separate file, separate lifecycle. Also written when switching Home → Gallery.

**T3 recipe = filter + select + any added transformations:** The left sidebar filter rows are Yellow nodes in the T3 recipe. Selections/exclusions are Yellow nodes. Any additional transformation nodes are Yellow nodes. There is only one recipe artifact. The recipe structure is the same YAML format as a manifest wrangling block, making it machine-readable and re-executable.

**Adding a new transformation node (non-filter):** This is a real open question — how does the user enter a new wrangling node? Options:

- **A): Action picker UI** — dropdown of registered actions + auto-generated param fields (like a form)
- **B): YAML text input** — paste a manifest snippet directly
- **C): Gallery transplant** — clone a recipe from the gallery (which already has structured nodes)

For `pipeline_exploration_advanced` persona (target for T3), option A or C is more appropriate than raw YAML. Option B is developer territory. My recommendation: A for the standard T3 sandbox, B only for `developer` persona.

**Export — the report:**

- Content: all plots (saved files, paths linked in report), T3 data snapshot, full T3 recipe as audit trace with reasons, timestamps
- Format: **HTML** (via Quarto render — simpler than PDF, portable, no LaTeX dependency)
- Manifest traceability: include a hash of the source manifest (SHA256 of the master YAML) in the report front-matter — links the T3 session back to the pipeline version it was derived from
- Pandoc export to DOCX/PDF available as a secondary step (user-triggered from the HTML, or a separate button)
- The "Methods" section of the report renders each Yellow node as plain English (template-based: e.g., "Samples matching `sample_id = S_LAB_042` were excluded. Reason: instrument failure.")

**Gallery → T3 transplant:**

- Reasons deferred until `btn_apply` — nodes cloned as Yellow without reasons, Apply blocked until filled
- Gallery knows the last-active Home sub-tab and clones into that specific sub-tab's T3 recipe
- A T3 ghost save triggers when switching Home → Gallery (to protect current work)

**Home module state object** (survives all panel switches):

```
active_group_tab: str
active_plot_subtab: str  
tier_toggle: "T1"|"T2"|"T3_Wrangling"|"T3_Plot"
applied_filters: list[FilterRow]          # committed row filters (also Yellow nodes)
_pending_filters: list[FilterRow]         # staged but not yet applied
t3_recipe: list[RecipeNode]               # the full T3 audit trace, in execution order
t3_recipe_pending: bool                   # True if unsaved changes since last Apply
accordion_plot_expanded: bool
accordion_data_expanded: bool
```

**T1/T2 table filter/select = transient preview only:** No audit entry, no Apply gate, resets on sub-tab change. Confirmed.

---

One remaining open question before I write this to the contract:

**When the user adds a non-filter node in T3 (option A — action picker) — does the action picker offer ALL registered transformer actions, or a curated subset appropriate for T3 exploration?**

My intuition: a curated subset for `pipeline_exploration_advanced` (filter, exclusion, rename, fill_nulls, replace_values, add_constant, drop_columns), and the full registry only for `developer`. This prevents a bioscientist from accidentally running `pivot` or `sink_parquet` mid-session. Do you agree with that boundary, or should `pipeline_exploration_advanced` get the full registry?

Once you confirm that, I'll write the full §12 Tier 3 Audit Trace + the Home module state spec into `ui_implementation_contract.md`, and update `rules_ui_dashboard.md` to reflect the unified T3 recipe / audit trace model.


# Good — this is exactly the right place to pause. The T3 scope is the crux of everything else.

---

## The Core Tension

You're identifying a real architectural boundary. The question is: **what is T3 actually for?**

Two philosophically different answers lead to very different systems:

**Answer A — T3 is a "Publication Finisher"** The pipeline produced correct results. The scientist wants to clean up the presentation: exclude a contaminated outlier, focus on a subset of categories, adjust which columns are visible. These are **data selection and view adjustments**, not data transformation. The audit exists to document _why_ something was excluded, not _what_ was computed.

→ T3 = filters + column selection + exclusions only. No action picker. Plain-language audit report works perfectly because every action is a simple "included/excluded X because Y."

**Answer B — T3 is a "Lightweight Wrangling Sandbox"** The scientist needs to do small transformations (rename a category, fill a null, derive a simple column) that weren't anticipated in the pipeline. This requires an action picker with parameters.

→ T3 = mini-wrangling layer. The audit report becomes more complex. The UI becomes much harder to build and use correctly.

---

## My Recommendation: Answer A, with one escape hatch

Keep T3 strictly to **select + filter + exclusion**. Here is why:

1. **Your user is a bioscientist, not a developer.** An action picker with `unpivot`, `regex_extract`, `coalesce` etc. would be confusing and dangerous — wrong transforms on T3 data silently invalidate the scientific result.
    
2. **The "Methods" template only works cleanly for A.** "Samples where identity < 90% were excluded. Reason: below quality threshold." is publication-ready. "Samples were unpivoted on columns [gene, class]. Reason: ???" is not something a bioscientist writes in a methods section.
    
3. **The Blueprint already exists for anything more complex.** If a user needs a real transformation, the correct workflow is: request it from a developer → developer adds it to the T2 manifest → the pipeline re-runs → T3 starts clean. This is a feature, not a limitation — it enforces that pipeline logic stays in the pipeline.
    
4. **Gallery nodes as T3 source:** The gallery should be inspiration for _developers building new manifests_, not a source of runtime wrangling nodes for scientists. Transplanting a gallery recipe into T3 would bypass the audit gate and introduce complex nodes that don't produce clean plain-English methods text.
    

**The one escape hatch:** For `developer` persona only, allow raw YAML node injection (option B from before). This is already gated, explicitly developer territory, and doesn't affect the user-facing design.

---

## Proposed T3 Scope (for decision)

|T3 action|Persona|Audit entry|Methods text template|
|---|---|---|---|
|Row filter (column op value)|All with T3 access|Yellow node, reason required|"Samples where `{col}` {op} `{val}` were excluded. Reason: {reason}."|
|Row exclusion by brush/selection|All with T3 access|Yellow node, reason required|"Samples `{ids}` were manually excluded. Reason: {reason}."|
|Column visibility (show/hide)|All with T3 access|Yellow node, reason required|"Column `{col}` was hidden from analysis. Reason: {reason}."|
|Raw YAML node injection|`developer` only|Yellow node, reason required|Rendered as-is (no template)|

Gallery remains read-only reference — no transplant into T3. Export to T3 is removed from gallery scope.

---

This keeps the system buildable, the audit report meaningful, and the user experience clean. The gallery question and module state question both simplify considerably once this boundary is set.

Do you agree with Answer A + developer escape hatch, or do you want to keep some middle ground (e.g., a small curated list of 3-4 safe actions like `fill_nulls`, `replace_values`, `rename`)?


# ## Final T3 Scope — Confirmed

**Core T3 actions (all personas with T3 access):**

- Row filter (column op value) — Yellow node, reason required
- Row exclusion by brush/manual selection — Yellow node, reason required
- Column visibility (show/hide) — Yellow node, reason required

**Plot aesthetic overrides (potential addition — lightweight, no data change):** Color, fill, transparency, shape for points/categories. These are pure `plot_spec` overrides — they don't touch the data at all, only the VizFactory render parameters. They would be a separate category of Yellow node: `aesthetic_override`. No reason required for aesthetic changes (no scientific justification needed for "I changed the color to blue"). This keeps the audit clean — only data decisions need justification.

**Developer escape hatch:** Raw YAML node — pasted as a manifest wrangling snippet, validated against the action registry before allowing Apply. Reason required. No plain-English template — rendered verbatim in the report.

---

## Module State — Confirmed Simple Rule

**Every top-level panel (Home, Gallery, Blueprint) remembers its last state independently.** Switching panels never resets anything. This is the same principle as browser tabs — you leave, you come back, you are where you were.

The ghost save question for Gallery ↔ Blueprint is separate — that is about Blueprint's T3-equivalent (the sandbox in the architect), which we don't need to design now.

---

## One Last Clarification Before Writing

The **aesthetic override nodes** — should these:

**Option 1:** Be part of the T3 recipe YAML (so they are re-applied on re-run and included in the export bundle as part of the recipe)

**Option 2:** Be stored separately in the plot spec, outside the wrangling recipe (cleaner separation — data recipe vs. plot config)

My recommendation is **Option 2** — aesthetic overrides live in the plot spec layer (`plot_config` overrides), not in the wrangling recipe. This means:

- The T3 wrangling recipe contains only data decisions (filters, exclusions, column visibility)
- The aesthetic overrides are a separate `t3_plot_overrides` dict per plot sub-tab
- Both are saved in the session file and the export bundle
- The audit report lists data decisions (with reasons) separately from aesthetic choices (no reasons)
- Clean separation: wrangling engine never sees aesthetic nodes, VizFactory never sees wrangling nodes

Does Option 2 feel right, or do you want everything unified in one recipe?