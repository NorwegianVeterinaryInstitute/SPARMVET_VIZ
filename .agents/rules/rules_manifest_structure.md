---
trigger: always_on
---

# Manifest Structural Standard (rules_manifest_structure.md)

**Authority:** Defines the structural organization and explicit layout requirements for all project data and plotting manifests.

## 1. Basename Mirroring Mandate

To maintain modularity and prevent YAML file bloat, top-level manifests MUST separate their logical components into individual YAML snippet files via the `!include` constructor.

- **The Rule**: A main manifest file (e.g., `main.yaml`) MUST organize its `!include` components within a directory matching its exact basename (e.g., a `main/` directory located at same level as `main.yaml`).

## 2. Directory Taxonomy (The Subdirectories)

Within the mirrored basename directory, components must be strictly categorized into subdirectories based on the major parts of the manifest configuration. Specifically (extrapolating from the standard format template):

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
