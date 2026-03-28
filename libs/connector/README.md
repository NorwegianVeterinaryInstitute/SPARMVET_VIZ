# Connector Library

## Purpose
The "Bridge" layer that manages network communications, authentication, and API integrations to external platforms (e.g., Use Galaxy, IRIDA) to fetch remote datasets into the application's local scope.

## Key Components
- `GalaxyConnector (galaxy_connector.py)`: Handles BioBlend API calls, session mapping, and dataset extraction from Galaxy instances.

## I/O Summary
- **Input**: API Credentials, server URLs, and unique target file identifiers (e.g., History IDs).
- **Output**: Downloaded raw data files placed into the local application state for subsequent ingestion.

## Installation (Editable Mode)
According to the workspace standard, this library must be installed locally via:
```bash
pip install -e ./libs/connector
```
