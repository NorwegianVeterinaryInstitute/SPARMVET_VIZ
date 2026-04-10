# SPARMVET_VIZ: AMR Visualization Architecture 🔬📊

SPARMVET (SP-Analytical AMR Visualization Engine) is a modular, declarative framework for building high-integrity visualizations from genomic and AMR surveillance data.

## 🚀 Core Philosophy

1. **Strict Data Contracts (ADR-013)**: Data enters through an ingestion layer where it is immediately validated against a manifest.
2. **3-Tier Data Lifecycle (ADR-024)**:
    - **Tier 1 (The Trunk)**: Foundations. Cleaning, joining, and relational tidy-up.
    - **Tier 2 (The Branch)**: Specifics. Reshaping and aggregation for a particular plot.
    - **Tier 3 (The Leaf)**: Transient. Reactive filtering in the UI via Predicate Pushdown.
3. **Electronic Artist Pillar (VizFactory)**: A declarative Plotnine/ggplot abstraction that decouples "what to plot" from "how to plot."

## 📜 Declarative Manifest Syntax

Wrangling logic is separated into logical tiers to promote reuse and clarity:

```yaml
id: "example_manifest"
wrangling:
  tier1: # Relational Foundations
    - action: "rename"
      mapping: { "old": "new" }
    - action: "join"
      right_ingredient: "metadata"

  tier2: # Plot-Ready Reshaping (Optional)
    - action: "summarize"
      group_by: ["sample_id"]
      metrics: { "counts": "sum" }
```

> [!NOTE]
> If `tier2` is omitted, the system invokes **Identity Logic (ADR-014)**, passing the refined Tier 1 data directly to the visualization engine.

## 🛠️ Library Ecosystem

- [**ingestion**](./libs/ingestion/): TSV/Parquet discovery and schema normalization.
- [**transformer**](./libs/transformer/): The central wrangling and assembly engine.
- [**viz_factory**](./libs/viz_factory/): Graphical composition and Plotnine orchestration.
- [**utils**](./libs/utils/): Unified diagnostic registry and configuration management.

## 📖 Documentation

Detailed technical guides and the exhaustive user appendix are available in the [docs/](./docs/) directory:

- [Data Flow Analogy](./docs/appendix/data_flow_analogy.qmd): Non-technical guide to wrangling tiers.
- [Wrangling Guide](./docs/workflows/wrangling.qmd): Detailed technical spec for actions.
- [Visualization Gallery](./docs/appendix/user_guide_gallery.qmd): Pre-baked recipes for plots.

## ⚖️ Standards & Governance

This project follows the **Violet Law** (Component naming convention) and the **@verify Protocol** (Mandatory evidence-based testing).
