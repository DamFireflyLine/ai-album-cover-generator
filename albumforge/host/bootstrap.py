"""Application bootstrap.

Order matters: configure logging, load config, ensure runtime dirs, load
extensions into the registry, then hand control to the Qt event loop. Any
failure before the event loop exits with a non-zero code and a logged
reason — no silent half-starts.
"""

from __future__ import annotations

import sys

from albumforge.config.loader import load_config
from albumforge.host.registry import Registry
from albumforge.host.loader import ExtensionLoader
from albumforge.utils.logging import configure_root, get_logger
from albumforge.utils.paths import ensure_runtime_dirs, extensions_dir

_log = get_logger(__name__)


def bootstrap(argv: list[str]) -> int:
    config = load_config()
    configure_root(config["app"]["log_level"])
    _log.info("AlbumForge starting, argv=%r", argv)

    ensure_runtime_dirs()

    registry = Registry()
    loader = ExtensionLoader(registry, disabled=set(config["plugins"]["disabled"]))
    loaded, failed = loader.load_all(extensions_dir())
    _log.info("extensions: %d loaded, %d failed", loaded, failed)

    if "--headless" in argv:
        from albumforge.host.headless import run_headless

        return run_headless(config, registry)

    from albumforge.host.window import run_gui

    return run_gui(config, registry)


if __name__ == "__main__":
    raise SystemExit(bootstrap(sys.argv[1:]))