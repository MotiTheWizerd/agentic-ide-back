import asyncio
import logging
from collections import defaultdict
from typing import Callable, Coroutine, Any

from app.core.events import Event

logger = logging.getLogger(__name__)

EventHandler = Callable[[Event], Coroutine[Any, Any, None]]


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)

    def on(self, event_type: str, handler: EventHandler) -> None:
        self._handlers[event_type].append(handler)
        logger.debug("Registered handler %s for '%s'", handler.__name__, event_type)

    def off(self, event_type: str, handler: EventHandler) -> None:
        self._handlers[event_type].remove(handler)

    async def emit(self, event: Event) -> None:
        handlers = self._handlers.get(event.type, [])
        if not handlers:
            return
        logger.debug("Emitting '%s' to %d handler(s)", event.type, len(handlers))
        for handler in handlers:
            asyncio.create_task(self._safe_call(handler, event))

    async def _safe_call(self, handler: EventHandler, event: Event) -> None:
        try:
            await handler(event)
        except Exception:
            logger.exception("Handler %s failed for event %s", handler.__name__, event.type)


event_bus = EventBus()
