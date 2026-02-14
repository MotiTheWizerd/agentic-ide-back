"""Image description executor — sends an uploaded image to a vision LLM."""

from __future__ import annotations

import logging
import os
import re
import time

from anthropic import AsyncAnthropic

from app.modules.execution.models import NodeExecutionContext, NodeOutput

logger = logging.getLogger(__name__)

_client: AsyncAnthropic | None = None

DEFAULT_VISION_MODEL = "claude-sonnet-4-20250514"

SYSTEM_PROMPT = (
    "You are an expert image analyst. Describe the image in rich, "
    "precise detail — covering subjects, composition, colors, mood, "
    "lighting, style, and any text visible. Your description will be "
    "used as a prompt to recreate the image, so be thorough."
)


def _get_client() -> AsyncAnthropic:
    global _client
    if _client is None:
        _client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
    return _client


def _parse_data_uri(data_uri: str) -> tuple[str, str]:
    """Extract (media_type, base64_data) from a data URI.

    Accepts both ``data:image/png;base64,AAAA...`` and raw base64 strings.
    """
    match = re.match(r"data:([^;]+);base64,(.+)", data_uri, re.DOTALL)
    if match:
        return match.group(1), match.group(2)
    return "image/png", data_uri


async def image_describer(ctx: NodeExecutionContext) -> NodeOutput:
    """Describe an uploaded image using Claude vision."""
    start = time.perf_counter()

    image_value = ctx.node_data.get("image") or ""
    if not image_value:
        return NodeOutput(error="No image provided for description")

    media_type, base64_data = _parse_data_uri(image_value)
    model = ctx.model or DEFAULT_VISION_MODEL

    client = _get_client()
    response = await client.messages.create(
        model=model,
        max_tokens=2500,
        temperature=ctx.temperature,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": base64_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": "Describe this image in detail.",
                    },
                ],
            },
        ],
    )

    description = response.content[0].text
    duration = (time.perf_counter() - start) * 1000

    return NodeOutput(
        text=description,
        image=image_value,
        duration_ms=duration,
    )
