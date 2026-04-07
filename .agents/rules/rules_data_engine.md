# Data Engine & Transformation Protocols (rules_data_engine.md)

**Authority:** Defines the 3-Tier Tree Lifecycle and Wrangling contracts (Replaces tiered_data and wrangling legacy docs).

## 1. The 3-Tier Tree Data Lifecycle

To resolve 22-minute render bottlenecks and orchestrate Polars data hand-offs, the VIGAS-P pipeline strictly adheres to a three-tier lifecycle:

### Tier 1 (The Trunk): Relational Anchor

- **Definition:** The fully composed, joined, and tidied dataset resulting from heavy multi-source ingestion (Layer 1 Wrangling + Layer 2 Assembly). This anchor is shared by all the plots depending on the data source, ensuring the engine remains generic enough to be used globally.
- **Persistence:** Materialized to disk via `pl.sink_parquet("tmp/session_anchor.parquet")`.
- **Execution:** Triggered exclusively on initial load or base manifest change.

### Tier 2 (The Branch): Plot-Specific Anchor

- **Definition:** A shrunken, pre-aggregated, or transformed permutation of Tier 1 intended for computationally heavy UI plots.
- **Persistence:** Saved optimally as specific Parquet branches (e.g., `tmp/branch_plot_density.parquet`).
- **The Bifurcation Point Rule:** If a specific transformation or pre-aggregation is shared by **more than 3 plots**, it MUST be pushed back/upstream to **Tier 1 (The Trunk)**. If the transformation is completely unique to 1-2 specific visual assets, it remains in Tier 2.

### Tier 3 (The Leaf): Interactive UI View

- **Definition:** Transient, dynamic subsets generated on-the-fly (`pl.LazyFrame`) derived directly from Tier 1 or Tier 2.
- **Execution:** Handled exclusively via Predicate Pushdown (`pl.scan_parquet().filter()`) from user UI inputs (sidebars, date ranges).
- **Handoff:** Only this lightweight leaf is collected into memory (`.collect()`) prior to sending to `VizFactory`.

## 2. Wrangling Decorator Standards (The Law of Decorators)

- **Homogeneity:** All wrangling actions MUST use `@register_action("name")`.
- **Signature:** Actions accept exactly two arguments: `(lf: pl.LazyFrame, spec: Dict[str, Any])`.
- **Atomicity:** Actions must be independent, extracting parameters entirely from `spec`.
- **1:1:1 Naming Law:** Logic: `@register_action("name")` -> Manifest: `name_manifest.yaml` -> Data: `name_test.tsv`.

## 3. The Manifest Data Contract (ADR-013 & Identity Logic)

YAML manifests MUST contain:

1. `input_fields`: Raw incoming schema.
2. `wrangling`: Sequential list of operational dicts for atomic processing.
3. `output_fields`: The Published Contract (Terminal Polars `.select()` step).

- **Identity Transformations:** If `wrangling` is omitted/empty, the data bypasses actions. If `output_fields` is omitted/empty, all `input_fields` are retained (Import-As-Is).
