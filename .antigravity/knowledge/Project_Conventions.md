# Project Conventions

## 1. The "Knowledge Bank" File Registry

### libs/ (Core Engine & Tooling)
**libs/connector/**
- `src/adapter_*.py`: Adapters designed to normalize raw ingested data (e.g., from an API or file system) before wrangling. They map API or raw fields to standard initial structure.
  - *Inputs/Outputs*: API payloads / Raw Data TSVs -> Python Dictionary or JSON.
  - *Key Logic*: Translates external format into the project's internal ingestion representations.
  - *Key terms*: `Adapter`, `payload`.

**libs/ingestion/**
- `src/ingestor.py`: Manages the reading process of the local data (resolving the explicit `source` block from YAML manifests) to initiate the pipeline. Validates that the primary keys and mandatory schema fields match the `input_fields`. 
  - *Inputs/Outputs*: CSV/TSV source paths -> Polars LazyFrames.
  - *Key Logic*: Early validation logic leveraging the "Fail-Fast" principle before sending data to the transformer.
  - *Key terms*: `csv_reader`, `validation_error`.

**libs/transformer/src/**
- `data_wrangler.py`: Core Layer 1 atomic cleaner. Loops through the `wrangling` list of the manifest applying registered wrapper transformations to independent datasets.
  - *Inputs/Outputs*: Data schema dict & Raw dataset LazyFrame -> Cleaned Tidy LazyFrame.
  - *Key Logic*: Action-agnostic dynamic dispatch mapping manifest `action: X` strings directly to Python functions.
  - *Key terms*: `.pipe()`, `LazyFrame`, `spec`.

- `data_assembler.py`: Core Layer 2 orchestration. Builds the relational mapping from multiple atomic sources. Executes sequential declarative join steps.
  - *Inputs/Outputs*: Multiple `DataWrangler` results (datasets) -> Final Unified assembly.
  - *Key Logic*: Loop execution mapping datasets against keys dynamically utilizing the "Shared Registry" strategy.
  - *Key terms*: `.join()`, `recipe`, `Assembler`.

- `registry.py`: The single centralized dictionary container pointing to the loaded `AVAILABLE_WRANGLING_ACTIONS`.
  - *Inputs/Outputs*: String key -> Function object.
  - *Key Logic*: O(1) Action lookup dict.
  - *Key terms*: `AVAILABLE_WRANGLING_ACTIONS`.

**libs/transformer/src/actions/**
- `base.py`: Declares the foundational explicit decorator logic that captures and registers any wrangler operation.
  - *Inputs/Outputs*: Undecorated function -> Registered wrapper.
  - *Key Logic*: Decorator pattern binding Python logic to the YAML parser dictionary.
  - *Key terms*: `@register_action`.

- `advanced/categories.py` / `advanced/regex.py`: Complex business logic rules such as evaluating mapping thresholds and category generation against reference TSVs.
  - *Inputs/Outputs*: Column string values, Reference TSVs -> Extracted metadata dimensions.
  - *Key Logic*: External dictionary fetching using lookup joins explicitly defined in the YAML instructions.
  - *Key terms*: `derive_categories`, `@register_action`.

- `core/cleaning.py` / `core/duplicates.py` / `...`: Atomic core rules for sanitizing individual LazyFrames (e.g., `strip_whitespace`, `fill_nulls`).
  - *Inputs/Outputs*: LazyFrame subsets -> Standardized LazyFrame subsets.
  - *Key Logic*: Strict Polars-only (e.g., `pl.col().str.strip()`) expression-based vectorization.
  - *Key terms*: `pl.col()`, `@register_action`.

- `core/relational.py`: Joins designed for assembly blocks.
  - *Inputs/Outputs*: Multiple LazyFrames -> Joined LazyFrame.
  - *Key Logic*: Defines standard explicit left/inner joins or "whitelisting" filtering (like `join_filter`).
  - *Key terms*: `how="left"`, `@register_action`.

**libs/transformer/tests/**
- `test_wrangler.py`: Universal runner test script mapping test TSV files against dummy Yaml representations to verify standard functionality independently of the UI.
  - *Inputs/Outputs*: Local testing files -> Materialized TSV assertions.
  - *Key Logic*: Follows Verification Protocol rules (CLI-execution, argparse, isolated environment).
  - *Key terms*: `pytest`, `assert`.

### assets/scripts/ (Orchestration & Verification Asset Tooling)
- `create_manifest.py` / `SF_create_manifest.py`: Automates the generation of compliant Hybrid Manifest boilerplate from legacy templates.
  - *Inputs/Outputs*: Excel/Templates -> `input_fields`, `output_fields`, and `wrangling` YAML files.

- `assembler_debug.py`: Command Line executor bridging the YAML manifest definitions and the `DataAssembler` relational module for Phase 4 checks.
  - *Inputs/Outputs*: Pipeline schema and synthetic sources -> Final verified joined table outputs in `./tmp/`.
  - *Key Logic*: Evaluates multi-source join outcomes (generating the `EVE_assembler_...` logs).
  - *Key terms*: `argparse`, `.collect()`.

- `create_test_data.py` / `create_test_deployment.py`: Generator scripts designed to populate `.tsv` matrices with synthetic fake inputs reflecting the configured contracts.
  - *Inputs/Outputs*: Contract manifest details -> Mock dataset instances.
  - *Key terms*: `synthetic_data`.

- `wrangle_debug.py`: CLI testing environment explicitly tailored to debug single dataset transformations (Wrangler context) prior to full assembly joining.
  - *Inputs/Outputs*: Single TSV + specific manifest block -> Raw verified table representation.
  - *Key Logic*: Emulates the core DataFrame manipulations without UI overhead.
  - *Key terms*: `.glimpse()`.

### config/manifests/ (Declarative Configuration Repositories)
**pipelines/1_Abromics_general_pipeline/**
- `*input_fields.yaml` / `*output_fields.yaml` / `*wrangling.yaml`: The distributed schema blocks (Data Contract) governing the boundaries and processing limits of distinct datasets (MLST, ResFinder, Metadata, Virulence).
  - *Inputs/Outputs*: Not applicable - Metadata definition files.
  - *Key Logic*: Dual-Validation schema enforcement rules to separate pure validation mapping from transformations.
  - *Key terms*: `fields`, `action:`.

- `1_Abromics_general_pipeline.yaml` / `AR1_..._Virulence.yaml`: The master orchestrating index files. Aggregates all atomic dataset sources via `!include` arrays and explicitly defines the `assembly_manifests` layer (Recipes + Joins).
  - *Inputs/Outputs*: Includes sub-layers -> Exposes full architecture scope to parsing engine.
  - *Key Logic*: The absolute "Source of Truth" regarding logic order and system operation rules for the VIGAS-P framework.
  - *Key terms*: `assembly_manifests`, `!include`.

## 2. Latent Rule Extraction

### Implicit Systemic Code Behaviors
1. **Implicit Polars Execution Scope**: 
   - `libs/` maintains pure `LazyFrame` processing all the way until `viz_factory` rendering or `assets/scripts/` debug evaluations. Code must NOT utilize `.collect()` inside standard action decorators in order to preserve optimization and cross-decorator deferment.
2. **Key-as-ID Join Resolution**:
   - Instead of explicitly handling every column mapping variation, multi-dataset Assembly heavily relies on evaluating the `is_primary_key: true` property flag located dynamically in `yaml` sources formatting them consistently into `sample_id` before left or inner joining operations.
3. **Dynamic Decorator Loading (`@register_action`)**: 
   - Instead of manually importing action implementations, rules are tied loosely into isolated single-purpose script files (like `libs/transformer/src/actions/core/null_handling.py`). These scripts are initialized passively through the local module directory `__init__.py`, executing their `@register_action(name)` block to populate the global `AVAILABLE_WRANGLING_ACTIONS` dictionary upon app boot. 
4. **Final Contract as a Safe `.select()` Query Guard**:
   - The end-state `output_fields` contract strictly mimics the SQL/Polars `SELECT` command acting as the primary defense against unexpected metadata drift. It prunes column noise that might be unintentionally ingested or created via intermediate joins.
5. **The `spec` Dict Unpacking Technique**: 
   - Every registered decorator exclusively accepts `(lf: pl.LazyFrame, spec: Dict[str, Any])`. Direct parameters extraction (like `spec.get("separator", ",")`) must occur inside the wrapper body. This guarantees homogeneity in the Registry call signatures.
