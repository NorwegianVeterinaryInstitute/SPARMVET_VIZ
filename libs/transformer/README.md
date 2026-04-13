# Transformer Library

## Purpose

The central engine for data wrangling and Phase 4 relational assembly. It enforces the ADR-013 data contracts by cleaning raw data and joining disparate sources into a single, tidy Polars DataFrame ready for visualization.

## Documentation
>
> [!IMPORTANT]
> This README is a high-level summary. For exhaustive deep-dives, architectural ADRs, and the full gallery of actions, you MUST refer to the official [Transformer Dev-to-User Guide](../../docs/workflows/wrangling.qmd).

## Key Components

- `DataWrangler (data_wrangler.py)`: Core engine that executes atomic cleaning actions against single datasets using declarative YAML pipelines.
- `DataAssembler (data_assembler.py)`: Relational join orchestrator. Implements **Strict Assembly Enforcement**: requires all ingredients explicitly defined in a recipe, otherwise triggers a controlled crash to protect data integrity.
- `PipelineExecutor (pipeline.py)`: Top-level runner that coordinates the full end-to-end flow (Ingest -> Wrangle -> Assemble).
- `ActionRegistry (registry.py)`: Central dictionary mapping YAML action keys to Python function logic.
- `MetadataValidator (metadata_validator.py)`: Ensures user-provided metadata aligns with the established joining contracts.
- `IntegritySuite (transformer_integrity_suite.py)` - [Orchestrator]: Programmatically verifies the correctness of every registered action.
- `WranglerDebugger (debug_wrangler.py)` - [Dev Tool]: CLI harness to test isolated atomic transformations manually.
- `AssemblerDebugger (debug_assembler.py)` - [Dev Tool]: CLI executor for emulating multi-source relational logic.
- `PipelineDebugger (debug_pipeline.py)` - [Test Utility]: CLI tool to verify full pipeline execution and materialize output for audit.
- `ExpressionsDebugger (debug_expressions.py)` - [Dev Tool]: Isolated runner to test atomic Polars expressions (Cast, Coalesce).
- `DecoratorDebugger (debug_decorator_suite.py)` - [Helper]: Specialized runner for Layer 1 action verification.
- **Action Sub-Packages (ADR-024)**:
  - `Reshapinger (reshaping/core.py)`: Structural transformations (Pivot, Unpivot, Explode, Split).
  - `Cleaner (cleaning/core.py)`: Atomic cleaning (Rename, Replace, Nulls, Selection, Sanitization).
  - `Expressionist (cleaning/expressions.py)`: Pattern-based extraction (Regex) and atomic logic (Cast, Coalesce, Label_If).
  - `Categorizer (cleaning/advanced.py)`: Complex lookup mapping.
  - `Joiner (relational/joins.py)`: Relational assembly logic.
  - `Summarizer (performance/aggregation.py)`: Pre-visualization data collapsing for Tier 2.
- `Anchor (persistence/anchor.py)`: Tier 1 disk materialization tools (`sink_parquet`).
- **Reactive State (Tier 3)**: Transient views generated via Predicate Pushdown. Supports **Gated Reactivity** via the `btn_apply` trigger, allowing for side-by-side inspection in the **Comparison Theater**.
- **Path Authority**: Persistence locations (Tiers 1-3) are determined by `config/connectors`, decoupling hardware from the UI.

## Manifest Syntax (Tiered Wrangling Mandate)

Following **ADR-024**, every `wrangling` entry in a manifest MUST use a nested key structure. This formalizes the separation between generic data cleaning and plot-specific preparation.

```yaml
wrangling:
  tier1: # THE TRUNK: Tidy, Clean, Wide Data (Shared foundation)
    - action: "clean_column_names"
    - action: "join"
      right_ingredient: "metadata"
      on: ["sample_id"]
    - action: "rename"
      mapping: { "raw_gene": "Gene_Name" }

  tier2: # THE BRANCH: Plot-Ready, Aggregated, Long Data (Optional)
    - action: "summarize"
      group_by: ["sample_id", "species"]
      metrics: { "gene": "count" }
```

### Identity Logic (ADR-014)

- **Automatic Fallback**: If the `tier2` block is omitted or left empty, the system automatically uses the Tier 1 output for visualization.
- **Recommendation**: Only utilize Tier 2 when the plot requires data transformations (e.g., pivoting to long format or aggregation) that differ from the tidy Tier 1 table.

## Short-Circuit & Freshness Guard (ADR-024)

To maximize performance when iterating on complex pipelines, the `DataAssembler` implements a **Short-Circuit Execution** pattern.

- **The Logic**: If a `sink_parquet` action is detected and the target file already exists, the assembler skips all preceding ingestion, wrangling, and join operations, loading the pre-computed Parquet directly.
- **Automated Freshness Check**: The system automatically invalidates the short-circuit if it detects that any manifest component (including `!include` files in mirrored directories) has a modification timestamp newer than the Parquet file.
- **Manual Override**: To force a full re-computation regardless of timestamps (e.g., if raw data changed but manifests did not), use the `--force` CLI flag or set `force_recompute: true` in the YAML manifest.

## I/O Summary

- **Input**: Raw `pl.LazyFrame`s from the Ingestion layer, and YAML Manifest `spec` dictionaries.
- **Output**: Cleaned, joined, and contract-enforced `pl.LazyFrame`s matching the `output_fields` specification.

## Local CLI Runners

For Phase 1 & Phase 4 verification, use the local debugging runners to execute declarative YAML manifests and verify output TSVs.

**Full Suite Verification (The Automated Gate):**

```bash
./.venv/bin/python libs/transformer/tests/transformer_integrity_suite.py --output_dir tmp/transformer/
```

**Atomic Wrangling (Isolated Action):**

```bash
./.venv/bin/python libs/transformer/tests/debug_wrangler.py --data [INPUT] --manifest [YAML] --output [OUT_TSV]
```

**Relational Assembly (Multi-Source Job):**

```bash
./.venv/bin/python libs/transformer/tests/debug_assembler.py --manifest [YAML] --data [DATA_DIR] --output [OUT_TSV]
```

## Installation (Editable Mode)

According to the workspace standard, this library must be installed locally via:

```bash
pip install -e ./libs/transformer
```
