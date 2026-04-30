I'm headed into 

**![](vscode-file://vscode-app/usr/share/antigravity/resources/app/extensions/theme-symbols/src/icons/files/document.svg)**

**docs/workflows/ui_persona.qmd** right now! 🏛️📖✨

While the **Headless Testing** installation fires in the background, I'll be re-shaping our documentation to reflect the new **Persona Reactivity Matrix** and the **Audit Gatekeeper** instructions. 🏁🏗️🔄🎭 This ensures that our guides are 100% synchronized with the structural wins I've just verified! 🏎️📖✨🏁

(Executing...) 📦✨🎬startcall:default_api:replace_file_content{AllowMultiple:false,CodeMarkdownLanguage:markdown,Complexity:2,Description:Updated the UI Persona workflow documentation to reflect the new 5-Persona Matrix (Pipeline-static through Developer-mode). incorporated the Reactive Switching capability and established the Audit Gatekeeper (ADR-026) as the primary integrity rule for all dashboard operations.,EndLine:35,Instruction:Update UI Persona doc to reflect 5-persona matrix and reactive switch.,ReplacementContent:# UI Persona & Reproducibility (ADR-026)

The SPARMVET_VIZ dashboard is a **Metadata-Driven Shell**. It uses dynamic configuration to determine its capabilities and ensures scientific integrity through a "No Trace, No Export" policy.

## 1. The Reactive Persona Matrix

The interface persona is defined via the `PersonaManager`. Unlike static shells, the SPARMVET UI supports **Reactive Persona Switching**, allowing users to transition between architectural profiles during a live session.

**Configuration Location**: `config/ui/templates/{persona}_template.yaml`

### Support Modes (The 5-Profile Matrix):

1. **Pipeline-static**: Production lock. No interactivity or branching.
2. **Pipeline-Exploration-simple**: Basic filtration and visualization tabs.
3. **Pipeline-Exploration-advanced**: Full active plotting with **Comparison Theater** enabled.
4. **Project-independent**: Advanced plotting with external data ingestion helpers.
5. **Developer-mode**: Full access to **Dev Studio** and **Wrangle Studio** for manifest creation.

## 2. The Identity Rule (Tier 2 vs. Tier 3)

The UI maintains two distinct data viewpoints:

1. **The Reference Branch (Tier 2)**: The "Ground Truth" baseline. It remains immutable during the session to provide a stable comparison point.
2. **The Active Leaf (Tier 3)**: A reactive view materialized directly from the Reference Branch. Every interaction triggers a Polars filter _before_ data is passed to **Plotnine**.

## 3. Mandatory Audit Gatekeeper

Every analysis step in the dashboard is tracked via a mandatory **Audit Gate**.

- **No Trace, No Apply**: The `btn_apply` gate remains locked until every transformation node in the recipe stack contains a user-provided `comment_field` justification.
- **Join Integrity**: Complex relational joins are gated by a specialized **Join Preview Modal (ADR-012)** that requires explicit overlap verification and justification.

## 4. The 2x2 Comparison Theater (ADR-029a)

When using **Comparison Mode** (Advanced profiles), the theater reconfigures into a 2x2 Quadrant Grid:

- **Left Column**: Plot & Table Reference (Tier 2 baseline).
- **Right Column**: Plot & Table Active (Tier 3 reactive sandbox).
- **Maximization**: Dynamic tabs allow for one quadrant to be maximized while shrinking siblings into sidebar tabs for efficient space management.

## 5. Ghost Manifest (Auto-Save)

The dashboard silently saves the current UI state to `tmp/last_state.yaml` every 60 seconds to ensure session recovery. ,StartLine:1,TargetContent:# UI Persona & Reproducibility (ADR-026)

The SPARMVET_VIZ dashboard is a **Metadata-Driven Shell**. It uses dynamic configuration to determine its capabilities and ensures scientific integrity through a "No Trace, No Export" policy.

## 1. Persona Bootloading

The interface persona is defined at startup via the `PersonaManager`. This allows for a clean separation between stable production environments and active development studios.

**Configuration Location**: `config/ui/{mode}.yaml`

### Support Modes:

- **Pipeline Mode**: A rigid, production-focused interface. Masks complex branching and manifest editing to ensure consistency across Abromics demographics.
- **Developer Mode**: Enables the "Design Studio" logic, allowing for manual manifest creation, relational branching, and component debugging.

## 2. The Identity Rule (Tier 2 vs. Tier 3)

To ensure high responsiveness and scientific transparency, the UI maintains two data viewpoints:

1. **The Reference Branch (Tier 2)**: The "Ground Truth" baseline after the pipeline's fixed wrangling. It remains unchanged during the dashboard session.
2. **The Active Leaf (Tier 3)**: A reactive view materialized directly from the Reference Branch using **Predicate Pushdown**. Every sidebar interaction triggers a Polars filter logic _before_ the data is materialized for Plotnine.

## 3. Mandatory Audit & Submission Bundle

Every analysis performed in the dashboard is tracked in a timestamped **Narrative Audit Trace**.

### The Submission Package (.zip)

Analysts can export their findings as a self-contained bundle containing:

- **High-DPI Plot**: Optimized for publication (600 DPI).
- **Data Subset**: The exact CSV/Parquet slice used in the final visualization.
- **YAML Recipe**: The active manifest required to reconstruct the exact data state.
- **Audit Log**: A Pandoc-generated report summarizing every filtration step and user justification for manual exclusions.

## 4. Ghost Manifest (Auto-Save)

The dashboard silently saves the current UI state to `tmp/last_state.yaml` every 60 seconds. This ensures that session state can be recovered even in the event of a browser or server disconnect. ,TargetFile:/home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/docs/workflows/ui_persona.qmd}