import logging
from collections import defaultdict

from fastapi import WebSocket

from app.core.ws.models import WSMessage

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self) -> None:
        self._connections: dict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, user_id: int, ws: WebSocket) -> None:
        await ws.accept()
        self._connections[user_id].append(ws)
        logger.info("WS connected: user %d (%d total)", user_id, self.count)

    def disconnect(self, user_id: int, ws: WebSocket) -> None:
        self._connections[user_id].remove(ws)
        if not self._connections[user_id]:
            del self._connections[user_id]
        logger.info("WS disconnected: user %d (%d total)", user_id, self.count)

    async def send_to_user(self, user_id: int, message: WSMessage) -> None:
        for ws in self._connections.get(user_id, []):
            try:
                await ws.send_json(message.model_dump())
            except Exception:
                logger.warning("Failed to send to user %d", user_id)

    async def broadcast(self, message: WSMessage) -> None:
        for user_id in list(self._connections):
            await self.send_to_user(user_id, message)

    @property
    def count(self) -> int:
        return sum(len(conns) for conns in self._connections.values())


ws_manager = ConnectionManager()
