"""Flux image provider (Black Forest Labs via Fireworks AI) — async implementation."""

from __future__ import annotations

import asyncio
import base64
import logging
import os
from math import gcd

import httpx

from app.modules.execution.providers.image_base import ImageResult

logger = logging.getLogger(__name__)

BASE_URL = "https://api.fireworks.ai/inference/v1/workflows"
DEFAULT_MODEL = "flux-kontext-pro"
MAX_POLL_ATTEMPTS = 60
POLL_INTERVAL = 2.0
TERMINAL_STATUSES = {"Error", "Content Moderated", "Request Moderated"}

ASPECT_RATIO_MAP: dict[tuple[int, int], str] = {
    (1024, 1024): "1:1",
    (1024, 768): "4:3",
    (768, 1024): "3:4",
    (1280, 720): "16:9",
    (720, 1280): "9:16",
}


class FluxImageProvider:
    """Async Flux image provider using the Fireworks AI workflow API."""

    def __init__(self, api_key: str = "") -> None:
        self._api_key = api_key or os.environ.get("FIREWORKS_API_KEY", "")
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0, read=60.0),
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
        )

    async def generate(
        self,
        prompt: str,
        model: str = "",
        aspect_ratio: str = "1:1",
        output_format: str = "png",
        width: int | None = None,
        height: int | None = None,
    ) -> ImageResult:
        resolved_model = model or DEFAULT_MODEL
        resolved_aspect = _resolve_aspect_ratio(aspect_ratio, width, height)
        url = f"{BASE_URL}/accounts/fireworks/models/{resolved_model}"

        logger.debug(
            "Flux generate: model=%s, aspect=%s", resolved_model, resolved_aspect,
        )

        # Step 1: Submit generation request
        resp = await self._client.post(
            url,
            json={
                "prompt": prompt,
                "output_format": output_format,
                "aspect_ratio": resolved_aspect,
                "safety_tolerance": 6,
            },
        )
        resp.raise_for_status()
        request_id = resp.json()["request_id"]

        # Step 2: Poll for result
        result_url = f"{url}/get_result"
        for _ in range(MAX_POLL_ATTEMPTS):
            result_resp = await self._client.post(
                result_url, json={"id": request_id},
            )
            data = result_resp.json()
            status = data.get("status")

            if status == "Ready":
                image_url = data["result"]["sample"]
                img_resp = await self._client.get(image_url)
                img_resp.raise_for_status()
                image_b64 = base64.b64encode(img_resp.content).decode("ascii")
                return ImageResult(
                    image_base64=image_b64,
                    content_type=f"image/{output_format}",
                    prompt_used=prompt,
                )

            if status in TERMINAL_STATUSES:
                raise RuntimeError(f"Flux generation failed: {status} — {data}")

            await asyncio.sleep(POLL_INTERVAL)

        raise RuntimeError(
            f"Flux generation timed out after {MAX_POLL_ATTEMPTS * POLL_INTERVAL}s",
        )


def _resolve_aspect_ratio(
    aspect_ratio: str,
    width: int | None,
    height: int | None,
) -> str:
    """Convert explicit width/height to a Flux aspect ratio string."""
    if width and height:
        mapped = ASPECT_RATIO_MAP.get((width, height))
        if mapped:
            return mapped
        g = gcd(width, height)
        return f"{width // g}:{height // g}"
    return aspect_ratio
