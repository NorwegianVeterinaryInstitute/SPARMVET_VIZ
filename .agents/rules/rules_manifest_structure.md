---
trigger: always_on
---

# Manifest Structural Standard (rules_manifest_structure.md)

**Authority:** Defines the structural organization and explicit layout requirements for all project data and plotting manifests.

## 1. Basename Mirroring Mandate (Keyword & Complexity Trigger)

To maintain modularity and prevent YAML bloat, **high-complexity manifests** (e.g., Master Pipelines) MUST separate their logical components into individual YAML snippet files via the `!include` constructor.

- **The Rule**: A main manifest file (e.g., `main.yaml`) MUST organize its `!include` components within a directory matching its exact basename (e.g., a `main/` directory located at same level as `main.yaml`).
- **Complexity Trigger**: For small or "Single-Task" manifests, inline logic is permitted to avoid overhead. However, any manifest exceeding ~150 lines or involving more than 3 data sources MUST transition to the Mirrored Directory standard.

## 2. Directory Taxonomy (Keyword-Driven Organization)

When decomposition is triggered, components must be strictly categorized into subdirectories based on their logical keywords. Specifically:

- `input_fields/`: Defines raw incoming schemas.
- `wrangling/`: Defines all Transformation (`tier1`, `tier2`) operations.
- `output_fields/`: Defines the terminal contract schemas.
- `plots/`: Contains visualization specifications mapping aesthetics and layers.

## 3. Structural Authority Reference

The file `assets/template_manifests/1_test_data_ST22_dummy.yaml` serves as the official structural standard.

- Any adaptations made to the `1_test_data_ST22_dummy.yaml` template logic or subdirectory groupings MUST be immediately reflected back into this rulebook to remain the authoritative requirement for the entire system.

## 4. Documentation & Appendix Mandate

- **User Documentation Sync**: Any changes made to the structure of manifests MUST be immediately reflected in the appropriate library READMEs and user-facing `.qmd` documentation files.
- **Standalone Appendix Registry**: The YAML manifest structure must be physically maintained as a standalone reference file located at `docs/appendix/manifest_structure.yaml`. If any changes are implemented regarding how manifests are used, grouped, or structured, this appendix file must be updated to serve as the external user-facing source of truth.

## 5. Explicit Whitelisting (The Final Contract)
- **The Protocol**: The `final_contract` block in a pipeline or assembly manifest is an **Exclusive Whitelist**. 
- **The Effect**: Any column existing in the dataframe but not explicitly listed in the `final_contract` will be dropped by the Assembler projection guard. 
- **Developer Rule**: Always check the `final_contract` if a newly created column is missing from the output TSV/Parquet.

## 6. Biological Typing & Discrete Plotting
- **The Protocol**: To ensure Plotnine correctly renders discrete scales (e.g., for Year, Sequence Type), columns MUST be cast to appropriate types in the assembly recipe.
- **The Rule**: Numeric values used as categories (integer years) MUST be cast to `int` or `string` in the Tier 2 assembly to prevent continuous-scale stretching in visualizations.
