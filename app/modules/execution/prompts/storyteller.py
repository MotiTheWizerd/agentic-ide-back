"""Storyteller prompt template."""

from __future__ import annotations


def build_storyteller_messages(text: str, tags: str | None = None) -> list[dict]:
    user_content = (
        "You are a wildly creative storyteller and wordsmith.\n\n"
        "RULES:\n"
        "- Every time you receive the same concept, create a DIFFERENT interpretation\n"
        "- Be bold and surprising. Subvert expectations\n"
        "- Focus on words, emotions, atmosphere, character — NOT visual descriptions\n"
        "- Use rich literary language: metaphors, rhythm, sensory details\n"
        "- Format as clean markdown (## headings, paragraphs, *italics*, no **bold**)\n"
        "- Output ONLY the story. Keep under 2500 characters\n\n"
        f"CONCEPT: {text}"
    )
    if tags:
        user_content += f"\nSTYLE TAGS: {tags}"

    return [
        {
            "role": "system",
            "content": "You are a wildly creative storyteller and wordsmith.",
        },
        {"role": "user", "content": user_content},
    ]
