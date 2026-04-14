# Persona Traceability Matrix (Component Masking)

**Objective**: Systematic verification of UI stability, functional parity, and persona masking, superseding the UI Contract traceability.

## Layout & Reactive Matrix

The UI dynamically alters element availability based on the active persona profile. The configurations within `config/ui/templates/` must map exactly to these 5 primary definitions:

| Persona Profile | Left Panel Elements | Tier 3 (Right Panel) / App UI | Advanced Filters / Registry |
| :--- | :--- | :--- | :--- |
| **1. Pipeline-static** | Basic loading & export allowed. | Fully Hidden / Disabled. View is locked to 1x2 grid (Ref modes only). | None |
| **2. Pipeline-Exploration-simple** | Project loader, basic Session. | Tier 3 is toggleable/collapsible. Revert enabled. | Basic schema pickers and simple dropdown filters. |
| **3. Pipeline-Exploration-advanced** | Standard left panel features. | Full active plotting, Tier 3 Single Stack wrangling enabled. | Includes Mathematical Expressions & Interval ranges. |
| **4. Project-independent** | Full Nav + External Import helper. | Full active plotting + Sandbox + Revert. | Same as advanced. |
| **5. Developer-mode** | Dev studio mode, Gallery browser. | Full interactive sandbox. | Complete access to every `@register_action` in the codebase. |

## Element Behaviors

| UI Category | Element ID | Functionality / Rule |
| :--- | :--- | :--- |
| **Navigation** | `project_id` | Project discovery and loading |
| **Navigation** | `persona_selector` | Persona switching (changes active masking template) |
| **Navigation** | `export_global` | Session bundling/export |
| **Filters** | `tier1_tier2_filters` | Visual only - does not alter underlying data logic. |
| **Filters** | `tier3_filters` | Appends transformation steps (e.g. drop column) to `t3_recipe` |
| **Theater** | `theater_layout` | Dynamic shifts between 1x2 and 2x2 depending on Tier 3 activation |
| **Theater** | `btn_max_pane` | Maximizes one pane, converts other 3 into minimized edge tabs |
| **Audit Stack** | `t3_recipe` | A SINGLE position-aware stack; inherited T2 (Violet), user (Yellow) |
| **Audit Stack** | `btn_revert` | Restores `t3_recipe` to the original T2 blueprint |
| **Audit Stack** | `btn_apply` | Executes recalculation of T3 workflow; GATED by mandatory comments |

*Note: Tier 1 and Tier 2 are immutable caches backed by Parquet files. Modifications/recalculations on the Sandbox only affect Tier 3.*
