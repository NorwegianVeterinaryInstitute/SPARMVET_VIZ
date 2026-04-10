# Transformer Library Integrity Suite 🛡️

This directory contains standalone tests for investigating and verifying the logic of individual wrangling actions.

## Tiered Manifest Structure (ADR-024)

All manifests in this directory follow the **Tiered Wrangling Structure**. When contributing new tests, ensure the wrangling block uses `tier1` and/or `tier2`:

```yaml
id: "example_test"
data_schemas:
  test_dataset:
    source:
      type: "local_tsv"
      path: "libs/transformer/tests/data/example_test.tsv"
    wrangling:
      tier1:
        - action: "rename"
          mapping: { "old": "new" }
      tier2:
        - action: "summarize"
          # Aggregations go here
    output_fields:
      new: {}
```

## Test Runners

- **debug_wrangler.py**: Dedicated runner for Layer 1 actions.
  - usage: `python debug_wrangler.py --manifest path/to/manifest.yaml --tier [tier1|tier2|all]`
- **transformer_integrity_suite.py**: Executes all atomic action tests and generates a pass/fail report.

## Materialization Gate (@verify)

The `--output` argument in runners materializes the result into `tmp/`. Always verify the output data visually or via `glimpse()` before considering a task [DONE].
