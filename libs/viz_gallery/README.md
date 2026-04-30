# VizGallery Library (viz_gallery)

**Scientific Textbook & Cookbook Persistence Layer**

## Overview

`viz_gallery` manages the storage, retrieval, and indexing of SPARMVET recipes. It ensures that every plot in the "Scientific Cookbook" adheres to the formal governance standards.

## Key Components

- **GalleryManager (gallery_manager.py)**: Handles the creation of gallery bundles (YAML, TSV, MD, PNG).
- **GalleryIndexer (integrated in GalleryManager)**: Generates the `gallery_index.json` Pivot-Index for zero-latency filtering.

## Maintenance (ADR-037)

The gallery requires a pre-computed index for UI efficiency. Run the following command from the project root to rebuild the index and perform an integrity audit:

```bash
export PYTHONPATH=$PYTHONPATH:. && ./.venv/bin/python libs/viz_gallery/assets/refresh_gallery.py
```

## Governance (Mandatory Triplet)

Every gallery bundle folder MUST contain:

1. `recipe_manifest.yaml` (including taxonomy: family, pattern, difficulty)
2. `example_data.tsv`
3. `recipe_meta.md`
4. `preview_plot.png`
