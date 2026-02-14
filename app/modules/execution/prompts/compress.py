"""Text compression prompt template."""

from __future__ import annotations


def build_compress_messages(text: str) -> list[dict]:
    return [
        {
            "role": "system",
            "content": "You are a text compression specialist.",
        },
        {
            "role": "user",
            "content": (
                "Compress the following text to be shorter while preserving ALL information.\n"
                "Output ONLY the compressed text.\n\n"
                f"{text}"
            ),
        },
    ]
