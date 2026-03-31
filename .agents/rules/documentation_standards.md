# Documentation Standards

This rulebook defines the "Dev-to-User" documentation strategy for the SPARMVET_VIZ project. It mandates a clear separation between high-level architectural overview and exhaustive, concrete implementation recipes.

## 1. The Split-Documentation Strategy
Core architecture and workflow documents (foundations/, workflows/) MUST provide only high-level, rapid overviews or tables for developers. All concrete YAML "Recipes" and exhaustive usage examples MUST reside in the `appendix/` to serve non-programmer users without bloating the mental model of the primary guides.

- **Primary Guides**: Compressed, technical, focused on "Why" and "Flow".
- **Appendix Galleries**: Step-by-step, exhaustive, focused on "Copy-Paste" recipes and "How-To".

## 2. Concrete Examples Mandate
All human-facing documentation defining pipelines (Wrangling) or visual components (Viz Factory) MUST include concrete YAML usage examples ("Recipes"). We build for non-programmers; theoretical descriptions without code examples are strictly forbidden.

## 3. The Violet Law (Documentation Standard)
Agents MUST use the explicit 'Violet' standard format when referring to architectural components in any **DOCUMENTATION** (.qmd files, README 'Key Components' lists, and high-level docs).
- **Format:** `ComponentName (file_name.py)`
- **Exception:** This is a DOCUMENTATION-ONLY standard. It MUST NOT be used for functional variable names, filenames, or class definitions within the logic.

## 4. Documentation DRY Rule
- **No Source Repetition**: Never repeat source code or data content within docs. Use Quarto's `{{< include path/to/script.py >}}` directive to dynamically embed live code files.
- **Single Source of Truth**: All changes MUST be reflected in the user docs (`docs/`) as the end-of-project absolute source of truth for the human reader.
