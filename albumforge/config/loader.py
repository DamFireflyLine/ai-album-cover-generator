"""Config loading: defaults.toml merged with the user override file.

Precedence: user config > defaults.toml > hardcoded fallback. The merge is
a deep merge for tables, a replace for scalars and arrays. Arrays are never
concatenated — if you want to extend a list, do it in the user config.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

try:
    import tomllib  # type: ignore[import-not-found]
except ModuleNotFoundError:  # Python < 3.11
    import tomli as tomllib  # type: ignore[no-redef]

import tomli_w

from albumforge.utils.logging import get_logger

_log = get_logger(__name__)

_DEFAULTS_PATH = Path(__file__).with_name("defaults.toml")


def _user_config_path() -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "AlbumForge" / "config.toml"


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Merge `override` onto `base`. Tables merge recursively; everything else replaces."""
    out = dict(base)
    for key, value in override.items():
        if key in out and isinstance(out[key], dict) and isinstance(value, dict):
            out[key] = _deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def load_config() -> dict[str, Any]:
    """Return the effective config dict. Never raises on a missing user file."""
    with _DEFAULTS_PATH.open("rb") as fh:
        config = tomllib.load(fh)

    user_path = _user_config_path()
    if user_path.exists():
        try:
            with user_path.open("rb") as fh:
                user = tomllib.load(fh)
            config = _deep_merge(config, user)
            _log.info("loaded user config from %s", user_path)
        except (OSError, tomllib.TOMLDecodeError) as exc:
            _log.warning("user config at %s is unreadable (%s); using defaults", user_path, exc)

    return config


def save_user_config(config: dict[str, Any]) -> None:
    """Persist `config` to the user config path, creating parent dirs."""
    path = _user_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as fh:
        tomli_w.dump(config, fh)
    _log.info("wrote user config to %s", path)