"""
@deps
provides: function:load_manifest, function:tier1_key, function:tier2_key, function:manifest_fileset_hash, function:project_keys, class:LoadedManifest, class:ProjectKeys
consumes: libs/utils/src/utils/config_loader.py
consumed_by: app/modules/orchestrator.py, app/modules/session_manager.py, app/src/server.py, app/tests/test_cache_keys.py
doc: .claude/knowledge/architecture_decisions.md#adr-089, docs/foundations/reproducibility_hash_schema.qmd
@end_deps

Cache chain keys (ADR-089), headless, no Shiny.

Every stored stage has a key made from its own inputs and the key of the stage before it:

    tier1_key = hash(engine version, resolved manifest minus downstream-only parts, data_batch_hash)
    tier2_key = hash(tier1_key, the join's tier2 steps)

so a change anywhere upstream reaches every stage after it, and nothing is missed.

Fail-safe rule: the Tier 1 material is the resolved manifest WITHOUT a short list of known
downstream parts. A new or unknown section is therefore part of Tier 1 automatically, so a
wrong guess can only cause an extra rebuild, never a stale result.

Two manifest hashes, two purposes:
  - manifest_sha256 (provenance, session key, export): hash of the FILE SET (entry file and
    every included file). Independently verifiable with sha256sum.
  - the cache keys use the RESOLVED content, so comments, spacing and how the manifest is
    split into files do not force a rebuild.

The loaded manifest is kept in memory and revalidated against the content of its files.
"""
import hashlib
import json
import os
import threading
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path
from typing import Any, Iterable, Optional, Union

from utils.config_loader import ConfigManager

# Bump when an action's behaviour or these key rules change: it invalidates every stored stage.
ENGINE_CACHE_VERSION = "1"

# Top-level manifest sections that only matter after Tier 2 (the plots). Everything else,
# including sections this code has never heard of, belongs to Tier 1 (fail-safe rule).
_DOWNSTREAM_TOP_LEVEL = ("info", "analysis_groups", "plot_defaults", "plots")


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_hash(obj: Any) -> str:
    """SHA256 of a JSON form with sorted keys: independent of key order and YAML formatting."""
    return hash_text(json.dumps(obj, sort_keys=True, default=str, separators=(",", ":")))


def _package_version(name: str) -> str:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return "unknown"


def engine_fingerprint() -> str:
    """The code that produces the data: cache version constant plus the installed engine versions."""
    return f"{ENGINE_CACHE_VERSION}|polars={_package_version('polars')}|transformer={_package_version('transformer')}"


# ---------------------------------------------------------------------------
# Which parts of the resolved manifest belong to which stage
# ---------------------------------------------------------------------------


def tier1_material(raw: dict) -> dict:
    """The resolved manifest without the downstream-only parts (fail-safe: unknown parts stay in)."""
    material = {k: v for k, v in raw.items() if k not in _DOWNSTREAM_TOP_LEVEL}
    joins = material.get("join_manifests")
    if isinstance(joins, dict):
        stripped = {}
        for join_id, spec in joins.items():
            recipe = spec.get("recipe") if isinstance(spec, dict) else None
            if isinstance(recipe, dict) and "tier2" in recipe:
                spec = {**spec, "recipe": {k: v for k, v in recipe.items() if k != "tier2"}}
            stripped[join_id] = spec
        material["join_manifests"] = stripped
    return material


def tier2_steps(raw: dict, join_id: str) -> list:
    """The tier2 steps of one join's recipe (empty when there are none: T2 equals T1)."""
    joins = raw.get("join_manifests")
    spec = joins.get(join_id) if isinstance(joins, dict) else None
    recipe = spec.get("recipe") if isinstance(spec, dict) else None
    steps = recipe.get("tier2") if isinstance(recipe, dict) else None
    return list(steps) if steps else []


# ---------------------------------------------------------------------------
# Keys
# ---------------------------------------------------------------------------


def tier1_key(material_hash: str, data_batch_hash: str) -> str:
    return hash_text("\n".join(["tier1", engine_fingerprint(), material_hash, data_batch_hash]))


def tier2_key(tier1_key_value: str, steps: list) -> str:
    return hash_text("\n".join(["tier2", tier1_key_value, canonical_hash(steps)]))


def manifest_fileset_hash(files: Iterable[Union[str, Path]], base_dir: Union[str, Path]) -> str:
    """Hash of the manifest file set: `relative_path:sha256` lines, sorted, joined, hashed again."""
    base = os.path.abspath(str(base_dir))
    lines = []
    for f in files:
        absolute = os.path.abspath(str(f))
        try:
            digest = hashlib.sha256(Path(absolute).read_bytes()).hexdigest()
        except OSError:
            digest = "MISSING"
        lines.append(f"{os.path.relpath(absolute, base)}:{digest}")
    return hash_text("\n".join(sorted(lines)))


def files_signature(files: Iterable[Union[str, Path]]) -> tuple:
    """(path, content digest) per file, to see whether anything changed on disk.

    Content, not size and modification time: an edit that keeps the size and lands in the same
    clock tick (version 1 -> version 2) would otherwise be missed. Manifest files are small, so
    reading them is cheap. (The data files are large and are hashed once per session instead.)
    """
    signature = []
    for f in files:
        try:
            digest = hashlib.sha256(Path(f).read_bytes()).hexdigest()
        except OSError:
            digest = "MISSING"
        signature.append((str(f), digest))
    return tuple(signature)


# ---------------------------------------------------------------------------
# The loaded manifest, kept in memory and revalidated against the disk
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LoadedManifest:
    path: str
    config: ConfigManager
    files: tuple
    signature: tuple
    manifest_sha256: str  # file-set hash (provenance)
    material_hash: str    # canonical hash of the Tier 1 material (cache keys)

    @property
    def raw(self) -> dict:
        return self.config.raw_config


@dataclass(frozen=True)
class ProjectKeys:
    """Everything the stored stages of one project depend on, computed once per session."""

    manifest_sha256: str   # file-set hash (provenance, session key)
    data_batch_hash: str   # content hash of the source data files
    tier1_key: str         # chained key of the Tier 1 parquet


def project_keys(loaded: "LoadedManifest", data_batch_hash: str) -> ProjectKeys:
    return ProjectKeys(
        manifest_sha256=loaded.manifest_sha256,
        data_batch_hash=data_batch_hash,
        tier1_key=tier1_key(loaded.material_hash, data_batch_hash),
    )


_CACHE: dict[str, LoadedManifest] = {}
_LOCK = threading.Lock()


def load_manifest(path: Union[str, Path]) -> LoadedManifest:
    """Load a manifest, or return the one in memory when none of its files changed on disk.

    A failed load (a manifest error) is never cached.
    """
    key = os.path.abspath(str(path))
    with _LOCK:
        entry = _CACHE.get(key)
        if entry is not None and files_signature(entry.files) == entry.signature:
            return entry
        config = ConfigManager(key)
        files = tuple(os.path.abspath(f) for f in config.loaded_files)
        loaded = LoadedManifest(
            path=key,
            config=config,
            files=files,
            signature=files_signature(files),
            manifest_sha256=manifest_fileset_hash(files, os.path.dirname(key)),
            material_hash=canonical_hash(tier1_material(config.raw_config)),
        )
        _CACHE[key] = loaded
        return loaded


def clear_manifest_cache() -> None:
    with _LOCK:
        _CACHE.clear()


def peek_manifest(path: Union[str, Path]) -> Optional[LoadedManifest]:
    """The manifest in memory for this path, without loading or validating it (for tests)."""
    return _CACHE.get(os.path.abspath(str(path)))
