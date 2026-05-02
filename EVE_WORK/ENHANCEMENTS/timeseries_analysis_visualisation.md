# Enhancement: Time Series Analysis and Visualisation

**Status:** Pre-design — funding/scoping document  
**Date:** 2026-05-02  
**Author:** @evezeyl  
**Relates to:** tasks.md §Open Issues (AUDIT-3 temporal dimension), VizFactory deferred, ST22 Lineage 2

---

## 1. Goal

Enable SPARMVET_VIZ to perform **temporal analysis and produce publication-quality time series
figures** directly from the existing manifest-driven pipeline — covering the standard analytical
methods used in AMR and veterinary epidemiology surveillance (NORM-VET, EFSA, EARS-Net, WHO GLASS).

Currently, any figure involving a time axis beyond a simple bar/scatter requires the analyst to
step outside the platform and use R (`ggplot2 + trend`, `incidence2`, `surveillance` package) or
custom Python scripts. Integrating time series into the manifest pipeline closes this gap and
makes temporal analyses reproducible, auditable, and shareable with the same workflow as all other
analytical outputs.

### Concrete use cases

| Analysis type | Epidemiological question |
|---|---|
| **Trend line over years** | Is ESBL prevalence in *E. coli* from poultry increasing or decreasing? |
| **Epidemic curve (epicurve)** | What is the weekly incidence distribution during a Salmonella outbreak? |
| **Seasonal decomposition** | Does AMR prevalence in companion animals show a seasonal pattern? |
| **Interrupted time series (ITS)** | Did the 2022 fluoroquinolone restriction reduce resistance rates? |
| **Rolling prevalence** | Smooth yearly resistance % for a moving 3-year window |
| **Multi-species trend facets** | Compare AMR trend trajectories across cattle / pigs / poultry simultaneously |
| **Year-over-year change** | Which resistance classes increased > 5% between 2023 and 2024? |
| **Panel/longitudinal tracking** | Track individual herd or farm resistance profile over monitoring visits |

---

## 2. Current System — What Exists

### 2.1 Data pipeline

```
TSV/Excel files
    → DataIngestor (polars)       — reads, validates, schema-checks
    → DataAssembler               — joins, filters, pivots via YAML recipe steps
    → home_theater materialise    — polars LazyFrame → pandas DataFrame
    → VizFactory.render()         — pandas + plotnine → matplotlib figure
```

### 2.2 Rendering primitives already registered in VizFactory

The following plotnine components are **already registered and working**:

| Component | Registered as | Time series use |
|---|---|---|
| `geom_line` | `geom_line` | Core time series trace |
| `geom_area` | `geom_area` | Filled area under line (incidence area charts) |
| `geom_step` | `geom_step` | Step function (discrete-time transitions) |
| `geom_ribbon` | *imported, not yet registered* | Confidence/prediction band around a line |
| `geom_smooth` | `geom_smooth` | LOESS/linear trend overlay |
| `geom_errorbar` | `geom_errorbar` | Year-level uncertainty bars |
| `geom_point` | `geom_point` | Observed data points on a trend line |
| `geom_vline` | `geom_vline` | Mark intervention date (ITS) |
| `geom_hline` | `geom_hline` | Threshold / EUCAST breakpoint lines |
| `scale_x_date` | `scale_x_date` | Date axis with `date_breaks` / `date_labels` |
| `scale_x_datetime` | `scale_x_datetime` | Datetime axis |
| `scale_x_timedelta` | `scale_x_timedelta` | Duration axis (re-enabled 2026-05-01) |
| `facet_wrap` / `facet_grid` | *via themes* | Multi-species / multi-region panels |

**The visualisation layer is largely ready.** The gap is in the **analysis and aggregation layer**
upstream of the plot — pre-computing rolling averages, running trend tests, detecting changepoints,
and decomposing seasonality — and in missing high-level factory types that encode the full
time series workflow in a single manifest declaration.

### 2.3 Date/time handling in the current pipeline

- Polars reads date columns as `Polars.Date` or `Polars.Datetime` when the manifest declares
  `type: "date"` in the data schema.
- The assembler supports `filter` and `mutate` recipe steps that can operate on date columns.
- There is no current support for: temporal aggregation (roll up to week/month/year),
  rolling windows, lag/diff operations, or epiweek assignment.
- Polars has full native support for all of these operations; they are just not yet exposed as
  manifest recipe step types.

### 2.4 Existing factory_ids

Current high-level factory_ids: `heatmap_logic`, `bar_logic`, `scatter_logic`, `boxplot_logic`,
`violin_logic`. None are designed for time series. A time series manifest currently requires
manually specifying layers (geom_line + scale_x_date + ...) in a low-level layer list, which is
verbose and does not encode epidemiological intent.

---

## 3. Current Limitations

### 3.1 No temporal aggregation in the assembly recipe

The assembler has no recipe step for temporal grouping:
```yaml
# Does NOT exist yet:
- resample:
    by: "week"
    value_col: "n_resistant"
    agg: "sum"
```
Analysts must pre-aggregate in Excel or external scripts before ingestion, which breaks
reproducibility and the T3 audit trail.

### 3.2 No epiweek support

ISO epiweeks (ISO 8601-1, starts Monday) and CDC/MMWR epiweeks (starts Sunday) are the standard
temporal unit in outbreak and surveillance reporting. Neither the ingestor nor the assembler can
derive an epiweek column from a date column. The `epiweeks` Python library handles this but is
not installed.

### 3.3 No statistical trend analysis

There is no mechanism to run a Mann-Kendall trend test or Cochran-Armitage test and embed the
result (p-value, slope, direction) as an annotation in the figure or export it alongside the plot
data. These tests are mandatory in NORM-VET and EFSA annual surveillance reports.

### 3.4 No rolling / smoothing operations in the recipe

Rolling mean, rolling sum, and LOESS smoothing over time windows are standard for epidemic curve
visualisation and for suppressing year-to-year noise in resistance trend figures. These require
pre-computation before plotnine; there is no recipe step type that does this.

### 3.5 No interrupted time series (ITS) support

ITS analysis — segmented regression with a declared intervention date — is the primary method for
evaluating the impact of a regulatory or prescribing change on AMR rates. It requires:
a fitted statistical model (statsmodels or PyMC), a structural break point in the time axis, and
a counterfactual projection. None of this is currently supported.

### 3.6 No epicurve factory

An epicurve (epidemic curve) is a histogram of case counts over time at a standardised temporal
resolution (day / week / month), coloured optionally by case source or pathogen. It is the most
common figure in outbreak investigation reports and is not available as a factory type. Building
one from scratch in a manifest requires specifying a histogram + date axis + custom bin width,
which is feasible but undiscoverable.

### 3.7 No confidence intervals from statistical models

`geom_ribbon` is imported but not registered as a component. Outputting model-derived confidence
bands (e.g. from a Poisson regression trend model or LOESS) requires both running the model
upstream and passing the CI columns to the ribbon layer — neither is currently supported in the
manifest schema.

### 3.8 Missing dependencies

| Library | Role | Status |
|---|---|---|
| `statsmodels` | ARIMA, seasonal decomposition (STL), Holt-Winters, OLS/GLM for ITS | NOT installed |
| `pymannkendall` | Mann-Kendall trend test, Sen's slope, 11 variants incl. autocorr-corrected | NOT installed |
| `epiweeks` | ISO and CDC epiweek calculation from date columns | NOT installed |
| `prophet` | Trend + seasonality decomposition + changepoint detection | NOT installed (optional) |

`scipy.stats` (Kendall tau, linear regression) is likely available as a polars/pandas transitive
dependency but not explicitly declared.

---

## 4. What Implementation Would Require

### 4.1 New Python dependencies

**Core (required for basic time series support):**
```toml
statsmodels>=0.15.0   # ~25 MB; seasonal decomposition, ARIMA, OLS for ITS
pymannkendall>=1.4.3  # ~1 MB; Mann-Kendall + Sen's slope
epiweeks>=2.2.0       # <1 MB; ISO/CDC epiweek arithmetic
```

**Optional (forecasting and Bayesian ITS):**
```toml
prophet>=1.1.5        # ~150 MB; trend + changepoint detection
# OR
sktime>=0.35.0        # ~80 MB; unified forecasting API
```

All are compatible with Python 3.11–3.13 and work in a standard venv.

### 4.2 New assembler recipe step types

New YAML recipe step keywords exposing polars native time series operations:

```yaml
# Temporal aggregation — roll up rows to a calendar period
- resample:
    date_col: "collection_date"
    period: "1w"              # 1d / 1w / 1mo / 1y  (polars duration string)
    group_by: ["country", "resistance_class"]
    agg:
      n_isolates: sum
      n_resistant: sum

# Derived columns — epiweek, year, month
- add_epiweek:
    from_col: "collection_date"
    system: "iso"             # "iso" or "cdc"
    new_col: "epiweek"

# Rolling window
- rolling:
    date_col: "collection_date"
    value_col: "prevalence_pct"
    window: "3y"
    agg: "mean"
    new_col: "rolling_3y_mean"

# Lag / difference
- lag:
    col: "prevalence_pct"
    n: 1
    new_col: "prev_year_pct"
```

These map directly to polars operations (`group_by_dynamic`, `rolling_mean_by`, `shift`,
epiweeks library call) and are fully compatible with the existing assembler architecture.

### 4.3 New manifest schema — statistical analysis block

A new optional `analysis:` block in a plot spec declares what statistical tests or model fits
to run on the assembled data before rendering:

```yaml
analysis_groups:
  Trends:
    plots:
      esbl_ecoli_trend:
        factory_id: "timeseries_logic"
        target_dataset: "annual_resistance_summary"
        x: "year"
        y: "prevalence_pct"
        group_by: "animal_species"
        analysis:
          trend_test:
            method: "mann_kendall"        # or "sens_slope" / "cochran_armitage"
            alpha: 0.05
            annotate: true                # embed p-value + trend direction on figure
          smoothing:
            method: "loess"               # or "rolling_mean"
            window: 3                     # years
            show_ci: true                 # geom_ribbon for 95% CI
        title: "ESBL prevalence trend — *E. coli* by animal species 2015–2024"
        
      salmonella_epicurve:
        factory_id: "epicurve_logic"
        target_dataset: "outbreak_cases"
        date_col: "onset_date"
        period: "1w"                      # epiweek bins
        fill: "serotype"
        title: "Epidemic curve — Salmonella outbreak 2024"
        
      flu_restriction_its:
        factory_id: "its_logic"
        target_dataset: "annual_resistance"
        x: "year"
        y: "prevalence_pct"
        intervention_date: "2022-01-01"   # fluoroquinolone restriction
        model: "ols_segmented"            # statsmodels OLS with breakpoint
        show_counterfactual: true         # projected trend absent intervention
        title: "Impact of fluoroquinolone restriction on resistance (ITS)"
```

### 4.4 New VizFactory factory types

Three new high-level factory_ids, each encoding a full epidemiological workflow:

| factory_id | Description | Key layers |
|---|---|---|
| `timeseries_logic` | General time series: line + optional trend overlay + CI ribbon | `geom_line`, `geom_smooth`/`geom_ribbon`, `scale_x_date`, Mann-Kendall annotation |
| `epicurve_logic` | Epidemic curve: histogram with epiweek/day bins | `geom_bar`, `scale_x_date` with `date_breaks`, optional fill by case classification |
| `its_logic` | Interrupted time series: segmented regression + counterfactual | `geom_line` (observed), `geom_line` (fitted), `geom_ribbon` (CI), `geom_vline` (intervention), `geom_line` dashed (counterfactual) |

### 4.5 Statistical output alongside figures

Trend test results (Mann-Kendall p-value, Sen's slope, trend direction) should be:
- Annotated on the figure (configurable, on by default)
- Written to a sidecar `.json` or `.tsv` file included in the export bundle
- Captured in the T3 audit recipe as a `statistical_test` node type (new node kind)

This makes the analysis reproducible: another user opening the same manifest + data gets the
same figure and the same statistical annotation.

### 4.6 T3 audit integration

Time series analysis raises specific audit design questions (see §5), but the existing
infrastructure maps well:

- Temporal aggregation recipe steps (`resample`, `add_epiweek`) are standard assembler steps and
  are fully auditable in the T3 recipe.
- An intervention date in an ITS analysis is an **analytical decision** with significant impact —
  it should be a first-class T3 audit node, requiring a reason field ("fluoroquinolone
  restriction effective 2022-01-01, per Norwegian Medicines Agency circular").
- Rolling window width and smoothing method choices should also be captured in the audit trail.

### 4.7 `geom_ribbon` registration

`geom_ribbon` is already imported in `libs/viz_factory/src/viz_factory/geoms/core.py` but not
registered. It is needed for confidence bands on trend lines and ITS counterfactual projections.
This is a one-line addition alongside the existing `geom_errorbar` handler.

---

## 5. Open Questions to Resolve Before Implementation

### 5.1 Temporal resolution and the data contract

- Are dates stored consistently in source TSVs? (ISO 8601: `YYYY-MM-DD` vs `DD.MM.YYYY` vs
  Excel serial dates). The ingestor needs to enforce a canonical format or normalise at ingest.
- For annual surveillance data (NORM-VET style), dates may only be `YYYY` integers rather than
  full dates. Should `year` be a special temporal type in the manifest schema?
- What is the minimum date resolution available in the current ST22 data?

### 5.2 Trend test selection

- Mann-Kendall is the standard non-parametric test for monotonic trend in AMR surveillance.
  However, it assumes no autocorrelation. For short time series (< 10 years) with high
  autocorrelation (resistance rates are correlated year-to-year), the Hamed-Rao correction or
  pre-whitening is recommended. Should the manifest support selecting the correction, or should
  the system apply it automatically?
- Cochran-Armitage is the standard for proportions (n_resistant / n_tested) across ordered
  groups. For NORM-VET-style data (annual counts of susceptible/resistant isolates), this is
  often more appropriate than Mann-Kendall on derived percentages.

### 5.3 Interrupted time series — model selection

- Simple OLS segmented regression (statsmodels) is the most common ITS approach in AMR
  literature but assumes linearity and normally-distributed residuals — often violated with
  small counts or percentage data.
- Poisson or negative-binomial regression (count outcomes), or logistic regression (proportion
  outcomes) are more appropriate but require explicit model selection in the manifest.
- Bayesian ITS (PyMC or CausalPy) gives full uncertainty quantification but is a large
  additional dependency (~500 MB) and long runtime.
- **Decision needed**: Define a supported model menu for the initial implementation
  (recommended: OLS + Poisson) and document limitations clearly.

### 5.4 Seasonality and the current dataset structure

- Seasonality detection (STL decomposition) requires sub-annual data (monthly at minimum).
  Current ST22 data is annual. This feature is only meaningful when veterinary monitoring data
  with monthly/weekly resolution is available.
- For outbreak investigation, weekly data is standard. Is there current or planned data in the
  project at weekly resolution?

### 5.5 Epiweek system choice

- NORM-VET and European surveillance (EFSA, ECDC) use ISO epiweeks.
- WHO uses ISO epiweeks.
- US CDC uses MMWR (CDC) epiweeks.
- The manifest should require explicit declaration of the epiweek system rather than defaulting,
  to avoid silent mismatches when sharing data with international partners.

### 5.6 Interaction with the T3 audit: intervention dates

- An ITS intervention date is an analytical parameter that changes the shape of the figure and
  the statistical conclusion. It must be auditable.
- Should the intervention date live in the manifest (fixed at manifest authoring time) or be
  settable by the user at runtime via the T3 audit pipeline (more flexible, but requires a new
  parameter-type T3 node)?
- The former is simpler and appropriate for pre-planned analyses; the latter is better for
  exploratory investigation. Both may be needed.

### 5.7 Interactive vs. static time series

- For publication, static plotnine figures are the goal.
- For exploration (zooming into a specific year range, hovering over a data point to see sample
  counts), an interactive component is far superior. The research confirms Plotly + Shiny's
  `shinywidgets` is the most mature integration path.
- Should this enhancement cover both static (plotnine) and interactive (Plotly) time series, or
  should interactive time series be a separate follow-on enhancement? This decision significantly
  affects scope and testing effort.

---

## 6. Challenges and Risks

| Challenge | Severity | Notes |
|---|---|---|
| Short time series in current data | High | NORM-VET-style data has 5–15 annual observations. Most statistical tests (Mann-Kendall, ARIMA) lose power below 10 observations. Must document minimum required series length prominently. |
| Autocorrelation in resistance rates | High | Year-to-year resistance rates are correlated. Standard Mann-Kendall p-values are anti-conservative; the Hamed-Rao autocorrelation correction should be the default. |
| Irregular time series (gaps, unequal spacing) | Medium | Surveillance data frequently has missing years or starts at different years for different species. Rolling operations on irregular series require careful handling in polars (`group_by_rolling` with `closed` and `min_periods` parameters). |
| Date column standardisation across source files | Medium | Source TSVs may encode dates inconsistently. The ingestor must normalise or reject non-standard formats before temporal operations are applied. |
| ITS model assumptions easily violated | Medium | Non-statisticians may apply ITS without checking linearity or distributional assumptions. Manifest schema should include a `model_check` field that logs residual diagnostics to the export bundle. |
| `statsmodels` install size | Low | ~25 MB; acceptable. Already commonly pre-installed in scientific Python environments. |
| `prophet` install size | Medium | ~150 MB with Stan backend; only worth installing if changepoint detection use cases are confirmed. Mark as optional. |
| Confounding in trend analysis | High (scientific) | AMR trends are confounded by changes in sampling strategy, species composition of submissions, and testing methodology over time. Statistical tests will find "trends" that are artefacts. This is a scientific interpretation issue, not a software issue — but documentation and user guidance are needed. |
| T3 audit trail for analytical parameters | Medium | Rolling window width, smoothing method, intervention date, and model choice all affect the conclusion. The T3 audit node schema needs a `parameter_override` node type to capture these changes. |

---

## 7. Effort Estimate (rough)

| Component | Effort |
|---|---|
| Dependency audit + install + tests | 0.5 day |
| `geom_ribbon` registration + tests | 0.5 day |
| Assembler: `resample`, `add_epiweek`, `rolling`, `lag` step types | 2–3 days |
| `timeseries_logic` factory + Mann-Kendall annotation | 2 days |
| `epicurve_logic` factory | 1 day |
| `its_logic` factory (OLS + Poisson segmented regression) | 2–3 days |
| Manifest schema extension (`analysis:` block, `factory_id` additions) | 1 day |
| Statistical output sidecar (JSON export alongside plot) | 0.5 day |
| T3 audit integration for intervention dates / analytical parameters | 1–2 days |
| Tests (unit + integration with synthetic annual/weekly data) | 2 days |
| Documentation (manifest authoring guide, statistical method notes) | 1 day |
| **Core total (timeseries_logic + epicurve_logic, no ITS)** | **~10–11 person-days** |
| **Full total (incl. ITS + T3 audit parameters)** | **~15–17 person-days** |

Interactive time series (Plotly / shinywidgets) is **not included** in this estimate — it is a
separate enhancement estimated at an additional 5–7 person-days.

---

## 8. Recommended Next Steps

1. **Confirm minimum data resolution**: Identify the temporal granularity available in current
   and planned datasets. If only annual data exists, seasonality and epicurve functionality
   cannot be validated and should be deferred to a second phase.

2. **Decide static vs. interactive scope**: Resolve whether this enhancement covers plotnine
   static output only, or also includes Plotly interactive time series in Shiny. This is the
   largest scope branch point.

3. **Prototype Mann-Kendall on current ST22 data**: Take the AMR annual resistance data,
   run `pymannkendall` directly in a Jupyter notebook, and confirm the test produces
   interpretable output and that the time series is long enough to be meaningful.

4. **Register `geom_ribbon`**: One-line change, independent of all other work, can be done
   immediately.

5. **Draft the ADR** (ADR-054 or ADR-055 proposed) covering: new recipe step types, the
   `analysis:` manifest block, the statistical output contract, and T3 audit implications for
   analytical parameters.

6. **Write one real surveillance figure spec**: Take a resistance trend figure from the most
   recent NORM-VET report and write the manifest YAML that would produce it under the proposed
   schema. This is the best way to stress-test the design before building.

---

## 9. Relationship to Other Enhancements

| Enhancement | Relationship |
|---|---|
| [Spatial manifests / geom_map](spatial_manifests_geospatial_viz.md) | Independent. Both can proceed in parallel. A combined spatio-temporal map (resistance trend animated over geography) is a future extension of both. |
| PROP-1 filter propagation (done) | The column-presence check in the propagation modal will need to handle date columns and epiweek columns correctly when time series manifests are introduced. |
| AUDIT-3 (propagation to all plots) | A resistance trend filtered to a specific year range should propagate correctly to all plots in the same analysis group — this is the same propagation design question already open. |
| ITS intervention dates as T3 nodes | Requires a new `parameter_override` T3 node type, distinct from `filter_row` and `drop_column`. Design work needed — see §5.6 above. |

---

## 10. References

- plotnine `scale_x_date`: https://plotnine.org/reference/scale_x_date.html
- plotnine `geom_smooth` / `stat_smooth`: https://plotnine.org/reference/geom_smooth.html
- Polars time series operations: https://docs.pola.rs/user-guide/transformations/time-series/
- pyMannKendall (11 variants + Sen's slope): https://github.com/mmhs013/pyMannKendall
- statsmodels seasonal decomposition: https://www.statsmodels.org/dev/generated/statsmodels.tsa.seasonal.seasonal_decompose.html
- epiweeks library (ISO + CDC): https://epiweeks.readthedocs.io/
- Prophet (Meta) changepoint detection: https://facebook.github.io/prophet/
- CausalPy — Bayesian ITS: https://causalpy.readthedocs.io/
- EFSA guidance on statistical methods for AMR trend analysis: https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2022.7122
- NORM-VET annual reports (NVI): https://www.vetinst.no/en/surveillance-programmes/norm-vet
- Shiny for Python + Plotly widgets: https://shiny.posit.co/py/components/outputs/plot-plotly/
- Cochran-Armitage trend test for proportions: https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportions_chisquare.html
