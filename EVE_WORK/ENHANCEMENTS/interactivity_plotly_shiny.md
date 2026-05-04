# Enhancement: Interactive Visualisation — Plotly + Shiny for Python

**Status:** Pre-design — funding/scoping document  
**Date:** 2026-05-02  
**Author:** @evezeyl  
**Relates to:** tasks.md §Theater/State (STATE-1/2, THEATER-1), UX-1 slow rendering, EXPORT-2/3  
**Companion note:** [interactivity_geospatial.md](interactivity_geospatial.md) — interactive maps specifically

---

## 1. Goal

Introduce **interactive, explorable visualisations** alongside the existing static publication
figures in SPARMVET_VIZ — enabling users to zoom, filter, hover for sample details, and click
to drill down, without leaving the dashboard or writing code.

Currently all plots are static plotnine/matplotlib figures. They are well-suited for publication
export (the primary output of surveillance work) but are unsuitable for data exploration: you
cannot zoom into a year range, hover over a data point to see isolate counts, or click a bar to
filter the data preview. Every exploratory question requires re-running the assembly with different
parameters, which is slow and disconnected from the audit pipeline.

The goal is not to replace static figures — it is to add an **exploration mode** where the
analyst can interrogate the data interactively before committing a view to the T3 audit trail.
Static plotnine output remains the canonical publication artifact.

### Concrete use cases

| Interaction | Epidemiological value |
|---|---|
| **Hover on a data point** | See exact n_resistant / n_tested / prevalence % for a year+species combination without reading a table |
| **Click a bar / point** | Filter the data preview panel to the isolates that contribute to that bar |
| **Zoom into a date range** | Inspect 2019–2021 closely without re-running the assembly |
| **Select multiple points** | Compare the selected subset's distribution vs. the rest (lasso/box select) |
| **Toggle legend items** | Show/hide individual species or resistance classes without re-rendering |
| **Cross-filter between plots** | Click a country on the map → resistance trend plot updates to show only that country |
| **Sortable/filterable data table** | Sort isolates by MIC value, filter to a specific farm or year, without leaving the UI |
| **Download from browser** | One-click PNG/SVG of the current interactive view, sized for a slide |

---

## 2. Current System — What Exists

### 2.1 Rendering pipeline (today)

```
polars LazyFrame
    → pandas DataFrame
    → plotnine ggplot object
    → matplotlib figure
    → Shiny @render.plot  →  static PNG in browser
```

All figures are rendered server-side as PNG and sent to the browser as images. There is no
client-side rendering, no browser-side interaction, and no event routing back to Shiny.

### 2.2 What Shiny for Python already provides

- `ui.input_date_range()`, `ui.input_slider()`, `ui.input_selectize()` — these inputs already
  drive the filter panel and tier toggle. The reactive graph is established and working.
- `render.DataGrid` — sortable/filterable table backed by polars or pandas. Already used for
  the Data Preview panel. Selection events from DataGrid can be captured.
- `@render.plot` — current static figure renderer. Will coexist with interactive figures.

### 2.3 What is missing

- No client-side interactive chart renderer.
- No event routing from figure clicks/selections back to Shiny reactive graph.
- No cross-filtering between plots (clicking one plot updates another).
- No browser-side zoom, pan, hover tooltips on data points.

---

## 3. Recommended Technology Path

### 3.1 Primary recommendation: Plotly + shinywidgets

| Library | Role | Version (May 2026) | Install size |
|---|---|---|---|
| `plotly` | Interactive chart engine | 6.7.0 | ~125 MB |
| `shinywidgets` | Bridges Jupyter/ipywidget ecosystem into Shiny | latest | ~5 MB |
| `kaleido` | Server-side static image export from Plotly figures | 0.2.x | ~15 MB |

**How it works:**

```python
from shinywidgets import render_widget, output_widget
import plotly.graph_objects as go

@render_widget
def resistance_trend():
    fig = go.FigureWidget()          # FigureWidget, not Figure — enables event callbacks
    fig.add_scatter(x=df["year"], y=df["prevalence_pct"], mode="lines+markers")
    return fig
```

In the UI: `output_widget("resistance_trend")` instead of `output.plot("resistance_trend")`.

Plotly `FigureWidget` objects:
- Render client-side in the browser (no server round-trip for zoom/hover)
- Fire `.on_click()`, `.on_hover()`, `.on_selection()` Python callbacks
- React to Shiny inputs (`@reactive.Effect` updates the figure in-place)
- Export static PNG/SVG via Kaleido from the server

### 3.2 Why not Bokeh

Bokeh works via `shinywidgets` but requires Python callbacks for interactivity, which need a
running Tornado server alongside Shiny. In a standard Shiny deployment this is an unnecessary
complexity. Bokeh is better suited to standalone applications. **Not recommended.**

### 3.3 Why not matplotlib interactive backends

Matplotlib interactive backends (e.g. ipympl) render in Jupyter but do not integrate cleanly
with Shiny's reactive model. They have no event routing to Shiny reactive values. **Not viable.**

---

## 4. Architecture — Static + Interactive Coexistence

The key design principle: **plotnine (static) and Plotly (interactive) coexist in the same app.**
They use different render decorators and target different output slots. No rendering conflicts.

```
Same assembled pandas DataFrame
    ├─ @render.plot  →  plotnine figure  →  static PNG  (publication export)
    └─ @render_widget  →  Plotly FigureWidget  →  interactive browser chart (exploration)
```

**Proposed layout pattern:**

Each plot in the Home Theater panel shows:
- Primary view: **Plotly interactive figure** (default in exploration mode)
- A "Publication view" toggle → switches the same output slot to the static plotnine figure
- Export button always exports the plotnine version (guarantees publication quality)

This means VizFactory needs to produce *two* outputs per plot spec: the existing plotnine figure
and a new Plotly figure. A new `factory_id` convention (`timeseries_logic_interactive`,
or more cleanly, an `interactive: true` flag in the manifest) would route to the Plotly renderer.

---

## 5. What Implementation Would Require

### 5.1 New Python dependencies

```toml
shinywidgets>=0.3.0   # bridges ipywidgets/Plotly into Shiny — ~5 MB
plotly>=6.0.0         # already the standard interactive chart lib — ~125 MB
kaleido>=0.2.0        # server-side static image export from Plotly — ~15 MB
```

`kaleido` replaces the deprecated `orca` renderer for server-side PNG/SVG export. Required for
the download-from-Shiny workflow.

### 5.2 VizFactory — Plotly render path

A parallel render path alongside the existing plotnine path. For each factory type that supports
interactivity, a `render_plotly()` method alongside the existing `render()` method:

```python
# Current
viz = VizFactory(config)
fig = viz.render(df)                  # returns matplotlib Figure

# Proposed addition
interactive_fig = viz.render_plotly(df)   # returns plotly FigureWidget
```

The manifest would opt in with `interactive: true` at the plot level, or this could be a global
persona-level flag (`interactive_mode_enabled`) consistent with the existing flag architecture.

### 5.3 Plotly factory types needed

| Plotly factory type | Equivalent plotnine factory | Key Plotly API |
|---|---|---|
| `timeseries_interactive` | `timeseries_logic` | `go.Scatter` with hover template, date axis |
| `bar_interactive` | `bar_logic` | `go.Bar` with click events |
| `scatter_interactive` | `scatter_logic` | `go.Scatter`, lasso select |
| `heatmap_interactive` | `heatmap_logic` | `go.Heatmap` with hover |
| `epicurve_interactive` | `epicurve_logic` | `go.Bar` with epiweek x-axis |

### 5.4 Event routing — click-to-filter

The most valuable interaction: clicking a bar/point in one figure updates the data preview and
other figures. Implementation:

```python
@reactive.Effect
def _handle_plot_click():
    click_data = plotly_click.get()          # captured from FigureWidget.on_click()
    if click_data:
        selected_year = click_data["points"][0]["x"]
        selected_species = click_data["points"][0]["customdata"]
        active_filters.set([{"col": "year", "op": "eq", "value": selected_year},
                             {"col": "species", "op": "eq", "value": selected_species}])
```

This integrates with the **existing `applied_filters` reactive** — no new state management
needed. Clicking a Plotly point is functionally equivalent to adding a filter row in the left
panel filter builder.

### 5.5 Export integration

Plotly figures export from the browser via the built-in modebar (camera icon → PNG). Configurable:

```python
fig.update_layout(
    modebar_add=["toImageButtonOptions"],
)
fig.update_layout({
    "toImageButtonOptions": {
        "format": "svg",
        "filename": f"{plot_id}_{timestamp}",
        "height": 800,
        "width": 1200,
        "scale": 2
    }
})
```

For the server-side export bundle, the download handler calls `fig.write_image("plot.png")`
via Kaleido — identical interface to the current plotnine `savefig()` call.

### 5.6 T3 audit integration

Interactive exploration adds a new question: when a user clicks a bar to filter and then promotes
that filter to the T3 audit pipeline, the filter was authored via click rather than via the filter
builder UI. The T3 audit node should be identical regardless of how the filter was authored —
the `filter_row` RecipeNode schema already captures column/op/value, so click-sourced filters
can be injected into the same pipeline with no schema change.

### 5.7 DataGrid upgrade — itables

Shiny's built-in `render.DataGrid` supports sorting and basic filtering but has a limited
feature set. `itables` (DataTables.net Python wrapper) provides:
- Column-level text search
- Pagination with configurable page size
- Export to CSV/Excel from the table header
- Integration with `shinywidgets`

```python
from itables.widget import ITable
@render_widget
def data_preview():
    return ITable(df, caption="Active plot data")
```

For the current use case (browsing 1,000–50,000 rows of surveillance data), `itables` is a
significant UX improvement over the current DataGrid.

---

## 6. Current Limitations of the Proposed Approach

### 6.1 Two render paths to maintain

Every factory type that supports interactive mode needs a parallel Plotly implementation.
Keeping the plotnine and Plotly versions consistent (same colour scheme, same faceting logic,
same axis labels) is ongoing maintenance work. Changes to a manifest spec must be reflected in
both render paths.

**Mitigation:** Define a shared spec-to-aesthetics translator. Only the rendering backend
differs — aesthetics, colours, axis labels, and facet structure can be resolved once and passed
to both renderers.

### 6.2 Plotly figure customisation is different from plotnine

plotnine uses grammar-of-graphics layer stacking. Plotly uses a trace + layout model. Complex
multi-layer plotnine figures (e.g. a bar + line overlay + error bars + annotations) require
non-trivial translation to Plotly.

**Recommendation for initial scope:** Implement interactive mode only for the simpler factory
types (timeseries, bar, scatter, heatmap). Complex compound figures remain plotnine-only.

### 6.3 Performance with large datasets

Plotly handles up to ~1M points with WebGL (`go.Scattergl`), but for 50,000+ rows with rich
hover tooltips, the initial page load can be slow. Pre-aggregation server-side (polars groupby
before sending to Plotly) is required for any factory type that operates on raw isolate-level data.

### 6.4 Kaleido for server-side export

Kaleido is a headless Chromium-based renderer (~15 MB). It works in most server environments but
may require additional setup on headless HPC nodes or Docker containers without a display server.
Verify in the Galaxy/IRIDA deployment environments before committing to Kaleido.

### 6.5 Persona/flag gating for interactivity

Interactive mode adds a new capability dimension. The persona flag architecture (ADR-053) should
define a new flag `interactive_mode_enabled` rather than hardcoding which personas see Plotly
figures. This is consistent with the existing design — a one-line addition to the persona
templates and validator.

---

## 7. Open Questions

1. **Scope of interactive mode**: All plots, or only specific factory types? Recommended: opt-in
   per plot spec (`interactive: true`) with a persona-level gate.
2. **Publication mode toggle**: Should the static/interactive switch be per-plot or global (a
   "Exploration mode / Publication mode" toggle at the session level)?
3. **Click-to-T3**: If a user drills down via click and then wants to promote that filter to the
   T3 audit trail, is the UX clear? The filter panel would need to reflect the click-sourced
   filter as a visible row.
4. **Cross-plot filtering scope**: When clicking plot A filters the data in plot B, does this
   apply to all plots in the current group, or only the data preview? Design needed.
5. **itables vs DataGrid**: Is the upgrade to `itables` in scope for this enhancement, or a
   separate item?
6. **Galaxy/IRIDA headless Kaleido**: Confirmed workable before proceeding.

---

## 8. Effort Estimate

| Component | Effort |
|---|---|
| Dependency audit + shinywidgets + Plotly install | 0.5 day |
| `render_plotly()` path in VizFactory (architecture) | 1 day |
| `bar_interactive`, `scatter_interactive` factories | 2 days |
| `timeseries_interactive` factory | 1.5 days |
| `heatmap_interactive` factory | 1.5 days |
| Click → `applied_filters` event routing | 1 day |
| Kaleido export integration | 0.5 day |
| `interactive_mode_enabled` persona flag + template updates | 0.5 day |
| `itables` DataGrid upgrade (optional) | 1 day |
| Tests (unit + Playwright smoke for interactive outputs) | 2 days |
| Documentation | 1 day |
| **Total estimate** | **~12–13 person-days** |

Interactive geospatial (Plotly choropleth + ipyleaflet) is in a separate companion note and
estimated there: [interactivity_geospatial.md](interactivity_geospatial.md).

---

## 9. Recommended Next Steps

1. **Install `shinywidgets` and `plotly`** in the dev venv and run the minimal proof-of-concept:
   a Plotly `FigureWidget` bar chart in the Home Theater alongside the existing plotnine figure.
2. **Define the `interactive: true` manifest flag** and the ADR for the dual render path.
3. **Implement `bar_interactive` first** — it is the simplest and covers the most common use
   case (resistance class bar chart). Validate the click → filter event routing with the existing
   `applied_filters` reactive.
4. **Confirm Kaleido** works in the project's deployment targets.
5. **Decide persona flag gating** — add `interactive_mode_enabled` to all persona templates,
   gate the Plotly output behind it.

---

## 10. Relationship to Other Enhancements

| Enhancement | Relationship |
|---|---|
| [Time series analysis](timeseries_analysis_visualisation.md) | `timeseries_interactive` factory is the interactive counterpart of `timeseries_logic`. Both share the same assembler pipeline. |
| [Spatial manifests](spatial_manifests_geospatial_viz.md) | `geom_map` (plotnine, static) is the static counterpart of the Plotly choropleth. |
| [Interactive geospatial](interactivity_geospatial.md) | Companion note — Plotly choropleth + ipyleaflet maps. Shares the `shinywidgets` + Plotly infrastructure described here. |
| EXPORT-2 (selective export) | Plotly modebar + Kaleido replace/complement the current plotnine export for interactive figures. Design must be unified. |
| STATE-1/STATE-2 | Click-based cross-filtering will share the same reactive state management bug surface. Fix STATE-1 before wiring cross-filter events. |
| ADR-053 (flag-only persona gating) | `interactive_mode_enabled` flag must be added following the same pattern as `t3_sandbox_enabled`. |

---

## 11. References

- Shiny for Python + Plotly: https://shiny.posit.co/py/components/outputs/plot-plotly/
- Plotly FigureWidget events: https://plotly.com/python/figurewidget/
- shinywidgets GitHub: https://github.com/posit-dev/py-shinywidgets
- Plotly static image export (Kaleido): https://plotly.com/python/static-image-export/
- Plotly performance / WebGL: https://plotly.com/python/performance/
- Shiny for Python date range input: https://shiny.posit.co/py/components/inputs/date-range-selector/
- Shiny DataGrid: https://shiny.posit.co/py/components/outputs/data-grid/
- itables (DataTables.net Python): https://mwouts.github.io/itables/
- Plotly 6.7.0 release notes: https://pypi.org/project/plotly/
