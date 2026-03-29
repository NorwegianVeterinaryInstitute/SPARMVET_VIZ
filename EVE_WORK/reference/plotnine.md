# Plotnine 

Doc : <https://plotnine.org/reference/>
Repo : <https://github.com/has2k1/plotnine>


# Directories we want to inspect
cd plotnine/plotnine
 

├── composition
├── coords
├── data
├── doctools.py
├── exceptions.py
├── facets
├── geoms
├── ggplot.py
├── guides
├── helpers.py
├── iapi.py
├── __init__.py
├── labels.py
├── layer.py
├── mapping
├── _mpl
├── options.py
├── positions
├── __pycache__
├── py.typed
├── qplot.py
├── scales
├── session.py
├── stats
├── themes


| **Module**       | **Plotnine Source Match** | **Responsibility**                                                    |
| ---------------- | ------------------------- | --------------------------------------------------------------------- |
| **`geoms/`**     | `geoms/`, `stats/`        | The actual marks (bars, points, lines) and statistical transforms.    |
| **`scales/`**    | `scales/`                 | Controlling how data maps to aesthetics (colors, sizes, axis limits). |
| **`themes/`**    | `themes/`                 | Non-data ink (fonts, backgrounds, margins).                           |
| **`facets/`**    | `facets/`                 | Sub-plotting logic (`facet_wrap`, `facet_grid`).                      |
| **`coords/`**    | `coords/`                 | Coordinate systems (Fixed, Flip, Polar).                              |
| **`guides/`**    | `guides/`, `labels/`      | Legend positioning and Plot/Axis titles.                              |
| **`positions/`** | `positions/`              | How geoms sit relative to each other (dodge, stack, jitter).          |
| 

SPARMVET_VIZ Antigravity Specialist

Custom Gem

## SPARMVET_VIZ Antigravity Specialist said

In **Plotnine** (and the original `ggplot2` logic), every **Geom** (Geometric object) has a default **Stat** (Statistical transformation), and every **Stat** has a default **Geom**. They are two sides of the same coin.

Putting them in the same module reflects how the library actually functions under the hood. Here is the reasoning:

### 1. The Functional Coupling

In most cases, a user thinks about the _result_ (a bar, a box, a point).

- `geom_bar()` uses `stat_count()` by default.
    
- `geom_boxplot()` uses `stat_boxplot()` by default.
    
- `stat_smooth()` defaults to `geom_smooth()` (a line with a ribbon).
    

Because they are so tightly intertwined, separating them into different top-level modules in our **Viz Factory** would force the developer to jump between directories to manage a single visual element.

### 2. Statistical Geoms vs. Identity Geoms

Plotnine categorizes layers based on what they do to the data:

- **Identity Geoms**: Just draw the data as-is (e.g., `geom_point`).
    
- **Statistical Geoms**: Perform a calculation before drawing (e.g., `geom_histogram` calculates bins).
    

By keeping them in `geoms/`, we categorize by **Visual Output**. Whether you call `geom_bar(stat="count")` or `stat_count(geom="bar")`, the primary goal is to put a bar on the screen.

### 3. Reducing "Registry Bloat"

If we created a separate `stats/` module, our `manifest.yaml` logic would become more complex. We would have to distinguish between:

YAML

```
# Complexity we want to avoid:
- type: "stat_summary" 
- type: "geom_point"
```

By grouping them, the **Viz Factory** can treat any layer that creates "ink" on the coordinate system as a "Geom-style" component.

### 4. When to create a `stats/` module

The only reason to create a separate `stats/` directory in our `libs/viz_factory/src/` is if we plan to write **custom heavy-math transformers** that exist _independently_ of Plotnine (e.g., a complex bio-informatic normalization that happens right before plotting).

However, since our **Transformer (transformer.py)** handles the heavy lifting, the **Viz Factory** should stay focused on the "Grammar of Graphics" where Stats and Geoms are partners.


# Implementation: 
### 1. Viz Factory Architectural Structure

To support every component identified in the API context, the `./libs/viz_factory/src/` directory will be organized into the following functional modules. Each module will contain its own registry for decoupled, manifest-driven building.

| **Module**       | **Plotnine Mirror** | **Responsibility**                                          |
| ---------------- | ------------------- | ----------------------------------------------------------- |
| **`geoms/`**     | `geoms/`, `stats/`  | Geometric marks (points, lines) and statistical transforms. |
| **`scales/`**    | `scales/`           | Aesthetic mappings (colors, discrete/continuous scales).    |
| **`themes/`**    | `themes/`           | Visual appearance (minimal, classic, dark).                 |
| **`facets/`**    | `facets/`           | Sub-panel layouts (`facet_wrap`, `facet_grid`).             |
| **`coords/`**    | `coords/`           | Coordinate systems (Cartesian, Flipped, Transformed).       |
| **`positions/`** | `positions/`        | Handling overlaps (dodge, stack, jitter).                   |
| **`guides/`**    | `guides/`           | Legend and axis title management.                           |
| 

SPARMVET_VIZ Antigravity Specialist

Custom Gem

## SPARMVET_VIZ Antigravity Specialist said

This strategy establishes the foundation for the **Artist Pillar** by aligning the **Viz Factory (viz_factory.py)** architecture with the complete "Grammar of Graphics" layers found in the Plotnine source code.

### 1. Viz Factory Architectural Structure

To support every component identified in the API context, the `./libs/viz_factory/src/` directory will be organized into the following functional modules. Each module will contain its own registry for decoupled, manifest-driven building.

|Module|Plotnine Mirror|Responsibility|
|---|---|---|
|**`geoms/`**|`geoms/`, `stats/`|Geometric marks (points, lines) and statistical transforms.|
|**`scales/`**|`scales/`|Aesthetic mappings (colors, discrete/continuous scales).|
|**`themes/`**|`themes/`|Visual appearance (minimal, classic, dark).|
|**`facets/`**|`facets/`|Sub-panel layouts (`facet_wrap`, `facet_grid`).|
|**`coords/`**|`coords/`|Coordinate systems (Cartesian, Flipped, Transformed).|
|**`positions/`**|`positions/`|Handling overlaps (dodge, stack, jitter).|
|**`guides/`**|`guides/`|Legend and axis title management.|


