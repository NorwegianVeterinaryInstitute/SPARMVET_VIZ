# UI Traceability Matrix (ADR-034 Governance)

**Objective**: Systematic verification of UI stability, functional parity, and persona masking.

| UI Category | Element ID | Functionality | [ST22_dummy] Status | Latest Test | Failure Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Navigation** | `project_id` | Project discovery and loading | [ ] | | |
| **Navigation** | `sidebar_nav` | Sidebar Tab switching (Hub/Wrangle/Viz/Dev) | [ ] | | |
| **Navigation** | `persona_selector` | Persona switching (User/Dev) | [ ] | | |
| **Navigation** | `file_ingest` | External manifest upload | [ ] | | |
| **Navigation** | `btn_ingest` | Ingestion trigger | [ ] | | |
| **Navigation** | `export_global` | Session bundling/export | [ ] | | |
| **Filters** | `filter_*` | Dynamic column predicate pushdown | [ ] | | |
| **Theater** | `btn_max_plot` | Maximize plot (100% width) | [ ] | | |
| **Theater** | `btn_max_table` | Maximize table (100% width) | [ ] | | |
| **Theater** | `btn_reset_theater` | Reset Theater to split view | [ ] | | |
| **Theater** | `comparison_mode` | Dual-pane Comparison mode | [ ] | | |
| **Theater** | `triple_tier_mode` | 3-column grid (T1/T2/T3) | [ ] | | |
| **Theater** | `central_theater_tabs` | Manifest-driven dynamic tabs | [ ] | | |
| **Theater** | `ref_tier_switch` | Reference Sandbox (Wide vs Transformed) | [ ] | | |
| **Theater** | `btn_apply` | Gated Apply mechanism | [ ] | | |
| **Theater** | `view_toggle` | Main View (Wide vs Long/Aggregated) | [ ] | | |
| **Theater** | `column_visibility_picker` | Column picker (Hide/Show) | [ ] | | |
| **Theater** | `plot_leaf_brush` | Plot telemetry for outlier lookup | [ ] | | |
| **Audit Stack** | `audit_nodes_tier2` | Inherited Tier 2 step display | [ ] | | |
| **Audit Stack** | `audit_nodes_tier3` | User-defined Tier 3 step display | [ ] | | |
| **Audit Stack** | `btn_gallery_open_submission` | Submission gate modal | [ ] | | |
| **Audit Stack** | `restore_session` | Reset sync / session restore | [ ] | | |

---
**LEGEND**:

- ✅ : Success (Expected behavior)
- ⚠️ : Partial / Bug (Latency or cosmetic issue)
- ❌ : Failure (Crashes or logic break)
- 🚫 : Masked (Correctly hidden for persona)
