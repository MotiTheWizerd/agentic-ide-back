"""Translation prompt template."""

from __future__ import annotations


def build_translate_messages(text: str, language: str) -> list[dict]:
    return [
        {
            "role": "system",
            "content": "You are a professional translator.",
        },
        {
            "role": "user",
            "content": (
                f"Translate the following text to {language}.\n"
                "Output ONLY the translation, nothing else.\n"
                "Keep under 2500 characters.\n\n"
                f"{text}"
            ),
        },
    ]
