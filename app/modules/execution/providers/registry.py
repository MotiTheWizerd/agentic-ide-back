"""Provider registry — lazy factory for text provider clients."""

from __future__ import annotations

import os
from typing import Union

from app.modules.execution.providers.claude import ClaudeProvider
from app.modules.execution.providers.openai_compat import OpenAICompatProvider

TextProviderInstance = Union[OpenAICompatProvider, ClaudeProvider]

_providers: dict[str, TextProviderInstance] = {}


def _init_providers() -> None:
    if _providers:
        return

    _providers["mistral"] = OpenAICompatProvider(
        base_url="https://api.mistral.ai/v1",
        api_key=os.environ.get("MISTRAL_API_KEY", ""),
    )
    _providers["glm"] = OpenAICompatProvider(
        base_url="https://api.z.ai/api/coding/paas/v4",
        api_key=os.environ.get("GLM_API_KEY", ""),
    )
    _providers["openrouter"] = OpenAICompatProvider(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPENROUTER_API_KEY", ""),
    )
    _providers["huggingface"] = OpenAICompatProvider(
        base_url="https://router.huggingface.co/v1",
        api_key=os.environ.get("HF_API_KEY", ""),
    )
    _providers["claude"] = ClaudeProvider()


def get_text_provider(provider_id: str) -> TextProviderInstance:
    _init_providers()
    provider = _providers.get(provider_id)
    if not provider:
        raise ValueError(f"Unknown text provider: {provider_id}")
    return provider
