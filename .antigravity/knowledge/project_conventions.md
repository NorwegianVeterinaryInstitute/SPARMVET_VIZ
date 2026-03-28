# Project Conventions & Quick Reference (Combat Log)

## 1. File Registry (Compressed)
| Component | Purpose | I/O | Key Logic / Terms |
|---|---|---|---|
| `adapter_*.py` | Normalizes incoming API/data payloads | Raw Payload → Dict | `Adapter`, format mapping |
| `ingestor.py` | Reads sources, implements early "Fail-Fast" validation | YAML/Paths → LazyFrame | `csv_reader`, primary key checks |
| `data_wrangler.py` | Layer 1 execution: Dispatches dynamic rules for one dataset | Dataset → Tidy LazyFrame | `.pipe()`, `spec` unpacking |
| `data_assembler.py`| Layer 2 orchestration: Joins multiple standard datasets | Multiple LFs → Unified LF | `.join()`, `recipe` |
| `registry.py` | Single O(1) dictionary holding loaded decorations | String ID → Function | `AVAILABLE_WRANGLING_ACTIONS`|
| `actions/base.py` | Declares the registry wrapper linking logic to parser | Naked func → Registered | `@register_action` |
| `actions/core/*.py`| Atomic lazyframe operations (fill_nulls, strip_ws, etc) | LF → LF subset | Strict `pl.col()` vectors |
| `actions/advanced/*.py` | Complex rules mapping against reference DBs | Values/DB → Metadata | `derive_categories` |
| `actions/core/relational.py`| Joins tailored for assembly schemas | LF + LF → LF | `join_filter`, `how="left"` |
| `wrangler_debug.py` | Universal Layer 1 Runner: Dispatches rules for any dataset | TSV/YAML → Log / TSV | ADR-005, Ingestor |
| `assembler_debug.py`| Layer 2 Debugger: Validates assembly via explicit execution | Schema/Sources → `EVE_*.tsv`| `.collect()`, `argparse` |
| `test_decorator_suite.py`| Automated Runner: Iterates through all atomic test manifests | (Suite) → Pass/Fail Summary | CI, Verification Loop |
| `create_manifest*` | Bootstraps boilerplate JSON/YAML hybrid definitions | Templates → 3-block schema| `input_fields`, `output_fields` |
| `pipeline/*.yaml` | Master configurations and nested data contracts | (Defs) → Pipeline state | `!include`, `assembly_manifests`|

## 2. Verification Protocol (Cheat Sheet)
1. **The Contract**: Pre-define `_test.tsv` & `_manifest.yaml`. STOP for `@confirm_contract`.
2. **Execute via CLI**: `python test_script.py --data [tsv] --manifest [yaml]` (Use `argparse` overrides).
3. **Naming Law (1:1:1)**: 
    - Action: `@register_action("name")`
    - Manifest: `./libs/transformer/tests/data/name_manifest.yaml`
    - Data: `./libs/transformer/tests/data/name_test.tsv`
4. **Generate Evidence**: 
    - Materialize `tmp/USER_debug_view.tsv` (`.collect()`) OR save Plotnine to `tmp/USER_debug_plot.png`.
5. **Console Out**: Print 10 rows + schema via `df.glimpse()`.
6. **@verify Gate**: HALT execution. Print standard message: "Data/Plot ready in tmp/... Waiting for @verify". No task is [DONE] in `tasks.md` without this.

## 3. Assembler Logic (Cheat Sheet)
- **Role**: Combines wrangled 'ingredients' via 'recipes' (Relational Joins).
- **Decorators**: Shares `@register_action(name)` with Wrangler.
- **Key-as-ID**: Leverages `is_primary_key: true` tags automatically for joins.
- **Contract Boundary**: `output_fields` is the terminal `.select()` query guarding against column drift.
