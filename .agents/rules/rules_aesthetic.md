---
trigger: always_on
date: 2026-03-29
purpose: Aesthetic and documentation standards for SPARMVET_VIZ
---

# Aesthetics & Documentation Standards (rules_aesthetic.md)

## 1. The Violet Law (Documentation Standard ONLY)
Agents MUST use the explicit 'Violet' standard format when referring to architectural components in any **DOCUMENTATION**. This is a DOCUMENTATION-ONLY standard. It applies to .qmd files, intended for USER/HUMAN consumption only (NOT to READMEs, and high-level Docstrings). It MUST NOT be used for functional variable names, filenames, or class definitions within the logic.
- **Format:** `ComponentName (file_name.py)`
- **Core Examples:**
    - `DataWrangler (data_wrangler.py)`
    - `DataAssembler (data_assembler.py)`
    - `ActionRegistry (registry.py)`
    - `DataIngestor (ingestor.py)`
    - `VizFactory (viz_factory.py)`
    - `UniversalRunner (wrangler_debug.py)`

## 2. Documentation Integrity
- **No Source Repetition:** Never repeat source code or data content within docs. Use relative links instead.
- **Ultimate Source of Truth:** All changes MUST be reflected in the user docs (`docs/`). At the end of the project, `docs/` is the absolute source of truth for the human reader.
- **Split-Documentation Strategy:** Core architecture and workflow documents (`foundations/`, `workflows/`) MUST provide only high-level, rapid overviews/tables for developers. All concrete YAML "Recipes" and exhaustive usage examples MUST reside in the `appendix/` to serve non-programmer users without bloating the mental model of the primary guides.
- **Concrete Examples Mandate:** All human-facing documentation defining pipelines or visual components MUST include concrete YAML usage examples ("Recipes") so non-programmers can natively implement the logic.
- **Native Quarto Integration (No Redundancy):** Do not create redundant `.qmd` files in the root folder or invent arbitrary new directories. All new directives and standards MUST be organically integrated into the existing architectural sections (`foundations/`, `workflows/`, `reference/`, `appendix/`) based on semantic fit.
- **Knowledge Mirroring:** 
    - Master Source: `docs/*/*.qmd` (Long prose).
    - Combat Log: `./.antigravity/knowledge/*.md` (Compressed summaries).
    - Sync Rule: Combat Log must match Master Source technically but stay aggressively compressed.

## 3. Visual & Aesthetic Standards (Documentation Only)
1. **Library READMEs:** Every library in `./libs/` MUST contain a `README.md` including Purpose, I/O, and Key Components (Violet Standard).
2. **Inline Code:** Use the 'Deep Violet' CSS theme for all **DOCUMENTATION** inline code blocks (`background: #3a2a4d`, `color: #e0cffc`).
3. **Plotting Themes:** Functional plotting themes in `libs/viz_factory/` MUST use standard descriptive names (e.g., `theme_minimal`, `theme_dashboard`). Do NOT use 'violet' as a prefix for functional logic.
4. **Mermaid Diagrams:** Large diagrams must be wrapped in a `::: {.lightbox}` div to enable click-to-zoom in Quarto.
5. **CLI Prefix:** All logic verification CLI scripts must use the `debug_` prefix to distinguish them from unit tests.
