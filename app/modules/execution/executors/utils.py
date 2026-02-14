"""Shared executor utilities."""

from __future__ import annotations

from app.modules.execution.models import NodeOutput

LANGUAGE_NAMES: dict[str, str] = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese",
    "ar": "Arabic",
    "hi": "Hindi",
    "tr": "Turkish",
    "pl": "Polish",
    "nl": "Dutch",
    "sv": "Swedish",
    "da": "Danish",
    "no": "Norwegian",
    "fi": "Finnish",
    "cs": "Czech",
    "el": "Greek",
    "he": "Hebrew",
    "th": "Thai",
    "vi": "Vietnamese",
    "id": "Indonesian",
    "ms": "Malay",
    "uk": "Ukrainian",
    "ro": "Romanian",
}


def merge_input_text(inputs: list[NodeOutput]) -> str:
    """Join upstream output text fields with double newlines.

    Collects ``text``, ``replace_prompt``, ``injected_prompt``, and
    ``persona_description`` from each input, skipping ``None`` values.
    """
    parts: list[str] = []
    for inp in inputs:
        for field in ("text", "replace_prompt", "injected_prompt", "persona_description"):
            val = getattr(inp, field, None)
            if val:
                parts.append(val)
    return "\n\n".join(parts)


def extract_personas(adapter_inputs: list[NodeOutput]) -> list[dict[str, str]]:
    """Extract persona entries from adapter inputs.

    Returns a list of ``{"name": ..., "description": ...}`` dicts for
    inputs that carry a ``persona_description``.
    """
    personas: list[dict[str, str]] = []
    for inp in adapter_inputs:
        if inp.persona_description:
            personas.append({
                "name": inp.persona_name or "Unknown",
                "description": inp.persona_description,
            })
    return personas
