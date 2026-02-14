"""Prompt enhancement templates."""

from __future__ import annotations

_SYSTEM = "You are an expert prompt engineer specializing in AI image generation prompts."

_WITH_NOTES = """{system}
Take the following prompt and enhance it according to the instructions provided.

## ORIGINAL PROMPT:
{text}

## ENHANCEMENT INSTRUCTIONS:
{notes}

Apply the enhancement instructions to improve the original prompt.
Output ONLY the enhanced prompt. Keep under 2500 characters."""

_WITHOUT_NOTES = """{system}
Take this simple prompt and transform it into a detailed, rich prompt suitable for AI image generation.
Add vivid details about composition, lighting, style, mood, and atmosphere.
Output ONLY the enhanced prompt. Keep under 2500 characters.

{text}"""


def build_enhance_messages(text: str, notes: str | None = None) -> list[dict]:
    if notes:
        content = _WITH_NOTES.format(system=_SYSTEM, text=text, notes=notes)
    else:
        content = _WITHOUT_NOTES.format(system=_SYSTEM, text=text)

    return [
        {"role": "system", "content": _SYSTEM},
        {"role": "user", "content": content},
    ]
