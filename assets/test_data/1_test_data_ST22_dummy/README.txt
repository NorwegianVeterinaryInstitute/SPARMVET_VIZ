simple dummy dataset created from 1_test_data_ST22
ROOT="SPARMVET_VIZ"
source $ROOT/.venv/bin/activate

DATA_IN_DIR="../dashboard_raw_test_data/1_test_data_ST22"
TESTDATA_OUT="SPARMVET_VIZ/assets/test_data"
SCRIPT_DIR="SPARMVET_VIZ/assets/scripts"

cd $TESTDATA_OUT
# WARNING here I only output in the raw data directory
$SCRIPT_DIR/parse_pipeline_excel.py  --h
$SCRIPT_DIR/parse_pipeline_excel.py --excel_file $DATA_IN_DIR/Galaxy_report_APEC_test.xlsx \
--standardized_pkey "sample_id" --config $DATA_IN_DIR/extractor_config.yaml --out_dir $DATA_IN_DIR/tsv

# same for metadata
$SCRIPT_DIR/parse_pipeline_excel.py --excel_file $DATA_IN_DIR/Metadata_APEC_test_260129.xlsx \
--standardized_pkey "sample_id" --config $DATA_IN_DIR/extractor_config_metadata.yaml --out_dir $DATA_IN_DIR/tsv
```

- run the helper to write the data contract
```bash
$SCRIPT_DIR/create_test_data.py --h
$SCRIPT_DIR/create_test_data.py --data_dir $DATA_IN_DIR/tsv \
--data_files Summary.tsv Detailed_Summary.tsv ResFinder.tsv PlasmidFinder.tsv MLST_results.tsv FastP.tsv Bracken.tsv Quast.tsv Quality_metrics.tsv \
--metadata_file $DATA_IN_DIR/tsv/260129_metadata.tsv \
--primary_key_data sample_id --primary_key_metadata sample_id --out_dir 1_test_data_ST22_dummy

```
Maual editting the countries so I can have a bit more diverse data for countries
