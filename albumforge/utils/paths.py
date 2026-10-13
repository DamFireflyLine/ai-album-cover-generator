"""Path resolution helpers. All app paths go through here — no bare
`Path("output")` scattered around the codebase, because that breaks the
moment someone runs the app from a different working directory.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]


def repo_root() -> Path:
    return _REPO_ROOT


def models_dir() -> Path:
    return _REPO_ROOT / "models"


def output_dir() -> Path:
    return _REPO_ROOT / "output"


def cache_dir() -> Path:
    return _REPO_ROOT / "cache"


def extensions_dir() -> Path:
    return _REPO_ROOT / "albumforge" / "extensions"


def ensure_runtime_dirs() -> None:
    """Create the runtime dirs if missing. Called once at bootstrap."""
    for path in (models_dir(), output_dir(), cache_dir()):
        path.mkdir(parents=True, exist_ok=True)


def is_frozen() -> bool:
    """True when running from a PyInstaller bundle."""
    return getattr(sys, "frozen", False)