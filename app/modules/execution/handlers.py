"""Event handlers that bridge execution events to WebSocket.

Auto-discovered by ``discover_handlers("app.modules")``. Each handler
receives a domain event from the EventBus and pushes a WSMessage to
the user's WebSocket connections.
"""

from __future__ import annotations

import logging

from app.core.events import Event, EventTypes, subscribe
from app.core.ws.manager import ws_manager
from app.core.ws.models import WSMessage

logger = logging.getLogger(__name__)


# ── Run-level events ──


@subscribe(EventTypes.EXECUTION_STARTED)
async def on_execution_started(event: Event) -> None:
    await ws_manager.send_to_user(
        event.payload["user_id"],
        WSMessage(type="execution.started", data={
            "run_id": event.payload["run_id"],
        }),
    )


@subscribe(EventTypes.EXECUTION_COMPLETED)
async def on_execution_completed(event: Event) -> None:
    await ws_manager.send_to_user(
        event.payload["user_id"],
        WSMessage(type="execution.completed", data={
            "run_id": event.payload["run_id"],
            "outputs": event.payload.get("outputs", {}),
        }),
    )


@subscribe(EventTypes.EXECUTION_FAILED)
async def on_execution_failed(event: Event) -> None:
    await ws_manager.send_to_user(
        event.payload["user_id"],
        WSMessage(type="execution.failed", data={
            "run_id": event.payload["run_id"],
            "error": event.payload.get("error", "Unknown error"),
        }),
    )


# ── Node-level events ──


@subscribe(EventTypes.NODE_PENDING)
async def on_node_pending(event: Event) -> None:
    await ws_manager.send_to_user(
        event.payload["user_id"],
        WSMessage(type="execution.node.status", data={
            "run_id": event.payload["run_id"],
            "node_id": event.payload["node_id"],
            "status": "pending",
        }),
    )


@subscribe(EventTypes.NODE_RUNNING)
async def on_node_running(event: Event) -> None:
    await ws_manager.send_to_user(
        event.payload["user_id"],
        WSMessage(type="execution.node.status", data={
            "run_id": event.payload["run_id"],
            "node_id": event.payload["node_id"],
            "status": "running",
        }),
    )


@subscribe(EventTypes.NODE_COMPLETED)
async def on_node_completed(event: Event) -> None:
    await ws_manager.send_to_user(
        event.payload["user_id"],
        WSMessage(type="execution.node.completed", data={
            "run_id": event.payload["run_id"],
            "node_id": event.payload["node_id"],
            "output": event.payload.get("output", {}),
        }),
    )


@subscribe(EventTypes.NODE_FAILED)
async def on_node_failed(event: Event) -> None:
    await ws_manager.send_to_user(
        event.payload["user_id"],
        WSMessage(type="execution.node.failed", data={
            "run_id": event.payload["run_id"],
            "node_id": event.payload["node_id"],
            "error": event.payload.get("error", "Unknown error"),
        }),
    )


@subscribe(EventTypes.NODE_SKIPPED)
async def on_node_skipped(event: Event) -> None:
    await ws_manager.send_to_user(
        event.payload["user_id"],
        WSMessage(type="execution.node.status", data={
            "run_id": event.payload["run_id"],
            "node_id": event.payload["node_id"],
            "status": "skipped",
            "error": event.payload.get("reason", ""),
        }),
    )
