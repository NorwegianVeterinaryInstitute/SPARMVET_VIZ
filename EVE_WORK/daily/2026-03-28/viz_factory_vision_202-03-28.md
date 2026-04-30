## Prompt:
I want to initiate the viz\_factory build (previous agent has done some work but I am usure if it follows the rules and the standards I want). The rules will be similar to the building of the transformer with its decorators.

Where we need to use actions adding plots and their different layers to the manifest. We will be able to do default plots manifests so they can be reused. Easily (aka plots template manifests)

So the process should be verify simpliar and follow the same logic (and building way) that we have used for the transformer.

We will need to have a way to have the "data agnostic mapping" of data to plots (eg what is x, what is y , what is grouping layer for fill, for symbol osv) - and this will need to be defined in the manifest

Note also that we will need at one point an plot update: and this part is tricky, we will need to implement a way to update the data that is passed to the plot -\> send a message to the transformer -\> update the data -\> send a message to the plot -\> update the plot (because eg we will want to be able to do data exploration -\> reactualize the plot). And here I think we will need a way to mark the data as unmodified Vs filtered ... so we can go back to the unmodified data/plot if needed.

What we have to determine is exactly what to build and how to build it.

We will have the possibility to do several plots per manifest (so we need to think a bit how to handle this best).

We need to determine what is registred as list or dictionary in the manifest

I think that A plot should be a list of layers, and each layer is a dictionary of parameters for the layer (so we need to think a bit how to handle this best).

I think maybe the plots names itself should be a dictionary (we have a set of plots names that we can use.) Because when we will have to create the UI for the shiny app, we will want to offer the possibility to select a plot name and then the UI will have to display the selected plot (so we need to think a bit how to handle this best).

For the organisation of the viz factory code, I suggest that there is one subdirectory for each layer type (so we need to identify the types of layers that are used in plotnine - I now in R you have different layers - eg. scales, plots types, themes, coordinates, etc.)

And we will need a good way to handle the aesthetics, eg changing the color theme, the fill, the symbol, using different color palettes, etc. (I am not sure if this should be consider within a layer or as an utiliy ...) ...

We will need plots defaults ... box plots, histograms, etc. for each type of data (e.g. continuous, categorical, etc.)

## Response:
Starting the **Viz Factory (Artist Pillar)** is the most exciting transition yet. We are moving from the "Workforce" (Data Wrangling) to the "Expression" (Visualization). To ensure this build is as robust as the **Transformer**, we will mirror the decorator-based registry and manifest-driven logic you've already mastered.

Following your vision, here is the architectural blueprint for the `VizFactory (viz_factory.py)`.

### 🎨 1. The Registry & Decorator Logic

We will implement a `@register_plot_component` decorator. This allows us to keep the code modular, just like the `Transformer`.

*   **Registry**: A central dictionary `AVAILABLE_PLOT_COMPONENTS` mapping YAML keys to Plotnine functions.
*   **Categories**: Components will be registered under types: `geoms`, `scales`, `themes`, `coords`, and `facets`.
*   **Standard Signature**: Each registered function will accept `(plot_object, spec_dict)` and return the modified `plot_object`.

### 📊 2. Data-Agnostic Manifest Structure

To handle multiple plots and data-agnostic mapping, the manifest will use the **Dictionary-for-Names, List-for-Layers** structure you suggested.

```
plots:
  distribution_analysis: # Unique Plot ID (The Dictionary Key)
    mapping:             # Data-Agnostic Mapping (The "aes" block)
      x: "gene_name"
      y: "identity_score"
      fill: "species"
    layers:              # The Ordered List of Layers
      - type: "geom_boxplot"
        params: { "outlier_alpha": 0.5, "width": 0.7 }
      - type: "scale_fill_brewer"
        params: { "palette": "Dark2" }
      - type: "theme_minimal"
```

### 📂 3. Directory Architecture

We will organize `libs/viz_factory/src/` by layer type to maintain "Clear Lines":

*   `./geoms/`: Functions wrapping `geom_point`, `geom_boxplot`, etc.
*   `./scales/`: Aesthetic utilities (color palettes, symbol shapes, axis transformations).
*   `./themes/`: Custom branding and layout defaults.
*   `./facets/`: Logic for multi-panel plotting (e.g., `facet_wrap`).

### 🔄 4. Reactivity: The "Filtered vs. Unmodified" State

To handle updates and data exploration without losing the original state:

*   **The Anchor**: The `DataAssembler (data_assembler.py)` will provide a `Master Tidy Table`.
*   **State Flag**: We will implement a `is_filtered` boolean in the UI orchestration layer.
*   **The Loop**:
    1.  **User Action**: Filter applied in Shiny.
    2.  **Transformer**: `wrangle_debug.py` (or the equivalent logic) creates a `Filtered View`.
    3.  **Viz Factory**: Re-renders using the _same_ manifest but the _new_ data slice.
    4.  **Reset**: Reverting the toggle simply swaps the `Filtered View` back to the `Master Tidy Table`.

* * *

### 🛠️ The "Viz Factory Initialization" Prompt

```
@Agent: @dasharch - INITIALIZE VIZ FACTORY (Artist Pillar).

1. Library Setup:
   - Initialize ./libs/viz_factory/src/ and ./libs/viz_factory/tests/.
   - Create pyproject.toml and install in Editable Mode in the root .venv [ADR-011].

2. Core Implementation - VizFactory (viz_factory.py):
   - Implement the @register_plot_component decorator and central registry.
   - Logic: The factory must accept (dataframe, manifest_dict, plot_id).
   - Logic: It must initialize a ggplot() object with the 'mapping' block and then iterate through the 'layers' list, piping each component.

3. Module Organization (Subdirectories):
   - Create directories for: geoms, scales, themes, and facets.
   - Implementation: In ./geoms/core.py, register 'geom_boxplot' and 'geom_histogram' as initial test layers.

4. Data Hand-off (ADR-010):
   - Ensure the factory includes a helper to convert Polars LazyFrames to Pandas strictly at the moment of plotting [ADR-010].

5. Debug Runner - debug_viz.py:
   - Create ./libs/viz_factory/tests/debug_viz.py following the 'debug_' convention [Section 8, Workspace Standard].
   - Goal: Load a test TSV, apply a plot manifest, and save the output to ./tmp/viz/test_plot.png.

6. README & Standards:
   - Create ./libs/viz_factory/README.md using the 'Violet Component' standard: VizFactory (viz_factory.py) [Section 8].
   - Document the 'Data-Agnostic Mapping' rules.

HALT for @verify:
   - Demonstrate a boxplot generated from a manifest, showing the console log of the registered layers being applied.
```

### 🛡️ Why This Works

By treating plots as a **List of Layer Dictionaries**, you can eventually build a UI where a user clicks "Add Layer" and the Shiny app simply appends a new dictionary to the manifest. This is the foundation for the "Plot Template" system you requested.

**Would you like me to suggest some "Standard Palettes" for the scales module to ensure your first test plots have the Deep Violet aesthetic?**


----
2023-04-29 : preparing implementation
### 1. Architectural Alignment Check

Before we trigger the Agent, here is how your vision maps to our established mandatory standards:

| **Feature**             | **Logic**                                 | **Rule/Standard Reference**        |
| ----------------------- | ----------------------------------------- | ---------------------------------- |
| **Decorator Pattern**   | `@register_plot_component`                | **rules_wrangling.md** (Section 1) |
| **Manifest Structure**  | Dictionary (Names) → List (Layers)        | **rules_wrangling.md** (Section 2) |
| **Component Format**    | `VizFactory (viz_factory.py)`             | **rules_aesthetic.md** (Section 1) |
| **Data Hand-off**       | Polars (Lazy) → Pandas (Materialized)     | **ADR-010 / rules_runtime.md**     |
| **Directory Hierarchy** | `geoms/`, `scales/`, `themes/`, `facets/` | **Modular Library Autonomy**       |
| 

### 2. The "Filtered vs. Anchor" Reactivity

To support your requirement for data exploration, the **`VizFactory (viz_factory.py)`** must remain data-agnostic. It will receive a dataframe (either the **Anchor** or the **Filtered View**) and apply the _same_ manifest layers. This ensures that "updating the plot" is simply a re-execution of the factory against a different data slice.