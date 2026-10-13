"""Logging setup shared by host, extensions, and tests.

Library code must never call `print()`. Get a logger with
`get_logger(__name__)` and use it. The host configures the root logger once
at bootstrap; extensions inherit the config automatically.
"""

from __future__ import annotations

import logging
import sys

_CONFIGURED = False

_FORMAT = "%(asctime)s %(levelname)-7s %(name)s: %(message)s"
_DATEFMT = "%H:%M:%S"


def configure_root(level: str = "info") -> None:
    """Configure the root logger exactly once. Idempotent."""
    global _CONFIGURED
    if _CONFIGURED:
        return
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(_FORMAT, datefmt=_DATEFMT))
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level.upper())
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Return a namespaced logger. Safe to call before configure_root()."""
    return logging.getLogger(name)