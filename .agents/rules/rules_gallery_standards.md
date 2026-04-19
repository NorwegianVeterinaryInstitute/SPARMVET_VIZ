# Gallery Asset Standards (rules_gallery_standards.md)

**Authority:** Enforced on all static gallery assets in `assets/gallery_data/`.

## 1. The Scientific Triplet (Mandatory Files)

Every gallery bundle directory MUST contain exactly:

- **`recipe_manifest.yaml`**: The executable logic (info, plots, wrangling).
- **`example_data.tsv`**: A representative dataset (tab-separated).
- **`recipe_meta.md`**: High-density scientific guidance and author metadata.
- **`preview_plot.png`**: The rendered evidence of the visualization.

## 2. Taxonomy Requirements

The `info:` block in `recipe_manifest.yaml` MUST define the following taxonomy fields:

| Field | Mandatory Values (Strict Enum) |
| :--- | :--- |
| **family** | Distribution, Correlation, Comparison, Ranking, Evolution, Part-to-Whole |
| **pattern** | 1 Numeric, 2 Numeric, 1 Numeric 1 Categorical, 1 Numeric 2 Categorical, etc. |
| **difficulty** | Simple, Intermediate, Advanced |

## 3. The Pivot-Index Integrity Gate

- The `gallery_index.json` is the sole source of truth for the UI.
- Direct editing of the index is FORBIDDEN.
- The index must be updated via `assets/scripts/refresh_gallery.py`.
- Any bundle failing the "Triplet Check" or missing taxonomy will be excluded from the index and marked as **[OOS] (Out of Standard)** in the audit log.

## 4. Documentation Hierarchy

- Markdown files MUST use the standard headers (`## Family`, `## Data Pattern`, `## Difficulty`) as specified in ADR-033/035.
- These headers are the primary source for the initial metadata extraction script.
