# README for MANIFEST 2_test_data_ST22_dummy


> Note: Following: architectural standards (ADR-041)



## AMR Profiling
- integrated ResFinder data with Metadata
- implemented the multi-resistance annotation logic [DESCRIBE]
- ResFinder Data was joined with metadata
    - filtered by biological thresholds (min 90% identity, min 60% overlap)
    - annotated with an is_multi_resistant flag (isolates resistant to ≥ 2 antimicrobial classes).
