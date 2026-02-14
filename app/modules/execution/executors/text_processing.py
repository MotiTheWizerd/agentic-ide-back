"""Text processing executors — each calls an LLM via provider clients."""

from __future__ import annotations

import time

from app.modules.execution.executors.utils import (
    LANGUAGE_NAMES,
    extract_personas,
    merge_input_text,
)
from app.modules.execution.models import NodeExecutionContext, NodeOutput
from app.modules.execution.prompts.compress import build_compress_messages
from app.modules.execution.prompts.enhance import build_enhance_messages
from app.modules.execution.prompts.grammar_fix import build_grammar_fix_messages
from app.modules.execution.prompts.inject_persona import build_inject_persona_messages
from app.modules.execution.prompts.storyteller import build_storyteller_messages
from app.modules.execution.prompts.translate import build_translate_messages
from app.modules.execution.providers.registry import get_text_provider

COMPRESSION_THRESHOLD = 2500


async def _inject_personas_if_present(
    text: str,
    ctx: NodeExecutionContext,
) -> str:
    """If adapter inputs contain personas, inject them into the text."""
    personas = extract_personas(ctx.adapter_inputs)
    if not personas:
        return text

    messages = build_inject_persona_messages(personas, text)
    provider = get_text_provider(ctx.provider_id)
    result = await provider.chat(
        messages=messages,
        model=ctx.model,
        temperature=ctx.temperature,
        max_tokens=2500,
    )
    return result


async def initial_prompt(ctx: NodeExecutionContext) -> NodeOutput:
    """Read node text field, optionally inject personas."""
    start = time.perf_counter()
    text = ctx.node_data.get("text") or ""

    if not text:
        text = merge_input_text(ctx.text_inputs)

    text = await _inject_personas_if_present(text, ctx)
    duration = (time.perf_counter() - start) * 1000

    return NodeOutput(text=text, injected_prompt=text, duration_ms=duration)


async def prompt_enhancer(ctx: NodeExecutionContext) -> NodeOutput:
    """Enhance a prompt, optionally inject personas."""
    start = time.perf_counter()
    text = merge_input_text(ctx.text_inputs)
    notes = ctx.node_data.get("notes") or None

    messages = build_enhance_messages(text, notes)
    provider = get_text_provider(ctx.provider_id)
    enhanced = await provider.chat(
        messages=messages,
        model=ctx.model,
        temperature=ctx.temperature,
        max_tokens=2500,
    )

    enhanced = await _inject_personas_if_present(enhanced, ctx)
    duration = (time.perf_counter() - start) * 1000

    return NodeOutput(text=enhanced, duration_ms=duration)


async def translator(ctx: NodeExecutionContext) -> NodeOutput:
    """Translate upstream text to the selected language."""
    start = time.perf_counter()
    text = merge_input_text(ctx.text_inputs)
    lang_code = ctx.node_data.get("language") or ""

    if not lang_code:
        # No language selected → pass-through
        duration = (time.perf_counter() - start) * 1000
        return NodeOutput(text=text, duration_ms=duration)

    language = LANGUAGE_NAMES.get(lang_code, lang_code)
    messages = build_translate_messages(text, language)
    provider = get_text_provider(ctx.provider_id)
    translated = await provider.chat(
        messages=messages,
        model=ctx.model,
        temperature=ctx.temperature,
        max_tokens=2500,
    )
    duration = (time.perf_counter() - start) * 1000

    return NodeOutput(text=translated, duration_ms=duration)


async def story_teller(ctx: NodeExecutionContext) -> NodeOutput:
    """Generate a creative narrative."""
    start = time.perf_counter()
    text = merge_input_text(ctx.text_inputs) or ctx.node_data.get("idea") or ""
    tags = ctx.node_data.get("tags") or None

    messages = build_storyteller_messages(text, tags)
    provider = get_text_provider(ctx.provider_id)
    story = await provider.chat(
        messages=messages,
        model=ctx.model,
        temperature=ctx.temperature,
        max_tokens=2500,
    )

    story = await _inject_personas_if_present(story, ctx)
    duration = (time.perf_counter() - start) * 1000

    return NodeOutput(text=story, duration_ms=duration)


async def grammar_fix(ctx: NodeExecutionContext) -> NodeOutput:
    """Fix grammar, spelling, and punctuation."""
    start = time.perf_counter()
    text = merge_input_text(ctx.text_inputs)
    style = ctx.node_data.get("style") or None

    messages = build_grammar_fix_messages(text, style)
    provider = get_text_provider(ctx.provider_id)
    fixed = await provider.chat(
        messages=messages,
        model=ctx.model,
        temperature=ctx.temperature,
        max_tokens=2500,
    )
    duration = (time.perf_counter() - start) * 1000

    return NodeOutput(text=fixed, duration_ms=duration)


async def compressor(ctx: NodeExecutionContext) -> NodeOutput:
    """Compress text if it exceeds the threshold."""
    start = time.perf_counter()
    text = merge_input_text(ctx.text_inputs)

    if len(text) <= COMPRESSION_THRESHOLD:
        duration = (time.perf_counter() - start) * 1000
        return NodeOutput(text=text, duration_ms=duration)

    messages = build_compress_messages(text)
    provider = get_text_provider(ctx.provider_id)
    compressed = await provider.chat(
        messages=messages,
        model=ctx.model,
        temperature=ctx.temperature,
        max_tokens=2500,
    )
    duration = (time.perf_counter() - start) * 1000

    return NodeOutput(text=compressed, duration_ms=duration)
