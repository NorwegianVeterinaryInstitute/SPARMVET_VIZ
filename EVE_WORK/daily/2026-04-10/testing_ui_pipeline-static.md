# Testing UI with the simple persona : pipeline-static

## Command starting testing

```bash
# 1. Environment variables set the UI Profile and Backend
# 2. PYTHONPATH ensures all modular libraries and the app package are discovered
# 3. Running via 'shiny run' to activate the reactive dashboard


# Clear old bytecode to force a fresh import of the fixed server.py
find app/ -name "__pycache__" -type d -exec rm -rf {} +

# Run the app with the same environment variables
SPARMVET_PERSONA=pipeline-static \
SPARMVET_CONNECTOR=local \
PYTHONPATH=.:libs/ingestion/src:libs/transformer/src:libs/utils/src:libs/viz_factory/src \
./.venv/bin/python -m shiny run app/src/main.py
```
