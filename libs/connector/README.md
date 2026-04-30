# Connector Library

> **Status:** Phase 23 implementation pending (ADR-048). The current library contains a dev-mode LocalConnector only. Galaxy and IRIDA connectors are designed but not yet implemented.

## Purpose

The "Bridge" layer that resolves the active deployment profile and, for API-based deployments (IRIDA), fetches remote data into local scope before the rest of the app reads it. For filesystem-based deployments (Galaxy-mounted dirs, local PC, server), the connector is a no-op after path resolution.

## Architecture (ADR-048)

One Docker image + one deployment profile YAML = one running SPARMVET instance. The Bootloader resolves the active profile through a 4-level chain (env var → `~/.sparmvet/` → `/etc/sparmvet/` → dev fallback). The connector library provides the type-specific adapter for each `deployment_type`.

## Planned Key Components (Phase 23-B)

- `BaseConnector (base.py)`: Abstract interface — `resolve_paths()`, `fetch_data()`, `get_manifest_path()`.
- `FilesystemConnector (filesystem.py)`: Reads profile locations directly. No-op `fetch_data()`. Covers Galaxy-mounted dirs, local PC, server.
- `IridaConnector (irida.py)`: OAuth2 fetch via `SPARMVET_IRIDA_TOKEN` → local cache → paths like filesystem.
- `GalaxyConnector (galaxy.py)`: Thin wrapper; maps Galaxy job dir env vars to profile locations.

## Current Dev Fallback

The active dev fallback lives in `config/connectors/local/local_connector.yaml` and is loaded by `bootloader.py` when no profile env var or system profile is found.

## Deployment Profile Schema

See `config/connectors/templates/connector_template.yaml` and `docs/workflows/connector.qmd` for the full ADR-048 schema.

## Installation (Editable Mode)

```bash
pip install -e ./libs/connector
```
