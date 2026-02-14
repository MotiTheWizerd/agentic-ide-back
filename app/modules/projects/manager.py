import logging

from app.core.bus import event_bus
from app.core.events import Event, EventTypes

logger = logging.getLogger(__name__)


class ProjectManager:
    async def create(self, project_name: str, user_id: int) -> None:
        logger.info("Creating project: %s for user %s", project_name, user_id)
        await event_bus.emit(Event(
            type=EventTypes.PROJECT_CREATED,
            payload={"project_name": project_name, "user_id": user_id},
        ))

    async def delete(self, project_id: int) -> None:
        logger.info("Deleting project: %s", project_id)
        await event_bus.emit(Event(
            type=EventTypes.PROJECT_DELETED,
            payload={"project_id": project_id},
        ))
