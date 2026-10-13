"""Shared contracts between the host and extensions.

Every extension implements one or more of these. The host depends on the
contracts, never on concrete extensions. Keep this package free of any
imports from `albumforge.extensions` — that would create a cycle and defeat
the whole plugin-host design.
"""

from albumforge.contracts.renderer import RendererContract, RenderRequest, RenderResult
from albumforge.contracts.prompt import PromptEnhancerContract
from albumforge.contracts.postprocess import PostProcessorContract
from albumforge.contracts.exporter import ExporterContract
from albumforge.contracts.manifest import ExtensionManifest

__all__ = [
    "RendererContract",
    "RenderRequest",
    "RenderResult",
    "PromptEnhancerContract",
    "PostProcessorContract",
    "ExporterContract",
    "ExtensionManifest",
]