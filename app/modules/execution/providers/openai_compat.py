"""OpenAI-compatible provider client for Mistral, GLM, OpenRouter, HuggingFace."""

from __future__ import annotations

import logging

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)


class OpenAICompatProvider:
    def __init__(self, base_url: str, api_key: str, default_model: str = "") -> None:
        self._client = AsyncOpenAI(base_url=base_url, api_key=api_key)
        self._default_model = default_model

    async def chat(
        self,
        messages: list[dict],
        model: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2500,
    ) -> str:
        resolved_model = model or self._default_model
        logger.debug("OpenAI-compat chat: model=%s", resolved_model)

        response = await self._client.chat.completions.create(
            model=resolved_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""
