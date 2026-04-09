# Connector Library

## Purpose

The "Bridge" layer that manages network communications, authentication, and API integrations to external platforms (e.g., Use Galaxy, IRIDA) to fetch remote datasets into the application's local scope.

## Key Components

- `GalaxyConnector (galaxy_connector.py)`: Handles BioBlend API calls, session mapping, and dataset extraction from Galaxy instances.
- `LocalConnector (adapter_A..D.py)`: Resolves local system paths via normalized adapters and identifies hardware locations per ADR-031.
- `PathAuthority (local_connector.yaml)`: Configuration anchor that resolves the 5 mandatory system locations (Raw, Manifests, User, etc.).

## I/O Summary

- **Input**: API Credentials, server URLs, and unique target file identifiers (e.g., History IDs) OR Local Configuration paths defined in `config/connectors/`.
- **Output**: Downloaded raw data files or resolved local paths placed into the application state for ingestion.

## Installation (Editable Mode)

According to the workspace standard, this library must be installed locally via:

```bash
pip install -e ./libs/connector
```
