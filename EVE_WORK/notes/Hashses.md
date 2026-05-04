**Fixed across all export surfaces:**

| Surface                      | Before                                                     | After                                                            |
| ---------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------------- |
| Bundle README                | manifest + T1-content fingerprint (different method)       | manifest SHA256 + data_batch_hash (raw files) + recipe hash note |
| Bundle QMD report provenance | two bare hash lines                                        | 3-row table with Meaning column                                  |
| Bundle QMD footer            | two bare hash lines                                        | labelled with what each hash means                               |
| SGE README                   | truncated 16-char fragment hash + T1 TSV hash (both wrong) | manifest SHA256 + data_batch_hash from home_state + recipe note  |

**One remaining gap — EXPORT-HASH-2:** The `decision_hash` (wrangling recipe SHA256 stored in each Parquet file's metadata) is referenced by name in all exports but not yet read out as an actual value. To do that properly, the export code needs to know which Parquet files were materialized and call `get_parquet_metadata_hash(path)` on each. Registered as **EXPORT-HASH-2** in tasks — straightforward to implement but needs the Parquet file paths at export time.