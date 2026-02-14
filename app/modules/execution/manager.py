"""ExecutionManager — entry point for graph execution.

Auto-discovered by ``discover_managers("app.modules")`` and registered as
a singleton in the ServiceRegistry.
"""

from __future__ import annotations

import asyncio
import logging
from uuid import uuid4

from app.core.bus import event_bus
from app.core.events import Event, EventTypes
from app.modules.execution.runner import run_execution

logger = logging.getLogger(__name__)


class ExecutionManager:
    async def run(
        self,
        user_id: int,
        flow_id: str,
        nodes: list[dict],
        edges: list[dict],
        provider_id: str,
        trigger_node_id: str | None = None,
        cached_outputs: dict[str, dict] | None = None,
    ) -> str:
        """Start an execution run. Returns *run_id* immediately.

        The actual execution runs as a background asyncio task. Status
        updates flow through the EventBus → WS handlers.
        """
        run_id = uuid4().hex

        await event_bus.emit(Event(
            type=EventTypes.EXECUTION_STARTED,
            payload={
                "run_id": run_id,
                "user_id": user_id,
                "flow_id": flow_id,
            },
        ))

        asyncio.create_task(
            self._execute(
                run_id, user_id, flow_id, nodes, edges,
                provider_id, trigger_node_id, cached_outputs,
            )
        )

        return run_id

    async def _execute(
        self,
        run_id: str,
        user_id: int,
        flow_id: str,
        nodes: list[dict],
        edges: list[dict],
        provider_id: str,
        trigger_node_id: str | None,
        cached_outputs: dict[str, dict] | None,
    ) -> None:
        try:
            await run_execution(
                run_id=run_id,
                user_id=user_id,
                flow_id=flow_id,
                nodes=nodes,
                edges=edges,
                provider_id=provider_id,
                trigger_node_id=trigger_node_id,
                cached_outputs=cached_outputs,
            )
        except Exception as exc:
            logger.exception("Execution %s failed unexpectedly", run_id)
            await event_bus.emit(Event(
                type=EventTypes.EXECUTION_FAILED,
                payload={
                    "run_id": run_id,
                    "user_id": user_id,
                    "error": str(exc),
                },
            ))
