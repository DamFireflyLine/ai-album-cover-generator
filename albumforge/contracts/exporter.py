"""Exporter contract.

Exporters write a finished image to disk in a specific format, optionally
embedding metadata (prompt, seed, model, generation params) into the file.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, runtime_checkable

from PIL import Image


@dataclass(slots=True, frozen=True)
class ExportContext:
    prompt: str
    seed: int
    backend_id: str
    extra: dict[str, object]


@runtime_checkable
class ExporterContract(Protocol):
    format_id: str
    """e.g. `png`, `jpeg`, `webp`, `psd`."""

    def export(self, image: Image.Image, dest: Path, ctx: ExportContext) -> Path:
        """Write `image` to `dest`. Return the actual path written."""
        ...