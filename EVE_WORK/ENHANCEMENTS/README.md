Four documents in `EVE_WORK/ENHANCEMENTS/`:

|Document|Lines|Scope|
|---|---|---|
|[spatial_manifests_geospatial_viz.md](vscode-webview://0e5hnbisb03ag4fcngug03203c1s4jbnfqap153h296d87qmbsj9/EVE_WORK/ENHANCEMENTS/spatial_manifests_geospatial_viz.md)|338|Static geom_map, geopandas pipeline|
|[timeseries_analysis_visualisation.md](vscode-webview://0e5hnbisb03ag4fcngug03203c1s4jbnfqap153h296d87qmbsj9/EVE_WORK/ENHANCEMENTS/timeseries_analysis_visualisation.md)|467|Time series analysis + epicurves + ITS|
|[interactivity_plotly_shiny.md](vscode-webview://0e5hnbisb03ag4fcngug03203c1s4jbnfqap153h296d87qmbsj9/EVE_WORK/ENHANCEMENTS/interactivity_plotly_shiny.md)|372|General interactivity — Plotly, shinywidgets, click events|
|[interactivity_geospatial.md](vscode-webview://0e5hnbisb03ag4fcngug03203c1s4jbnfqap153h296d87qmbsj9/EVE_WORK/ENHANCEMENTS/interactivity_geospatial.md)|348|Interactive maps — Plotly choropleth + ipyleaflet|

Two things worth highlighting for the funding case:

**Strongest insight from the geospatial note:** Plotly interactive choropleths work from raw GeoJSON with `json.load()` — no geopandas, no GDAL, no compiled C extensions. This means interactive maps can be implemented _without_ solving the geopandas deployment problem on Galaxy/HPC. The static publication-quality map (geom_map) has the harder dependency story; the interactive version is unblocked. That's a meaningful sequencing argument for a funding proposal.

**Clearest cross-cutting theme across all four:** the `shinywidgets` + Plotly infrastructure is shared between general interactivity, time series interactive, and interactive maps — implementing it once (the general enhancement) unlocks all three. That bundling argument could support a single work package rather than three separate ones.