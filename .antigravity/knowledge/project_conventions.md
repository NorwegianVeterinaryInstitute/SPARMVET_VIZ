# Project Conventions & Quick Reference (Combat Log)

## 1. File Registry (Compressed)
| Component | Purpose | I/O | Key Logic / Terms |
|---|---|---|---|
| `protocol_tiered_data.md` | Logic Protocol for Anchor vs View (ADR-024) | Source of Truth | Short-Circuit, Predicate Pushdown |
| `adapter_*.py` | Normalizes incoming API/data payloads | Raw Payload → Dict | `Adapter`, format mapping |
| `ingestor.py` | Reads sources, implements early "Fail-Fast" validation | YAML/Paths → LazyFrame | `csv_reader`, primary key checks |
| `data_wrangler.py` | Layer 1 execution: Dispatches dynamic rules for one dataset | Dataset → Tidy LazyFrame | `.pipe()`, `spec` unpacking |
| `data_assembler.py`| Layer 2 orchestration: Joins multiple standard datasets | Multiple LFs → Unified LF | `.join()`, `recipe`, `sink_parquet` |
| `registry.py` | Single O(1) dictionary holding loaded decorations | String ID → Function | `AVAILABLE_WRANGLING_ACTIONS`|
| `actions/base.py` | Declares the registry wrapper linking logic to parser | Naked func → Registered | `@register_action` |
| `actions/core/*.py`| Atomic lazyframe operations (fill_nulls, strip_ws, etc) | LF → LF subset | Strict `pl.col()` vectors |
| `actions/advanced/*.py` | Complex rules mapping against reference DBs | Values/DB → Metadata | `derive_categories` |
| `actions/core/relational.py`| Joins tailored for assembly schemas | LF + LF → LF | `join_filter`, `how="left"` |
| `wrangler_debug.py` | Universal Layer 1 Runner: Dispatches rules for any dataset | TSV/YAML → Log / TSV | ADR-005, Ingestor |
| `assembler_debug.py`| Layer 2 Debugger: Validates assembly via explicit execution | Schema/Sources → `EVE_*.tsv`| `.collect()`, `argparse` |
| `transformer_integrity_suite.py`| Automated Integrity Suite: Programmatically verifies 25+ actions | Registry → Integrity Report | Layer 1 + 2 Validation |
| `viz_factory_integrity_suite.py`| Artist Integrity Suite: Programmatically verifies 120+ components | Registry → Integrity Report | Layer 1 (Geom/Scale/Theme) |
| `create_manifest*` | Bootstraps boilerplate JSON/YAML hybrid definitions | Templates → 3-block schema| `input_fields`, `output_fields` |
| `pipeline/*.yaml` | Master configurations and nested data contracts | (Defs) → Pipeline state | `!include`, `assembly_manifests`|

## 2. Verification Protocol (Logic Authority)
- **Standard**: All manual verification must follow the **Evidence Loop** defined in [rules_behavior.md](../../.agents/rules/rules_behavior.md).
- **Mandatory Halt**: No task is [DONE] without a `@verify` gate and materialization to `tmp/`.

## 3. Data Type Selection & Wrangling (Logic Authority)
- **Standard**: All wrangling actions and manifest schema types must follow the standards defined in [rules_wrangling.md](../../.agents/rules/rules_wrangling.md).
- **Enforcement**: String-based cleaning must precede Categorical casting in `output_fields`.
- **Tiered Lifecycle (ADR-024)**: 
    - **Tier 1 (The Anchor)**: Materialized via `Persistor (persistence.py)` using `sink_parquet`.
    - **Tier 2 (The View)**: Derived via `Summarizer (performance.py)` with `scan_parquet` + aggregation for rapid exploration.

## 4. SDK Workflow (Generator SDK)
- **Path**: `libs/generator_utils` (**Headless**, no UI dependencies).
- **A. Extraction**: `.xlsx` (Multi-sheet) → Standardized `.tsv` (Ingestion).
- **B. Bootstrapping**: `.tsv` → Manifest YAML inference (`input_fields`, `output_fields`).
- **C. Aqua Suite**: Samples categorical pools/ranges → High-integrity synthetic relational data.
- **D. Reconciler Workflow**: Scan -> Intersection Analysis -> Regex Generation -> Boundary Check -> TSV Materialization.
- **Law of Basename Anchor**: Folder Name == Master Manifest Name.

## 5. Assembler & Join Logic (Logic Authority)
- **Standard**: Relational logic and assembly orchestration follow [rules_wrangling.md](../../.agents/rules/rules_wrangling.md).
- **Key-as-ID**: Leverages `is_primary_key: true` tags automatically for joins.
- **Contract Boundary**: `output_fields` is the terminal `.select()` query guarding against column drift.

## 6. Viz Factory Workflow (Artist Pillar)
- **Path**: `libs/viz_factory` (**Headless**, returns ggplot objects).
- **A. Data-Agnostic Mapping**: Define 'aes' (x, y, fill) in the manifest, independent of the plot type.
- **B. Layer Composition**: Plots are built as a sequence of registered components (geoms -> scales -> themes).
- **C. Component Standard**: Use the **Violet Component** standard (`ComponentName (file_name.py)`) ONLY for documentation (.qmd files and README 'Key Components' lists). DO NOT apply it to functional classes, variables, filenames, or high-level docstrings.
- **D. Hand-off Rule**: Convert Polars to Pandas *only* at the final moment of `ggplot()` initialization.

## 7. Developer Standards (Library Integrity)
- **README Policy**: Every library in `./libs/` MUST have a `README.md` including Purpose, I/O, and Key Components (Violet Standard).
- **Interactive Debugging**: Use the `debug_` prefix for all CLI verification scripts (e.g., `debug_viz.py`).

## 8. Assets Scripts — Tool Suite (`assets/scripts/`)
All scripts in `assets/scripts/` MUST use `argparse` with a `--help` description explaining their role.
No `sys.path.insert` or `sys.path.append` is permitted (ADR-011 compliance).

| Script | Purpose | Key Args |
|---|---|---|
| `create_manifest.py` | Bootstrap YAML manifests from TSV schema | `--source`, `--out` |
| `create_test_data.py` | Generate synthetic test data for pipeline validation | `--out` |
| `figshare_triple_integration.py` | Stage 1+2 integration: CSV→TSV normalization + 3-way join | `--csv-dir`, `--tsv-dir`, `--out-dir` |
| `figshare_plot_integration.py` | Stage 3: Generate 3 integration plots from the materialized join | `--src`, `--out-dir` |
| `debug_viz_factory_audit.py` | Cross-reference tasks.md vs registered components and test triplets | `--tasks`, `--src-dir`, `--test-dir` |
| `debug_apply_manifest_standards.py` | Enforce ADR-013 header on YAML manifests | `--test-dir`, `--dry-run` |
| `debug_bootstrap_viz_yamls.py` | Bootstrap missing YAML test manifests for VizFactory components | `--test-dir`, `--dry-run` |

### Performance Note (2026-03-31)
**Tiered Acceleration (ADR-024):** Plotnine rendering from 200k-row join frames is optimized by the Tier 2 Summarizer.
The data volume is reduced via `.group_by().agg()` before `ggplot()` hand-off, targetting < 5s render times.
Anchor persistence (Tier 1) uses `pl.sink_parquet()` in the DataAssembler to enable rapid virtual subsetting.

## 10. The Integrity Suite Mandate (Standardization)
**Authority:** Mandatory for all packages in `./libs/`
**Goal:** Automated discovery and validation of all registered decorators.

1. **Required Artifact**: Every library MUST contain a `tests/{lib}_integrity_suite.py` runner.
2. **Action Discovery**: The suite must programmatically query the library's registry (e.g., `AVAILABLE_WRANGLING_ACTIONS` or `PLOT_COMPONENT_REGISTRY`) to list all implemented actions.
3. **1:1:1 Validation**: For every registered action, the suite must locate and execute its corresponding test triplet (TSV data, YAML manifest, and verification output).
4. **Automated Reporting**: The suite must generate a standardized `integrity_report.txt` in `tmp/` covering:
    - **Inventory**: All implemented actions and their categories.
    - **Status**: [PASSED], [FAILED], or [NO TEST DATA] (strictly for helper exceptions).
    - **Compliance**: Verification of ADR-013 (Dual-Validation) and ADR-022 (Violet Law).
