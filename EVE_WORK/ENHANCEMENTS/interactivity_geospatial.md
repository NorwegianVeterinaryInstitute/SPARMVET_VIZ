# Supplementary Note: Interactive Geospatial Visualisation

**Status:** Pre-design — supplementary to the spatial and interactivity enhancement notes  
**Date:** 2026-05-02  
**Author:** @evezeyl  
**Parent documents:**
- [spatial_manifests_geospatial_viz.md](spatial_manifests_geospatial_viz.md) — static geom_map, geopandas pipeline
- [interactivity_plotly_shiny.md](interactivity_plotly_shiny.md) — general Plotly/Shiny interactivity

---

## 1. Goal

Extend the spatial enhancement to cover **interactive maps** — enabling users to zoom into a
region, hover over a country to see AMR statistics, click a country to drill into the isolate
data for that country, and toggle between resistance classes without leaving the dashboard.

This note covers the interactive map layer only. The static `geom_map` (plotnine) pipeline is
described in [spatial_manifests_geospatial_viz.md](spatial_manifests_geospatial_viz.md).

As with the general interactivity enhancement, the design principle is:
- **Static plotnine `geom_map`** → publication-quality figure, included in the export bundle
- **Interactive Plotly choropleth or ipyleaflet map** → exploration and drill-down

---

## 2. Technology Options

Two libraries are viable for interactive maps in Shiny for Python:

### 2.1 Plotly choropleth (recommended for country-level AMR maps)

`plotly.express.choropleth` and `plotly.graph_objects.Choropleth` accept:
- A pandas/polars DataFrame with a country identifier column
- A GeoJSON dict (loaded via `json.load()` — **no geopandas required**)
- Or built-in ISO 3166-1 alpha-3 country codes for world maps (no GeoJSON at all)

```python
import plotly.express as px
import json

with open("assets/geodata/natural_earth_countries_50m.geojson") as f:
    countries_geo = json.load(f)

fig = px.choropleth(
    df,
    geojson=countries_geo,
    locations="country_iso3",
    featureidkey="properties.ISO_A3",
    color="amr_prevalence_pct",
    color_continuous_scale="Reds",
    hover_name="country_name",
    hover_data={"n_isolates": True, "n_resistant": True},
    title="ESBL prevalence — E. coli by country of origin"
)
fig.update_geos(showcoastlines=True, fitbounds="locations")
```

Key capabilities:
- Zoom, pan, hover tooltips with custom data
- Click events routable to Shiny reactives via `FigureWidget.on_click()`
- Color scale selector (toggle between resistance classes via Shiny dropdown)
- **No geopandas or shapely required** — GeoJSON is read as plain JSON
- Modebar camera button for browser-side PNG download

Limitations:
- No tile layer background (Plotly `choropleth` uses outline-only geography)
- No sub-national boundaries without a sub-national GeoJSON
- No marker/bubble overlay on the choropleth without combining trace types

### 2.2 Plotly scatter map (for point/bubble maps — sampling locations)

`plotly.express.scatter_map` (replaces deprecated `scatter_mapbox`):

```python
fig = px.scatter_map(
    df,
    lat="sampling_lat",
    lon="sampling_lon",
    size="n_isolates",
    color="amr_prevalence_pct",
    hover_name="farm_id",
    hover_data={"year": True, "species": True},
    map_style="carto-positron",   # free, no API key required
    zoom=4,
    title="Sampling locations — ST22 isolates"
)
```

Free tile providers (no API key required):
- `carto-positron` — clean light background, suitable for publications
- `carto-darkmatter` — dark background for contrast
- `open-street-map` — full OSM detail

Mapbox named styles (`streets`, `satellite`) require a Mapbox API token.

### 2.3 ipyleaflet (recommended for sub-national or highly interactive maps)

`ipyleaflet` integrates natively with Shiny for Python via `shinywidgets` — it is the
**most reactive option**, enabling real-time updates of markers, choropleths, and popups without
a full figure redraw:

```python
from shinywidgets import render_widget, output_widget
from ipyleaflet import Map, GeoJSON, Marker, MarkerCluster

@render_widget
def interactive_map():
    m = Map(center=(55, 15), zoom=4)
    geo_layer = GeoJSON(
        data=countries_geojson,
        style={"fillColor": "blue", "opacity": 0.5},
        hover_style={"fillColor": "red"},
        name="AMR prevalence"
    )
    geo_layer.on_click(handle_country_click)   # routes click to Shiny reactive
    m.add(geo_layer)
    return m
```

ipyleaflet is better than Plotly for:
- Tile-based slippy maps with zoom to street level
- MarkerCluster (automatically clusters sampling points at low zoom)
- Per-feature style functions (colour each country dynamically from a Python dict)
- Real-time updates (add/remove markers without redrawing the whole map)

ipyleaflet requires slightly more setup than Plotly but is the best choice for maps that need to
show both country-level AMR data and point-level sampling locations on the same canvas.

### 2.4 Folium (not recommended for Shiny)

Folium produces HTML maps and can be embedded via `@render.ui` with `._repr_html_()`. However,
it has **no bidirectional reactivity with Shiny** — a user clicking a country cannot trigger a
Shiny reactive value update. Use only for static HTML map generation (e.g. standalone report
output), not for the interactive dashboard.

---

## 3. Dependency Comparison

| Library | geopandas required? | Extra deps | Shiny reactivity | Best for |
|---|---|---|---|---|
| `plotly.choropleth` | No | None beyond plotly | FigureWidget.on_click() | Country-level choropleth, publication-close output |
| `plotly.scatter_map` | No | None | FigureWidget.on_click() | Point/bubble maps, lat/lon data |
| `ipyleaflet` | No | ipywidgets, shinywidgets | Native, full | Tile maps, sub-national, marker clusters, mixed layer types |
| `folium` | No | None | None (display only) | Standalone HTML map reports, no dashboard use |

**Critical insight**: Neither Plotly choropleth nor ipyleaflet require geopandas or shapely.
They read GeoJSON directly as plain Python dicts. This means **interactive maps can be
implemented independently of the static `geom_map` geopandas pipeline** — they are not blocked
by the geopandas dependency question.

---

## 4. Recommended Architecture

### 4.1 Two-layer map strategy

Use both Plotly and ipyleaflet for different purposes in the same dashboard:

| Map type | Library | Use case |
|---|---|---|
| Country choropleth | Plotly `choropleth` | AMR prevalence by country — simple, clean, publication-close |
| Point / bubble map | Plotly `scatter_map` | Sampling location density, lat/lon from metadata |
| Mixed (choropleth + points) | ipyleaflet | When you need both country fill + individual farm markers on the same map, or sub-national boundaries |

### 4.2 Click-to-drill-down pattern

The most valuable interactive map interaction:

```
User clicks Norway on the choropleth
    → FigureWidget.on_click() fires with {"location": "NOR"}
    → Shiny reactive: selected_country.set("NOR")
    → resistance_trend plot updates: filters to country == "NOR"
    → data_preview updates: shows only Norwegian isolates
    → left-panel filter row added: country = NOR (visible in filter builder)
```

This reuses the existing `applied_filters` reactive — no new state needed. The click adds a
filter row exactly as if the user had typed it in the filter panel.

### 4.3 Manifest schema for interactive maps

```yaml
analysis_groups:
  Epidemiology:
    plots:
      amr_country_choropleth:
        factory_id: "choropleth_logic"
        target_dataset: "country_summary"
        geometry:
          source: "assets/geodata/natural_earth_countries_50m.geojson"
          join_on_geometry: "ISO_A3"
          join_on_data: "country_iso3"
        aes:
          color: "amr_prevalence_pct"
          hover: ["country_name", "n_isolates", "n_resistant"]
        color_scale: "Reds"
        interactive: true                # routes to Plotly; false routes to geom_map
        title: "AMR Prevalence by Country"
        
      sampling_locations:
        factory_id: "point_map_logic"
        target_dataset: "isolate_metadata"
        lat_col: "sampling_lat"
        lon_col: "sampling_lon"
        size: "n_isolates"
        color: "amr_prevalence_pct"
        hover: ["farm_id", "year", "animal_species"]
        map_style: "carto-positron"
        interactive: true
        title: "Sampling locations"
```

The `interactive: true` flag routes to the Plotly renderer; `interactive: false` (or absent)
routes to the existing static `geom_map` (plotnine) path. Both use the same geometry and
data spec — only the rendering backend differs.

---

## 5. What Implementation Would Require

### 5.1 Dependencies

```toml
# Already needed for general interactivity enhancement:
plotly>=6.0.0
shinywidgets>=0.3.0
kaleido>=0.2.0

# Additional for ipyleaflet (sub-national / tile maps):
ipyleaflet>=0.19.0   # ~10 MB; ipywidgets-based
```

No geopandas or shapely needed for interactive maps (Plotly and ipyleaflet read raw GeoJSON).

### 5.2 New VizFactory factory types

| factory_id | Library | Description |
|---|---|---|
| `choropleth_logic` | Plotly | Country-level fill choropleth from GeoJSON |
| `point_map_logic` | Plotly | Scatter/bubble point map from lat/lon columns |
| `tile_map_logic` | ipyleaflet | Mixed layer tile map for complex spatial views |

### 5.3 GeoJSON asset management

The GeoJSON files (Natural Earth countries, optionally NUTS sub-national boundaries) need to be:
- Stored in `assets/geodata/` and committed to the repository (or downloaded on first run)
- Loaded once at app startup and cached in a module-level dict (re-reading a 5 MB file on
  every render is unnecessary)
- Referenced by path in the manifest `geometry.source` field

Since geopandas is not required, the GeoJSON loading is simply:
```python
import json
from functools import lru_cache

@lru_cache(maxsize=8)
def _load_geojson(path: str) -> dict:
    with open(path) as f:
        return json.load(f)
```

### 5.4 Country name / ISO code normalisation

Join failures between data and geometry remain the primary reliability risk (same as for static
maps). A lookup table mapping common name variants to ISO3 codes should be bundled:
`assets/geodata/country_name_iso3_lookup.csv`. This is shared between the static `geom_map` and
interactive choropleth paths.

---

## 6. Advantages of Interactive-First for Maps

Compared to the static `geom_map` (geopandas-required) path, the Plotly-based interactive map:

- **No geopandas needed** — removes the largest installation/deployment risk
- **Can be implemented sooner** — not blocked by the geopandas deployment feasibility question
- **Higher user value** — hover tooltips and click-to-drill are far more useful for surveillance
  work than a static PNG
- **Still exports a static image** — Plotly's Kaleido renders a publication-quality PNG/SVG
  from any FigureWidget, so the export bundle requirement is met

**Recommendation:** Implement Plotly interactive choropleth before static geom_map.
The static geom_map path (geopandas) remains valuable for pixel-perfect publication figures
but is the harder and slower path. Interactive maps deliver more user value faster.

---

## 7. Challenges and Risks

| Challenge | Severity | Notes |
|---|---|---|
| Country ISO code join failures | Medium | Same as static maps — needs normalisation lookup table |
| Plotly `choropleth` no tile background | Low | Choropleth uses outline geography only. If a tile background is required, ipyleaflet is the right choice. |
| ipyleaflet GeoJSON styling for large feature sets | Medium | Styling 200 countries individually requires a Python style function; can be slow for complex GeoJSON. Simplify geometries to reduce vertex count. |
| Lat/lon availability in current data | Medium | Point maps require lat/lon columns in source data. Current ST22 data does not have sampling coordinates. |
| Kaleido in headless servers | Low | Same risk as general interactivity — verify in Galaxy/IRIDA environments. |
| NUTS boundary licencing | Low | EuroGeographics NUTS boundaries require attribution for publications. Natural Earth is public domain. |

---

## 8. Effort Estimate

| Component | Effort |
|---|---|
| GeoJSON asset acquisition + caching module | 0.5 day |
| Country name normalisation lookup table | 0.5 day |
| `choropleth_logic` factory (Plotly) + manifest schema | 1.5 days |
| `point_map_logic` factory (Plotly) | 1 day |
| `tile_map_logic` factory (ipyleaflet, optional) | 2 days |
| Click → `applied_filters` event routing | 0.5 day (shared with general interactivity) |
| Kaleido export for map figures | 0.5 day (shared) |
| Tests | 1 day |
| Documentation | 0.5 day |
| **Total (Plotly choropleth + point map only)** | **~5–6 person-days** |
| **Total (incl. ipyleaflet tile map)** | **~7–8 person-days** |

This estimate assumes the general interactivity enhancement (shinywidgets + Plotly base
infrastructure) is already implemented. If built standalone, add ~2 days for Plotly/shinywidgets
setup shared with that enhancement.

---

## 9. Sequencing Relative to Static geom_map

| Order | Rationale |
|---|---|
| 1. Interactive Plotly choropleth | No geopandas, higher user value, unblocked |
| 2. Static geom_map (geopandas) | Higher publication fidelity, but blocked on deployment feasibility |
| 3. ipyleaflet tile map | Only needed when sub-national or mixed-layer maps are required |

The interactive and static paths share the same manifest geometry spec — implementing one does
not create rework for the other.

---

## 10. References

- Plotly choropleth with GeoJSON: https://plotly.com/python/choropleth-maps/
- Plotly scatter map (replaces scatter_mapbox): https://plotly.com/python/maps/
- ipyleaflet documentation: https://ipyleaflet.readthedocs.io/
- Shiny for Python + ipyleaflet: https://shiny.posit.co/py/components/outputs/map-ipyleaflet/
- py-shinywidgets examples (ipyleaflet): https://github.com/posit-dev/py-shinywidgets/blob/main/examples/ipyleaflet/app.py
- Natural Earth GeoJSON (countries 50m): https://naturalearthdata.com/
- CARTO tile providers (no key required): https://carto.com/basemaps/
- Country ISO3 code reference (Natural Earth ISO_A3): https://www.naturalearthdata.com/downloads/50m-cultural-vectors/50m-admin-0-countries/
