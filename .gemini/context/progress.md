# Project Progress

## Milestones

- [x] Environment & Agent Configuration
- [x] Architecture Review & Documentation refinement 
- [x] Build helpers described in docs/guide/additional_utilities.qmd
- [x] user : change and defines a test dataset using the helper to build fake data from real data
- [x] Design YAML Configuration Registry (Action Registry & UI Help)
- [x] Build First Data Contract from a test dataset (tsv + metadata)
- [ ] User must edit the data contract for further iterative building of the dashboard
- [ ] Installation environment choice and exectution 
- [ ] updating dependencies for each libraries in .toml file and for the general project
- [ ] Implement Walking Skeleton Core Layers

### minor changes to implement
- [x] parse_pipeline_excel.py : add option to chose name of the primary key that will be used (to keep reusability for different kind of datasets)
- [x] create_test_data.py : add support for multiple disparate primary keys and an option to homogenize them in the output.

## Progress Log

### 2026-03-05
- **Architecture Review Completed**: Conducted a comprehensive review of the Walking Skeleton documentation in `docs/`. Identified and resolved multiple `#TODO` and `#REVIEW` tags.
- **Documentation Built**: Fixed paths, created `guide/new_species.qmd`, added sequence diagrams for the Dashboard Filter message flows, and formalized the codebase organization principles.
- **Key Technical Decisions Formalized**:
  - Adopted **Polars LazyFrames** execution over writing intermediate files for memory-efficient filtering.
  - Solidified **User Preferences** logic (deep updating visualization config while strictly blocking data contract modification).
  - Defined rigid **Validation Rules** (strict for pipeline `data_schema`, minimum mandatory for `metadata_schema`).
  - Outlined scale pathways utilizing **Git Submodules** for decoupled `libs/` business logic.
- **Context Updated**: Moved the completed architectural review report into `.gemini/context/2026-03-05_walking_skeleton_review.md`.

### 2026-03-06
- **Configuration Strategy Design**: Designed a reusable dashboard configuration strategy involving a hierarchical directory structure for YAML files, a recursive loader, and a deep merging strategy for plot archetypes, species manifests, and user preferences. Clarified handling of different data sources (user uploads vs. fixed pipelines).
- **Helper Scripts Built**: Created and refined Python helper scripts (`create_test_data.py`, `create_manifest.py`, `create_test_deployment.py`) to automate generating synthetic datasets, manifest files, and deployment configurations. Ensured TSV output standards and resolved linting/type-checking issues.

### 2026-03-07
- **YAML Configuration Registry Architecture**: Designed and implemented the "Four-Pillar Registration Strategy" to safely handle user-authored YAML wrangling rules.
  - **Python Registry (`libs/transformer/src/registry.py`)**: Created a central dictionary mapping string actions (e.g., `split_and_explode`) to Polars LazyFrame functions.
  - **Data Wrangler (`libs/transformer/src/data_wrangler.py`)**: Implemented core module capable of dynamically applying registered actions from YAML and expanding category tags (e.g., `@AMR`).
  - **Documentation & UI**: Authored the `docs/appendix/Standards_yaml.qmd` Cookbook for non-programmers and created the `app/modules/help_registry.py` Shiny module to auto-generate a UI Help tab directly from the Python Registry.

- **Missing Data Harmonization Strategy Resolved**: Upgraded data contract guidelines to deal with real-world null/not tested strings via `action_replace_values`. Updated `create_test_data.py` to optionally inject these edge cases (along with true 8-digit randomized primary keys and duplicates/mismatches generation).

- **Architectural Pivot: Native Multi-Dataset Ingestion**: Replaced the "Wide Table" concept for multi-sheet pipeline outputs in favor of a declarative multi-dataset ingestion framework. 
  - Substituted the single `data_schema` parameter with the modular `data_schemas` *dictionary* rule across all backend python and YAML templates (`e_coli.yaml`, `audit.yaml`).
  - Completed `docs/guide/new_data_contract.qmd` explaining automatic "Primary Key Harmonization" between dataset arrays and metadata keys during the ingestion cycle's Left Join layer.
  - Authored a fully functional `assets/scripts/parse_pipeline_excel.py` utility that flattens Excel sheets directly into clean CSV pipelines, negating the need for complex pandas joins.

- **Manifest Generator Evolution (`create_manifest.py`)**: Upgraded to natively scaffold Multi-Dataset architectures.
  - **Directory Input & Validation**: Added `--data_dir` and `--data_files` with strict file existence checks to ingest entire directories of pipeline results.
  - **Schema-on-Read Nomenclature**: Implemented severe Regex sanitization (`clean_column_name`) to ensure all TSV headers are translated into perfectly safe, snake_case YAML dictionary keys (whilst retaining the `original_name` for the ingestion Polars renaming logic).
  - **Glob-Match Schemas**: Implemented Regex filename stripping to generate clean schema lookup keys (e.g. `Summary` instead of `test_data_Summary_20260307.tsv`), laying the groundwork for glob-based directory loaders.

### 2026-03-08
- **Modular YAML Configurations (`!include`)**: Implemented a custom PyYAML constructor in `libs/utils/src/loader2.py` to natively stitch fragmented YAML dictionaries. This eradicates the need to maintain monolithic 600-line configuration files.
  - Successfully verified the `ConfigManager` can load a Master manifest, seamlessly traversing subdirectories to populate nested dictionary keys without upstream application modifications.
- **Native Modular Manifest Scaffolding**: Refactored the `create_manifest.py` helper script. It now automatically generates the "Master Configuration File" and a subfolder containing individual fragments (`ResFinder.yaml`, `metadata_schema.yaml`) joined via clean `!include` string tags.
- **Data Contract Proved**: Successfully generated `1_test_data_ST22_dummy.yaml`, thereby validating the scaffolded data contract from our previous fake dataset generator step.
- **Developer Documentation Split**: Completely separated generic "Conceptual Guidelines" (`docs/guide/`) from execution-heavy environments. Created the `docs/cheatsheets/` structure containing atomic, copy-paste snippets for setting up the `PYTHONPATH`, testing the `ConfigManager` via scripts (`libs/utils/tests/test_loader.py`), and running helper utilities.
