**Status:** FINALIZED / ARCHITECTURAL LOCK

# UI Implementation contract

## 1. The Tier 3 "Branching & Blueprint" Logic

Tier 3 is a sandbox branch of Tier 1. It pre-populates by copying the Tier 2 "Blueprint" recipe.

- **Node Inheritance**: Copied T2 nodes are **Violet** (#f3e5f5). New user nodes are **Yellow** (#fffde7).
- **Position Awareness**:
  - Nodes dragged **ABOVE** Violet nodes = Pre-transform (Wide Data/T1 filters).
  - Nodes dragged **BELOW** Violet nodes = Post-transform (Long Data/T2 filters).
- **The Deletion & Deactivation Protocol**:
  - **Disable (Strikethrough)**: A "Power" icon allows the user to toggle a node off. The node remains in the UI with a strikethrough effect but is ignored by the Polars engine.
  - **Trash (Permanent)**: A trash icon allows for removal. If the node is **Violet**, a modal triggers: _"CRITICAL: Removing a blueprint step may break the intended visualization. Are you sure?"_

- **The Revert Protocol**: The **btn_revert** performs a **Full Wipe**. It clears all user nodes and restores the Tier 3 stack to the exact state of the Tier 2 blueprint.
- **Direct Pass-Through**: If the T2 manifest contains zero transformation steps (T2=T1), the T3 recipe starts **Empty**.

## 2. Shell Architecture (The 3-Zone Navigator) — Updated ADR-043/ADR-044 (2026-04-23)

The UI implements a high-density **3-column nested shell** to maximize screen real estate. The right column (Pipeline Audit) is **persona-gated** and suppressed entirely for lower personas (see ADR-044):

- **Project Navigator (Left)**: Persistent controls for project selection and **context-reactive filter widgets** (scoped to the active plot sub-tab's `plot_spec` aesthetics). Uses a Dark Grey (#c0c0c0) background.
- **Home Theater (Center)**: The primary workspace. Structure (post-ADR-043):
  - Top-level tabs are **exclusively** driven by manifest `analysis_groups` — no hardcoded tabs (Inspector removed).
  - Each group tab contains `navset_underline` sub-tabs (one per declared plot), wrapped in a **collapsible accordion panel**.
  - A **separate collapsible accordion panel** below shows the data preview (T1/T2 table or T3 sandbox table).
  - A **Tier Toggle** radio-button strip (T1 / T2 / T3-Wrangle / T3-Plot, persona-gated) controls which tier is displayed.
  - Uses a Neutral Grey (#d1d1d1) background.
- **Pipeline Audit (Right)**: Audit trail for T2 blueprint and T3 sandbox transitions. **Visible only for ≥ `pipeline_exploration_advanced`**. When hidden, the theater column expands to fill the full layout width — the layout element itself is excluded, not merely hidden via CSS. Uses a Dark Grey (#c0c0c0) background.

**Manifest-Driven Tab Rule**: Home tabs and sub-tabs MUST derive exclusively from `analysis_groups` in the active manifest. No hardcoded tab names or fallback tabs are permitted (ADR-003/ADR-004 compliance).

**Tier Toggle Strip** (replaces `ref_tier_switch` + `view_toggle`):

| Button | Plot Pane | Data Pane | Persona Gate |
|---|---|---|---|
| **T1 Raw** | T2 Reference Plot (read-only) | T1 Anchor table (read-only) | All |
| **T2 Reference** | T2 Reference Plot (read-only) | T2 Branch table (read-only) | All |
| **T3 Wrangling** | T3 Active Plot (Apply-gated) | T3 post-wrangling table (sandbox) | ≥ `pipeline_exploration_advanced` |
| **T3 Plot** | T3 Active Plot (Apply-gated) | T3 post-plot data slice | ≥ `pipeline_exploration_advanced` |

**Comparison Mode** (Option A — Separate Toggle, Persona-Gated, ≥ `pipeline_exploration_advanced`):

- When **ON**: theater splits into a 2-column layout — left = T1/T2 reference (per Tier Toggle), right = T3 Active.
- When **OFF**: single-pane view driven by the Tier Toggle alone.
- Replaces the previous `is_comparison` + `is_triple` flag system.

**Collapsibility Rules**:

- Plot accordion panel: default **expanded**. User-collapsible. Collapse state MUST persist across sub-tab navigation.
- Data accordion panel: default **expanded**. User-collapsible. Collapse state MUST persist across sub-tab navigation.
- Column picker (T3 sandbox): MUST span `width: 100%`, `flex: 1 1 100%`. MUST NOT wrap to multiple rows.

## 3. The Mandatory Audit Gatekeeper (The Gate)

Reactivity in the Active Leaf (Right side) is strictly gated by documentation to ensure scientific reproducibility

- **Logic**: Every user action (Filter, Column Drop, Node Addition in Tier 3) generates a node that **MUST** have a comment.
- **Comment Mandate**: Every Yellow node (and modified Violet node) MUST have a non-empty string in its `comment_field`.
- **Execution Rule**: The **btn_apply** state is disabled if:
 	- **Disabled (Grey)**:
  1. No changes detected/made OR comments are missing (`recipe_pending == False`).
  2. Any node in the stack (excluding disabled ones / and ones inherited by tier 2) has an empty comment field.  
  - **Active (Orange/Green)**: Changes detected AND all nodes have comments.
- **Calculation Scope**: Clicking **btn_apply** executes the 3-stage Polars pipeline and updates only the **Active Leaf** (Right) panes.
- **Visualization**: Until **btn_apply** is pressed, the **Active Plot** remains in a "Pending" state (e.g., blurred or overlayed with an orange "Recalculate" badge).

## 4. Interaction & Event Mapping

| **UI Event**                 | **Resulting Action**               | **Audit Entry**         |
| ---------------------------- | ---------------------------------- | ----------------------- |
| **Brush on Active T3 Plot**     | Filter rows in T3 data.            | Automatic Yellow Node   |
| **Col Drop in Active T3 Table** | `df.drop_columns()` in T3.         | Automatic Yellow Node   |
| **(Advanced Filter) in active T3 Table**        | Filter cols in T3 data. | Automatic Yellow Node   |
| **Drag Node**                | Reorder Polars operation sequence. | Update `recipe_pending` |
| **Ref Table Filter** in Tier 1 or Tier 2 Table         | Visual-only filter for inspection. | **NONE** (Transient)    |
| **Ref Table Drop**  in Tier 1 or Tier 2 Table              | Visual-only drop for inspection. | **NONE** (Transient) |                             |                                    |                         |

## 5. The Theater Layout Model (Updated ADR-043, 2026-04-23)

The theater layout is controlled by two independent controls: the **Tier Toggle** and **Comparison Mode**.

**Single-Pane Mode** (Comparison Mode OFF — all personas):

| Tier Toggle State | Plot Area | Data Area |
|---|---|---|
| T1 Raw | T2 Reference Plot (read-only) | T1 Anchor table (read-only, collapsible) |
| T2 Reference | T2 Reference Plot (read-only) | T2 Branch table (read-only, collapsible) |
| T3 Wrangling* | T3 Active Plot (Apply-gated) | T3 wrangling table (sandbox, collapsible) |
| T3 Plot* | T3 Active Plot (Apply-gated) | T3 plot slice table (sandbox, collapsible) |

*T3 states hidden for personas < `pipeline_exploration_advanced`.

**Comparison Mode** (ON — ≥ `pipeline_exploration_advanced`):

```
┌──────────────────────┬──────────────────────┐
│  T2 Reference Plot   │  T3 Active Plot       │  ← Plot accordion (collapsible)
├──────────────────────┼──────────────────────┤
│  T1/T2 Data (R/O)   │  T3 Sandbox Data      │  ← Data accordion (collapsible)
└──────────────────────┴──────────────────────┘
```

- Left column tier (T1 or T2) is driven by the Tier Toggle.
- Both plot and data rows are independently collapsible via accordion panels.
- The previous `theater_grid` toggle, `btn_max_plot`, `btn_max_table`, and `btn_reset_theater` controls are **removed** (superseded by this model).

## 6. Component Interaction Matrix

|**Zone**|**ID**|**Reactive Behavior**|
|---|---|---|
|**Table Ref**|`table_ref`|**Visual Only**: Filtering here updates the table view but creates NO audit nodes and does NOT trigger the Apply button.|
|**Table Active**|`table_active`|**Recipe Driver**: "Brush" events or column de-selections automatically generate a new **Yellow Node** in the Audit Stack.|
|**Audit Stack**|`audit_stack`|**Order Matters**: Drag-and-drop reordering of nodes marks `recipe_pending = True`.|

## 7. Session Management vs. Global Export

To ensure a clean separation between "Working State" and "Final Provenance," the UI distinguishes between these two actions:

### 7.1 Session Save / Import (Left Sidebar — System Tools)

**Function:** Persists and restores the full working state so a user can resume interrupted work, or maintain separate sessions for different pipeline runs (e.g., AMR pipeline run 2025-01 vs run 2025-06).

**What is saved per session:**
- Active `t3_recipe` (all Yellow nodes and their comment fields)
- `applied_filters` (committed filter rows)
- Active sub-tab and tier toggle state
- Reference to the active manifest and data source (so the session knows which pipeline run it belongs to)
- If metadata was replaced (see §9): reference to the uploaded metadata filename

**Session model:**
- Each session is a named `.json` file stored in a subdirectory of Location 4 (`user_sessions/sessions/<session_id>.json`).
- Multiple sessions are allowed per user — users can switch between sessions (different pipeline runs, different dates).
- Sessions are **named at save time** — the UI prompts for a session label (e.g., "AMR_run_Jan2025").

**Ghost save:**
- Automatic background save on every `btn_apply` press and on every filter commit.
- Stored as `user_sessions/sessions/_autosave.json` — single slot, always overwritten.
- Restored automatically if the app detects an autosave newer than the last explicit session save.
- **Status:** Ghost save deferred to Phase 22+. Manual save/restore is the immediate target.

**Save location:** `user_sessions` (Location 4) from the active deployment profile. This path is deployment-specific — on Galaxy it maps to a Galaxy-accessible path; on a local machine it is a local directory. Users only have write access to Location 4 — they cannot choose an arbitrary path.

**UI controls (System Tools accordion):**
- `btn_save_session`: Save current state → prompts for session label → writes `<label>_<timestamp>.json`.
- `btn_restore_session`: Opens a modal listing available sessions (from Location 4) → user picks one → restores state.
- Ghost save indicator: subtle timestamp display showing "Last autosaved: HH:MM".

**Status:** Deferred to Phase 22+. Buttons present as stubs (disabled) in current UI.

---

### 7.2 Export Results Bundle (System Tools — Left Sidebar, ADR-047, Phase 21-I)

**Implementation:** `@render.download export_bundle_download` in `app/handlers/home_theater.py`.

**UI Controls:**
- `export_bundle_label` (text, sanitized — label is "Bundle label / name", not "Your name"). Sanitized: `re.sub(r"[^A-Za-z0-9_-]", "_", raw)[:40]`.
- `export_preset` radio: **Web / Presentation** (SVG) or **Publication** (PNG ≥600 DPI).
- Filter warning shown when `applied_filters` non-empty.
- Download button: `📦 Export Bundle`.

**Filename:** `YYYYMMDD_HHMMSS_<label>_results.zip`.

**Bundle contents:**

| Path | Contents |
|------|---------|
| `plots/` | SVG (web) or PNG ≥600 DPI (publication) per plot in manifest |
| `data/<ds>_T1.tsv` | T1 (Assembled) — always |
| `data/<ds>_T2.tsv` | T2 (Analysis-ready) — always |
| `data/<ds>_T3.tsv` | T3 (User-adjusted) — advanced+ persona only when `tier_toggle=="T3"` |
| `recipes/<proj>/` | All YAML wrangling/assembly/plot files for the active project |
| `FILTERS.txt` | Filter trace when `applied_filters` non-empty ("No Trace No Export" — ADR-021 extension) |
| `report.qmd` | Quarto source: front-matter, filter table, figure includes, data section |
| `README.txt` | Bundle manifest: timestamp, project, persona, preset, tiers, metadata source filename, counts |

**Metadata provenance in bundle:** If a custom metadata file was uploaded (§9), its original filename is recorded in `README.txt` and in the `report.qmd` front-matter. This ensures the bundle is self-documenting about its data sources.

**Export location:** Currently browser download (= local PC / client machine). This works identically in Galaxy (browser download from GxIT proxy), IRIDA, and local deployments. Server-side write to Location 4 is a deferred enhancement for pipeline archiving use cases.

**Deferred:**
- Per-plot checkbox selection (all plots always exported).
- Server-side write to Location 4.
- Re-export of raw + metadata source files alongside T1/T2 (to ensure full reproducibility when metadata was replaced — see §9).

---

### 7.3 Export Active Graph (System Tools — Persona-Gated)

Available to any persona with T3 access (≥ `pipeline_exploration_simple` with filters, or ≥ `pipeline_exploration_advanced` with full T3 sandbox). Exports a single-plot bundle:

| Path | Contents |
|------|---------|
| `<plot_id>.<svg\|png>` | The currently active plot at the active tier |
| `<plot_id>_recipe.yaml` | The plot spec + any active T3 overrides |
| `FILTERS.txt` | Active filter trace if filters applied (mandatory — No Trace No Export) |

**Status:** Deferred to Phase 22. Stub in System Tools accordion.

## 8. Filter Recipe Builder (Phase 21-F — Left Sidebar, 2026-04-23)

Row filters live in the left sidebar (Home mode only). They affect both plots and the data preview.

**State model:**
- `_pending_filters`: staging area (`reactive.Value[list]`) — rows added by user, not yet applied.
- `applied_filters`: committed (`reactive.Value[list]`) — consumed by all `@render.plot` handlers and `home_data_preview`.

**Each row:** `{column: str, op: "eq"|"ne"|"gt"|"ge"|"lt"|"le"|"in"|"not_in", value: str|list[str], dtype: str}`.

**Ops for discrete columns (or `scale_x_discrete` declared):** `in`, `not_in`, `eq`, `ne`.
**Ops for numeric columns:** `eq`, `ne`, `gt`, `ge`, `lt`, `le`.

**Type coercion rule:** Values are always stored as strings (selectize returns strings). `_apply_filter_rows` casts column to Utf8 for set ops (`in`/`not_in`); coerces scalar value to column dtype for numeric comparisons. Auto-promotes `eq`→`in` / `ne`→`not_in` when value is a list.

**VizFactory predicate pushdown:** `applied_filters` are injected into `plot_config["filters"]` (without `dtype`) before `viz_factory.render()`. VizFactory supports: `eq`, `ne`, `gt`, `ge`, `lt`, `le`, `in`, `not_in`.
  
## 9. Metadata Ingestion (System Tools — Persona-Gated)

**Purpose:** Allow a user to upload an updated metadata file that replaces the metadata source for the active pipeline run. This is a **full replacement** — the uploaded file becomes the new source of truth for that metadata source. It triggers a T1 rebuild.

**When used:** Users correct errors in metadata (e.g., wrong collection date, corrected resistance phenotype, updated sample annotations) and need the plots to reflect the correction without re-running the upstream pipeline.

**Persona gate:** Available to personas with data ingestion access — at minimum `pipeline_exploration_advanced` and above. Configurable in persona template (`metadata_ingestion_enabled: true/false`). Hidden for `pipeline_static` and `pipeline_exploration_simple`.

**Flow:**
1. User uploads a TSV/CSV metadata file via file input in System Tools.
2. `MetadataValidator` gates the upload: validates that required columns (defined in `input_fields` contract for the metadata schema) are present. Uses fuzzy matching to suggest corrections if columns are missing.
3. If validation passes: the uploaded file is written to Location 1 (`raw_data`) as the new metadata source, **replacing** the previous file. The original filename is recorded (for provenance).
4. T1 rebuild is triggered automatically — the DataOrchestrator re-runs ingestion and assembly. A "Recalculating..." overlay is shown.
5. On completion: T2 and all plots update. A notification confirms: "Metadata updated from `<filename>`. T1 rebuilt."

**Provenance obligation:** The original uploaded filename (not just its path) is stored in a sidecar file (e.g., `metadata_provenance.yaml` in Location 1) so that exports and session files can reference it. This filename is included in `README.txt` and `report.qmd` of any subsequent export bundle.

**What is NOT replaced:** Raw instrument data (sequencing results, VCF files, etc.) — only the metadata source. The manifest's `input_fields` contract determines which file is considered "metadata" for validation purposes.

**Status:** Deferred to Phase 22+. UI stub (greyed file input + label) present in System Tools when persona allows. Validation and rebuild flow designed here; implementation pending.

---

## 10. Data Ingestion & Excel Converter (System Tools — Advanced Persona Only)

**Purpose:** Allow a user to provide raw data files when the app is deployed independently of an automated pipeline (e.g., pipeline deposited results in an Excel file that the user now uploads manually).

**Persona gate:** `import_helper_enabled: true` in persona template. Available to ≥ `pipeline_exploration_advanced` (or `project_independent` / `developer`). Hidden for lower personas. Also deactivatable at the deployment level (profile sets `data_ingestion_enabled: false`) for deployments where data is always pushed automatically by a pipeline — the System Tools section for ingestion is suppressed entirely.

**Supported ingestion types:**
- **Raw data** — TSV/CSV instrument output
- **Metadata** — sample annotation files (goes through MetadataValidator gate, same as §9)
- **Extra data** — supplementary tables (e.g., reference databases, additional annotation layers)

**Manifest association:** When uploading, the user must associate the file with a manifest schema (dropdown of known schemas from `locations.manifests`). This tells the DataOrchestrator which `input_fields` contract to validate against and which pipeline slot the file fills.

**Multi-file upload:** A `+` button allows queuing multiple files (e.g., one per schema). Each queued file shows its assigned schema and validation status before the user commits the ingestion.

**Excel → TSV Converter (within Data Ingestion):**
- Available as a sub-step when an `.xlsx` file is uploaded.
- App reads sheet names from the workbook (via `ExcelHandler` — `libs/ingestion/src/ingestion/excel_handler.py`).
- User assigns each sheet to a role: **raw data**, **metadata**, or **extra data**, and selects the target schema from the manifest dropdown.
- Converter writes TSVs to Location 1 (`raw_data`) in the user-accessible directory.
- After conversion, the resulting TSVs are queued for ingestion as normal.
- **Why here and not Dev Studio:** Scientists receive Excel files from collaborators and pipelines — this is a practical data preparation step, not a developer concern. Dev Studio is for synthetic data generation (AquaSynthesizer).

**Status:** Deferred to Phase 22+. Design finalized here. `ExcelHandler` backend already exists.

---

## 11. Left Sidebar — Panel-Context Dependency

The left sidebar content is **not static** — it changes based on which top-level panel (mode) is active. The same sidebar slot renders different content per panel.

| Active Panel | Left Sidebar Content |
|---|---|
| **Home** | Project Navigator + Filter Recipe Builder (§8) + System Tools (§7, §9, §10) |
| **Blueprint Architect** | Manifest/component navigation (dataset pipeline selector, TubeMap node selector) |
| **Gallery** | Focus Mode (ADR-038) — operation controls hidden; search/filter for gallery only |
| **Dev Studio** | TBD — deferred until Dev Studio is finalized. Left sidebar content for this panel is an open design question. |

**Implementation rule:** The `sidebar_nav_ui` render function reads the active top-level nav item and renders the appropriate sidebar content. Switching panels clears and replaces the entire left sidebar DOM subtree (not CSS-hide — physical replacement, following the Shell Stability Law in §3a of `project_conventions.md`).

**Filter Recipe Builder scope:** Filters are a Home-mode-only feature. They are never rendered in Blueprint Architect, Gallery, or Dev Studio left sidebars. The filter `_pending_filters` and `applied_filters` reactive state is preserved across panel switches but the filter UI widgets are only mounted when Home is active.

**Blueprint Architect left sidebar:** May eventually include filter-like controls (e.g., field search, schema filtering within the TubeMap) — decision deferred until Architect mode is finalized. Not the same as the Home row-filter system.

---

# UI Configuration Dependencies

## Deployment Profile (ADR-048)

Defined in deployment profile YAML. Resolution chain:
1. `SPARMVET_PROFILE` env var → path to profile
2. `~/.sparmvet/profile.yaml`
3. `/etc/sparmvet/profile.yaml`
4. `config/connectors/local/local_connector.yaml` (dev fallback)

Profile declares `default_manifest`, `default_persona`, `project_root`, and the five `locations` keys.
See: `config/connectors/templates/connector_template.yaml` for full schema.

## Persona

Defined in persona templates: `config/ui/templates/<persona_name>_template.yaml`.
Controls feature visibility flags: `interactivity_enabled`, `developer_mode_enabled`, `gallery_enabled`, `comparison_mode_enabled`, `session_management_enabled`, `import_helper_enabled`, `export_bundle_enabled`, `metadata_ingestion_enabled` (new), `data_ingestion_enabled` (new).

## User Preferences [Implementation Deferred]

Saving location: Location 4 (`user_sessions`) from deployment profile, filename `user-preferences.yaml`.
Overrides persona template settings where permitted (priority rule).
Not implemented yet.
