"""Post-processor contract.

Post-processors run on the rendered image before export. Crop, upscale,
color-grade, watermark, add a vinyl-sleeve border — anything that mutates
the pixels. They run in `priority` order, same convention as enhancers.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from PIL import Image


@runtime_checkable
class PostProcessorContract(Protocol):
    processor_id: str
    priority: int

    def process(self, image: Image.Image, *, context: dict[str, object]) -> Image.Image:
        """Return the processed image. Must not mutate the input in place."""
        ...