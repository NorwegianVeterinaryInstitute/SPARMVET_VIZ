

|**Category**|**Action Name**|**Polars Source**|**Purpose**|
|---|---|---|---|
|**Reshaping**|`unpivot`|`pl.melt()` / `pl.unpivot()`|Converts wide data (gene matrices) to Tidy long format.|
||`explode`|`pl.explode()`|Expands list columns; essential for AMR data with multiple hits per sample.|
||`unnest`|`pl.unnest()`|Flattens complex struct columns from bio-informatics Parquet/JSON formats.|
||`pivot`|`pl.pivot()`|Re-shapes Tidy data for specific "Matrix View" exports for end-users.|
|**Cleaning**|`coalesce`|`pl.coalesce()`|Fills nulls by choosing the first available value across prioritized columns.|
||`cast`|`pl.cast()`|Enforces strict schema types (Categorical, Int, Date) for Viz Factory stability.|
||`label_if`|`pl.when().then()`|Declarative conditional logic (e.g., "if result > 0.06 then 'Resistant'").|
|**Relational**|`anti_join`|`pl.join(how="anti")`|Identifies samples in Metadata that are missing from Phenotypes (Data QC).|
|**Persistence**|`checkpoint`|`pl.sink_parquet()`|**Tier 1 Logic**: Materializes the Anchor table to disk.|
||`restore`|`pl.scan_parquet()`|**Tier 2 Logic**: Virtually subsets the Anchor table for rapid UI views.|
|**Performance**|`summarize`|`pl.group_by().agg()`|Pre-aggregates data to reduce row counts before Plotnine rendering.|