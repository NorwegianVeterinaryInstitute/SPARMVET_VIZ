"""
Unit tests for libs/connector — ADR-048 deployment connector library.

Run from project root:
    pytest libs/connector/tests/test_connectors.py -v

All tests use in-memory profile dicts — no filesystem access required.
"""
import os
import pytest
from pathlib import Path

from connector import (
    BaseConnector,
    FilesystemConnector,
    GalaxyConnector,
    IridaConnector,
    get_connector,
)

# ── Shared fixtures ────────────────────────────────────────────────────────────

MINIMAL_LOCATIONS = {
    "raw_data": "inputs/",
    "manifests": "manifests/",
    "curated_data": "parquet/",
    "user_sessions": "sessions/",
    "gallery": "gallery/",
}

FS_PROFILE = {
    "deployment_type": "filesystem",
    "locations": MINIMAL_LOCATIONS,
}

FS_PROFILE_WITH_ROOT = {
    "deployment_type": "filesystem",
    "project_root": "/data/pipeline/",
    "default_manifest": "manifests/amr/master.yaml",
    "default_persona": "pipeline-static",
    "deployment_name": "AMR Pipeline",
    "locations": MINIMAL_LOCATIONS,
}

IRIDA_PROFILE = {
    "deployment_type": "irida",
    "irida": {
        "base_url": "https://irida.example.ca",
        "project_id": 42,
        "auth": "oauth2",
        "local_cache": "/tmp/irida_cache/",
    },
    "locations": MINIMAL_LOCATIONS,
}

GALAXY_PROFILE = {
    "deployment_type": "galaxy",
    "locations": MINIMAL_LOCATIONS,
}

GALAXY_PROFILE_WITH_ROOT = {
    "deployment_type": "galaxy",
    "project_root": "/galaxy/job/123/",
    "locations": MINIMAL_LOCATIONS,
}


# ── BaseConnector ──────────────────────────────────────────────────────────────

def test_base_connector_is_abstract():
    with pytest.raises(TypeError):
        BaseConnector({})  # cannot instantiate abstract class


# ── FilesystemConnector ────────────────────────────────────────────────────────

class TestFilesystemConnector:

    def test_resolve_paths_no_root(self):
        c = FilesystemConnector(FS_PROFILE)
        paths = c.resolve_paths()
        assert paths["raw_data"] == Path("inputs")
        assert paths["manifests"] == Path("manifests")

    def test_resolve_paths_with_root(self):
        c = FilesystemConnector(FS_PROFILE_WITH_ROOT)
        paths = c.resolve_paths()
        assert paths["raw_data"] == Path("/data/pipeline/inputs")
        assert paths["manifests"] == Path("/data/pipeline/manifests")

    def test_resolve_paths_absolute_not_prepended(self):
        profile = {
            "project_root": "/root/",
            "locations": {**MINIMAL_LOCATIONS, "raw_data": "/absolute/data/"},
        }
        c = FilesystemConnector(profile)
        paths = c.resolve_paths()
        assert paths["raw_data"] == Path("/absolute/data")
        assert paths["manifests"] == Path("/root/manifests")

    def test_fetch_data_is_noop(self):
        c = FilesystemConnector(FS_PROFILE)
        c.fetch_data()  # must not raise

    def test_get_manifest_path_none_when_absent(self):
        c = FilesystemConnector(FS_PROFILE)
        assert c.get_manifest_path() is None

    def test_get_manifest_path_with_root(self):
        c = FilesystemConnector(FS_PROFILE_WITH_ROOT)
        mpath = c.get_manifest_path()
        assert mpath == Path("/data/pipeline/manifests/amr/master.yaml")

    def test_get_manifest_path_no_root(self):
        profile = {**FS_PROFILE, "default_manifest": "config/manifests/amr.yaml"}
        c = FilesystemConnector(profile)
        assert c.get_manifest_path() == Path("config/manifests/amr.yaml")

    def test_get_manifest_path_absolute(self):
        profile = {**FS_PROFILE, "default_manifest": "/absolute/manifest.yaml"}
        c = FilesystemConnector(profile)
        assert c.get_manifest_path() == Path("/absolute/manifest.yaml")

    def test_get_default_persona(self):
        c = FilesystemConnector(FS_PROFILE_WITH_ROOT)
        assert c.get_default_persona() == "pipeline-static"

    def test_get_default_persona_none(self):
        c = FilesystemConnector(FS_PROFILE)
        assert c.get_default_persona() is None

    def test_get_deployment_name(self):
        c = FilesystemConnector(FS_PROFILE_WITH_ROOT)
        assert c.get_deployment_name() == "AMR Pipeline"

    def test_get_deployment_name_default(self):
        c = FilesystemConnector(FS_PROFILE)
        assert c.get_deployment_name() == "SPARMVET_VIZ"

    def test_get_deployment_type(self):
        c = FilesystemConnector(FS_PROFILE)
        assert c.get_deployment_type() == "filesystem"


# ── GalaxyConnector ────────────────────────────────────────────────────────────

class TestGalaxyConnector:

    def test_resolve_paths_with_root_ignores_env(self, monkeypatch):
        monkeypatch.setenv("_GALAXY_JOB_HOME_DIR", "/env/job/")
        c = GalaxyConnector(GALAXY_PROFILE_WITH_ROOT)
        paths = c.resolve_paths()
        assert paths["raw_data"] == Path("/galaxy/job/123/inputs")

    def test_resolve_paths_env_var_fallback(self, monkeypatch):
        monkeypatch.setenv("_GALAXY_JOB_HOME_DIR", "/env/job/")
        c = GalaxyConnector(GALAXY_PROFILE)
        paths = c.resolve_paths()
        assert paths["raw_data"] == Path("/env/job/inputs")

    def test_resolve_paths_no_root_no_env(self, monkeypatch):
        monkeypatch.delenv("_GALAXY_JOB_HOME_DIR", raising=False)
        monkeypatch.delenv("GALAXY_SLOTS_DIR", raising=False)
        c = GalaxyConnector(GALAXY_PROFILE)
        paths = c.resolve_paths()
        assert paths["raw_data"] == Path("inputs")

    def test_fetch_data_is_noop(self):
        c = GalaxyConnector(GALAXY_PROFILE)
        c.fetch_data()  # must not raise

    def test_is_filesystem_subclass(self):
        assert issubclass(GalaxyConnector, FilesystemConnector)


# ── IridaConnector ─────────────────────────────────────────────────────────────

class TestIridaConnector:

    def test_resolve_paths_uses_local_cache(self):
        c = IridaConnector(IRIDA_PROFILE)
        paths = c.resolve_paths()
        assert paths["raw_data"] == Path("/tmp/irida_cache/inputs")
        assert paths["manifests"] == Path("/tmp/irida_cache/manifests")

    def test_resolve_paths_no_local_cache_falls_back(self):
        profile = {**IRIDA_PROFILE, "irida": {"base_url": "x", "project_id": 1}}
        c = IridaConnector(profile)
        paths = c.resolve_paths()
        assert paths["raw_data"] == Path("inputs")

    def test_fetch_data_raises_env_error_without_token(self, monkeypatch):
        monkeypatch.delenv("SPARMVET_IRIDA_TOKEN", raising=False)
        c = IridaConnector(IRIDA_PROFILE)
        with pytest.raises(EnvironmentError, match="SPARMVET_IRIDA_TOKEN"):
            c.fetch_data()

    def test_fetch_data_raises_value_error_without_irida_block(self, monkeypatch):
        monkeypatch.setenv("SPARMVET_IRIDA_TOKEN", "tok")
        c = IridaConnector({**FS_PROFILE, "deployment_type": "irida"})
        with pytest.raises(ValueError, match="irida"):
            c.fetch_data()

    def test_fetch_data_raises_not_implemented_when_configured(self, monkeypatch):
        monkeypatch.setenv("SPARMVET_IRIDA_TOKEN", "tok")
        c = IridaConnector(IRIDA_PROFILE)
        with pytest.raises(NotImplementedError, match="Phase 23-D"):
            c.fetch_data()

    def test_get_irida_base_url(self):
        c = IridaConnector(IRIDA_PROFILE)
        assert c.get_irida_base_url() == "https://irida.example.ca"

    def test_get_irida_project_id(self):
        c = IridaConnector(IRIDA_PROFILE)
        assert c.get_irida_project_id() == 42

    def test_is_filesystem_subclass(self):
        assert issubclass(IridaConnector, FilesystemConnector)


# ── get_connector factory ──────────────────────────────────────────────────────

class TestGetConnector:

    def test_filesystem_type(self):
        c = get_connector(FS_PROFILE)
        assert isinstance(c, FilesystemConnector)
        assert not isinstance(c, GalaxyConnector)
        assert not isinstance(c, IridaConnector)

    def test_galaxy_type(self):
        c = get_connector(GALAXY_PROFILE)
        assert isinstance(c, GalaxyConnector)

    def test_irida_type(self):
        c = get_connector(IRIDA_PROFILE)
        assert isinstance(c, IridaConnector)

    def test_absent_type_defaults_to_filesystem(self):
        c = get_connector({"locations": MINIMAL_LOCATIONS})
        assert isinstance(c, FilesystemConnector)
        assert not isinstance(c, GalaxyConnector)
