"""Scene attribute prompt blocks for the sceneBuilder executor.

Each key maps a dropdown field to a dict of value → prompt text.
The ``compose_scene_prompt`` function joins selected blocks.
"""

from __future__ import annotations

SCENE_PROMPT_BLOCKS: dict[str, dict[str, str]] = {
    "imageStyle": {
        "photorealistic": "Photorealistic style with lifelike detail and natural lighting",
        "anime": "Anime art style with vibrant colors and expressive features",
        "oil-painting": "Oil painting style with rich textures and visible brushstrokes",
        "watercolor": "Watercolor style with soft edges and translucent washes",
        "digital-art": "Digital art style with clean lines and vivid colors",
        "comic-book": "Comic book style with bold outlines and dynamic poses",
        "3d-render": "3D rendered style with realistic materials and lighting",
        "pixel-art": "Pixel art style with retro aesthetic and limited palette",
        "pencil-sketch": "Pencil sketch style with detailed shading and line work",
        "cinematic": "Cinematic style with dramatic lighting and film-quality composition",
    },
    "lighting": {
        "natural": "Natural ambient lighting from the environment",
        "dramatic": "Dramatic lighting with strong contrasts and deep shadows",
        "soft": "Soft diffused lighting with gentle shadows",
        "neon": "Neon lighting with vibrant glowing colors",
        "golden-hour": "Golden hour lighting with warm amber tones",
        "moonlight": "Cool moonlight illumination with blue-silver tones",
        "studio": "Professional studio lighting with controlled highlights",
        "backlit": "Backlit scene with silhouette effects and rim lighting",
    },
    "timeOfDay": {
        "dawn": "Early dawn with soft pink and orange sky",
        "morning": "Bright morning light with clear skies",
        "noon": "Midday with overhead sun and minimal shadows",
        "afternoon": "Warm afternoon light with lengthening shadows",
        "sunset": "Sunset with rich orange and purple hues across the sky",
        "dusk": "Dusk with fading light and deep blue atmosphere",
        "night": "Nighttime setting with dark skies and artificial or moonlight",
    },
    "weather": {
        "clear": "Clear weather with blue skies",
        "cloudy": "Overcast sky with diffused light",
        "rainy": "Rainy atmosphere with wet surfaces and falling rain",
        "snowy": "Snow-covered scene with falling snowflakes",
        "foggy": "Foggy atmosphere with limited visibility and mystery",
        "stormy": "Stormy weather with dark clouds and dramatic atmosphere",
    },
    "cameraAngle": {
        "eye-level": "Shot from eye level, natural perspective",
        "low-angle": "Low angle shot looking upward, conveying power and grandeur",
        "high-angle": "High angle shot looking downward, showing scope and context",
        "birds-eye": "Bird's eye view from directly above",
        "dutch-angle": "Tilted dutch angle creating tension and unease",
        "close-up": "Close-up shot with tight framing on the subject",
        "wide-shot": "Wide establishing shot showing the full scene",
    },
    "cameraLens": {
        "standard": "Standard 50mm lens with natural perspective",
        "wide-angle": "Wide-angle lens capturing expansive scenes with slight distortion",
        "telephoto": "Telephoto lens with compressed perspective and shallow depth of field",
        "macro": "Macro lens with extreme close-up detail",
        "fisheye": "Fisheye lens with extreme wide-angle barrel distortion",
        "tilt-shift": "Tilt-shift lens creating miniature effect with selective focus",
    },
    "mood": {
        "peaceful": "Peaceful and serene atmosphere",
        "mysterious": "Mysterious and enigmatic mood with hidden elements",
        "joyful": "Bright and joyful energy with warmth",
        "melancholic": "Melancholic and contemplative mood with muted tones",
        "epic": "Epic and grandiose atmosphere with awe-inspiring scale",
        "horror": "Dark horror atmosphere with unsettling elements",
        "romantic": "Romantic and dreamy mood with soft atmosphere",
        "futuristic": "Futuristic and sci-fi mood with advanced technology elements",
    },
}

SCENE_KEYS = ("imageStyle", "lighting", "timeOfDay", "weather", "cameraAngle", "cameraLens", "mood")


def compose_scene_prompt(node_data: dict) -> str:
    """Join prompt blocks for all selected scene attributes."""
    parts: list[str] = []
    for key in SCENE_KEYS:
        value = node_data.get(key)
        if value and key in SCENE_PROMPT_BLOCKS:
            text = SCENE_PROMPT_BLOCKS[key].get(value)
            if text:
                parts.append(text)
    return "\n\n".join(parts)
