# README for MANIFEST 2_test_data_ST22_dummy


> Note: Following: architectural standards (ADR-041)

> Note: Rendering 
- libs/transformer/tests/debug_wrangler.py  - for T1 wrangling.
- libs/transformer/tests/debug_assembler.py - for T2 assembly.
- assets/scripts/materialize_manifest_plots.py - for plot materialization.

## AMR Profiling
- integrated ResFinder data with Metadata
- implemented the multi-resistance annotation logic [DESCRIBE]
- ResFinder Data was joined with metadata
    - filtered by biological thresholds (min 90% identity, min 60% overlap)
    - annotated with an is_multi_resistant flag (isolates resistant to ≥ 2 antimicrobial classes).


```bash
#python3 -m venv .venv && source .venv/bin/activate
# Tier 1
./.venv/bin/python libs/transformer/tests/debug_wrangler.py \
  --manifest config/manifests/pipelines/2_test_data_ST22_dummy.yaml \
  --tier tier1 \
  --output tmp/2026-04-23/AMR_Profile/tier1/

# Tier 2
./.venv/bin/python libs/transformer/tests/debug_assembler.py \
  --manifest config/manifests/pipelines/2_test_data_ST22_dummy.yaml \
  --output tmp/2026-04-23/AMR_Profile/tier2/AMR_Profile_Joint.tsv

# Plots
./.venv/bin/python assets/scripts/materialize_manifest_plots.py \
  --manifest config/manifests/pipelines/2_test_data_ST22_dummy.yaml \
  --output_root tmp/2026-04-23/AMR_Profile/plots/
```

