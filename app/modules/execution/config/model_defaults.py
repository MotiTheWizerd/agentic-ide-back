"""Per-node-type provider and model defaults.

Priority chain for model resolution:
1. Node-level override (node_data.providerId + node_data.model)
2. Node-type default (NODE_MODEL_DEFAULTS)
3. Flow-level provider
"""

from __future__ import annotations

from app.modules.execution.models import ResolvedModel

NODE_MODEL_DEFAULTS: dict[str, dict[str, str | float]] = {
    "grammarFix":       {"provider_id": "mistral", "model": "ministral-14b-2512", "temperature": 0.7},
    "compressor":       {"provider_id": "mistral", "model": "ministral-14b-2512", "temperature": 0.7},
    "promptEnhancer":   {"provider_id": "mistral", "model": "ministral-14b-2512", "temperature": 0.7},
    "initialPrompt":    {"provider_id": "mistral", "model": "ministral-14b-2512", "temperature": 0.7},
    "translator":       {"provider_id": "mistral", "model": "ministral-14b-2512", "temperature": 0.7},
    "storyTeller":      {"provider_id": "mistral", "model": "labs-mistral-small-creative", "temperature": 0.95},
    "imageDescriber":   {"provider_id": "claude",  "model": "", "temperature": 0.7},
    "personasReplacer": {"provider_id": "claude",  "model": "", "temperature": 0.7},
}


def resolve_model_for_node(
    node_data: dict,
    node_type: str,
    flow_provider_id: str,
) -> ResolvedModel:
    """Resolve provider + model for a node using the priority chain."""
    node_provider = node_data.get("providerId") or ""
    node_model = node_data.get("model") or ""

    # 1. Node-level override
    if node_provider and node_model:
        temp = NODE_MODEL_DEFAULTS.get(node_type, {}).get("temperature", 0.7)
        return ResolvedModel(
            provider_id=node_provider,
            model=node_model,
            temperature=float(temp),
        )

    # 2. Node-type default
    defaults = NODE_MODEL_DEFAULTS.get(node_type)
    if defaults:
        return ResolvedModel(
            provider_id=node_provider or str(defaults["provider_id"]),
            model=node_model or str(defaults["model"]),
            temperature=float(defaults.get("temperature", 0.7)),
        )

    # 3. Flow-level fallback
    return ResolvedModel(provider_id=flow_provider_id, model="", temperature=0.7)
