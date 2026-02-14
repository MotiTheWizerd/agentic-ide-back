"""Output executor — merges upstream text, no API call."""

from __future__ import annotations

from app.modules.execution.executors.utils import merge_input_text
from app.modules.execution.models import NodeExecutionContext, NodeOutput


async def text_output(ctx: NodeExecutionContext) -> NodeOutput:
    """Merge all upstream text inputs into a single output."""
    merged = merge_input_text(ctx.text_inputs)
    return NodeOutput(text=merged)
