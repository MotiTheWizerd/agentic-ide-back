"""Image provider protocol."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class ImageResult:
    """Result of an image generation call."""

    image_base64: str
    content_type: str = "image/png"
    prompt_used: str = ""


class ImageProvider(Protocol):
    async def generate(
        self,
        prompt: str,
        model: str = "",
        aspect_ratio: str = "1:1",
        output_format: str = "png",
        width: int | None = None,
        height: int | None = None,
    ) -> ImageResult: ...
