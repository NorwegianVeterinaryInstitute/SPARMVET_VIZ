



```bash
#python3 -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install polars numpy pyyaml

python3 -m venv .venv && source .venv/bin/activate
source .venv/bin/activate
python3 -m venv .venv && source .venv/bin/activate

```

## Preparing prompt context for AI : repomix
```bash
bash /home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/distrobox/scripts/SPARMVET_VIZ_GEM_context.sh
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
