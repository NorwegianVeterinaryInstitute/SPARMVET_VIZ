# Pipeline development Notes


## 2026-03-07

### Exporting the excel sheet to tsv

- Extracting to tsv before creating the fake dataset 
```bash
# root project only
ROOT="/home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ"
source $ROOT/.venv/bin/activate

DATA_IN_DIR="/home/evezeyl/Documents/Insync/gdrive/OBSWORK/10_ACTIVE_PROJECTS/02_OH4S_34096/07_Data_Row/dashboard_raw_test_data/1_test_data_ST22"
TESTDATA_OUT="/home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/assets/test_data"
SCRIPT_DIR="/home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/assets/scripts"

cd $TESTDATA_OUT
# WARNING here I only output in the raw data directory
$SCRIPT_DIR/parse_pipeline_excel.py  --h
$SCRIPT_DIR/parse_pipeline_excel.py --excel_file $DATA_IN_DIR/Galaxy_report_APEC_test.xlsx \
--standardized_pkey "sample_id" --config $DATA_IN_DIR/extractor_config.yaml --out_dir $DATA_IN_DIR/tsv

# same for metadata 
$SCRIPT_DIR/parse_pipeline_excel.py --excel_file $DATA_IN_DIR/Metadata_APEC_test_260129.xlsx \
--standardized_pkey "sample_id" --config $DATA_IN_DIR/extractor_config_metadata.yaml --out_dir $DATA_IN_DIR/tsv
```

### Helper to write data contract for pipelines feks

- run the helper to write the data contract 
```bash
$SCRIPT_DIR/create_test_data.py --h
$SCRIPT_DIR/create_test_data.py --data_dir $DATA_IN_DIR/tsv \
--data_files Summary.tsv Detailed_Summary.tsv ResFinder.tsv PlasmidFinder.tsv MLST_results.tsv FastP.tsv Bracken.tsv Quast.tsv Quality_metrics.tsv \
--metadata_file $DATA_IN_DIR/tsv/260129_metadata.tsv \
--primary_key_data sample_id --primary_key_metadata sample_id --out_dir 1_Abromics_general_pipeline

``` 
Maual editting the countries so I can have a bit more diverse data for countries

Now testing the script to help prefil a manifest template 

```bash
cd /home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/assets/template_manifests
DUMMYDATA_DIR="/home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/assets/test_data/1_Abromics_general_pipeline"

$SCRIPT_DIR/create_manifest.py --h

$SCRIPT_DIR/create_manifest.py --data_dir $DUMMYDATA_DIR \
--data_files test_data_Summary_20260307_105756.tsv test_data_Detailed_Summary_20260307_105756.tsv \
test_data_ResFinder_20260307_105756.tsv test_data_PlasmidFinder_20260307_105756.tsv \
test_data_MLST_results_20260307_105756.tsv test_data_FastP_20260307_105756.tsv \
test_data_Bracken_20260307_105756.tsv test_data_Quast_20260307_105756.tsv \
test_data_Quality_metrics_20260307_105756.tsv \
--metadata_file  $DUMMYDATA_DIR/test_metadata_20260307_105756.tsv \
--primary_key_data sample_id --primary_key_metadata sample_id \
--out_file 1_Abromics_general_pipeline.yaml
```



## 2026-03-08

- dummy data is ready to done
- first pipeline schema partially imlemented, testing loader
- developer cheatsheet done -> documentation

Activating dev environment

```bash
ROOT="/home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ"
source $ROOT/.venv/bin/activate
export PYTHONPATH=$ROOT:$PYTHONPATH
```

test config loader 

```bash
SCRIPTDIR="$ROOT/libs/utils/tests"
YAML="$ROOT/config/manifests/pipelines/1_Abromics_general_pipeline.yaml"

python $SCRIPTDIR/test_config_loader.py -h
python $SCRIPTDIR/test_config_loader.py --yaml $YAML
```
OK 

test ingestion 

```bash
SCRIPTDIR="$ROOT/libs/ingestion/tests"
YAML="$ROOT/config/manifests/pipelines/1_Abromics_general_pipeline.yaml"
DATADIR="$ROOT/assets/test_data/1_test_data_ST22_dummy"

python $SCRIPTDIR/test_ingestion.py --help
python $SCRIPTDIR/test_ingestion.py --yaml $YAML --data $DATADIR

```

test wrangling

```bash
SCRIPTDIR="$ROOT/libs/transformer/tests"
YAML="$ROOT/config/manifests/pipelines/1_Abromics_general_pipeline.yaml"
DATADIR="$ROOT/assets/test_data/1_test_data_ST22_dummy"

python $SCRIPTDIR/test_wrangler.py --help
python $SCRIPTDIR/test_wrangler.py --yaml $YAML --data $DATADIR
```