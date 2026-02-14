import logging

from app.core.events import Event, EventTypes, subscribe

logger = logging.getLogger(__name__)


@subscribe(EventTypes.PROJECT_CREATED)
async def on_project_created(event: Event) -> None:
    logger.info("Handle project.created: %s", event.payload)


@subscribe(EventTypes.PROJECT_DELETED)
async def on_project_deleted(event: Event) -> None:
    logger.info("Handle project.deleted: %s", event.payload)
