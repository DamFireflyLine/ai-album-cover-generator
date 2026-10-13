"""Prompt-enhancer contract.

Enhancers rewrite the user's prompt before it reaches a renderer. They run
in a chain, ordered by `priority` (lower runs first). A typical chain is:
genre classifier -> style injector -> negative-prompt builder.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class PromptEnhancerContract(Protocol):
    enhancer_id: str
    """Stable identifier, e.g. `genre_style_injector`."""

    priority: int
    """Lower runs earlier in the chain. Host sorts ascending."""

    def enhance(self, prompt: str, *, genre: str | None = None) -> str:
        """Return the rewritten prompt. Must be pure — no I/O, no state."""
        ...