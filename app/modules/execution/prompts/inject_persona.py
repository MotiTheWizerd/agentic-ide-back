"""Persona injection prompt template."""

from __future__ import annotations


def build_inject_persona_messages(
    personas: list[dict[str, str]],
    prompt_text: str,
) -> list[dict]:
    characters_block = ""
    for p in personas:
        characters_block += f"### {p['name']}\n{p['description']}\n\n"

    user_content = (
        "You are an expert prompt engineer specializing in AI image generation prompts.\n"
        "Your task is to inject specific character appearance details into an existing prompt.\n\n"
        "## CHARACTERS:\n"
        f"{characters_block}"
        "## ORIGINAL PROMPT:\n"
        f"{prompt_text}\n\n"
        "## YOUR TASK:\n"
        "Rewrite the original prompt so that each named character's physical appearance\n"
        "is injected where they are referenced.\n"
        "Rules:\n"
        "1. KEEP everything from original (scene, setting, clothing, pose, action...)\n"
        "2. REPLACE/ENRICH character references with physical traits\n"
        "3. Unmatched character names stay as-is\n"
        "4. Generic \"a woman\" with single character → replace with traits\n"
        "5. MERGE naturally into sentences\n"
        "6. Do NOT add clothing from CHARACTER descriptions — only physical traits\n"
        "7. Use traits exactly as described\n"
        "8. If no character reference, add characters naturally into the scene\n"
        "Output ONLY the rewritten prompt. Keep under 2500 characters."
    )

    return [
        {
            "role": "system",
            "content": "You are an expert prompt engineer specializing in AI image generation prompts.",
        },
        {"role": "user", "content": user_content},
    ]
