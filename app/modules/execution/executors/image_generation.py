"""Image generation executor — calls an image provider to generate images."""

from __future__ import annotations

import time

from app.modules.execution.executors.utils import merge_input_text
from app.modules.execution.models import NodeExecutionContext, NodeOutput
from app.modules.execution.providers.image_registry import get_image_provider


async def image_generator(ctx: NodeExecutionContext) -> NodeOutput:
    """Generate an image from upstream prompt text or the node's prompt field."""
    start = time.perf_counter()

    prompt = merge_input_text(ctx.text_inputs)
    if not prompt:
        prompt = ctx.node_data.get("prompt") or ""

    if not prompt:
        return NodeOutput(error="No prompt provided for image generation")

    width = ctx.node_data.get("width") or None
    height = ctx.node_data.get("height") or None

    provider = get_image_provider(ctx.provider_id)
    result = await provider.generate(
        prompt=prompt,
        model=ctx.model,
        width=int(width) if width else None,
        height=int(height) if height else None,
    )

    duration = (time.perf_counter() - start) * 1000
    image_data = f"data:{result.content_type};base64,{result.image_base64}"

    return NodeOutput(
        text=prompt,
        image=image_data,
        duration_ms=duration,
    )
