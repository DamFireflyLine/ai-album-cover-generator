"""Renderer contract — the core extension point.

A renderer turns a `RenderRequest` into a `RenderResult`. The host never
calls a concrete renderer by name; it asks the registry for the renderer
matching the requested backend id.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol, runtime_checkable

from PIL import Image


@dataclass(slots=True, frozen=True)
class RenderRequest:
    """Immutable description of one render job.

    `prompt` and `negative_prompt` are already enhanced by the active
    prompt-enhancer chain before they reach a renderer. `seed` of -1 means
    "pick a random seed and report it back in the result."
    """

    prompt: str
    negative_prompt: str = ""
    width: int = 1024
    height: int = 1024
    steps: int = 28
    guidance: float = 7.0
    seed: int = -1
    sampler: str = "dpmpp_2m"
    extra: dict[str, object] = field(default_factory=dict)


@dataclass(slots=True)
class RenderResult:
    """What a renderer hands back. `image` is always present on success."""

    image: Image.Image
    seed_used: int
    backend_id: str
    elapsed_ms: float
    metadata: dict[str, object] = field(default_factory=dict)


@runtime_checkable
class RendererContract(Protocol):
    """Implement this to add a diffusion backend to AlbumForge."""

    backend_id: str
    """Stable identifier, e.g. `sdxl`. Referenced from config and the CLI."""

    def is_available(self) -> bool:
        """Return False if required weights or accelerators are missing."""
        ...

    def render(self, request: RenderRequest) -> RenderResult:
        """Render one image. May raise `RenderError` on unrecoverable failure."""
        ...

    def unload(self) -> None:
        """Free VRAM/RAM. Called when the user switches backends."""
        ...


class RenderError(RuntimeError):
    """Raised by a renderer when a job cannot complete."""