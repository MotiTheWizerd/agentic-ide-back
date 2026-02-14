"""BFS traversal utilities for upstream and downstream node discovery."""

from __future__ import annotations

from collections import deque


def get_upstream_nodes(
    start_node_id: str,
    nodes: list[dict],
    edges: list[dict],
) -> set[str]:
    """BFS backwards from *start_node_id* to find all ancestor node IDs."""
    node_ids = {n["id"] for n in nodes}
    parent_map: dict[str, list[str]] = {nid: [] for nid in node_ids}
    for e in edges:
        src, tgt = e["source"], e["target"]
        if src in node_ids and tgt in node_ids:
            parent_map[tgt].append(src)

    visited: set[str] = set()
    queue: deque[str] = deque([start_node_id])

    while queue:
        nid = queue.popleft()
        for parent in parent_map.get(nid, []):
            if parent not in visited:
                visited.add(parent)
                queue.append(parent)

    return visited


def get_downstream_nodes(
    start_node_id: str,
    nodes: list[dict],
    edges: list[dict],
) -> set[str]:
    """BFS forward from *start_node_id* to find all descendant node IDs."""
    node_ids = {n["id"] for n in nodes}
    child_map: dict[str, list[str]] = {nid: [] for nid in node_ids}
    for e in edges:
        src, tgt = e["source"], e["target"]
        if src in node_ids and tgt in node_ids:
            child_map[src].append(tgt)

    visited: set[str] = set()
    queue: deque[str] = deque([start_node_id])

    while queue:
        nid = queue.popleft()
        for child in child_map.get(nid, []):
            if child not in visited:
                visited.add(child)
                queue.append(child)

    return visited
