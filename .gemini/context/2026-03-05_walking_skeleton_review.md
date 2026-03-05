> GEMINI 3.1 Pro in Antigravity
# Walking Skeleton Architecture Review

Overall, the architecture described in the `docs/` is exceptionally well-thought-out. The separation of concerns (Ingestion -> Wrangling -> Configuration -> Visualization Factory -> Dashboard UI) is a strong foundation. Using YAML for data contracts (allowing non-programmers to configure species) and employing Polars + Plotnine ensures both performance and visual quality.

I have reviewed the documentation and extracted all the `#REVIEW` and `#TODO` comments. I've grouped them into distinct architectural challenges we need to resolve before/during coding, along with analysis of potential contradictions and best practices.

## 1. Data Exploration & State Management 
<1. We will use polarsdataframe but we need to use the lazy exectution. The choice of polars was based on this possibility of lazy execution and it should also appear in the reason for the choices made. >
**References:** `TODO_REVIEW.qmd`, `dashboard_app.qmd`, `wrangling.qmd`

- **The Question:** How should data filtering/exploration be handled? Do we keep a "filtered view" in memory? Should the wrangling layer return Parquet files or Polars DataFrames? 
- **Analysis & Best Practice:** `wrangling.qmd` mentions potentially returning Parquet files, but returning in-memory `Polars DataFrames` to the orchestrator is the standard and correct approach for a live Shiny Dashboard. Writing to Parquet during active user filtering (e.g., using a slider) would cause massive disk I/O bottlenecks. 
- **Recommendation:** The Server should load the wrangled `Polars DataFrame` into memory (or maintain a lazy execution plan if the data is massive). When a user updates a filter, Shiny triggers a reactive update, Polars executes the filter in-memory, and passes the filtered DataFrame to the Visualization Factory.

## 2. User Preferences vs. Data Contracts
<OK your suggestion seems good. This needs to be added to the documentation.>
**References:** `TODO_REVIEW.qmd`, `visualisation_factory.qmd`, `user_preferences.qmd`, `configuration.qmd`

- **The Question:** How do user preferences work? How do we merge configs, handle palettes, and prevent users from breaking the data contract? Where are they persisted?
- **Analysis & Best Practice:** We must strictly separate the *Data Contract* (`data_schema`, `metadata_schema`) from *Visual Preferences* (`plot_defaults`, palettes).
- **Recommendation:** 
  1. Load the core Module/Species YAML first.
  2. If a User Preference YAML exists (uploaded or fetched from a user profile/account), perform a "deep update" on the configuration dictionary, **but explicitly block/ignore any keys that attempt to alter the `data_schema` or `metadata_schema`**.
  3. Palettes can be defined in a master `manifest.yml` for the app, overridden by the species config, and ultimately overridden by the user config.

## 3. Data Validation & Mandatory Columns
<I think columns from data_schema needs to be mandatory because the data will originate from analyses pipelines (automated) if they are missing it can mean that the pipeline fails. However, for metadata we can have a minimum set of mandatory metadata while the rest can be available for plotting. Can this decision be added to the documentation also ?>
**References:** `new_data_contract.qmd`, `core_architecture_code.qmd`

- **The Question:** Are all columns in the `data_schema` mandatory by default? Where does validation happen?
- **Analysis & Best Practice:** `new_data_contract.qmd` states "All columns in the data_schema are mandatory by default." This might be too rigid for a general tool. If a user uploads a dataset missing a column they don't even intend to plot, the app shouldn't crash.
- **Recommendation:** By default, only the `is_primary_key` should be strictly mandatory for the join. Other columns should be checked: if they are missing, they simply aren't available for plotting, and plots relying on them are disabled/hidden. Validation should occur purely in the **Ingestion Layer**, using a dedicated Config Loader/Validator before it ever hits Polars.

## 4. Connectors & External API
<OK, this needs to be added to the documentation>
**References:** `connector.qmd`

- **The Question:** Should Connectors (links to APIs like Galaxy/IRIDA) also be configured via YAML?
- **Recommendation:** Yes. A `connectors.yml` that defines endpoints, expected auth headers (handled securely), and data paths allows you to easily point the app to a different Galaxy instance without changing the python code.

## 5. Minor Documentation Needs
<Can you add the filtermessage to the flow graph to index. 
For core_architecture_code.qmd and configuration.qmd I will need help on how to improve this (guidelines). 
- done core_architecture_code.qmd
>

- **`dashboard_app.qmd`:** Add the filter message flow graph to `index.qmd`. 
- **`core_architecture_code.qmd`:** Improve the CodeBase organization section.
- **`configuration.qmd`:** Document what works "out of the box" so users know how to make a new species dashboard easily.

---

### Suggested Next Steps for Implementation
<For implementation we will first need to build a real data contract (this wil lbe the first step) then the rest is ok.>
1. **Config Loader & Validator:** Build the Python utility that reads the YAML, parses the data contract, and merges user preferences safely.
2. **Ingestion Layer:** Build the CSV/Metadata reader that uses the Config Loader to validate required keys.
3. **Wrangling Layer:** Build the Polars join logic, returning a tidy DataFrame.
4. **Visualisation Factory:** Build one simple Plotnine function that accepts the tidy DataFrame and the config dictionary.
5. **Shiny App:** Wire it all together in a basic UI to prove the "Walking Skeleton".
