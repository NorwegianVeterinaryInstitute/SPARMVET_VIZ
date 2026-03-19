# SpAM Vet Viz Project Blockers & Critical Tasks

## Current Blockers

- **Environment Selection**: Final choice and execution of the installation environment (needs resolution for deployment validation).
- **Dependency Management**: Synchronization of dependency versions across different libraries (.toml files).
- **Registry Refactoring Complexity**: Completing the migration to a fully decoupled `actions/` plugin system from the monolithic `registry.py` is in progress but needs full verification.

## Imminent Critical Tasks

- **Dashboard-Shiny Integration**: Establishing the reactive link between the `DataIngestor`/`DataTransformer` output (Polars DataFrames) and the Shiny dashboard state.
- **Visualization Framework**: Development of modular Plotly wrappers that consume the "Native Nested Multi-Dataset" output structure.
- **Wrangling Action Documentation**: Ensuring all declarative actions are documented in the Quarto cheatsheet with clear YAML syntax examples for non-programmer maintainers.
- **Multi-Dataset Validation**: Stretching the "Explode-Join-Collapse" algorithm for complex AMR phenotype mappings beyond the ResFinder example.
