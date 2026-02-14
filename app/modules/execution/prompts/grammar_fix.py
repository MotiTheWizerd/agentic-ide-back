"""Grammar fix prompt template."""

from __future__ import annotations


def build_grammar_fix_messages(text: str, style: str | None = None) -> list[dict]:
    user_content = (
        "You are a proofreader. Fix all grammar, spelling, and punctuation errors.\n"
    )
    if style:
        user_content += f"After fixing, lightly adjust tone to be more {style}.\n"

    user_content += (
        "Output ONLY the corrected text. Preserve original structure and length.\n\n"
        f"{text}"
    )

    return [
        {
            "role": "system",
            "content": "You are a professional proofreader and editor.",
        },
        {"role": "user", "content": user_content},
    ]
