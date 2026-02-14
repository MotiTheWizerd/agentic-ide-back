"""Text provider protocol."""

from __future__ import annotations

from typing import Protocol


class TextProvider(Protocol):
    async def chat(
        self,
        messages: list[dict],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2500,
    ) -> str: ...
