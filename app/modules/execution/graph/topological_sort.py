"""Kahn's topological sort with cycle detection.

Filters out group nodes, deduplicates by ID, and returns an ordered list
of ExecutionSteps with classified input/adapter dependencies.
"""

from __future__ import annotations

from collections import defaultdict, deque

from app.modules.execution.graph.edge_classification import (
    get_adapter_input_node_ids,
    get_text_input_node_ids,
)
from app.modules.execution.models import ExecutionStep


def topological_sort(
    nodes: list[dict],
    edges: list[dict],
) -> list[ExecutionStep]:
    """Run Kahn's algorithm and return execution steps in dependency order.

    Raises ``ValueError`` if the graph contains a cycle.
    """
    # Filter out group nodes and deduplicate
    seen_ids: set[str] = set()
    filtered: list[dict] = []
    for n in nodes:
        nid = n["id"]
        ntype = n.get("type") or (n.get("data") or {}).get("type") or ""
        if ntype == "group" or nid in seen_ids:
            continue
        seen_ids.add(nid)
        filtered.append(n)

    node_ids = {n["id"] for n in filtered}

    # Build adjacency and in-degree maps (only for edges within filtered set)
    in_degree: dict[str, int] = {nid: 0 for nid in node_ids}
    dependents: dict[str, list[str]] = defaultdict(list)

    for e in edges:
        src, tgt = e["source"], e["target"]
        if src in node_ids and tgt in node_ids:
            in_degree[tgt] += 1
            dependents[src].append(tgt)

    # Seed the queue with zero-in-degree nodes
    queue: deque[str] = deque(
        nid for nid, deg in in_degree.items() if deg == 0
    )

    type_by_id: dict[str, str] = {}
    for n in filtered:
        ntype = n.get("type") or (n.get("data") or {}).get("type") or ""
        type_by_id[n["id"]] = ntype

    sorted_steps: list[ExecutionStep] = []

    while queue:
        nid = queue.popleft()
        sorted_steps.append(
            ExecutionStep(
                node_id=nid,
                node_type=type_by_id[nid],
                input_node_ids=get_text_input_node_ids(nid, edges),
                adapter_node_ids=get_adapter_input_node_ids(nid, edges),
            )
        )
        for dep in dependents[nid]:
            in_degree[dep] -= 1
            if in_degree[dep] == 0:
                queue.append(dep)

    if len(sorted_steps) != len(node_ids):
        raise ValueError("Graph contains a cycle")

    return sorted_steps


def group_by_levels(
    steps: list[ExecutionStep],
) -> list[list[ExecutionStep]]:
    """Group topologically sorted steps into parallel levels.

    Level 0 = nodes with no dependencies.
    Level N = nodes whose deepest dependency is at level N-1.
    All nodes in the same level can execute concurrently.
    """
    if not steps:
        return []

    node_level: dict[str, int] = {}

    for step in steps:
        all_deps = step.input_node_ids + step.adapter_node_ids
        if not all_deps:
            node_level[step.node_id] = 0
        else:
            max_dep_level = max(node_level.get(d, 0) for d in all_deps)
            node_level[step.node_id] = max_dep_level + 1

    max_level = max(node_level.values(), default=0)
    levels: list[list[ExecutionStep]] = [[] for _ in range(max_level + 1)]
    for step in steps:
        levels[node_level[step.node_id]].append(step)

    return levels
