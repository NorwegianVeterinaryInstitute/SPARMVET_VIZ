---
trigger: always_on
date: 2026-03-29
purpose: Wrangling and transformation standards for SPARMVET_VIZ
---

# Wrangling & Transformation Standards (rules_wrangling.md)

## 1. Decorator Standards (The Law of Decorators)
- **Homogeneity:** All wrangling actions MUST follow the exact same architectural pattern using the `@register_action("name")` decorator.
- **Function Signature:** Every action MUST accept exactly two arguments: `(lf: pl.LazyFrame, spec: Dict[str, Any])`.
- **Parameter Extraction:** All parameters MUST be extracted from the `spec` dictionary.
- **Independence:** Actions MUST be atomic and independent, returning a modified `LazyFrame` without side effects.
- **Naming Convention (1:1:1 Law):**
    - **Logic:** `@register_action("name")`
    - **Manifest:** `./libs/transformer/tests/data/name_manifest.yaml`
    - **Data:** `./libs/transformer/tests/data/name_test.tsv`

## 2. Universal Wrangling Format
- **Sequential Staging:** Wrangling configurations in YAML manifests MUST use a **Sequential List of Dictionaries**.
- **Iteration Order:** Steps are staged (appended to the query plan) exactly in the order they appear in the manifest.
- **Lazy Execution:** The `DataWrangler (data_wrangler.py)` must ensure atomic actions do not trigger premature Polars collection (ADR-010).

## 3. ADR-013: The Manifest Data Contract
All yaml manifests MUST follow this mandatory block structure:
1. **Header:** ID and Description.
2. **`input_fields`:** Raw incoming schema (Raw/Ingestion).
3. **`wrangling`:** Operational bridge (Atomic actions).
4. **`output_fields`:** The Published Contract. This is a strict Polars `.select()` contract guarding against "Column Drift".

## 4. Data Type Selection Guide
| Type | Example | Usage Rule |
| :--- | :--- | :--- |
| **string** | 'Sample_01' | Use for raw names or IDs before final cleaning. |
| **categorical**| 'ST22' | **MANDATORY** for all discrete metadata in `output_fields`. |
| **integer** | 42 | Used for discrete counts or primary keys. |
| **float** | 0.985 | Used for identity scores or measurements. |
| **boolean** | True | Presence/absence or binary flags. |

## 5. Pattern Crystallization
- **Threshold:** When a new component type reaches a count of 3, the pattern MUST be codified as a standard.
- **Maintenance:** Once a rule is written, agents follow the rule rather than re-evaluating existing files.
