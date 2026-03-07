# Project Progress

## Milestones

- [x] Environment & Agent Configuration
- [x] Architecture Review & Documentation refinement 
- [x] Build helpers described in docs/guide/additional_utilities.qmd
- [ ] user : change and defines a test dataset using the helper to build fake data from real data
- [x] Design YAML Configuration Registry (Action Registry & UI Help)
- [ ] Build First Data Contract from a test dataset (tsv + metadata)
- [ ] Installation environment choice and exectution 
- [ ] updating dependencies for each libraries in .toml file and for the general project
- [ ] Implement Walking Skeleton Core Layers

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
