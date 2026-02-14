"""Executor registry — maps node_type string to its async executor function."""

from __future__ import annotations

from app.modules.execution.executors.base import ExecutorFn
from app.modules.execution.executors.data_sources import (
    consistent_character,
    scene_builder,
)
from app.modules.execution.executors.image_description import image_describer
from app.modules.execution.executors.image_generation import image_generator
from app.modules.execution.executors.output import text_output
from app.modules.execution.executors.text_processing import (
    compressor,
    grammar_fix,
    initial_prompt,
    prompt_enhancer,
    story_teller,
    translator,
)

EXECUTORS: dict[str, ExecutorFn] = {
    # Data sources
    "consistentCharacter": consistent_character,
    "sceneBuilder": scene_builder,
    # Text processing
    "initialPrompt": initial_prompt,
    "promptEnhancer": prompt_enhancer,
    "translator": translator,
    "storyTeller": story_teller,
    "grammarFix": grammar_fix,
    "compressor": compressor,
    # Output
    "textOutput": text_output,
    # Image
    "imageDescriber": image_describer,
    "imageGenerator": image_generator,
}


def register_executor(node_type: str, fn: ExecutorFn) -> None:
    EXECUTORS[node_type] = fn


def get_executor(node_type: str) -> ExecutorFn | None:
    return EXECUTORS.get(node_type)
