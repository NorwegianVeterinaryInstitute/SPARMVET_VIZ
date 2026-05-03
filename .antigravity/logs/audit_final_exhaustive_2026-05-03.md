# Exhaustive Architectural Audit & Technical Debt Report
**Date:** 2026-05-03
**Scope:** Full repository assessment against ADRs, conventions, and roadmaps.

## Executive Summary
This report compiles all undiscovered architectural violations, legacy drift, and bugs found across the SPARMVET_VIZ codebase, fully merged with the previous in-depth audit findings. It serves as the single, authoritative actionable checklist for the remediation agent. Several critical rules (like the Two-Category Law, Path-Hacking Ban, and Violet Law) are systematically violated, alongside known scientific blockers and UI deficits.

---

## 1. Unreported Incomplete Tasks & Logic Gaps

### A. Ingestion Sanitization (Ghost Logic)
`libs/ingestion/src/ingestion/placeholder/um_sanitization.py` contains critical `TODO`s that are completely absent from `tasks.md`. The module lacks implementations for:
- Data type transformations
- Missing mandatory column reporting
- Whitespace/Windows character cleaning
- Informing the Orchestrator on failures

### B. ST22 Lineage 2 (Plasmid Dynamics) Incompletion
`tasks.md` lists the assembly step as: `[ ] Assemble with metadata and AMR results`. However, `config/manifests/pipelines/2_test_data_ST22_dummy/assembly/Plasmid_Profile_Joint.yaml` only joins `metadata_schema` and fails to integrate the required AMR data (`amr_data`).

### C. VizFactory Gaps (Spatial & Network Data)
- **Spatial Data (`GALLERY-MAP` / `geom_map`):** Blocked because the system lacks a spatial manifest format and `GeoDataFrame` support within `VizFactory`.
- **Network Data (`GALLERY-FLOW`):** Blocked because Plotnine has no native support for Chord/Sankey diagrams. Requires a decision on whether `VizFactory` should support non-Plotnine renderers.

---

## 2. Inconsistencies, Errors, and Engine Bugs

### A. The Boolean Manifest Trap (Critical)
The data engine is susceptible to silent failures when `on:` is unquoted, as YAML parses it as `True: ...`. The following manifests violate the `"Always write it as 'on':"` rule:
- `config/manifests/templates/complex_demo/master_recipe.yaml:4`
- `config/manifests/templates/simple_project_template.yaml:43`
- `config/manifests/pipelines/1_test_data_ST22_dummy/assembly/Summary_phenotype_length_fragmentation_assembly.yaml:33`
- `config/manifests/pipelines/1_test_data_ST22_dummy/wrangling/Detailed_Summary_assembly_wrangling.yaml:3`
- `config/manifests/pipelines/1_test_data_ST22_dummy/wrangling/Summary_wrangling.yaml:12`

### B. Missing `SPARMVET_Error` (ADR-034 Violation)
ADR-034 explicitly states that "every significant component MUST include at least one Automated Failure Test... that intentionally triggers a `SPARMVET_Error`". The `SPARMVET_Error` class does not exist in the codebase. Tests currently raise fragmented errors (`ManifestError`, `TransformationError`, etc.).

### C. Cross-Library Imports (ADR-011 Violation)
The "Clear Lines Library Policy" strictly forbids libraries in `libs/` from importing from one another. This is actively violated:
- `libs/transformer/src/transformer/pipeline.py` imports `ingestion.ingestor` and `utils.config_loader`.
- `libs/transformer/src/transformer/data_wrangler.py` and `metadata_validator.py` import `utils.errors`.
- `libs/transformer/src/transformer/data_assembler.py` imports `utils.hashing`.

### D. T3 LazyFrame Threading
When new Tier 3 node types (e.g., rename, derive, pivot) are added, the threading mechanism in `_apply_t3_to_lf` needs explicit expansion. This design is pending review in `design_sge_lineage_t3.md`.

---

## 3. Path Hacking & CLI Protocol Violations

### A. Path Hacking Ban (ADR-016)
`sys.path.append` and `sys.path.insert` are explicitly forbidden across the entire project (including tests). Violations exist in:
- `libs/viz_gallery/tests/debug_gallery_ui_logic.py`
- `libs/utils/tests/debug_blueprint_mapper.py`
- `app/tests/debug_pipeline_connector.py`
- `app/tests/debug_home_theater.py`
- `app/tests/debug_session_flow.py`
- `libs/viz_gallery/assets/generate_previews.py`

### B. Argparse & Hardcoded Paths (rules_verification_testing.md §2)
"Hardcoding paths in the execution blocks is strictly FORBIDDEN." The following scripts lack `argparse` and/or contain hardcoded paths:
- `assets/scripts/generate_demo_data.py` (Hardcodes `Path("assets/test_data/...")`)
- `assets/scripts/materialize_manifest_plots.py`
- `assets/scripts/figshare_plot_integration.py`
- `libs/transformer/tests/debug_decorator_suite.py`
- `libs/utils/tests/debug_blueprint_mapper.py`

### C. Directory Governance (ADR-032 Violation)
Library-internal test/debug runners belong inside their respective `libs/` packages. `assets/scripts/` is reserved for cross-library helpers. 
- **Inconsistency:** `assets/scripts/debug_viz_factory_audit.py` should be moved to `libs/viz_factory/tests/`.

### D. Materialization & Debugging Infrastructure
The debug runners (`debug_wrangler.py` and `debug_assembler.py`) do not automatically route output to standard dated subfolders (`tmp/YYYY-MM-DD/{lineage_id}/`) as prescribed by the scientific audit protocol.

---

## 4. UI Architecture Violations (ADR-045) & UX Deficits

### A. The Two-Category Law
Files inside `app/modules/` are strictly limited to pure Python introspection and must contain "Zero Shiny imports." The following files violate this law by importing `shiny` (and should be moved to `app/handlers/` or refactored):
- `app/modules/wrangle_studio.py`
- `app/modules/help_registry.py`
- `app/modules/gallery_viewer.py`
- `app/modules/dev_studio.py`

### B. Theater and Export Functionality
- **`THEATER-1` (Plot Collapse):** Users cannot currently collapse/minimize individual plot panels within the accordion.
- **`EXPORT-TUBEMAP`:** Global export bundle lacks a static map of the T1→T2 lineage. A headless render path for `BlueprintMapper.generate_cy_elements()` is required.
- **Selective Export (`EXPORT-2`):** Global export lacks UI checkboxes allowing users to selectively include/exclude T1/T2/T3 data or recipes.

### C. Notification Resilience
- **`UX-NOTIF-2`:** Toast notifications do not survive a page refresh because they are not persisted to the T3 ghost state.
- **`UX-NOTIF-3`:** There is no project-load notification when the Blueprint Architect reloads a manifest without changing the `project_id`.

---

## 5. Dependency Tracking System Failures

### A. Missing `@deps` Blocks (workspace_standard.md §5)
Over 70 Python files lack the mandatory `@deps` annotation block. This cripples the dependency graph generation. Major violators include:
- Core UI files: `app/src/main.py`, `app/src/bootloader.py`, `app/src/server.py`, `app/src/ui.py`
- App handlers: `app/handlers/notification_utils.py`
- All connector adapters (`libs/connector/src/connector/*.py`)
- All generator utils (`libs/generator_utils/src/generator_utils/*.py`)
- All gallery viewer components (`libs/viz_gallery/`)

---

## 6. Documentation State & Violet Law Drift

### A. The Violet Law
ADR-029 states: "Agents MUST use the explicit 'Violet' standard format when referring to architectural components in HUMAN-FACING DOCUMENTATION ONLY". The `README.md` files inside the libraries use plain markdown codeblocks (e.g., `` `VizFactory` ``) instead of the mandated `` `VizFactory (viz_factory.py)` `` format. 
Violating files:
- `libs/viz_factory/README.md`
- `libs/connector/README.md`
- `libs/transformer/README.md`
- `libs/generator_utils/README.md`
- `libs/utils/README.md`

### B. Pipeline Terminology Drift
Generic terminology like `phenotype` still exists in some manifests instead of the mandated `predicted_phenotype`. A systematic renaming pass is needed.

### C. Taxonomy Documentation Drift
The newly added 6-axis taxonomy (`geom`, `show`, `sample_size`), referenced in `TAXONOMY_CHEATSHEET.md` and Phase 26 updates, has not been documented in the user-facing guides. Both `docs/appendix/viz_factory_components.qmd` and `docs/user_guide/viz_gallery.qmd` are outdated. Furthermore, a Taxonomy Data Audit (`assets/gallery_data/*/recipe_manifest.yaml`) is required to verify the tags.

---

## Recommended Action Plan for Remediation Agent

1. **Mass `@deps` Injection:** Run a script to scaffold `@deps` blocks for all missing Python files, then execute `build_dep_graph.py`.
2. **YAML Sanitization & Terminology:** Use regex to replace unquoted `on:` with `'on':` across all manifests, and perform a precision renaming pass (`phenotype` -> `predicted_phenotype`).
3. **ADR-045 Refactoring:** Strip `shiny` imports from `app/modules/` or migrate those files entirely to `app/handlers/`.
4. **Library Isolation:** Refactor `pipeline.py` to remove `ingestor` dependency (potentially moving orchestration to `app/`). Migrate `TransformationError` out of `utils` if it's meant to be domain-specific, or update ADR-011 to explicitly whitelist `utils.errors`.
5. **Path Hacking Eradication:** Remove all `sys.path` inserts in tests; rely solely on `pip install -e .`. Move scripts like `debug_viz_factory_audit.py` out of `assets/scripts/` into library test folders.
6. **Argparse & Materialization Logic:** Rewrite `generate_demo_data.py` to use `argparse`. Ensure debug runners dynamically route output to `tmp/YYYY-MM-DD/`.
7. **Documentation Sync:** Run a global find-and-replace for Violet Law compliance in all `README.md` files and update `.qmd` files with the new taxonomy guidelines.
8. **Lineage 2 Completion:** Update `Plasmid_Profile_Joint.yaml` to successfully join the `amr_data` dataset.
