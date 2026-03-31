---
trigger: always_on
---

# Logic Protocol: Tiered Data Lifecycle

This rulebook enforces **ADR-024**, which mandates the separation of Relational Assembly (Tier 1) from UI Exploration (Tier 2) to eliminate 22-minute render bottlenecks.

## 1. The "Anchor" (Tier 1) Rules
- **Definition**: The complete, joined, and tidied dataset resulting from Layer 1 (Wrangling) and Layer 2 (Assembly).
- **Execution**: MUST be triggered ONLY on initial load or manifest change.
- **Persistence**: MUST be materialized to disk using `pl.sink_parquet("tmp/session_anchor.parquet")`.
- **Memory Safety**: Preserves the "State of Truth" without taxing system memory for every UI interaction.

## 2. The "View" (Tier 2) Rules
- **Definition**: A transient `pl.LazyFrame` derived directly from the Tier 1 Anchor for a specific plot or UI component.
- **Execution**: Triggered by user UI inputs (e.g., sidebars, filters, date pickers).
- **Mandatory Process**: Uses `pl.scan_parquet("tmp/session_anchor.parquet")` followed by `.filter()` or `.group_by().agg()`.
- **Hand-off**: Only this reduced/filtered view is collected (`.collect()`) prior to being sent to the `VizFactory`.

## 3. The Efficiency Workflow
1. **Raw Ingestion**: `DataIngestor` reads source files.
2. **Layer 1/2**: `DataWrangler` and `DataAssembler` create the **Anchor**.
3. **Checkpoint**: `DataAssembler` lands the Anchor in `tmp/` as Parquet.
4. **UI Query**: User selects a filter.
5. **Rapid Retrieval**: Transformer scans the Parquet (Tier 2) and applies filters instantly via Predicate Pushdown.
6. **Fast Render**: `VizFactory` receives a lightweight table.

## 4. The Short-Circuit Rule
If `tmp/session_anchor.parquet` exists and the underlying manifest/sources have not changed, the Transformer **MUST** bypass Layers 1 and 2 and proceed directly to Tier 2 retrieval.

## 5. Required Integrations
- **ADR-010 (Polars Engine)**: Must stay in `LazyFrame` mode until the final Tier 2 hand-off.
- **ADR-012 (Staged Assembly)**: Must maintain the strict distinction between atomic cleaning and multi-source joining.
