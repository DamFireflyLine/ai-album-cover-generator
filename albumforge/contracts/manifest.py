"""Extension manifest — the `extension.toml` schema.

Every extension folder must contain an `extension.toml`. The loader parses
it, verifies the module hash, and hands the manifest to the registry.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class ExtensionManifest(BaseModel):
    """Validated representation of an `extension.toml`."""

    model_config = {"frozen": True}

    id: str = Field(pattern=r"^[a-z][a-z0-9_]{2,40}$")
    name: str
    version: str = Field(pattern=r"^\d+\.\d+\.\d+$")
    author: str
    description: str = ""
    entrypoint: str = Field(description="Module path, e.g. 'albumforge.extensions.sdxl_renderer'")
    provides: list[str] = Field(default_factory=list)
    """Contract kinds this extension satisfies: renderer | prompt | postprocess | exporter."""
    requires_host: str = ">=0.4.0"
    module_sha256: str = Field(description="SHA-256 of the entrypoint module file.")
    enabled_by_default: bool = True

    @field_validator("provides")
    @classmethod
    def _known_kinds(cls, value: list[str]) -> list[str]:
        allowed = {"renderer", "prompt", "postprocess", "exporter"}
        unknown = set(value) - allowed
        if unknown:
            raise ValueError(f"unknown contract kinds: {sorted(unknown)}")
        return value

    def module_path(self) -> Path:
        """Resolve the entrypoint module path relative to the repo root."""
        rel = self.entrypoint.replace(".", "/") + ".py"
        return Path(__file__).resolve().parents[2] / rel