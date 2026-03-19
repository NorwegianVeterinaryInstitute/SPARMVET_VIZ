# SpAM Vet Viz Project Milestones

## Completed Milestones (Walking Skeleton Foundation)

- **Environment & Agent Configuration**: Completed (Phase 1).
- **Architecture Review & Doc Refinement**: Completed. Comprehensive review with sequence diagrams and formalized codebase organization.
- **YAML Configuration Registry (Action Registry & UI Help)**: Built using the "Four-Pillar Registration Strategy".
- **Data Contract Prototyping**: First data contract built from test datasets (TSV + metadata).
- **Modular YAML Implementation (`!include`)**: Custom PyYAML constructor for recursive loader / `ConfigManager` implemented.
- **Reference Catalogue Architecture**: Established `config/references/` governance with mandatory READMEs.
- **Core Library Refactoring**: Standardized Python module names (`config_loader.py`, `DataIngestor`).
- **Transformer Plugin Action Registry**: Scalable system using `@register_action(name)` decorators.
- **End-to-End System Verification**: Successful ResFinder dataset ingestion and transformation (validation of Category Derivation).
- **Documentation Standards**: Implementation of Documentation DRY rule using Quarto's `{{< include >}}`.

## Planned & Partially Completed (Next Steps)

- **Transformer Extensibility (Phase 2)**:
  - Refactoring Action Registry into Submodule (In progress: `actions/` plugin system).
  - Documentation of Wrangling Actions (Quarto cheatsheet/handbook).
  - Validation of ResFinder wrangling against specific rules.
- **Dashboard Assembly (Phase 3)**:
  - Drafting Plotly visualization wrappers.
  - Integration with Shiny (Express) application state.
- **System Orchestration**:
  - Installation environment choice and execution.
  - Dependency update for all sub-libraries and central project.
