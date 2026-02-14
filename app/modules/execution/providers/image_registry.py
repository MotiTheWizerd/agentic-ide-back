"""Image provider registry — lazy factory for image provider clients."""

from __future__ import annotations

import os

from app.modules.execution.providers.flux import FluxImageProvider

ImageProviderInstance = FluxImageProvider

_image_providers: dict[str, ImageProviderInstance] = {}


def _init_image_providers() -> None:
    if _image_providers:
        return

    _image_providers["blackforestlabs"] = FluxImageProvider(
        api_key=os.environ.get("FIREWORKS_API_KEY", ""),
    )


def get_image_provider(provider_id: str) -> ImageProviderInstance:
    _init_image_providers()
    provider = _image_providers.get(provider_id)
    if not provider:
        raise ValueError(f"Unknown image provider: {provider_id}")
    return provider
