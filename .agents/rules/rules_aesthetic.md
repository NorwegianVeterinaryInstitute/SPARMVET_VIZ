---
trigger: always_on
date: 2026-03-29
purpose: Aesthetic and documentation standards for SPARMVET_VIZ
---

# Aesthetics & Documentation Standards (rules_aesthetic.md)

## 1. The Violet Law (Component Reference Standard)
Agents MUST use the explicit 'Violet' standard format when referring to architectural components in any documentation (Markdown, Quarto, IDE):
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
- **Knowledge Mirroring:** 
    - Master Source: `docs/*/*.qmd` (Long prose).
    - Combat Log: `./.antigravity/knowledge/*.md` (Compressed summaries).
    - Sync Rule: Combat Log must match Master Source technically but stay aggressively compressed.

## 3. Visual & Aesthetic Standards
1. **Library READMEs:** Every library in `./libs/` MUST contain a `README.md` including Purpose, I/O, and Key Components (Violet Standard).
2. **Inline Code:** Use the 'Deep Violet' CSS theme for all inline code blocks (`background: #3a2a4d`, `color: #e0cffc`).
3. **Mermaid Diagrams:** Large diagrams must be wrapped in a `::: {.lightbox}` div to enable click-to-zoom in Quarto.
4. **CLI Prefix:** All logic verification CLI scripts must use the `debug_` prefix to distinguish them from unit tests.
