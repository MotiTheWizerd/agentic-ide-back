"""Classify edges as text-input or adapter-input based on target handle prefix."""


def get_text_input_node_ids(node_id: str, edges: list[dict]) -> list[str]:
    """Return source node IDs for edges targeting text handles of *node_id*."""
    return [
        e["source"]
        for e in edges
        if e["target"] == node_id
        and not (e.get("targetHandle") or "").startswith("adapter-")
    ]


def get_adapter_input_node_ids(node_id: str, edges: list[dict]) -> list[str]:
    """Return source node IDs for edges targeting adapter handles of *node_id*."""
    return [
        e["source"]
        for e in edges
        if e["target"] == node_id
        and (e.get("targetHandle") or "").startswith("adapter-")
    ]
