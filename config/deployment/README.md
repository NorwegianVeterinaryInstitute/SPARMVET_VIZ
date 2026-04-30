# config/deployment/ — Deployment Profiles (ADR-048)

Deployment profiles describe **how SPARMVET is deployed into a specific environment**: where data lives, which manifest loads at startup, which persona is active by default, and what type of system it is.

One Docker image + one deployment profile = one running SPARMVET instance.

## Directory Layout

```
config/deployment/
├── local/
│   └── local_profile.yaml      ← Dev fallback (resolution level 4)
└── templates/
    └── connector_template.yaml ← Full schema reference with inline comments
```

## Profile Resolution Order

The Bootloader finds the active profile at startup (first match wins):

| Level | Source | Who uses it |
|---|---|---|
| 1 | `SPARMVET_PROFILE` env var | Galaxy XML wrapper, IRIDA container, Docker Compose, systemd |
| 2 | `~/.sparmvet/profile.yaml` | Local PC scientist / admin |
| 3 | `/etc/sparmvet/profile.yaml` | Institutional server (sysadmin) |
| 4 | `config/deployment/local/local_profile.yaml` | Developer running from the repo |

The active level is logged at startup: `[Bootloader] Profile resolved at level N (label): path`

## Creating a New Profile

Copy `templates/connector_template.yaml`, fill in your paths and deployment type, and place it at the appropriate level. The five required location keys are:

```yaml
locations:
  raw_data:      "..."   # read-only input files
  manifests:     "..."   # YAML manifests and recipes
  curated_data:  "..."   # Parquet caches (app writes here)
  user_sessions: "..."   # exports, saves, T3 artifacts (user-writable)
  gallery:       "..."   # gallery assets (read-only)
```

All location paths are relative to `project_root` (if set), otherwise relative to CWD.

## Deployment Types

| `deployment_type` | Adapter class | Notes |
|---|---|---|
| `filesystem` (default) | `FilesystemConnector` | Local PC, server, Galaxy-mounted dirs |
| `galaxy` | `GalaxyConnector` | Falls back to `_GALAXY_JOB_HOME_DIR` env var if `project_root` absent |
| `irida` | `IridaConnector` | Token via `SPARMVET_IRIDA_TOKEN` env var; fetch implementation Phase 23-D |

## Full Schema Reference

See `templates/connector_template.yaml` (inline comments) or `docs/workflows/connector.qmd` (narrative).
