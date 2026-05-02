
# Launching the app with a persona

Set `SPARMVET_PERSONA` to the persona ID before starting the app.

> **`SPARMVET_PERSONA` accepts a file path OR a shortname.**
> Path: `SPARMVET_PERSONA=/path/to/my_persona.yaml` → loaded directly (any location).
> Shortname: `SPARMVET_PERSONA=developer` → `config/ui/templates/developer_template.yaml` (backward compat).
> UI shows `display_name` from the config file, not the path.
> Terminal prints the resolved absolute path at startup — use that to confirm which file was loaded.
> Full reference: `docs/reference/environment_variables.qmd` | ADR-054 in architecture_decisions.md

```bash
# Full-access developer mode (Blueprint Architect, Gallery, all tiers, session mgmt)
export PYTHONPATH=$PYTHONPATH:. && SPARMVET_PERSONA=developer ./.venv/bin/python -m shiny run app/src/main.py --port 8001

# Advanced exploration (T3 audit, session mgmt, export graph, metadata upload — no Blueprint/Gallery)
export PYTHONPATH=$PYTHONPATH:. && SPARMVET_PERSONA=pipeline-exploration-advanced ./.venv/bin/python -m shiny run app/src/main.py --port 8001

# Simple exploration (T3 interactivity, session mgmt, export bundle — no T3 audit, no graph export)
[ HERE DOES NOT MAKE SENSE TO HAVE T3 - ok its only filtering but no apply works like that] [Deactivate Gallery !!!] #TODO 
export PYTHONPATH=$PYTHONPATH:. && SPARMVET_PERSONA=pipeline-exploration-simple ./.venv/bin/python -m shiny run app/src/main.py --port 8001

# Static pipeline (read-only — export bundle only, no interactivity, no session mgmt)
export PYTHONPATH=$PYTHONPATH:. && SPARMVET_PERSONA=pipeline-static ./.venv/bin/python -m shiny run app/src/main.py --port 8001

# Project-independent user (like advanced + data ingestion enabled)
export PYTHONPATH=$PYTHONPATH:. && SPARMVET_PERSONA=project-independent ./.venv/bin/python -m shiny run app/src/main.py --port 8001

# QA / Test Harness (PERSONA-2): every flag ON, ghost_save OFF for determinism.
# Use for headless tests / regression smoke / CI runs.
export PYTHONPATH=$PYTHONPATH:. && SPARMVET_PERSONA=qa ./.venv/bin/python -m shiny run app/src/main.py --port 8001
```

## Persona capability matrix (updated ADR-052, 2026-05-01)

| Persona | T3 audit | Blueprint | Gallery | Test Lab | Session mgmt | Export bundle | Export graph | Metadata upload | Data ingestion |
|---|---|---|---|---|---|---|---|---|---|
| `developer` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ 25-H | ✅ | ✅ |
| `project-independent` | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⏳ 25-H | ✅ | ✅ |
| `pipeline-exploration-advanced` | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ⏳ 25-H | ✅ | ❌ |
| `pipeline-exploration-simple` | passive only | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| `pipeline-static` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `qa` (test harness) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ 25-H | ✅ | ✅ |

> **passive only**: T1/T2 filter scratchpad — plot updates temporarily, nothing saved, no audit trail. No T3 right sidebar.
> **Test Lab** = renamed from "Dev Studio" (ADR-052, 25-A). Nav pill label change only.
> **Gallery** now enabled for `project-independent` (ADR-052, 25-A config change).
> Export graph (⏳ 25-H) un-deferred — will be built in Phase 25.

> **Export bundle** (`export_bundle_download`) IS live — full ZIP with all plots + T1/T2/T3 data + manifest + Quarto report + filters trace.
> **Export graph** (single-plot quick export — `export_graph_enabled` flag) is **deferred (Phase 22)**: persona matrix and feature flag exist, no UI button wired yet. Tracked as **EXPORT-1** in `tasks.md`.

- compare T2/t3 does not stay on - but is it voluntary if I do not have any T3.
---

# Tests

```bash
# APP
export PYTHONPATH=$PYTHONPATH:. && SPARMVET_PERSONA=developer ./.venv/bin/python -m shiny run app/src/main.py --port 8001
export SPARMVET_PERSONA=developer && ./.venv/bin/python -m shiny run app/src/main.py

export PYTHONPATH=$PYTHONPATH:. && ./.venv/bin/python libs/viz_gallery/tests/debug_gallery_ui_logic.py
```

# Env

[Plotnine version 0.15.3](https://plotnine.org/)

```bash
#python3 -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install polars numpy pyyaml

python3 -m venv .venv && source .venv/bin/activate
source .venv/bin/activate
python3 -m venv .venv && source .venv/bin/activate

# From any other location ...
source /home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/.venv/bin/activate
```

### Launching the ui app

export PYTHONPATH=.:$PYTHONPATH && ./.venv/bin/python -m shiny run app/src/main.py

### Viewing parquet files

./.venv/bin/python -c "import polars as pl; print(pl.read_parquet('tmp/session_anchor_test.parquet').glimpse())"

- export to tsv
./.venv/bin/python -c "import polars as pl; pl.read_parquet('tmp/session_anchor_test.parquet').write_csv('tmp/FULL_EXPORT_debug.tsv', separator='\t')"

To check if the file exists and its shape: ls -lh tmp/*.parquet && ./.venv/bin/python -c "import polars as pl; print(pl.read_parquet('tmp/session_anchor_test.parquet').shape)"

To view the full content (TSV):  ./.venv/bin/python -c "import polars as pl; pl.read_parquet('tmp/session_anchor_test.parquet').write_csv('tmp/USER_FULL_VIEW.tsv', separator='\t')"

### Cleaning and reinstalling python env

1. Clean

```bash
# Kill any lingering Python/Pip processes
pkill -9 python
pkill -9 pip
# Remove the broken venv and all legacy build metadata
rm -rf .venv/
rm -rf libs/*/*.egg-info
rm -rf libs/*/build/
rm -rf libs/*/dist/
```

1. create and insall

```bash
# Create the environment
python3 -m venv .venv

# Upgrade foundational build tools first
./.venv/bin/python -m pip install --upgrade pip setuptools wheel

# Install all libraries in editable mode
./.venv/bin/pip install -e libs/transformer/ \
                       -e libs/viz_factory/ \
                       -e libs/ingestion/ \
                       -e libs/connector/ \
                       -e libs/utils/ \
                       -e libs/generator_utils/
```

1. Control

``` bash
# Check if the package is importable and pointing to the correct physical path
./.venv/bin/python -c "import transformer; print(f'Success: {transformer.__file__}')"

# Run the automated suite to verify all 21+ actions
./.venv/bin/python libs/transformer/tests/transformer_integrity_suite.py
```

### Killing python process running in the environment

```bash
# This shows all python processes running from your .venv
ps aux | grep .venv

# To kill all python processes in one go (be careful if you have other apps running)
pkill -f python
```

If the IDE Agent is reporting "stuck terminals," it might be a socket or lock file in the Antigravity config directory.

Check for Locks: Look in ~/.config/Antigravity/ for any .lock or .socket files that might be lingering from a crashed session.

Clean tmp/: Since we are starting the "Triple-Threat" recipe, manually wipe your local tmp/ directory to ensure no old file-locks exist:

```bash
cd .config/Antigravity 
# Find all files ending in .lock in the config directory
find ~/.config/Antigravity -name "*.lock"

# Alternatively, check for files with .tmp extension
find ~/.config/Antigravity -name "*.tmp"

#rm -rf ./tmp/*
```

## Preparing prompt context for AI : repomix

```bash
DATE_LOG=$(date +%Y-%m-%d)
cd /home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/EVE_WORK/daily/$DATE_LOG

bash /home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/EVE_WORK/scr/SPARMVET_GEM_context.sh
```

## Testing wrangling and assembly from manifest

```bash
./.venv/bin/python libs/transformer/tests/assembler_debug.py \
  --manifest [PATH_TO_MANIFEST] \
  --data [PATH_TO_ASSETS_DIR] \
  --output [PATH_TO_RESULT]


./.venv/bin/python libs/transformer/tests/assembler_debug.py \
  --manifest config/manifests/pipelines/Abromics_Resistence_pipeline.yaml
```

## Creating manifests from data

For a single file

./.venv/bin/python ./assets/scripts/SF_create_manifest.py \
  --data ./assets/ref_data/Virulence_genes_APEC/Virulence_genes_APEC.tsv \
  --output tmp/EVE_manifest.yaml

```

For many files in a directory 

```bash
# Update the command 
./.venv/bin/python ./assets/scripts/create_manifest.py \
  --data ./assets/ref_data/Virulence_genes_APEC/Virulence_genes_APEC.tsv \
  --output tmp/EVE_manifest.yaml
```

## Testing manifests

- virulence finder - reference data

```bash
./.venv/bin/python ./libs/transformer/tests/test_wrangler.py \
  --data ./assets/ref_data/Virulence_genes_APEC/Virulence_genes_APEC.tsv \
  --manifest ./assets/ref_data/Virulence_genes_APEC/Virulence_genes_APEC_manifest.yaml \
  --output tmp/EVE_TEST.tsv
```

```bash
./.venv/bin/python ./libs/transformer/tests/test_wrangler.py \
  --data ./assets/test_data/2_VIGAS-P/VIGAS_VirulenceFinder/VIGAS_VirulenceFinder_test.tsv \
  --manifest ./config/manifests/VIGAS-P/VIGAS_VirulenceFinder.yaml \
  --output tmp/EVE_TEST.tsv
```

## Gettin logs - if seems to hang

ls -la /home/evezeyl/.config/Antigravity/logs/

- check the directory then
 tail -f /home/evezeyl/.config/Antigravity/logs/$(date)*/rendererPerf.log

# REPMIX extracting info

cd ./EVE_WORK/reference/
distrobox enter repomix-env --name repomix-env --no-tty -- repomix --include "plotnine/geoms/*.py,plotnine/stats/*.py,plotnine/scales/*.py,plotnine/themes/*.py,plotnine/facets/*.py,plotnine/coords/*.py,plotnine/positions/*.py" --output plotnine_api_context.md

# The Distinction: Indexing vs. Reading

to use `.aiignore` (embedding) to save your tokens while keeping the agent fully functional.

| **Action**               | **Controlled by .aiignore?** | **Token Cost**     | **When it happens**                  |
| ------------------------ | ---------------------------- | ------------------ | ------------------------------------ |
| **Embedding (Indexing)** | **YES**                      | Background/Storage | Proactively, to "learn" the project. |
| **Direct Reading**       | **NO**                       | Active Context     | Only when you say "Read this file."  |
| **Writing (Output)**     | **NO**                       | Generation         | When the agent creates code or logs. |


## Test command reference

Here are all the commands you need:

### Quick (pytest — unit tests, ~2s, run before every commit)

Safe baseline — skips pre-existing broken libs (`generator_utils`, `utils`, reactive shell stubs):

```bash
PYTHONPATH=. ./.venv/bin/python -m pytest \
  app/tests/test_filter_operators.py \
  libs/connector/tests/ \
  libs/viz_factory/tests/test_deco2_components.py \
  -q
```

Expected: **90/90 pass**.

> **Do NOT use** `PYTHONPATH=. ./.venv/bin/python -m pytest libs/ app/tests/ -q` — this hits broken libs (`generator_utils/tests/test_sdk.py`, `utils/tests/test_config_loader.py`) and reports spurious failures unrelated to your changes.

### Playwright smoke tests (headless browser, ~35s)

Requires `SPARMVET_PERSONA=qa` (all flags ON, ghost_save OFF for determinism):

```bash
PYTHONPATH=. SPARMVET_PERSONA=qa ./.venv/bin/python -m pytest app/tests/test_shiny_smoke.py -v
```

Expected: **10 pass, 2 skip** (persona-gated Gallery tests skipped for non-developer personas — this is correct behaviour).

What the smoke suite covers:
- T1 Startup: app loads, no Python traceback, project loads (dynamic_tabs renders)
- T2 Persona masking: sidebar nav renders, Gallery visible for `qa`/`developer`
- T3 Filter pipeline: filter form renders, add row (year>2000), apply, reset
- T4 Data preview: grid renders

### App import check

```bash
python -c "from app.src.main import app; print('OK')"
```

### Long (integrity suites — full PNG / parquet artefact rendering)

**viz_factory** (renders every `*_test.yaml` to PNG):

```bash
PYTHONPATH=. ./.venv/bin/python libs/viz_factory/tests/viz_factory_integrity_suite.py \
  --output_dir tmp/viz_factory/
```

**transformer** (runs every action's manifest+TSV through the wrangler/assembler):

```bash
PYTHONPATH=. ./.venv/bin/python libs/transformer/tests/transformer_integrity_suite.py \
  --output_dir tmp/transformer/
```

**Single-component dev runners** (when iterating on one action/component):

```bash
# viz_factory: render one component's manifest
PYTHONPATH=. ./.venv/bin/python libs/viz_factory/tests/debug_runner.py \
  libs/viz_factory/tests/test_data/{component}_test.yaml \
  --output_dir tmp/viz_factory/

# transformer: run one action's manifest through the assembler
PYTHONPATH=. ./.venv/bin/python libs/transformer/tests/debug_assembler.py \
  --manifest libs/transformer/tests/data/{action}_manifest.yaml
```

### App + headless UI behaviour

```bash
# Headless home_theater behaviour (renders sidebars + plots without browser)
PYTHONPATH=. ./.venv/bin/python app/tests/debug_home_theater.py

# Session ghost flow
PYTHONPATH=. ./.venv/bin/python app/tests/debug_session_flow.py
```

### Demo-readiness check (one-liner)

Runs unit baseline + app import + Playwright smoke in sequence:

```bash
PYTHONPATH=. ./.venv/bin/python -m pytest \
  app/tests/test_filter_operators.py \
  libs/connector/tests/ \
  libs/viz_factory/tests/test_deco2_components.py \
  -q && \
PYTHONPATH=. ./.venv/bin/python -c "from app.src.main import app; print('app import: OK')" && \
PYTHONPATH=. SPARMVET_PERSONA=qa ./.venv/bin/python -m pytest app/tests/test_shiny_smoke.py -q

```

If all three succeed → safe to push.

