"""The registry — the single source of truth for what extensions exist.

The host queries the registry by contract kind and id. Nothing else in the
codebase is allowed to import a concrete extension module. If you need a
renderer, ask the registry. If you need a specific renderer, ask the
registry for it by `backend_id` and handle the `KeyError`.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from albumforge.contracts import (
    ExporterContract,
    PostProcessorContract,
    PromptEnhancerContract,
    RendererContract,
)
from albumforge.utils.logging import get_logger

_log = get_logger(__name__)

_KIND_TO_CONTRACT = {
    "renderer": RendererContract,
    "prompt": PromptEnhancerContract,
    "postprocess": PostProcessorContract,
    "exporter": ExporterContract,
}


class Registry:
    """In-memory registry of active extension instances."""

    def __init__(self) -> None:
        self._by_kind: dict[str, dict[str, Any]] = defaultdict(dict)

    def register(self, kind: str, instance: Any) -> None:
        """Register `instance` under `kind`. Raises on unknown kind or dup id."""
        contract = _KIND_TO_CONTRACT.get(kind)
        if contract is None:
            raise ValueError(f"unknown extension kind: {kind!r}")
        if not isinstance(instance, contract):
            raise TypeError(f"{type(instance).__name__} does not satisfy {contract.__name__}")

        ident = _identity_of(kind, instance)
        bucket = self._by_kind[kind]
        if ident in bucket:
            raise ValueError(f"duplicate {kind} id: {ident!r}")
        bucket[ident] = instance
        _log.debug("registered %s %r", kind, ident)

    def get(self, kind: str, ident: str) -> Any:
        try:
            return self._by_kind[kind][ident]
        except KeyError as exc:
            raise KeyError(f"no {kind} registered with id {ident!r}") from exc

    def all_of(self, kind: str) -> list[Any]:
        return list(self._by_kind[kind].values())

    def renderers(self) -> list[RendererContract]:
        return self.all_of("renderer")  # type: ignore[return-value]

    def prompt_chain(self) -> list[PromptEnhancerContract]:
        """Enhancers sorted by ascending priority, ready to run in order."""
        chain = self.all_of("prompt")
        return sorted(chain, key=lambda e: e.priority)  # type: ignore[attr-defined,return-value]

    def postprocess_chain(self) -> list[PostProcessorContract]:
        chain = self.all_of("postprocess")
        return sorted(chain, key=lambda p: p.priority)  # type: ignore[attr-defined,return-value]

    def exporters(self) -> list[ExporterContract]:
        return self.all_of("exporter")  # type: ignore[return-value]

    def summary(self) -> dict[str, list[str]]:
        return {kind: sorted(bucket) for kind, bucket in self._by_kind.items()}


def _identity_of(kind: str, instance: Any) -> str:
    attr = {
        "renderer": "backend_id",
        "prompt": "enhancer_id",
        "postprocess": "processor_id",
        "exporter": "format_id",
    }[kind]
    ident = getattr(instance, attr, None)
    if not isinstance(ident, str) or not ident:
        raise ValueError(f"{type(instance).__name__} has no valid {attr}")
    return ident