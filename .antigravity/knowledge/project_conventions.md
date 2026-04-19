# Project Conventions & Quick Reference (Combat Log)

> Paths must be given according to the project root (`SPARMVET_VIZ/`), not any other folder.

## 1. File Registry (Compressed)

| Component | Purpose | I/O | Key Logic / Terms |
| :--- | :--- | :--- | :--- |
| `./.agents/` | DIRECTIVES (Rules & Workflows) | Folder | `workspace_standard`, `verification_protocol` |
| `./.antigravity/` | PROJECT STATE (Knowledge, Plans, Tasks) | Folder | `architecture_decisions`, `tasks.md`, `audit_*.md` |
| `app/src/bootloader.py` | Path Authority & Persona Bootstrapper | Config → Paths/Toggles | `Bootloader`, `persona`, ADR-031 |
| `app/src/ui.py` | 3-Zone Dashboard Shell | UI Spec → Layout | `Navigation`, `Theater`, `Audit Stack` |
| `app/src/server.py` | Thin Orchestration Layer (ADR-003) | Reactive Hooks → Logic | `DataOrchestrator`, `VizFactory` |
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

## 2. Verification & Logging Protocol

- **Standard**: All manual verification must follow the **Evidence Loop** defined in [rules_verification_testing.md](./.agents/rules/rules_verification_testing.md).
- **Mandatory Halt**: No task is [DONE] without a `@verify` gate and materialization to `tmp/`.
- **Phase-Gating Mandate**: UI Testing and module integration are STRICTLY PROHIBITED until the explicit Headless tests pass.
- **Headless Artifact Routing**: Automatic library test outputs map to `tmp/{lib}/`, while Manifest tests route strictly to `tmp/Manifest_test/{manifest_basename}/`.
- **Manifest Architecture**: Manifests must use the "Basename Mirroring" standard (`manifest_name/` directory containing components).
- **Session Audit**: Every significant architectural or data change MUST be logged in `./.antigravity/logs/audit_{{YYYY-MM-DD}}.md`. Append-only.

## 3. UI Shell Architecture (Phase 11 & Phase 12)

- **Navigation (Left, #f8f9fa)**: Pipeline selection, Persona toggle, Session storage, Global Export. Masked per persona profile.
- **Theater (Center, White)**: Dynamic Layout Shifting depending on Persona. 1x2 Vertical Split for static reference, transitioning up to 2x2 Grid Comparison for sandbox exploration.
- **Audit Stack (Right, #f8f9fa)**: Unified Tier 3 recipe manipulation UI (T2 imported as Violet, User acts as Yellow). Governed strictly by the Gatekeeper (`btn_apply`) and Comments constraint.
- **Thin UI (ADR-003)**: UI modules MUST NOT implement wrangling or plotting logic. Authoritative GUI specifications rely on `ui_implementation_contract.md`.

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
