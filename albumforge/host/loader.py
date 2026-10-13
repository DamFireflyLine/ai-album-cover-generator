"""Extension loader.

Walks the extensions directory, parses each `extension.toml`, verifies the
entrypoint module's SHA-256 against the manifest, imports the module, and
calls its `activate(registry)` function. Failures are isolated: one broken
extension never takes down the host. They're logged and counted.
"""

from __future__ import annotations

import hashlib
import importlib
import importlib.util
from pathlib import Path

try:
    import tomllib  # type: ignore[import-not-found]
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef]

from pydantic import ValidationError

from albumforge.contracts.manifest import ExtensionManifest
from albumforge.host.registry import Registry
from albumforge.utils.logging import get_logger

_log = get_logger(__name__)

_MANIFEST_NAME = "extension.toml"
_SKIP_PREFIXES = ("_", ".")


class ExtensionLoader:
    def __init__(self, registry: Registry, *, disabled: set[str] | None = None) -> None:
        self._registry = registry
        self._disabled = disabled or set()

    def load_all(self, root: Path) -> tuple[int, int]:
        """Return (loaded_count, failed_count). Never raises."""
        loaded = failed = 0
        if not root.is_dir():
            _log.warning("extensions dir missing: %s", root)
            return 0, 0

        for entry in sorted(root.iterdir()):
            if not entry.is_dir() or entry.name.startswith(_SKIP_PREFIXES):
                continue
            if entry.name in self._disabled:
                _log.info("extension %s disabled by config", entry.name)
                continue
            try:
                self._load_one(entry)
                loaded += 1
            except Exception as exc:  # noqa: BLE001 — isolation is the point
                failed += 1
                _log.error("failed to load extension %s: %s", entry.name, exc)
        return loaded, failed

    def _load_one(self, folder: Path) -> None:
        manifest_path = folder / _MANIFEST_NAME
        if not manifest_path.is_file():
            raise FileNotFoundError(f"no {_MANIFEST_NAME} in {folder}")

        with manifest_path.open("rb") as fh:
            raw = tomllib.load(fh)
        try:
            manifest = ExtensionManifest.model_validate(raw)
        except ValidationError as exc:
            raise ValueError(f"invalid manifest in {folder.name}: {exc}") from exc

        if not manifest.enabled_by_default and manifest.id in self._disabled:
            return

        module_file = manifest.module_path()
        if not module_file.is_file():
            raise FileNotFoundError(f"entrypoint module not found: {module_file}")
        actual = _sha256(module_file)
        if actual != manifest.module_sha256:
            raise ValueError(
                f"hash mismatch for {manifest.id}: manifest says "
                f"{manifest.module_sha256[:12]}…, file is {actual[:12]}…"
            )

        module = importlib.import_module(manifest.entrypoint)
        activate = getattr(module, "activate", None)
        if not callable(activate):
            raise AttributeError(f"{manifest.entrypoint} has no callable activate()")
        activate(self._registry)
        _log.info("activated extension %s v%s", manifest.id, manifest.version)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
</｜｜DSML｜｜ parameter>