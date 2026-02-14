import logging

from app.core.bus import event_bus
from app.core.events import Event, EventTypes

logger = logging.getLogger(__name__)


class UserManager:
    async def register(self, username: str, email: str) -> None:
        logger.info("Registering user: %s", username)
        await event_bus.emit(Event(
            type=EventTypes.USER_REGISTERED,
            payload={"username": username, "email": email},
        ))

    async def deactivate(self, user_id: str) -> None:
        logger.info("Deactivating user: %s", user_id)
        await event_bus.emit(Event(
            type=EventTypes.USER_DEACTIVATED,
            payload={"user_id": user_id},
        ))
