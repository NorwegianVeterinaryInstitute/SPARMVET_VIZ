tags:: [UI-Contract, Design, Behavioral, Requirements, ui, dashboad, planning, thinking]

future discussions on the UI Requirements and Design Phase.
PART 1: First definition
# 🏛️ SPARMVET UI-Contract: Design & Behavioral Requirements

## 1. Multi-Panel Layout & Navigation
* **Logical Partitioning**: The UI shall use a tabset navigation (`ui.navset_tab`) to separate distinct workflows.
* **The Global Sidebar**: A persistent control panel on the left for universal filters (Date, Species, Antibiotic) that affects all tabs simultaneously.
* **Collapsible Cards**: Visualizations and data tables shall be housed in expandable cards, allowing users to "maximize" a plot or table for deep inspection.

## 2. Dual-State Data Strategy (ADR-024)
* **Tab A: Raw Baseline (Tier 1)**: A read-only "Ground Truth" view showing the un-filtered Anchor dataset to provide a constant reference point.
* **Tab B: Active Exploration (Tier 2)**: The "Working View" where users apply filters, clean data, and see real-time updates to plots.
* **The Short-Circuit**: The UI must leverage the Tier 1 Parquet anchor to ensure sub-5-second responsiveness even with 200k+ rows.

## 3. The "Excel-Plus" Interactivity
* **Synced Selection**: Selection in an Excel-like data grid (DT/DataGrid) must instantly highlight corresponding points in the Viz Factory plot.
* **Plot Interactivity (Brushing)**: Users can draw a box ("brush") over outliers in a Plotnine graph to identify specific Sample IDs for exclusion.
* **Manual Annotation**: Every manual exclusion or filter change must trigger a mandatory popup (modal) asking for a **User Note** (e.g., "Plate contamination suspected").

## 4. Immutable Audit Trace & Locking
* **The Narrative Log**: A sidebar "Journal" records every action: `[Action] + [Timestamp] + [Affected IDs] + [User Note]`.
* **Reversibility**: Users can "Undo" specific steps in the log, which triggers the Transformer to re-run the Tier 2 LazyFrame.
* **Session State Locking**: Once an export is initiated, the Audit Trace for that specific version is "Locked" and archived.

## 5. Publication-Ready Export Engine
* **The "Submission Package"**: Exports shall be delivered as a `.zip` bundle containing:
    1.  **Plots**: High-DPI PNG (600 DPI) for Word/PPT and SVG/PDF for journal submission.
    2.  **Audit Log**: A human-readable `.txt` or `.docx` file (via Pandoc) summarizing the "Materials and Methods" of the data cleaning.
    3.  **Data Subset**: The exact Tier 2 CSV/Parquet used for the final visualization.
* **Session Re-Run**: The system shall allow users to upload a saved Audit Trace to perfectly reconstruct a previous UI state for revision.

## 6. Implementation Principles
* **Violet Law Compliance**: All UI component IDs and reactive variables must follow the project's standardized naming convention.
* **Integrity Suite Support**: The UI must have a "Debug/QC" mode that runs the `viz_factory_integrity_suite.py` and displays the report directly to the user.


---- 
PART 2 : #TODO integrate all together at review  : The Extended UI-Contract: Branching & Persona Logic

# # 🗺️ SPARMVET UI-Contract: Versioning, Branching, and Personas

## 1. UI Bootloader & Persona Management
* **Environment-Aware Launch**: The app shall check a `ui_config.yaml` or environment flag (`--mode`) at startup to determine the "Persona" (Pipeline, Developer, or Hybrid).
* **Feature Masking**: 
    * **Pipeline Mode**: Features like "Add Data," "Branching," and "Manual Wrangling" are hidden/locked for performance and consistency.
    * **Developer Mode**: All "Helper" tools, the "Gallery," and "Branching" are active.
* **Component Registry**: UI elements (Sidebar, Tabs, Export Panel) shall be modular "Lego blocks" loaded dynamically based on the active Persona.

## 2. Immutable Anchor & Branching Logic (ADR-024)
* **The "Save Point" (Tier 1)**: Once a dataset is processed into a Tier 1 Anchor (Parquet), it becomes the immutable root for all further analysis.
* **Logic Branching**: Users can trigger a "New Branch" from any existing Anchor. This creates a secondary reactive path in the UI without re-loading the raw data.
* **Parallel Views**: The UI supports switching between "Branch A" and "Branch B" instantly by swapping the active Transformation Manifest.

## 3. Manifest Evolution & Recipes
* **Recipe-Based Analysis**: The UI shall save the "Recipe" (Steps) as a 2KB YAML Manifest, not the 200MB Data.
* **Cloning/Templating**: Users can "Clone" an existing Manifest to use as a starting point for a new branch, enabling rapid iteration.
* **Data-Agnostic Manifests**: A "Perfect Plot" manifest created on Dataset X can be "Replayed" on Dataset Y, provided it meets the Data Contract.

## 4. The Interactive Design Studio (Helpers)
* **Manifest Helper**: A visual interface for building Transformer chains (e.g., drag-and-drop 'unpivot' or 'filter' nodes).
* **The Inspiration Gallery**: A toggleable side-panel showing plot examples, required data contracts, and a "Copy to Sandbox" button.
* **Contextual Provenance**: Every manual filter in a branch must include a user-written "Why" note, stored in the Branch Manifest.

----
PART 3 #TODO important improvement usage 

# 💡 Advanced UI & Development Strategy: Strategic Improvements

## 1. Usability: The "Pre-Flight" Data Contract Validator
* **Concept**: Before applying a Manifest to a dataset, the UI performs a "Dry Run" to ensure the data columns match the requirements of the Wrangling steps and the Viz Factory Geoms.
* **User Experience**: Instead of a "Crash" or a blank plot, the user sees a **Compatibility Dashboard**.
* **Logic**: 
    * 🟢 **Green**: Data meets all requirements.
    * 🟡 **Yellow**: Minor mismatch (e.g., 'Species' column is named 'species_name'—UI suggests an auto-rename).
    * 🔴 **Red**: Critical missing data (e.g., 'MIC' column missing for a resistance plot).
* **Benefit**: Reduces user frustration and prevents "Ghost Errors" in scientific output.

## 2. Reliability: The "Ghost Manifest" (Session Auto-Save)
* **Concept**: The UI silently caches the current state (the active Manifest and Branching Tree) to the browser's local storage or a temporary `tmp/` file.
* **User Experience**: If the browser is accidentally closed or the session times out, a "Restore Session" prompt appears upon reload.
* **Logic**: Every change in the UI triggers a lightweight YAML sync to a hidden `last_state.yaml`.
* **Benefit**: Protects hours of "Manual Annotation" and "Branching" work from being lost to connectivity issues.

## 3. Development: "Headless" Persona Testing (Playwright/Shiny.test)
* **Concept**: Automated scripts that "impersonate" the different UI Personas (Pipeline, Developer, Hybrid) to verify feature masking.
* **Developer Experience**: You can run one command to verify that a new feature in 'Developer Mode' hasn't accidentally appeared in the 'Locked Pipeline' UI.
* **Logic**: CI/CD (Continuous Integration) scripts that click through the UI "blindly" to ensure permissions and buttons are correctly displayed/hidden based on the `ui_config.yaml`.
* **Benefit**: Ensures the "Production" environment remains stable while the "Developer" environment evolves rapidly.

## 4. Discovery: The "Component Sandbox" & Gallery
* **Concept**: A dedicated UI panel where users can "Test-Drive" individual Transformer decorators or Viz Factory Geoms without affecting their main branch.
* **User Experience**: A "Try it out" button in the Gallery that loads a tiny sample dataset so the user can see exactly how an 'unpivot' or 'facet_wrap' works before committing it to their analysis.
* **Benefit**: Acts as an "In-App University," teaching the user how to use the library's more advanced features.