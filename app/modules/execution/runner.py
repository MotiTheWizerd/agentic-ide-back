"""Execution runner — orchestrates graph execution with event-driven status updates.

The runner never imports WebSocket or any transport layer. It emits domain events
through the EventBus; separate handlers in handlers.py bridge those events to WS.
"""

from __future__ import annotations

import asyncio
import logging
import time

from app.core.bus import event_bus
from app.core.events import Event, EventTypes
from app.modules.execution.config.model_defaults import resolve_model_for_node
from app.modules.execution.executors.registry import get_executor
from app.modules.execution.graph.topological_sort import group_by_levels, topological_sort
from app.modules.execution.graph.traversal import get_downstream_nodes, get_upstream_nodes
from app.modules.execution.models import ExecutionStep, NodeExecutionContext, NodeOutput

logger = logging.getLogger(__name__)


async def run_execution(
    run_id: str,
    user_id: int,
    flow_id: str,
    nodes: list[dict],
    edges: list[dict],
    provider_id: str,
    trigger_node_id: str | None = None,
    cached_outputs: dict[str, dict] | None = None,
) -> dict[str, NodeOutput]:
    """Execute a graph and emit events for every state transition.

    Returns the final outputs map.
    """
    cached_outputs = cached_outputs or {}
    outputs: dict[str, NodeOutput] = {}

    # Index nodes by ID and extract type
    nodes_by_id: dict[str, dict] = {}
    for n in nodes:
        nid = n["id"]
        ntype = n.get("type") or (n.get("data") or {}).get("type") or ""
        nodes_by_id[nid] = {**n, "type": ntype, "data": n.get("data") or {}}

    # ── Topological sort ──
    try:
        steps = topological_sort(nodes, edges)
    except ValueError as exc:
        await event_bus.emit(Event(
            type=EventTypes.EXECUTION_FAILED,
            payload={"run_id": run_id, "user_id": user_id, "error": str(exc)},
        ))
        return outputs

    # ── Partial re-execution filter ──
    if trigger_node_id:
        downstream = get_downstream_nodes(trigger_node_id, nodes, edges)
        upstream = get_upstream_nodes(trigger_node_id, nodes, edges)
        execution_set = {trigger_node_id} | downstream

        # Pre-populate cached upstream nodes
        for uid in upstream:
            if uid in cached_outputs:
                outputs[uid] = NodeOutput(**cached_outputs[uid])
            else:
                execution_set.add(uid)

        steps = [s for s in steps if s.node_id in execution_set]

    # ── Level grouping for parallelism ──
    levels = group_by_levels(steps)

    # ── Emit pending for all nodes ──
    for step in steps:
        if step.node_id not in outputs:  # skip pre-cached
            await event_bus.emit(Event(
                type=EventTypes.NODE_PENDING,
                payload={"run_id": run_id, "user_id": user_id, "node_id": step.node_id},
            ))

    # ── Execute level by level ──
    for level in levels:
        tasks = [
            _execute_node(step, outputs, nodes_by_id, provider_id, run_id, user_id, cached_outputs)
            for step in level
        ]
        await asyncio.gather(*tasks)

    # ── Final event ──
    serialized = {nid: out.model_dump(exclude_none=True) for nid, out in outputs.items()}
    await event_bus.emit(Event(
        type=EventTypes.EXECUTION_COMPLETED,
        payload={"run_id": run_id, "user_id": user_id, "outputs": serialized},
    ))

    return outputs


async def _execute_node(
    step: ExecutionStep,
    outputs: dict[str, NodeOutput],
    nodes_by_id: dict[str, dict],
    flow_provider_id: str,
    run_id: str,
    user_id: int,
    cached_outputs: dict[str, dict],
) -> None:
    """Execute a single node, updating the shared outputs map."""
    node_id = step.node_id

    # Already computed (cached)?
    if node_id in outputs:
        return

    # Check cached_outputs from the request
    if node_id in cached_outputs:
        output = NodeOutput(**cached_outputs[node_id])
        outputs[node_id] = output
        await event_bus.emit(Event(
            type=EventTypes.NODE_COMPLETED,
            payload={
                "run_id": run_id, "user_id": user_id,
                "node_id": node_id, "output": output.model_dump(exclude_none=True),
            },
        ))
        return

    # ── Check upstream errors → skip ──
    all_deps = step.input_node_ids + step.adapter_node_ids
    for dep_id in all_deps:
        dep_output = outputs.get(dep_id)
        if dep_output and dep_output.error:
            reason = f"Upstream node {dep_id} failed"
            outputs[node_id] = NodeOutput(error=reason)
            await event_bus.emit(Event(
                type=EventTypes.NODE_SKIPPED,
                payload={"run_id": run_id, "user_id": user_id, "node_id": node_id, "reason": reason},
            ))
            return

    # ── Resolve executor ──
    executor = get_executor(step.node_type)
    if not executor:
        outputs[node_id] = NodeOutput(error=f"No executor for type: {step.node_type}")
        await event_bus.emit(Event(
            type=EventTypes.NODE_SKIPPED,
            payload={
                "run_id": run_id, "user_id": user_id,
                "node_id": node_id, "reason": f"No executor for type: {step.node_type}",
            },
        ))
        return

    # ── Gather inputs ──
    text_inputs = [outputs[nid] for nid in step.input_node_ids if nid in outputs]
    adapter_inputs = [outputs[nid] for nid in step.adapter_node_ids if nid in outputs]

    # ── Resolve model ──
    node_info = nodes_by_id.get(node_id, {})
    node_data = node_info.get("data") or {}
    resolved = resolve_model_for_node(node_data, step.node_type, flow_provider_id)

    ctx = NodeExecutionContext(
        node_id=node_id,
        node_type=step.node_type,
        node_data=node_data,
        text_inputs=text_inputs,
        adapter_inputs=adapter_inputs,
        provider_id=resolved.provider_id,
        model=resolved.model,
        temperature=resolved.temperature,
        run_id=run_id,
        user_id=user_id,
    )

    # ── Emit running ──
    await event_bus.emit(Event(
        type=EventTypes.NODE_RUNNING,
        payload={"run_id": run_id, "user_id": user_id, "node_id": node_id},
    ))

    # ── Execute ──
    try:
        start = time.perf_counter()
        output = await executor(ctx)
        if output.duration_ms is None:
            output.duration_ms = (time.perf_counter() - start) * 1000
        outputs[node_id] = output

        await event_bus.emit(Event(
            type=EventTypes.NODE_COMPLETED,
            payload={
                "run_id": run_id, "user_id": user_id,
                "node_id": node_id, "output": output.model_dump(exclude_none=True),
            },
        ))
    except Exception as exc:
        logger.exception("Executor failed for node %s", node_id)
        outputs[node_id] = NodeOutput(error=str(exc))
        await event_bus.emit(Event(
            type=EventTypes.NODE_FAILED,
            payload={"run_id": run_id, "user_id": user_id, "node_id": node_id, "error": str(exc)},
        ))
