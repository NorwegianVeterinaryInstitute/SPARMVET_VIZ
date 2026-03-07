# Reusable Dashboard Configuration Strategy

This plan outlines the architecture for the dashboard's configuration system, allowing for a highly modular, scalable, and reusable setup for YAML configurations. This strategy addresses the need for dynamic data sources, hierarchical configuration organization, and deep merging of plot templates with species-specific manifests.

## User Review Required

> [!IMPORTANT]
> **Data Sources Strategy:** The architecture assumes that the **Manifest** defines the *shape and contract* of the data and what plots to show, while the **Data Source** (upload, pipeline, Galaxy, etc.) is resolved dynamically by the UI or the pipeline orchestrator. The manifest does *not* hardcode a specific file or history ID unless strictly necessary for a fixed pipeline run. Is this aligned with your expectation?
> 
> **Config Directory Structure:** Please review the proposed directory structure below and confirm it fits your mental model for the libraries.

## Proposed Architecture

### 1. Configuration Directory Reorganization

To support the growing library of YAML files and subcategories, we will restructure the `config/` directory. Each primary type of configuration gets its own root folder. Because the Python loader uses a recursive search (`rglob`), you can nest folders as deeply as needed to organize species or specific pipeline runs.

```text
config/
├── manifests/              # The "Who & What" (Data contracts & requested plots)
│   ├── species/
│   │   ├── e_coli/
│   │   │   ├── ecoli_base_v1.yaml
│   │   │   └── ecoli_special_audit.yaml
│   │   └── listeria/
│   │       └── listeria_v2.yaml
│   ├── audits/
│   │   └── lab_audit_2026.yaml
│   ├── templates/          # Base templates for manifests (kept here for now)
│   │   └── base_manifest_template.yaml
│   └── pipelines/
│       └── standard_amr_run.yaml
│
├── plot_archetypes/        # The "How to Draw" (Base plot geometries and stylistic defaults)
│   ├── genomic/
│   │   └── core_genome_tree.yaml
│   ├── resistance/
│   │   └── amr_heatmap.yaml
│   ├── phenotypes/
│   │   └── growth_scatter.yaml
│   └── custom_specialized/ # New specialized categories can be created infinitely
│       └── project_x_custom_plot.yaml
│
├── connectors/             # The "How to Connect" (API configs, adapter defaults)
│   ├── galaxy/
│   │   └── base_galaxy_api.yaml
│   └── local/
│       └── file_upload.yaml
│
├── deployments/            # Application Launch Context (pipeline runs, environment configs)
│   ├── prod_galaxy_dashboard.yaml
│   └── local_dev.yaml
│
└── user_preferences/       # UI overwrites (Colors, chosen plots, custom thresholds)
    └── default_ui_prefs.yaml
```

### 2. Strategy for Growth (Scalability)

As the library grows to dozens or hundreds of YAML files, filesystem organization alone isn't enough. The system will rely on the required headers to manage scale:

**Required Headers & Data Contracts**
Every configuration file must have a standard header:
```yaml
id: "ecoli_base_v1"
type: "species" # or "audit", "plot_template", "connector_config"
info:
  display_name: "E. coli Base Run"
  category: "AMR Analysis" # Can be used by the UI to group dropdowns
  tags: ["public", "verified", "2026"] # Flexible tagging for search
  description: "Standard data contract for..."
  version: "1.0"
```

**How this handles growth:**
- **Infinite Nesting**: You can put `project_x_custom_plot.yaml` anywhere inside `config/plot_archetypes/`. The loader will find it.
- **UI Filtering**: The Shiny UI won't just list 100 files; instead, it will query the Python `ConfigRegistry` for all configs where `type == "species"` and `category == "AMR Analysis"`.
- **Decoupled References**: If `ecoli_base_v1.yaml` wants a custom plot, it references the `id: "project_x_custom_plot"`. The Python loader handles finding exactly which subfolder that plot template lives in.

### 3. The Generic Recursive Loader ([libs/utils/config_loader.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/libs/utils/config_loader.py))

We will implement a `ConfigRegistry` class in Python that traverses the `config/` directory recursively using `pathlib.Path.rglob('*.yaml')`. 

- **Discovery:** It scans all subdirectories inside `plot_archetypes/`, `manifests/`, etc.
- **Namespacing & Indexing:** Instead of relying entirely on file paths, the registry will parse the YAML and index the configurations by their required `id` and `type` fields.
- **Deep Merging Strategy:** To resolve a final plot configuration for the UI, the loader will merge configurations in this priority order (highest priority wins):
  1. **User Preferences** (`user_preferences/`): UI overwrites for colors, themes, or plot visibility.
  2. **Manifest Specifics** (`manifests/`): The mapping of specific columns and titles defined in the active data contract (e.g., `e_coli.yaml`).
  3. **Plot Archetypes** (`plot_archetypes/`): The generic library defaults (e.g., `amr_heatmap.yaml`).

### 4. Application Launch Context (Dynamic vs. Fixed Pipelines)

How does the app know where the data comes from if it's not in the species manifest? The system will use an **Application Launch Context** defined by a `deployment.yaml` or pipeline-specific configuration. 

This enables two distinct modes of operation:

**Mode A: General Dashboard (Dynamic Data)**
1. **Developer Setup:** The `deployment.yaml` defines the environment as "General Upload".
2. **User Action:** The user opens the Shiny App. The UI displays an "Upload Data (TSV)" and "Upload Metadata (TSV)" button alongside a dropdown for "Select Species".
3. **Execution:** The User selects the `ecoli_v1` manifest and uploads their file. The Orchestrator passes the local file to the Ingestion Layer.

**Mode B: Fixed Pipeline Dashboard (Automated Data)**
1. **Developer Setup:** A bioinformatic pipeline finishes running in Galaxy. The pipeline script automatically generates a `run_config.yaml` that specifies:
   ```yaml
   type: "pipeline_run"
   target_connector: "galaxy/base_galaxy_api"
   connector_params:
     history_id: "hist_8989abc"
   allowed_manifests: ["species/ecoli_v1", "species/salmonella_v3"]
   ```
2. **User Action:** The user opens the Shiny App deployed for this specific run. The UI detects the `run_config.yaml`. The Data upload button is hidden, while an optional "Upload Metadata (TSV)" button remains. The UI fetches the main data automatically using the fixed Galaxy connector.
3. **Execution:** The User *only* has to choose between "E. coli" or "Salmonella" from a restricted dropdown. The Orchestrator combines the fixed connector data with the chosen species schema and any uploaded metadata TSV.

This ensures the **Species Manifest** remains purely about the *biology and visualization structure*, while a separate **Run/Deployment Config** handles the *IT infrastructure and data location*.

## Proposed Changes

### `config/` Directory
- Create the hierarchical structure (`manifests/`, `plot_archetypes/`, `connectors/`, `user_preferences/`).
- Ensure subdirectories (like `manifests/species/` and `manifests/audits/`) are created to support data categorization.

### `libs/utils/`
#### [NEW] `libs/utils/config_loader.py`
Create a `ConfigRegistry` class responsible for:
- Recursively loading all `.yaml` files from a specified base directory.
- Parsing the mandatory headers (`id`, `type`, `info`) and indexing them.
- Providing a `deep_merge(*dicts)` utility function to combine the Archetype -> Manifest -> UI Preferences.

### `app/src/`
#### [MODIFY] `app/src/server.py` or equivalent Controller
- Initialize the `ConfigRegistry` on application startup.
- Update the UI logic so dropdowns are dynamically populated using the parsed `info` from the registry.

## Verification Plan

### Automated Tests
- Create Python unit tests (`tests/test_config_loader.py`) to verify:
  1. The recursive loader finds files in deeply nested subdirectories.
  2. The namespacing correctly identifies the type of config.
  3. The `deep_merge` function correctly overwrites base defaults with manifest specifics without mutating the original template.

### Manual Verification
- Start the Shiny app and verify that the UI dropdown successfully reads and lists the manifests found in the reorganized `config/manifests/` nested subdirectories.
