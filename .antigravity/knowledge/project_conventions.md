# Project Conventions & Quick Reference (Combat Log)

> Paths must be given according to the project root (`SPARMVET_VIZ/`), not any other folder.

## 1. File Registry (Compressed)

| Component | Purpose | I/O | Key Logic / Terms |
| :--- | :--- | :--- | :--- |
| `./.agents/` | DIRECTIVES (Rules & Workflows) | Folder | `workspace_standard`, `rules_app_structure`, `verification_protocol` |
| `./.antigravity/` | PROJECT STATE (Knowledge, Plans, Tasks) | Folder | `architecture_decisions`, `tasks.md`, `audit_*.md` |
| `app/src/bootloader.py` | Path Authority & Persona Bootstrapper | Config → Paths/Toggles | `Bootloader`, `persona`, ADR-031 |
| `app/src/ui.py` | 3-Zone Dashboard Shell (static HTML/CSS only) | UI Spec → Layout | `Navigation`, `Theater`, `Audit Stack` |
| `app/src/server.py` | **Thin Orchestrator only** (ADR-045, 228 lines) | Shared state/calcs → Handler delegation | `active_cfg`, `tier1_anchor`, `tier_reference`, `tier3_leaf`, 5× `define_server()` calls |
| `app/modules/manifest_navigator.py` | **Pure manifest introspection engine** (ADR-045) | Manifest path → Structural dicts | `build_sibling_map`, `build_schema_registry`, `build_lineage_chain`, `load_fields_file`, `resolve_fields_for_schema` — importable anywhere, zero Shiny dependency |
| `app/handlers/home_theater.py` | Home Theater Shiny wiring (ADR-043/045) | Reactive hooks → Home UI | `dynamic_tabs`, `sidebar_nav_ui`, `sidebar_tools_ui`, `sidebar_filters`, `plot_reference`, `plot_leaf`, `table_reference`, `table_leaf` |
| `app/handlers/audit_stack.py` | Pipeline Audit Shiny wiring (ADR-044/045) | Reactive hooks → Audit UI | `audit_nodes_tier2`, `audit_nodes_tier3`, `handle_apply`, `track_recipe_changes` |
| `app/handlers/blueprint_handlers.py` | Blueprint Architect Shiny wiring (ADR-039/045) | Reactive hooks → Architect UI | `_handle_manifest_import`, `_do_load_component`, `sync_blueprint_mapper`, `_handle_upload_*` |
| `app/handlers/gallery_handlers.py` | Gallery Shiny wiring (ADR-037/045) | Reactive hooks → Gallery UI | `_update_gallery_options`, `handle_gallery_clone`, `gallery_preview_img`, `gallery_md_content` |
| `app/handlers/ingestion_handlers.py` | Ingestion & persona Shiny wiring (ADR-045) | Reactive hooks → Ingest/Persona | `handle_ingest`, `update_persona_context` |
| `app/modules/orchestrator.py` | Tier 1 Ingestion & Assembly Bridge | Manifest + Data → Parquet | `DataOrchestrator (orchestrator.py)` |
| `libs/ingestion/src/ingestion/ingestor.py` | Reads sources, early validation | File → LazyFrame | `DataIngestor (ingestor.py)`, `scan_csv` |
| `libs/transformer/src/transformer/data_wrangler.py` | Layer 1 execution (Atomic) | Dataset → LazyFrame | `DataWrangler`, `@register_action` |
| `libs/transformer/src/transformer/data_assembler.py` | Layer 2 orchestration (Relational) | Multiple LFs → LazyFrame | `DataAssembler`, `sink_parquet` |
| `libs/utils/src/utils/config_loader.py` | Recursive YAML & Include Resolver | YAML → Python Dict | `ConfigManager`, `!include` |
| `libs/generator_utils/src/generator_utils/aqua_synthesizer.py` | [ADR-032] Relational Data Synthesis (SDK Core) | Schema → TSV | `AquaSynthesizer`, `--generate_only` |
| `libs/viz_factory/src/viz_factory.py` | Artist Pillar: Plot Composition | Data + Manifest → ggplot | `VizFactory`, `Plot Layers` |
| `libs/viz_gallery/assets/refresh_gallery.py` | [ADR-037] Gallery Indexing & Integrity Refresher | CLI Tool → JSON | `refresh_gallery.py`, Pivot-Index |
| `app/modules/gallery_viewer.py` | [ADR-033] Split-Pane Technical/Educational Gallery | Guidance → Sandbox | `GalleryViewer (gallery_viewer.py)` |
| `protocol_tiered_data.md` | Logic Protocol for Tiers (ADR-024) | Source of Truth | Short-Circuit, Predicate Pushdown |
| `transformer_integrity_suite.py` | Automated Integrity Suite (25+ Actions) | Registry → Report | `libs/transformer/tests/` |
| `libs/ingestion/src/ingestion/excel_handler.py` | [ADR-032] Excel Workbook Normalization | XLSX → Multi-TSV | `ExcelHandler`, authoritative extraction |
| `pipeline/*.yaml` | Master configurations and nested data contracts | (Defs) → Pipeline state | `input_fields`, `output_fields` |
| `libs/*/src/*/registry.py` | Authority for valid Wrangling and Viz actions | Registry → Validation | `@register_action`, `@register_geom` |

## 2. Verification & Logging Protocol

- **Standard**: All manual verification must follow the **Evidence Loop** defined in [rules_verification_testing.md](./.agents/rules/rules_verification_testing.md).
- **Mandatory Halt**: No task is [DONE] without a `@verify` gate and materialization to `tmp/`.
- **Phase-Gating Mandate**: UI Testing and module integration are STRICTLY PROHIBITED until the explicit Headless tests pass.
- **Headless Artifact Routing**: Automatic library test outputs map to `tmp/{lib}/`, while Manifest tests route strictly to `tmp/Manifest_test/{manifest_basename}/`.
- **Manifest Architecture**: Manifests must use the "Basename Mirroring" standard (`manifest_name/` directory containing components).
- **Session Audit**: Every significant architectural or data change MUST be logged in `./.antigravity/logs/audit_{{YYYY-MM-DD}}.md`. Append-only.

## 3. UI Shell Architecture (Phase 21 — ADR-043/ADR-044, 2026-04-23)

- **Navigation (Left, #c0c0c0)**: Project Selection, Blueprint Discovery, and Action Tools. Persistent global header for Home/Architect/Gallery switching. Filter widgets are **context-reactive to the active plot sub-tab** — regenerated on sub-tab change, scoped to that plot's `plot_spec` aesthetics.
- **Theater (Center, #d1d1d1)**:
  - **Home Mode (Unified)**: Tabs driven exclusively by manifest `analysis_groups`. Each group tab contains `navset_underline` plot sub-tabs wrapped in a **collapsible accordion**. Data preview in a **separate collapsible accordion below**. No hardcoded tabs. Controlled by the **Tier Toggle** (T1/T2 always; T3-Wrangle/T3-Plot persona-gated). **Comparison Mode** (persona-gated separate toggle) splits the theater into T2-reference (left) and T3-active (right).
  - **Architect Mode (Flight Deck)**: Tri-pane vertical stack (Collapsible TubeMap → Live Plot → Live Table). Unchanged.
- **Audit/Logic Stack (Right, #c0c0c0)**:
  - **Home Mode**: **Hidden** for `pipeline_static` and `pipeline_exploration_simple` (theater expands full width). Visible for ≥ `pipeline_exploration_advanced`: shows T2 Violet blueprint nodes + T3 Yellow sandbox nodes.
  - **Architect Mode**: Active Blueprint Component Logic Stack (The "Surgical" workbench). Unchanged.
- **Focus Mode (ADR-038)**: Global Navigation (Left Sidebar) programmatically hides "Operation" controls (Import/Session) when Discovery tabs (Gallery) are active.
- **Thin UI (ADR-003)**: UI modules MUST NOT implement wrangling or plotting logic. Authoritative GUI specifications rely on `ui_implementation_contract.md`.
- **Removed**: The "Analysis Theater / Viz" nav item is eliminated (ADR-043). The `theater_grid` toggle, `btn_max_plot`, `btn_max_table`, `btn_reset_theater` controls are superseded by the Tier Toggle + Comparison Mode model. The hardcoded "Inspector" tab is removed.

## 4. Path Authority Strategy (ADR-031)

System storage and hardware endpoints are strictly decoupled from UI code via `config/connectors/local/local_connector.yaml`.

- **Location 1 (Raw/Ingestion)**: Path to raw external data assets.
- **Location 2 (Manifests)**: Path to pipeline definitions and wrangling recipes.
- **Location 3 (Tiers 1 & 2)**: Curated Parquet Anchors & Views (`session_anchor.parquet`).
- **Location 4 (User & Tiers 3)**: User session states, active UI leaf interactions, and autosaves.
- **Location 5 (Gallery)**: Assets gallery for cloned/submitted recipes (`assets/gallery_data/`). Governed by `gallery_index.json` (Pivot-Index).

## 5. Tiered Data Lifecycle (ADR-024)

- **Tier 1 (Anchor)**: Fully assembled Tidy Table. Materialized via `sink_parquet` in `DataAssembler`.
- **Tier 2 (Branch)**: Shared summarizes/views derived from Tier 1 for rapid analysis discovery.
- **Tier 3 (Leaf)**: User-specific reactive transient view. Predicate Pushdown enabled via `scan_parquet` of the Tier 1 file.

## 9. Manifest Construction (ADR-041)

To ensure interoperability between the Blueprint Architect UI and the Polars Backend Engines, all manifest components must adhere to the following unified standard:

### 1. The Schema (Keyed)

- **Target**: `input_fields`, `output_fields`.
- **Format**: **Dictionary** (Key = Slug).
- **Rule**: Every entry must include `original_name`, `type`, and `label`.
- **Why**: Enables high-performance $O(1)$ lookup for ingestion and contract validation.

```yaml
# input_fields.yaml
sample_id:
  original_name: "Raw_Sample_ID"
  type: categorical
  label: "Sample ID"
```

### 2. The Logic (Ordered)

- **Target**: `wrangling.tier1`, `wrangling.tier2`.
- **Format**: **Sequential List** of Action Dicts.
- **Rule**: Tiered nesting is mandatory (ADR-024).
- **Why**: Order of execution is critical for data pipelining.

```yaml
# wrangling.yaml
tier1:
  - action: "rename"
    mapping: { "old": "new" }
  - action: "filter"
    query: "new > 0"
```

### 3. Fragments (Flat)

- **Target**: All `!include` files.
- **Format**: Flat dict or list (no redundant top-level anchoring key like `input_fields:`).
- **Why**: Allows direct unnesting and recursive loading by `ConfigManager`.

---

## 6. Logic Authority & Wrangling

- **Standard**: Wrangling follows definitions in [rules_data_engine.md](./.agents/rules/rules_data_engine.md).
- **Registry Recognition**: Actions registered via `@register_action` are automatically available to `DataWrangler` and `DataAssembler`.
- **Contract Boundary**: `output_fields` is the terminal `.select()` query guarding against column drift.

## 7. Viz Factory Workflow (Artist Pillar)

- **Path**: `libs/viz_factory` (Headless).
- **A. Data-Agnostic Mapping**: Aesthetics independent of plot type.
- **B. Layer Composition**: Sequence of geoms -> scales -> themes.
- **C. Violet Component Standard**: `ComponentName (file_name.py)` ONLY for docs and README lists.
- **D. Hand-off Rule**: Conversion to Pandas ONLY at the moment of `ggplot()` initialization.

## 8. Blueprint Architect — Lineage Index (ADR-040 / ADR-045)

Five pure functions in `app/modules/manifest_navigator.py` provide the manifest structural index powering the Blueprint Architect (moved from `server.py` in Phase 22, ADR-045):

| Function | Keyed by | Value summary |
| :--- | :--- | :--- |
| `build_sibling_map(manifest_path_str)` | `rel_path` (str) | `{role, schema_id, schema_type, siblings, ingredients}`. Role values: `input_fields`, `output_fields`, `wrangling`, `assembly`, `plot_spec`. |
| `build_schema_registry(manifest_path_str, includes_map)` | `schema_id` (str) | Full slot map: each slot is `str` (rel_path), `{"inline": val}`, or `None`. |
| `build_lineage_chain(selected_rel, ctx_map)` | — | Ordered `list[node_dict]` for the Rail; `is_active` marks the selected node. |
| `load_fields_file(abs_path)` | — | Reads standalone fields YAML with ADR-014 unnesting. |
| `resolve_fields_for_schema(schema_id, ctx_map, inc_map)` | — | Recursive field resolution with cycle guard; returns ADR-041 Rich Dict. |

**Key constraint**: Only `str` rel-paths are used as ctx dict keys. Inline YAML content (`{"inline": val}`) is stored in the `siblings` dict only — never as a dict key (unhashable).

**Assembly ingredient resolution**: Assembly wrangling files have `role="assembly"` and `ingredients=[schema_ids]`. To load ingredient fields in the upstream accordion, resolve `schema_id → output_fields rel_path` by scanning `ctx_map` for matching `schema_id` + `role="output_fields"`.

**Plot spec `target_dataset` resolution**: `target_dataset` names a data schema (e.g. `"FastP"`), not necessarily an assembly. Upstream lookup tries three passes: (1) assembly output_fields, (2) any output_fields for matching schema_id, (3) input_fields fallback.

**Sidebar display labels**: `_update_dataset_pipelines` shows `"{schema_id} — {role}"` labels. Option value stays as `rel_path` for `inc_map` lookup.

**Rail / TubeMap click → full load**: Both `handle_lineage_node_click` and `_sync_selector_from_node_click` call `ui.update_select(...)` then `ui.js_eval("document.getElementById('btn_import_manifest').click();")`.

**Live View plot preview**: `architect_active_plot` uses `ConfigManager(active_manifest_path.get()).raw_config` (full manifest). `active_viz_id` is set only when `role=="plot_spec"`. `active_raw_yaml` holds only the component fragment — do not use it for rendering.

**Temporary workspace**: `./tmpAI/` is agent-exclusive scratch space (headless tests, debug artifacts). `./tmp/` is for user-review outputs only (`@verify` evidence). Both are git-ignored. See `rules_verification_testing.md` §6

---

## 11. @bioscientist Protocol (Manifest Design)

- **Mandatory Knowledge**: `config/manifests/README.md`, `rules_persona_bioscientist.md`.
- **Registry Check**: Before generating YAML, the agent MUST verify action existence in `libs/transformer/src/transformer/registry.py` and `libs/viz_factory/src/viz_factory/registry.py`.
- **Logic Breakdown**: Every manifest proposal must include the scientific rationale for joins and transformation steps.
- **Gap Detection**: If an action is missing, it becomes a `[ENHANCEMENT REQUEST]` for the **@dasharch** persona, recorded in `tasks.md`.
---

## 10. Pipeline Stability & YAML Resilience (ADR-042)

To ensure the SPARMVET data engine survives diverse YAML formatting and large-scale relational joins:

- **Reserved Word Resilience**: Wrangling rule iteration and metadata purging MUST use `isinstance(k, str)` guards. Unquoted YAML `on:` is parsed as boolean `True`; the engine handles this via explicit `.get(True)` lookups in `DataWrangler` and `DataAssembler`.
- **Type-Safety in Recoding**: All comparison predicates in `recode_values` (e.g., `starts_with`, `contains`) MUST defensively cast targets to `pl.String`. This prevents `'bool' object has no attribute 'starts_with'` errors on heterogeneous datasets.
- **Contract Mapping Logic**: The `DataAssembler` final select query uses a contract-first approach. If columns are renamed or aliased during wrangling, the `output_fields` contract (or `final_contract`) must define the mapping. The system prioritizes `original_name` for projection to ensure contract compliance even when internal keys vary.
