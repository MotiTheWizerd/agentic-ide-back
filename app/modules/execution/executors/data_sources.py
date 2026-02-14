"""Data source executors — pure data pass-through, no API calls."""

from __future__ import annotations

from app.modules.execution.config.scene_prompts import compose_scene_prompt
from app.modules.execution.models import NodeExecutionContext, NodeOutput


async def consistent_character(ctx: NodeExecutionContext) -> NodeOutput:
    """Return character persona data from node fields."""
    description = ctx.node_data.get("characterDescription") or ""
    name = ctx.node_data.get("characterName") or ""

    if not description:
        return NodeOutput(error="No character selected")

    return NodeOutput(
        text=description,
        persona_description=description,
        persona_name=name,
    )


async def scene_builder(ctx: NodeExecutionContext) -> NodeOutput:
    """Compose a scene prompt from the node's dropdown selections."""
    scene_text = compose_scene_prompt(ctx.node_data)
    return NodeOutput(text=scene_text)
