# Enhancement: Geospatial Visualisation — Spatial Manifests & Choropleth/Point Maps

**Status:** Pre-design — funding/scoping document  
**Date:** 2026-05-02  
**Author:** @evezeyl  
**Relates to:** `geom_map` handler in `libs/viz_factory/` (currently deferred), tasks.md §VizFactory deferred

---

## 1. Goal

Enable SPARMVET_VIZ to produce **static publication-quality maps** directly from the existing
manifest-driven pipeline — without requiring users to write Python or use external GIS tools.

Concrete use cases for veterinary AMR epidemiology:

| Map type | Use case |
|---|---|
| **Choropleth (country level)** | AMR prevalence per country/region (e.g. % ESBL-positive *E. coli* isolates by country of origin) |
| **Choropleth (sub-national)** | Regional or county-level distribution within Norway or the EU |
| **Point map** | Sampling location of isolates (farm, slaughterhouse, monitoring station) |
| **Bubble map** | Point map with circle size proportional to isolate count or resistance frequency |
| **Time-animated** | Spread of a resistance gene or clone across countries over years (deferred — needs separate design) |

These map types appear routinely in NORM-VET reports, EAA/EFSA surveillance publications, and
One Health manuscripts. Currently, producing them requires stepping outside the platform and using
R (`ggplot2 + sf`), QGIS, or manual figure preparation. Integrating them into SPARMVET_VIZ would
close the gap between data processing and publication-ready output in the same workflow.

---

## 2. Current System — What Exists

### 2.1 Data pipeline

```
TSV/Excel files
    → DataIngestor (polars)     — reads, validates, schema-checks
    → DataAssembler             — joins, filters, pivots (YAML recipe steps)
    → home_theater materialise  — polars LazyFrame → pandas DataFrame
    → VizFactory.render()       — pandas + plotnine → matplotlib figure
```

All columns in this pipeline are **scalar types**: string, int, float, boolean, date.
The polars engine has no geometry column type.

### 2.2 VizFactory manifest schema (current)

A plot spec in a manifest `.yaml` file looks like:

```yaml
analysis_groups:
  Epidemiology:
    plots:
      amr_by_country:
        factory_id: "bar_logic"       # selects which VizFactory handler
        target_dataset: "amr_summary" # which assembled dataset to use
        x: "country"
        y: "prevalence_pct"
        fill: "resistance_class"
        title: "AMR Prevalence by Country"
```

The `factory_id` key selects a registered handler from `libs/viz_factory/`. Plotnine is called
inside that handler with the pandas DataFrame that the pipeline produced.

### 2.3 What `geom_map` needs (plotnine 0.15.3)

`geom_map` requires a pandas/GeoPandas DataFrame with:
- A **`geometry` column** containing Shapely geometry objects (Polygon, Point, etc.)
- Optionally: additional columns mapped via `aes()` for colour, fill, alpha

The geometry column must be present in the DataFrame at the time `render()` is called.
The current pipeline cannot produce this column — polars has no geometry type.

### 2.4 What is already implemented

- `geom_map` **imports fine** in plotnine 0.15.3 (confirmed 2026-05-01).
- The VizFactory handler skeleton exists in `libs/viz_factory/src/viz_factory/geoms/core.py:207-210`
  — commented out, 3 lines, trivially simple once the data arrives correctly.
- `geopandas` and `shapely` are **not installed** in the project venv.

---

## 3. Current Limitations

### 3.1 Missing dependencies

| Library | Role | Current status |
|---|---|---|
| `geopandas` | Read shapefiles/GeoJSON, manage geometry column, CRS transforms | NOT installed |
| `shapely` | Geometry type (Point, Polygon, …) | NOT installed |
| `pyproj` | Coordinate reference system (CRS) transforms | NOT installed |
| `fiona` | Low-level vector file I/O (geopandas dependency) | NOT installed |

Install footprint: ~50–80 MB with all dependencies. All have compiled C/C++ extensions — they work
in a standard venv but are not pure-Python.

### 3.2 Polars has no geometry type

Polars (used throughout the pipeline for performance) does not natively support a `geometry`
column. There are early-stage libraries (GeoPolars, polars-st, spatial-polars) but none are
production-ready as of early 2026.

The geometry must live **outside** the polars data path and be attached only at the visualisation
step (just before calling VizFactory).

### 3.3 No manifest schema for geometry sources

The current manifest schema has no concept of:
- A geometry data source (separate from tabular data)
- A join key linking tabular data to geometry features
- A CRS declaration
- A geometry column name

### 3.4 No ingestion path for spatial files

`DataIngestor` reads TSV, CSV, and Excel via polars. It cannot read GeoJSON, Shapefile, or
GeoParquet. A separate loader is needed.

### 3.5 plotnine `geom_map` does not support projections

`geom_map` draws raw lat/lon coordinates with no cartographic projection. This is adequate for
country-level choropleths (Plate Carrée / equirectangular is standard in surveillance reports) but
not for polar regions, conformal projections, or Web Mercator. For Norway/Nordic data, the
distortion at high latitudes is visible but acceptable for publications.

Interactive maps (zoom, click-to-inspect, tile layer backgrounds) are **not possible** with
plotnine. For interactive use, a separate integration with Folium or Plotly would be needed
(separate enhancement, out of scope here).

---

## 4. What Implementation Would Require

### 4.1 New Python dependencies

```toml
# pyproject.toml additions
geopandas>=1.0.0
shapely>=2.0.0
pyproj>=3.5.0
```

These are mature, widely-used libraries with good Python 3.11–3.13 support. Confirm compatibility
with the project's exact Python version before adding.

### 4.2 Basemap data assets

A set of reference geometry files needs to be bundled or downloaded at first use:

| Source | Coverage | Resolution | License | Format |
|---|---|---|---|---|
| **Natural Earth** | World countries, coastlines, disputed borders | 1:10m / 1:50m / 1:110m | Public domain | Shapefile, GeoJSON |
| **GADM** | Sub-national admin boundaries (level 1 = counties, level 2 = municipalities) | Varies | Free for academic; commercial restrictions | Shapefile, GeoPackage |
| **geoBoundaries** | 200+ countries, multiple admin levels | Varies | Open (CC BY 4.0) | GeoJSON, Shapefile |
| **EuroGeographics** | EU/EEA member states | NUTS 1/2/3 | Open for non-commercial | GeoJSON |

**Recommendation for initial implementation:** Natural Earth (1:50m countries) — public domain,
well-maintained, widely used in scientific publications, ~5 MB download. Norwegian sub-national
data: GADM or the Norwegian Mapping Authority (Kartverket, free for research).

### 4.3 Manifest schema extension

A new plot type would declare both its data source and its geometry source:

```yaml
analysis_groups:
  Epidemiology:
    plots:
      amr_choropleth_europe:
        factory_id: "map_logic"               # triggers geom_map handler
        target_dataset: "country_summary"      # assembled polars dataset (has join key + fill col)
        geometry:
          source: "assets/geodata/natural_earth_countries_50m.geojson"
          join_on_geometry: "ISO_A3"           # column in geometry file
          join_on_data: "country_iso3"         # column in target_dataset
          crs: "EPSG:4326"                     # expected CRS (WGS84 lat/lon)
        aes:
          fill: "amr_prevalence_pct"
          label: "country_name"
        title: "ESBL Prevalence by Country of Origin"
        limits:                                # optional bounding box
          xlim: [-25, 45]
          ylim: [34, 72]
```

### 4.4 Geometry loader module

A new module `libs/connector/geometry_loader.py` (or inside the assembler) to:
1. Read the geometry file (GeoJSON/shapefile/GeoParquet) via geopandas
2. Cache it in memory (base maps are read-only, re-used across renders)
3. Validate CRS and reproject if needed (`to_crs("EPSG:4326")`)
4. Return a GeoDataFrame ready to merge with the polars-derived data

### 4.5 VizFactory `map_logic` handler

The handler itself is simple once data arrives correctly:

```python
@register_plot_component("map_logic")
def handle_map(p: ggplot, spec: dict, geo_df: gpd.GeoDataFrame) -> ggplot:
    fill_col = spec.get("aes", {}).get("fill")
    return p + geom_map(aes(fill=fill_col), data=geo_df)
```

The challenge is the **data contract**: the handler needs both the assembled tabular DataFrame
and the geometry GeoDataFrame, merged on the declared join key, before `render()` is called.
This means the merge step happens in the materialisation path (home_theater / VizFactory
pre-render), not inside the handler itself.

### 4.6 T3 audit implications

The current T3 audit pipeline lets users filter rows and drop columns as auditable steps. Spatial
data raises two design questions:
- Can a user filter a choropleth by country (e.g. "exclude Norway from the map")? Yes — standard
  row filter on the tabular data before the geometry join.
- Can a user change the geometry source via T3? Almost certainly no — geometry sources are
  infrastructure config, not analytical decisions.

No changes to the T3 audit schema appear necessary for the initial implementation.

---

## 5. Open Questions to Resolve Before Implementation

These need answers before development starts. Some require design decisions; some require
investigation.

### 5.1 Dependency management
- Does the project's deployment target (Galaxy, IRIDA, institutional server) allow `geopandas`
  installation? It has compiled extensions (GDAL) and can be difficult on some HPC environments.
- Should spatial dependencies be optional (installed only when spatial manifests are present) or
  mandatory for all deployments?
- Should geometry files be bundled in the repository, downloaded at first use, or provided by the
  deployment administrator?

### 5.2 Join reliability
- Country names and ISO codes are inconsistently standardised across datasets (e.g. "United
  Kingdom" vs "UK" vs "GB" vs "GBR"). What normalisation strategy will be used?
- What happens when the join produces nulls (country in data has no geometry, or vice versa)?
  Should unmatched rows be flagged as a validation warning at manifest load time?

### 5.3 Coordinate reference systems
- SPARMVET data currently has no CRS metadata. If lat/lon coordinates appear in source data,
  are they guaranteed to be WGS84 (EPSG:4326)?
- Sub-national Norwegian data from Kartverket is often in ETRS89/UTM zone 33N (EPSG:25833) —
  reprojection to WGS84 is needed before plotnine.

### 5.4 Assembly pipeline integration point
- Where should the geometry join happen? Options:
  - **In the assembler** (as a new recipe step type `{spatial_join: ...}`) — keeps geometry in
    the recipe audit trail but requires polars-geopandas interop.
  - **In the materialisation path** (in `home_theater.py`, just before VizFactory call) — simpler,
    bypasses polars entirely, but geometry is invisible to the T3 audit trail.
  - **Inside VizFactory** (handler reads geometry directly from spec) — cleanest handler API but
    couples VizFactory to the filesystem.
- The recommended starting point is the materialisation path (option 2), with the option to
  promote to an assembler recipe step later.

### 5.5 Basemap file distribution
- Should Natural Earth files be committed to the repository (`assets/geodata/`) or downloaded
  on first run via a setup script?
- Committing ~5 MB of binary geodata to git is acceptable for a private/institutional repo but
  may be undesirable if the repo is ever made public.
- A `Makefile` target (`make download-geodata`) or a `scripts/setup_geodata.py` helper would
  handle the download cleanly.

### 5.6 plotnine vs. a dedicated mapping library
- For the publication-quality static output use case, plotnine + geom_map is adequate.
- If interactive exploration of map data becomes a requirement (click on a country to see isolate
  details, zoom to a region), plotnine is the wrong tool and a Folium or Plotly integration would
  be needed as a separate enhancement.
- This decision should be made explicitly before starting, to avoid implementing plotnine maps
  and then being asked to replace them with interactive ones.

---

## 6. Challenges and Risks

| Challenge | Severity | Notes |
|---|---|---|
| `geopandas` install on HPC/Galaxy environments | High | GDAL is a complex C dependency; some HPC environments do not allow user installs. Galaxy Tool Wrappers typically control the conda environment — need to verify. |
| Country name normalisation | Medium | Mismatched join keys will produce silent null geographies. Need a lookup table or fuzzy matching layer. |
| polars↔geopandas type boundary | Medium | The pipeline is polars-native for performance. Converting to pandas for geometry operations is straightforward but must be done at the right stage. |
| CRS diversity in source data | Medium | Veterinary monitoring data from multiple countries may carry different CRS or no CRS metadata at all. |
| plotnine high-latitude distortion | Low | Equirectangular projection visibly distorts Scandinavia. Acceptable for reports but should be documented. |
| Large geometry files at high resolution | Low | 1:10m Natural Earth files are ~15 MB. 1:50m (~5 MB) is usually sufficient for country-level maps. Sub-national data (GADM level 2) can be 50–200 MB — tile/simplify as needed. |
| T3 audit trail gaps | Low | Geometry joins happen outside the polars recipe pipeline, so they are not in the audit trail. For the initial implementation this is acceptable; document it explicitly. |
| Bundled geodata licensing | Low | Natural Earth is public domain; GADM has academic-only restrictions for redistribution. Verify licence before bundling in a shared repository. |

---

## 7. Effort Estimate (rough)

| Component | Effort |
|---|---|
| Dependency audit + install strategy | 0.5 day |
| Basemap file selection, download, and test | 0.5 day |
| Manifest schema extension (`geometry:` block) | 1 day |
| Geometry loader module + caching | 1 day |
| Materialisation path integration | 1–2 days |
| VizFactory `map_logic` handler + uncomment `geom_map` | 0.5 day |
| Country name normalisation lookup table | 1 day |
| Tests (unit + integration with a synthetic GeoJSON) | 1 day |
| Documentation (manifest authoring guide for spatial plots) | 0.5 day |
| **Total estimate** | **~7–8 person-days** |

This estimate assumes the deployment question (geopandas on Galaxy/IRIDA) is resolved first and
does not include interactive map support (Folium/Plotly), which would be a separate project.

---

## 8. Recommended Next Steps

1. **Confirm deployment feasibility**: Check whether `geopandas` can be installed in all target
   environments (Galaxy conda environment, institutional server, Docker image). This is the
   gate-blocking question.
2. **Identify one concrete map figure** from a recent NORM-VET or project report to use as the
   acceptance criterion — a specific plot that currently requires manual GIS work.
3. **Download and inspect Natural Earth 1:50m countries** as the baseline geometry asset.
4. **Prototype the join**: take the `country_summary` assembled dataset, load the Natural Earth
   GeoJSON, join on ISO3, call `geom_map` — verify the static output looks correct.
5. **Write the manifest schema extension ADR** (ADR-054 proposed) and get sign-off before
   building the full pipeline.

---

## 9. References

- plotnine `geom_map` documentation: https://plotnine.org/reference/geom_map.html
- GeoPandas installation guide: https://geopandas.org/en/stable/getting_started/install.html
- Natural Earth data: https://www.naturalearthdata.com/
- GADM boundaries: https://gadm.org/
- geoBoundaries (open, CC BY 4.0): https://www.geoboundaries.org/
- GeoParquet OGC standard v1.0.0: https://geoparquet.org/releases/v1.0.0/
- Kartverket (Norwegian Mapping Authority) open data: https://www.kartverket.no/en/open-data
- NORM-VET surveillance reports: https://www.vetinst.no/en/surveillance-programmes/norm-vet
