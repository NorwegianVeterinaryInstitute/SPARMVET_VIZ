# Logic Protocol: Tiered Data Lifecycle (ADR-024)
**Target Component:** libs/transformer & app/server
**Goal:** Eliminate 22-minute render bottlenecks by separating Assembly from Exploration.

## 1. The "Anchor" (Tier 1)
* **Definition**: The complete, joined, and tidied dataset resulting from Layer 1 (Wrangling) and Layer 2 (Assembly).
* **Execution**: Triggered only on initial load or manifest change.
* **Persistence**: MUST be materialized to disk using `pl.sink_parquet("tmp/session_anchor.parquet")`.
* **Benefit**: Preserves the "State of Truth" without taxing system memory for every UI interaction.

## 2. The "View" (Tier 2)
* **Definition**: A transient `LazyFrame` derived directly from the Tier 1 Anchor for a specific plot or UI component.
* **Execution**: Triggered by UI inputs (e.g., sidebars, filters, date pickers).
* **Process**: Uses `pl.scan_parquet("tmp/session_anchor.parquet")` followed by `.filter()` or `.group_by().agg()`.
* **Hand-off**: Only this reduced/filtered view is collected (`.collect()`) and sent to the `VizFactory`.

## 3. The Efficiency Loop (Workflow)
1. **Raw Ingestion**: `DataIngestor` reads source files.
2. **Layer 1/2**: `DataWrangler` and `DataAssembler` create the **Anchor**.
3. **Checkpoint**: `DataAssembler` lands the Anchor in `tmp/` as Parquet.
4. **UI Query**: User selects a filter.
5. **Rapid Retrieval**: Transformer scans the Parquet (Tier 2) and applies filters instantly via Predicate Pushdown.
6. **Fast Render**: `VizFactory` receives a lightweight table (e.g., 100 rows instead of 200k), rendering in milliseconds.

## 4. Short-Circuit Rule
If the `session_anchor.parquet` exists and the underlying manifest/sources have not changed, the Transformer MUST bypass Layers 1 and 2 and proceed directly to Tier 2 retrieval.


## 🛠️ Navigator's Summary for your Read List
The following architectural principles must integrate with : 
- ADR-010 (Polars Engine): Ensuring we stay in LazyFrame mode until the final Tier 2 hand-off.

- ADR-012 (Staged Assembly): Maintaining the distinction between atomic cleaning and multi-source joining.

- Memory Safety: Using Parquet to handle "Heavy Datasets" without RAM overflow.