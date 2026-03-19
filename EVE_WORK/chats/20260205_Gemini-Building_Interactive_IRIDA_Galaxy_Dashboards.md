# Building Interactive IRIDA/Galaxy Dashboards

**Exported:** 2/5/2026 8:04:36  
**Link:** [https://gemini.google.com/gem/4221cfdd4fe7/cfe2d141fe0adecb](https://gemini.google.com/gem/4221cfdd4fe7/cfe2d141fe0adecb)




#### **Layer 2: Visualization Factory (`viz_core.py`)**

*   **Role:** The "Artist." This contains your "Deep Modules." You write a function like `create_species_distribution(df, config)`.
*   **The Factory Pattern:** Instead of hardcoding "Show Serotype for E. coli," you pass a **Config Object**. The function asks the Config: _"What is the primary metadata column for this species?"_ and the Config replies _"Serotype."_
*   **Architectural Benefit:** Adding a new species (e.g., _Listeria_) only requires updating a small JSON/YAML config file, not writing new Python functions.

#### **Layer 3: The Dashboard App (`app.py`)**

*   **Role:** The "Stage." This is your **Shiny Express** file. It handles the sidebar, the file upload buttons, and the "Reactivity" (e.g., "When the user clicks E. coli, update the graph").
*   **Architectural Benefit:** Keeping this file "thin" (only UI and reactivity) makes it much easier to debug.

* * *

### 3\. Server vs. Shiny: Understanding the Runtime

*   **Server Logic:** In the context of **Shinylive**, the "Server" actually runs inside the user's browser using WebAssembly (Wasm). However, logically, you should still treat it as a backend. Heavy calculations (Polars joins) happen here.
*   **Shiny UI:** This is the HTML/CSS layer that defines how the user interacts.

* * *

### 4\. Requirement Discovery (Proactive Inquiry)

To ensure this architecture holds up during your prototyping phase, I need to identify two potential "Unknowns":

1.  **Data Volume:** Are we talking about 100 samples with 50 metadata columns, or 10,000 samples? _Reason: Polars is fast, but if the data is massive, we need to consider "Lazy Evaluation" to keep the browser responsive._
2.  **The "Species Gap":** How different is the metadata between species? Does _E. coli_ have completely different table structures than _S. aureus_, or is it just different column names? _Reason: This determines if our "Data Contract" needs to be flexible or strict._

### 5\. Research Findings: Similar Apps

While there is no "one-size-fits-all" dashboard for both IRIDA and Galaxy in Python, the following projects are the closest "prior art":

*   **Dash Bio:** Great for specific plots (Volcano, Manhattan) but lacks the easy multi-page layout of Shiny.
*   **Microreact:** A very popular bioinformatics tool for genomic epidemiology. It uses a "Data Contract" (CSV + Newick tree) very similar to what we are designing. We can learn from their CSV structure.
*   **Galaxy Interactive Tools (GxIT):** Most existing GxITs use R/Shiny. By using **Shiny for Python**, you are at the cutting edge of the Galaxy ecosystem.

**How would you like to proceed?** I can help you **restructure your document** into these formal layers, or if you say **"Let's build,"** I can provide the first code skeleton for `data_prep.py` and the `viz_core.py` Factory.

[Shiny for Python: Building Interactive Dashboards](https://www.youtube.com/watch?v=InyYw5Ii14U)
 This video provides a practical walkthrough of how to structure a Shiny for Python application, which is a perfect starting point for understanding the "Presentation Layer" of your architecture.

## Prompt:
For the layer, We had said that there is in a way 2 data layers : the first will use the data from irida / galaxy and wrangle it according to a defined data contract (the species need to be defined early, and it allows selection and filtering of useless things. 

This tidy data should also in a way be somewhat reduced from the original data. Then we will need a join with the metadata (here we will have standard minimum metadata and need to ensure that the format is tidy (if not, returning to user - their problem). 

The join metadata happen here . Then this can be injected in the shiny layer for visualisation. 

A bit unclear here is for me, if we could send eg. Filtering or selection instructions from shiny to server - 

that would allow to decrease load on the shiny (and would be more scalable), if not then it will need to be done in the shiny. 

The idea is that the user can explore it's data set. I love microreact, there is plenty at term that we would like to set up. ..so is shinny express a bad choie ? I would like to not use or minimize WASM operations to their minimum. I said in the document we won't use WASM, it won't be scalable for huge dataset (and if well designed, one day people will want more heavy datasets and display that require other types of data that can be heavy)

## Response:
It sounds like you are thinking deeply about **Performance vs. Portability**, which is the most critical crossroads for a Software Architect.

Let's address the "WASM or No-WASM" question first: **Shiny for Python (Express) is a perfect choice, even if you avoid WASM.** You can run Shiny on a standard server (FastAPI-based) where the "Server" handles the heavy Polars lifting, and only the results (JSON/HTML) are sent to the user's browser. This is the classic, scalable way to build.

Here is the refined architecture based on your vision of two distinct data stages and the server-side filtering requirement.

* * *

1\. The 3-Tier "Smart Simplicity" Architecture
----------------------------------------------

We will separate the **heavy lifting** (Polars on the Server) from the **interactive display** (Shiny in the Browser).

### Tier 1: The Bio-Wrangler (Pre-Join)

*   **Input:** Raw IRIDA/Galaxy outputs (e.g., assembly stats, AMR gene tables).
*   **Action:** Filters out "noise," enforces the Data Contract, and converts everything to a standardized "Tidy" Polars DataFrame.
*   **Result:** A clean, species-specific reduced dataset.

### Tier 2: The Orchestrator (Metadata Join & Filter)

*   **Input:** Tier 1 data + User-uploaded Metadata.
*   **Action:** This layer validates the metadata. If the user uploads "messy" data, this layer catches it and sends a "Tidy your data!" error back to the UI.
*   **Crucial Logic:** This is where **Server-Side Filtering** happens. When a user clicks a filter in Shiny, we don't filter in the browser; we tell Polars on the server: `df.filter(pl.col("species") == "E. coli")`.
*   **Why:** This keeps the browser light. You can process millions of rows in Polars on the server, and the user's computer only sees the final 1,000 rows.

### Tier 3: The Shiny Layer (Visual Interaction)

*   **Input:** Filtered, joined data from Tier 2.
*   **Action:** Uses the **Graph Factory** to turn that data into Plotly objects.
*   **Role:** Purely a "Window." It handles the buttons, sliders, and the rendering of the plots.

* * *

2\. The Logic Flow: From Data to Dashboard
------------------------------------------

To clarify your question about "Sending instructions from Shiny to Server," here is how the communication works:

| User Action (Shiny UI) | Signal Sent to Server | Server Action (Polars/Python) | UI Result |
| --- | --- | --- | --- |
| **Uploads CSV** | File Stream | Validate headers + Join with bio-data | Show "Success" message |
| **Selects Species** | String: `"S. aureus"` | `df.filter(pl.col("species") == "S. aureus")` | Update all plots |
| **Filters by Date** | Range: `[2023, 2024]` | `df.filter(pl.col("year").is_between(2023, 2024))` | Re-render Plotly graph |

* * *

3\. Organizing Your Codebase
----------------------------

To make your document clearer, I suggest this folder structure. This keeps your classes and factories separated from the "UI" code.

```
my_dashboard/
├── app.py                # Shiny Express (The Stage: UI & Reactivity)
├── core/
│   ├── data_prep.py      # Tier 1: Raw data wrangling (Polars)
│   ├── metadata_mgr.py   # Tier 2: Joins, validation, & server-side filters
│   └── viz_factory.py    # Tier 3: Graph Factory (Plotly functions)
├── config/
│   └── species_rules.yaml # Metadata mapping (e.g., E.coli -> Serotype)
└── assets/               # CSS and static images
```

* * *

4\. Proactive Inquiry & Coaching
--------------------------------

To ensure we don't hit a wall later, consider these **Trade-offs**:

*   **Static vs. Dynamic:** If you avoid WASM (Shinylive), you **must** have a running server (a Docker container or a Galaxy Interactive Tool). This is better for large data, but it means you can't just email someone an HTML file that "works" offline. Are you okay with requiring a server?
*   **The Metadata "Tidy" Enforcement:** Since you want the user to handle their own tidy data issues, should we include a **"Data Health Report"** in the dashboard? A small table that shows which samples failed to join? This is a huge help for novices.

### Next Step

**Would you like me to draft a Python class for the `MetadataManager` that handles the Polars join and validation logic?** This would be the first piece of the "Server-side" engine.

## Prompt:
As said in the document we will use plotnine (plotly is an eventual secondary addition)

## Response:
Got it—**Plotnine** it is. That’s a sophisticated choice. By using Plotnine (which is based on the Grammar of Graphics, like R’s `ggplot2`), you’re prioritizing high-quality, publication-ready visuals and a very clean, declarative syntax.

Since you've decided against WASM (Shinylive) and are leaning towards a server-side model for scalability, the architecture actually gets _more_ robust. You can handle the Polars wrangling and Plotnine rendering on the server, sending the final plots to the Shiny UI.

### 1\. The Updated Organigram: Server vs. UI

Here is how we visualize the flow. The "Server" is where the heavy lifting and the Plotnine "rendering" happen. The "Shiny UI" is just the remote control and the display case.

* * *

### 2\. Deep Dive: Teacher Mode (The "Why")
# HERE #TODO
**Why Plotnine + Polars on the Server?**

*   **Decoupling Rendering:** Plotnine creates static images (or SVGs). By generating these on the server, the user's browser doesn't have to calculate where every point on a scatter plot goes; it just displays an image. This is infinitely more scalable for "huge datasets."
*   **Tidy Data Interface:** Plotnine _requires_ tidy data. This forces your `MetadataManager` to be disciplined. If the data isn't tidy, the plot simply won't draw, which acts as a natural quality gate.
*   **The "Instructions" Flow:** When a user interacts with a Shiny slider, Shiny sends a small message (e.g., `{"species": "E. coli", "threshold": 5}`) to the server. The server runs the Polars filter, generates a _new_ Plotnine object, and sends the updated image back.

* * *

### 3\. Proposed Code Structure (The Skeleton)

To keep things "Smart and Simple," I recommend organizing your logic so the **Graph Factory** doesn't care if it's plotting _E. coli_ or _Listeria_. It just sees columns.

#### **Core Module: `viz_factory.py`**

This is where your "Deep Module" lives. Note how it doesn't know about Shiny; it only knows about Polars and Plotnine.

```
from plotnine import ggplot, aes, geom_bar, theme_minimal
import polars as pl

def draw_species_plot(df: pl.DataFrame, x_col: str, fill_col: str):
    """
    A generic factory function. 
    It doesn't care what the data is, as long as the columns exist.
    """
    # Plotnine logic
    plot = (
        ggplot(df.to_pandas(), aes(x=x_col, fill=fill_col)) 
        + geom_bar() 
        + theme_minimal()
    )
    return plot
```

#### **The Orchestrator: `metadata_mgr.py`**

This handles the "Data Contract" and the join you mentioned.

```
import polars as pl

class MetadataManager:
    def __init__(self, bio_data: pl.DataFrame):
        self.bio_data = bio_data  # The 'reduced' data from Layer 1

    def join_and_filter(self, user_metadata: pl.DataFrame, species_filter: str):
        # 1. Validation: Ensure ID columns match
        # 2. Server-side join
        joined = self.bio_data.join(user_metadata, on="sample_id", how="inner")
        
        # 3. Server-side filter (The 'Scalability' part)
        return joined.filter(pl.col("species") == species_filter)
```

* * *

### 4\. Refining the "Decision Document"

To make your document clearer for stakeholders, I suggest adding a **"Data Contract Specification"** section. It should define:

1.  **Required Columns:** (e.g., `sample_id`, `species_name`).
2.  **The Join Key:** Explicitly stating that the user's metadata _must_ have a column that matches the bio-pipeline output.
3.  **The Protocol:** Shiny (UI) → Signal → Polars (Filter) → Plotnine (Render) → Shiny (Display).

### Proactive Inquiry

1.  **Plot Interactivity:** Since Plotnine produces static plots (PNG/SVG), will your users need to hover over points to see sample names? If yes, we may eventually need to wrap the Plotnine object in `plotly.tools.mpl_to_plotly` or use a hybrid approach. Is "static but beautiful" enough for the first prototype?
2.  **The "Species Rules":** Does each species have its own unique plot type (e.g., a dendrogram for one, a map for another), or is the _type_ of plot the same, just with different columns?

**Would you like me to generate a template for the `species_rules.yaml` configuration file that the Factory would use to decide which columns to plot?** This is the "brain" that makes the dashboard multi-species.

## Prompt:
At first it will be 2. But when we add more graphs to the apps there might be some different types of graphs for some species. But at first it will be more the. Columns that are different. For the species configuration yes that is another question, eg. We might have a serie of genes for each species to look at but the names of those then column names will be different. Would eg. A tall file allow to describe eg. Category AMR and then list of genes ...and Category Classification and then list of columns? That would allow to have some types of plots per category that are more or less the same between species but with different column names

## Response:
That is a classic **Metadata Mapping** challenge. Your idea of using a "Tall" configuration file (usually structured as YAML or JSON) is the gold standard for this. It allows you to build a "Metadata Translation Layer."

Instead of your code saying, "Look for _bla\_CTX-M-15_," your code says, "Look for everything categorized as _AMR_ for this species."

* * *

1\. Teacher Mode: The "Configuration-Driven" Design
---------------------------------------------------

To keep the system modular, we use **Metadata Injection**. Your visualization functions should be "blind" to specific gene names. They should only care about **Roles** (e.g., "The X-axis variable," "The Color variable," "The AMR Column List").

By defining these roles in a configuration file, you can add a new species or a new set of genes without touching a single line of Python code. You just update the config.

### The "Tall" Config Structure (YAML Example)

This is how you bridge the gap between different species' column names:

```
# species_config.yaml
E_coli:
  categories:
    AMR:
      columns: ["bla_CTX-M", "ndm-1", "tetA"]
      plot_type: "heatmap"
    Classification:
      columns: ["serotype", "phylogroup"]
      plot_type: "bar"
  
S_aureus:
  categories:
    AMR:
      columns: ["mecA", "vanA"]
      plot_type: "heatmap"
    Classification:
    columns: ["spa_type", "sccmec_type"]
    plot_type: "bar"
```

* * *

2\. Updated Architecture Organigram
-----------------------------------

To accommodate this, we add a **Config Loader** that sits between your Data Layer and your Graph Factory.

* * *

3\. Implementation: The "Graph Factory" logic
---------------------------------------------

When the user selects "E. coli" and "AMR" in the Shiny UI, the server performs the following logic:

1.  **Lookup:** Find `E_coli` -\> `AMR` in the YAML.
2.  **Retrieve:** Get the list `["bla_CTX-M", "ndm-1", "tetA"]`.
3.  **Wrangle:** Tell Polars to select those specific columns from the main dataset.
4.  **Plot:** Pass those columns to a Plotnine function designed to handle "Category: AMR."

### Example Factory Function (viz\_core.py)

```
def plot_amr_presence(df, amr_columns):
    """
    Generic AMR plotter. 
    'amr_columns' is a list provided by the Config Loader.
    """
    # Convert wide data to long (tidy) for Plotnine
    df_long = df.select(amr_columns).melt() 
    
    plot = (
        ggplot(df_long, aes(x="variable", fill="value"))
        + geom_bar(position="fill")
        + labs(x="Resistance Gene", y="Proportion")
    )
    return plot
```

* * *

4\. Requirement Discovery: The "User Preference" Layer
------------------------------------------------------

You mentioned **User Preferences**. This adds a layer of complexity:

*   **Species Config:** Defined by _you_ (the expert) for everyone.
*   **User Preference:** Defined by the _user_ during their session (e.g., "I want the bars to be Blue instead of Red").

**Trade-off Analysis:**

*   **Hardcoding Preferences:** Easier to build now, but users will complain they can't customize their view.
*   **Session State:** Shiny handles this well. We can store a "User Config" dictionary in the Shiny session that overrides the "Species Config" defaults.

* * *

5\. Summary of the Code Organization
------------------------------------

To keep your document clear, here is the final breakdown of responsibilities:

| Component | Responsibility | Technology |
| --- | --- | --- |
| **Data Wrangler** | Enforce Data Contract (Tidy data) | Polars |
| **Config Loader** | Map Categories (AMR) to Column Names | YAML / Python Dict |
| **Metadata Manager** | Join Bio-data + User CSV | Polars |
| **Graph Factory** | Turn "Roles" into Plots | Plotnine |
| **Shiny App** | Capture User Input & Show Results | Shiny Express |

### Next Step

**Would you like me to write a small "Config Loader" script?** It would show you exactly how to read a YAML file and use it to filter a Polars DataFrame based on the species selected in the dashboard.

## Prompt:
We won't build user preference yet, but I would like to have it in mind because I do not have to rewrite functions because I forgot to think about it ..

## Response:
That is exactly the mindset of a Senior Architect: **"Build for today, but design for tomorrow."** To make your functions future-proof for user preferences without actually building the UI for it yet, we use **Dependency Injection**. Instead of hardcoding colors or labels inside your Plotnine functions, you pass a `style_config` object as an optional argument. If the user hasn't set preferences, the function uses the "Species Defaults."

### 1\. The "Future-Proof" Data Flow

In this model, the `Graph Factory` becomes a pure function that takes three things:

1.  **The Data:** A Tidy Polars DataFrame.
2.  **The Mapping:** Which columns represent which roles (from your YAML).
3.  **The Theme:** (Optional) Visual preferences like color scales or font sizes.

* * *

### 2\. Teacher Mode: The Configuration Loader

The "Brain" of your app is a script that bridges your raw data and your plots. By using a **YAML-to-Dictionary** approach, you can easily swap out species-specific logic.

#### Why YAML?

*   It is human-readable (easy for you to edit without breaking code).
*   It supports nested categories (e.g., `AMR` -\> `Columns`).
*   It is the standard for bioinformatics pipelines (Nextflow/Snakemake).

* * *

### 3\. Lead Dev Mode: The Code Skeleton

Here is a prototype of the **Config Loader** and how it interacts with **Polars**. This pattern ensures that if a user eventually wants to change a "Category," you only change the dictionary, not the plotting logic.

#### `core/config_loader.py`

```
import yaml
import polars as pl

class ConfigLoader:
    def __init__(self, config_path="config/species_rules.yaml"):
        with open(config_path, "r") as f:
            self._config = yaml.safe_load(f)

    def get_species_logic(self, species_name: str, category: str):
        """Returns the specific columns and plot type for a species/category combo."""
        species_data = self._config.get(species_name, {})
        category_data = species_data.get("categories", {}).get(category, {})
        
        return {
            "columns": category_data.get("columns", []),
            "plot_type": category_data.get("plot_type", "default_bar"),
            "display_name": category_data.get("display_name", category)
        }

# Usage Example:
# loader = ConfigLoader()
# amr_info = loader.get_species_logic("E_coli", "AMR")
# print(amr_info["columns"]) -> ["bla_CTX-M", "ndm-1", "tetA"]
```

#### `core/viz_factory.py` (The Future-Proof Plotter)

Notice how we include a `user_prefs` argument that defaults to `None`. This is your "Hook" for the future.

```
from plotnine import ggplot, aes, geom_bar, theme_minimal, scale_fill_manual

def draw_categorical_plot(df: pl.DataFrame, mapping: dict, user_prefs=None):
    """
    mapping: The dictionary returned by ConfigLoader.
    user_prefs: Future dictionary for colors, titles, etc.
    """
    # 1. Prepare data (Polars)
    # We select only the columns defined in our config
    plot_df = df.select(mapping["columns"]).to_pandas()
    
    # 2. Basic Plot Logic
    # Let's assume we plot the first column for this example
    target_col = mapping["columns"][0]
    
    p = (
        ggplot(plot_df, aes(x=target_col))
        + geom_bar()
        + theme_minimal()
    )
    
    # 3. FUTURE PROOFING: Inject user preferences if they exist
    if user_prefs and "colors" in user_prefs:
        p += scale_fill_manual(values=user_prefs["colors"])
        
    return p
```

* * *

### 4\. Updated Organigram (Code Structure)

To keep your document clear, here is how the files relate to each other:

*   **`app.py`**: The Shiny Express entry point. It calls `ConfigLoader` to see what buttons to show the user.
*   **`config/species_rules.yaml`**: The "Tall" file containing your AMR and Classification column names per species.
*   **`core/data_prep.py`**: The Polars engine that cleans the IRIDA/Galaxy data.
*   **`core/viz_factory.py`**: The Plotnine functions that accept data + config.

* * *

### 5\. Proactive Inquiry: The "Missing Link"

When you join the **Bio-data** (from Galaxy) with **User Metadata** (from their CSV), what happens if the user has a column name that conflicts with yours?

*   **Recommendation:** Use a prefix for all Bio-data columns (e.g., `bio_serotype`, `bio_amr_gene`). This prevents the app from crashing if a user uploads a CSV that also has a column named "Species" or "ID."

**Would you like me to create a "Sanitization" function for the Metadata Manager that automatically handles these column name conflicts during the Polars join?** This will make the app much more "Novice-proof."

## Prompt:
Yes please. Can you also generate an updated version of the organigramme and of my document (markdown formatted in a text box) so I can review it and share it with share orders. That would be nice also to include small justification of why this is a judicious choice eg. Starting by \> in the document. So it explains the logic of our choices

## Response:
This is a significant step toward a "production-ready" prototype. By focusing on a **Config-Driven Architecture** and a **Sanitized Data Join**, you are building a system that can grow from two species to two hundred without becoming a "spaghetti" mess of `if/else` statements.

Below is the updated Architectural Organigram, followed by the Sanitization logic, and finally the structured Project Charter/Document for your stakeholders.

### 1\. The Walking Skeleton Organigram

This diagram illustrates how the **Config** acts as the "brain," directing the **Data Manager** and **Graph Factory**.

* * *

### 2\. Lead Dev Mode: The Sanitization Logic

This function ensures that user-uploaded metadata never breaks your internal pipeline. It uses a **Namespacing** strategy.

```
import polars as pl

def sanitize_and_join(bio_df: pl.DataFrame, user_df: pl.DataFrame, join_key: str = "sample_id"):
    """
    Ensures bio-data and user-data can coexist without column name collisions.
    """
    # 1. Prefix Bio-Data to protect internal variables
    # Ex: 'serotype' -> 'bio_serotype'
    bio_df = bio_df.rename({col: f"bio_{col}" for col in bio_df.columns if col != join_key})
    
    # 2. Identify Collisions in User Data
    # If user uploaded a 'bio_...' column, we rename it to protect our namespace
    user_renames = {col: f"user_{col}" for col in user_df.columns if col.startswith("bio_")}
    user_df = user_df.rename(user_renames)
    
    # 3. The 'Strict' Join
    # We use an 'inner' join to ensure we only plot samples that exist in both
    final_df = bio_df.join(user_df, on=join_key, how="inner")
    
    return final_df
```

* * *

### 3\. The Project Charter (Review for Stakeholders)

Copy and paste the box below into your project documentation.

```
# Project Charter: Modular Bioinformatics Dashboard (IRIDA/Galaxy)

## 1. Vision
To build a "Walking Skeleton" for a multi-species dashboard that is modular, scalable, and easy to maintain. The dashboard utilizes **Shiny for Python (Express)**, **Polars** for high-performance data handling, and **Plotnine** for publication-quality, grammar-of-graphics visualizations.

---

## 2. Core Architectural Principles

### 2.1. Decoupled Logic (Separation of Concerns)
The application is split into three distinct layers:
1. **The Wrangler (Data Layer):** Uses Polars to clean raw outputs into a "Tidy" contract.
2. **The Orchestrator (Logic Layer):** Handles metadata joins and applies species-specific rules via a configuration file.
3. **The Stage (Presentation Layer):** A "thin" Shiny UI that handles user inputs and displays rendered plots.

> **Why?** This allows us to swap the UI (e.g., move from Shiny to another framework) or the Data source (e.g., move from CSVs to a SQL database) without rewriting the core visualization logic.

### 2.2. Configuration-Driven Design (The "Tall" Config)
Instead of hardcoding species-specific genes or columns, we use a `species_rules.yaml` file. 
* **AMR Category:** Maps to specific resistance genes per species.
* **Classification Category:** Maps to serotyping or MLST columns.

> **Why?** Adding a new species or updating a gene panel requires zero code changes—only a simple update to a text file. This empowers non-programmers to maintain the dashboard's biological content.

### 2.3. Server-Side Filtering (Performance)
Heavy data operations (joins, filters, aggregations) are performed on the server using **Polars**, rather than in the user's browser (WASM).

> **Why?** This ensures the dashboard remains responsive even as datasets grow to thousands of samples, as only the final rendered plot (not the raw data) is sent to the client.

---

## 3. The Data Contract
To ensure stability, the dashboard enforces a strict "Join Key" (default: `sample_id`). 
* **Bio-Data:** Standardized prefix (`bio_`) to prevent collisions.
* **Metadata:** User-provided; must be "Tidy" (one observation per row).

> **Why?** Namespacing columns prevents the app from crashing if a user uploads a CSV containing column names that overlap with pipeline outputs.

---

## 4. Future-Proofing: User Preferences
While not implemented in Phase 1, the visualization functions are designed using **Dependency Injection**. 

> **Why?** By passing an optional `user_prefs` object to plotting functions today, we ensure that adding "Dark Mode" or custom color palettes tomorrow won't require refactoring the existing code.
```

* * *

### Next Step

This document looks solid for a "Walking Skeleton" review. **Would you like me to generate a functional `app.py` prototype** that ties the `ConfigLoader`, `Sanitizer`, and a basic `Plotnine` bar chart together using a sample "E. coli" dataset?

## Prompt:
If you can find a sample dataset yes, that would be good

## Response:
To build this "Walking Skeleton," I'll provide a self-contained prototype. We'll simulate a bioinformatics scenario: **E. coli** with Serotype metadata and **S. aureus** with `spa_type` metadata.

### 1\. The Walking Skeleton: Logical Flow

Before looking at the code, here is how the pieces we've discussed finally click together:

* * *

### 2\. Lead Dev Mode: The "Let's Build" Prototype

You can run this locally to see how the architecture behaves. I have structured this into three logical sections: the **Config**, the **Engine**, and the **Shiny App**.

#### A. The "Tall" Config (`species_rules.yaml`)

This is where you define the biology.

```
E_coli:
  categories:
    Classification:
      columns: ["serotype", "phylogroup"]
      plot_type: "bar"
    AMR:
      columns: ["bla_CTX-M", "ndm-1"]
      plot_type: "heatmap"

S_aureus:
  categories:
    Classification:
      columns: ["spa_type", "sccmec_type"]
      plot_type: "bar"
```

#### B. The Core Engine (`core_logic.py`)

This handles the sanitization, the config loading, and the Plotnine factory.

```
import polars as pl
import yaml
from plotnine import ggplot, aes, geom_bar, theme_minimal, labs

class BioDashboardEngine:
    def __init__(self, config_str):
        self.config = yaml.safe_load(config_str)

    def sanitize_and_join(self, bio_df, user_df):
        # Namespace bio columns to avoid collisions
        bio_df = bio_df.rename({c: f"bio_{c}" for c in bio_df.columns if c != "sample_id"})
        return bio_df.join(user_df, on="sample_id", how="inner")

    def get_plot(self, df, species, category):
        spec_cfg = self.config.get(species, {}).get("categories", {}).get(category, {})
        cols = spec_cfg.get("columns", [])
        
        if not cols: return None
        
        # Use the first configured column for this demo
        target_col = cols[0] 
        
        # Plotnine rendering
        p = (
            ggplot(df.to_pandas(), aes(x=target_col, fill=target_col))
            + geom_bar()
            + theme_minimal()
            + labs(title=f"{species} {category} Distribution", x=target_col.replace("_", " ").title())
        )
        return p
```

#### C. The Shiny Express App (`app.py`)

This is the "Stage" that connects the user to the engine.

```
from shiny.express import input, render, ui
import polars as pl
from core_logic import BioDashboardEngine

# 1. Mock Data Setup (Simulating Galaxy/IRIDA Output)
mock_config = """
E_coli:
  categories:
    Classification: {columns: ["serotype"], plot_type: "bar"}
S_aureus:
  categories:
    Classification: {columns: ["spa_type"], plot_type: "bar"}
"""
engine = BioDashboardEngine(mock_config)

# Simulated Bio Pipeline Output
bio_data = pl.DataFrame({
    "sample_id": ["S1", "S2", "S3", "S4"],
    "serotype": ["O157", "O157", "O104", "O157"],
    "spa_type": ["t001", "t002", "t001", "t001"]
})

ui.panel_title("Bioinformatics Multi-Species Dashboard")

with ui.sidebar():
    ui.input_select("species", "Select Species", choices=["E_coli", "S_aureus"])
    ui.input_select("category", "Select Category", choices=["Classification", "AMR"])
    ui.input_file("metadata", "Upload User Metadata (CSV)", accept=[".csv"])

@render.plot
def main_plot():
    # 1. Start with bio data
    current_df = bio_data
    
    # 2. Join with metadata if uploaded
    if input.metadata():
        user_md = pl.read_csv(input.metadata()[0]["datapath"])
        current_df = engine.sanitize_and_join(bio_data, user_md)
    
    # 3. Generate Plot via Factory
    return engine.get_plot(current_df, input.species(), input.category())
```

* * *

### 3\. Summary of Judicious Choices (For Review)

> **Why the Namespace Renaming?** Notice in `sanitize_and_join` how we prefix columns with `bio_`. This ensures that even if a user uploads a CSV with a column named "serotype," it won't overwrite the validated result coming from your pipeline.
> 
> **Why Polars to Pandas in Plotting?** Plotnine currently requires a Pandas DataFrame. By keeping the data in Polars until the very last millisecond (inside the `get_plot` function), we ensure all filtering and joining happen at maximum speed on the server.
> 
> **Why the `BioDashboardEngine` Class?** By wrapping the logic in a class, the Shiny app stays "thin." If you want to move this dashboard to a different framework (like FastAPI or Dash) later, you just take the `BioDashboardEngine` with you.

### Next Step

To test this, you can create a simple `metadata.csv` with a `sample_id` column and upload it to the dashboard. **Would you like me to show you how to add a "Data Validation" table** in Shiny that highlights which samples from the user's CSV failed to match the IRIDA/Galaxy data?



---
Powered by [Gemini Exporter](https://www.ai-chat-exporter.com)