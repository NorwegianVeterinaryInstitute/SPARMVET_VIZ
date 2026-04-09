# Connector Library

## Purpose

The "Bridge" layer that manages network communications, authentication, and API integrations to external platforms (e.g., Use Galaxy, IRIDA) to fetch remote datasets into the application's local scope.

## Key Components

- `GalaxyConnector (galaxy_connector.py)`: Handles BioBlend API calls, session mapping, and dataset extraction from Galaxy instances.
- **Path Authority**: This library manages the HW/System connection registry. It resolves physical locations (Locations 1-5) defined in `config/connectors/`, decoupling hardware paths from UI configurations.

## I/O Summary

- **Input**: API Credentials, server URLs, and unique target file identifiers (e.g., History IDs) OR Local Configuration paths defined in `config/connectors/`.
- **Output**: Downloaded raw data files or resolved local paths placed into the application state for ingestion.

## Installation (Editable Mode)

According to the workspace standard, this library must be installed locally via:

```bash
pip install -e ./libs/connector
```
