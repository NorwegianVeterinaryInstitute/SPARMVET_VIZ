
```bash
#python3 -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install polars numpy pyyaml

python3 -m venv .venv && source .venv/bin/activate
source .venv/bin/activate
python3 -m venv .venv && source .venv/bin/activate

# From any other location ...
source /home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/.venv/bin/activate
```

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
