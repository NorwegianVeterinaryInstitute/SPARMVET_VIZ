
🏛️ 1. UI Architecture Vision: The Adaptive Metasystem
------------------------------------------------------

The dashboard operates as a **Metadata-Driven Shell**. Instead of a static interface, it uses a **Bootloader** to determine its "Persona" and capabilities at startup.

* **Persona Logic**:
  * **Pipeline Mode (Demo Priority)**: A high-speed, "locked" interface for production results. It masks development tools to ensure consistency and prevent accidental data corruption.
  * **Developer Mode (Deferred)**: A "Design Studio" for building new manifests, branching data, and testing visualization components.
* **The UI-Contract (ADR-021)**: All UI components must respect the **Violet Law** for documentation and use **Polars LazyFrames** for the "Leaf" (Tier 3) filtering to ensure sub-5-second responsiveness.

* * *

📑 2. Data Strategy: The Tiered View Model
------------------------------------------

To maintain scientific integrity, the UI manages data through two distinct tabs based on the **ADR-024 Lifecycle**:

* **Tab A: The Reference Branch (Ground Truth)**:
  * Displays **Tier 2 (The Branch)**.
  * This is the data _after_ the pipeline's fixed wrangling but _before_ user filtering. It provides a stable baseline for comparison.
* **Tab B: The Active Leaf (Exploration)**:
  * Displays **Tier 3 (The Leaf)**.
  * Initialized as an identity of Tier 2, it changes instantly when a user interacts with the sidebar via **Predicate Pushdown**.
* **Interactivity**: Selection in an "Excel-like" grid must sync with the **VizFactory** plot. Manual exclusions (brushing) trigger a mandatory **User Note** modal.

* * *

💾 3. Persistence & Reporting Engine
------------------------------------

Reproducibility is enforced through a "No Trace, No Export" policy.

* **Manifest Authority**: Analysis "Recipes" are saved as human-readable **YAML** manifests.
* **The Submission Package**: Exports are bundled as a `.zip` file containing:
    1. **High-DPI Plots**: (600 DPI PNG or SVG/PDF).
    2. **Audit Log**: A human-readable `.txt` (via Pandoc) summarizing all filtration steps and user comments.
    3. **Data Subset**: The exact Tier 2/3 Parquet/CSV used for the final visual.
    4. **Recipe**: The active YAML manifest for total reconstruction.

* * *

🛠️ 4. Technical Task Roadmap
-----------------------------

### Phase 10-A: Pipeline Demo Implementation (ACTIVE)

* **\[ \] UI Bootloader**: Implement `ui_config.yaml` to handle persona masking (Pipeline vs. Developer).
* **\[ \] Layout Scaffolding**: Create the `navset_tab` structure with Tab A (Reference) and Tab B (Active).
* **\[ \] Tier 3 Sidebar Connector**: Link Shiny inputs to `VizFactory` filters using Predicate Pushdown.
* **\[ \] Annotation Modal**: Implement the popup for "User Notes" upon manual data exclusion.
* **\[ \] Export Bundle Logic**: Automate the creation of the `.zip` submission package.

### Phase 10-B: Developer & Expansion Tools (DEFERRED)

* **\[ \] Branching Logic**: Allow users to trigger a "New Branch" from a Tier 1 Anchor and save a unique YAML manifest.
* **\[ \] Manifest Helper**: Build the "Design Studio" UI for drag-and-drop wrangling chain construction.
* **\[ \] Pre-Flight Validator**: Implement the "Compatibility Dashboard" (Green/Yellow/Red) for data contracts.
* **\[ \] Inspiration Gallery**: Integrate the component sandbox and example plot gallery.
* **\[ \] Ghost Manifest**: Implement the silent auto-save to `tmp/last_state.yaml`.

* * *

🛡️ 5. Implementation Guardrails for Antigravity Agent
------------------------------------------------------

To ensure the agent builds this correctly, the following logic is now **ADR-021**:

1. **Environment Lock**: Use `./.venv/bin/python` for all UI logic checks.
2. **State Management**: Shiny `server.py` acts as an **Orchestrator** only; heavy lifting stays in `libs/`.
3. **Zero-Discovery**: The agent must use `tree.txt` to navigate and never "guess" file locations.
4. **Audit Integrity**: The Audit Trace is "Locked" upon export to prevent version drift.
