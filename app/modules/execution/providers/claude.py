"""Claude provider using the Anthropic SDK."""

from __future__ import annotations

import logging
import os

from anthropic import AsyncAnthropic

logger = logging.getLogger(__name__)


class ClaudeProvider:
    def __init__(self) -> None:
        self._client = AsyncAnthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY", ""),
        )

    async def chat(
        self,
        messages: list[dict],
        model: str = "claude-sonnet-4-20250514",
        temperature: float = 0.7,
        max_tokens: int = 2500,
    ) -> str:
        # Anthropic separates system from user/assistant messages
        system_msg = ""
        chat_messages: list[dict] = []
        for msg in messages:
            if msg["role"] == "system":
                system_msg = msg["content"]
            else:
                chat_messages.append(msg)

        logger.debug("Claude chat: model=%s", model)

        kwargs: dict = dict(
            model=model,
            messages=chat_messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        if system_msg:
            kwargs["system"] = system_msg

        response = await self._client.messages.create(**kwargs)
        return response.content[0].text
