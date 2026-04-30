# Persona Traceability Matrix (Component Masking)

**Objective**: Systematic verification of UI stability, functional parity, and persona masking, superseding the UI Contract traceability.
**Last updated:** 2026-04-30 (Session 8 — Phase 21-E/G/H complete)

## Layout & Reactive Matrix

The UI dynamically alters element availability based on the active persona profile. The configurations within `config/ui/templates/` must map exactly to these 5 primary definitions:

| Persona ID | Display Name | Right Sidebar | T3 Tier | Comparison Mode | Gallery | Blueprint | Session Mgmt |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `pipeline-static` | Automated Pipeline — Static | **Hidden** | ❌ | ❌ | ❌ | ❌ | ❌ |
| `pipeline-exploration-simple` | Pipeline Exploration — Simple | **Hidden** | ✅ (toggle) | ❌ | ❌ | ✅ | ✅ |
| `pipeline-exploration-advanced` | Pipeline Exploration — Advanced | **Visible** | ✅ | ✅ | ❌ | ✅ | ✅ |
| `project-independent` | Project Independent User | **Visible** | ✅ | ✅ | ❌ | ✅ | ✅ |
| `developer` | Workflow Developer | **Visible** | ✅ | ✅ | ✅ | ✅ | ✅ |
| `qa` | QA / Test Harness | **Visible** | ✅ | ✅ | ✅ | ✅ | ✅ |

> **CRITICAL**: Persona IDs use **hyphens** (`pipeline-exploration-advanced`), never underscores. Underscore variants silently fail all persona gates. See Phase 22-H-2 for the bug history.

> **PERSONA-2 (2026-04-30)**: `qa` is a test-harness persona — same feature surface as `developer` but with `ghost_save.enabled: false` for deterministic automated testing. Not for end-users; intended for CI / regression smoke runs / future Playwright tests.

## Element Behaviors

| UI Category | Element ID | Functionality / Rule |
| :--- | :--- | :--- |
| **Navigation** | `project_id` | Project discovery and loading |
| **Navigation** | `persona_selector` | Persona switching (changes active masking template) |
| **Navigation** | `export_global` | Session bundling/export |
| **Tier Toggle** | `tier_toggle` | Radio strip: T1 (Assembled) / T2 (Analysis-ready) / T3 (My adjustments). T3 hidden for `pipeline-static` and `pipeline-exploration-simple`. |
| **Comparison Mode** | `comparison_mode` | Toggle visible only for advanced+ personas AND only when tier == T3. Splits each plot tab into 2-column layout: T2 baseline (left) vs T3 adjusted (right). |
| **Filters** | `sidebar_filters` | Recipe-builder row filter UI. In T3 mode, `➜ Audit (N)` button promotes rows into per-plot T3 audit stack instead of transient `applied_filters`. |
| **Filters** | `home_col_selector_ui` | Selectize column visibility for Data Preview. In T3 mode, `➜ Audit drops (N)` promotes deselected non-key columns to `drop_column` audit nodes. |
| **Theater** | `dynamic_tabs` | Manifest-driven: groups → `navset_pill`, plots → `navset_card_tab`. Reads `comparison_mode` for layout switching. |
| **Theater** | `home_data_preview` | DataGrid scoped to active plot's `target_dataset`. Applies committed T3 filter/drop nodes. |
| **Audit Stack** | `audit_nodes_tier2` | Violet read-only nodes (T2 blueprint steps). Visible for advanced+ personas only. |
| **Audit Stack** | `audit_nodes_tier3` | Per-plot Yellow nodes. Filtered to `home_state.active_plot_subtab`. Shows "Applied to N plots" badge and ⚠️ PK warning banner for PK-touching nodes. |
| **Audit Stack** | `audit_stack_tools_ui` | Apply button (gated — all pending nodes must have non-empty reason). Commits pending nodes into `t3_recipe_by_plot[plot_scope]` and ghost-saves. |
| **Audit Stack** | `propagation_modal` | 3-option scope dialog at T3 promotion: "This plot only / All plots / All plots except…". PK-touching nodes show ⚠️ warning banner inside modal. |
| **Audit Stack** | `🗑 delete` | Permanently removes a node and ALL linked copies sharing the same `id` across every plot stack + pending. Supersedes `btn_revert`. |
| **Session Mgmt** | `session_list_ui` | Lists all assembly/T3 ghosts. Restore + Export + Delete per session. Visible for ≥ `pipeline-exploration-simple`. |
| **Export** | `export_bundle_download` | ZIP: plots (SVG/PNG) + T1/T2/T3 TSVs + YAML recipes + Quarto `.qmd` + README. Advanced+ only for T3 data. |
| **Export** | `export_audit_report` | HTML/PDF audit report via Quarto. Methods deduplicated by linked id; PK-warning nodes prefixed `⚠️ [Primary key affected]`. Advanced+ only. |

*Note: Tier 1 and Tier 2 are immutable caches backed by Parquet files. Modifications/recalculations in the T3 audit pipeline only affect Tier 3 outputs.*

## Comparison Mode Detail (Phase 21-E)

- Toggle label: "⚖ Compare T2 vs T3"
- Gate: persona ∈ {`pipeline-exploration-advanced`, `project-independent`, `developer`} AND `tier_toggle == "T3"`
- Left column: `plot_group_{p_id}_cmp_base` — raw T1 data, NO T3 audit nodes applied (baseline)
- Right column: `plot_group_{p_id}` — same T1 data WITH committed T3 filter/drop nodes applied
- Column headers use Bootstrap badge styling: grey for baseline, amber for adjustments

## Right Sidebar Suppression (Phase 21-G / ADR-044)

- `hidden_personas = {"pipeline-static", "pipeline-exploration-simple"}` in `right_sidebar_content_ui`
- When persona ∈ `hidden_personas`: returns `ui.div()` — the sidebar slot renders empty, the theater expands to full width
- `btn_revert` concept was superseded in Phase 22-I by per-node 🗑 delete. The concept is no longer part of the UI.
