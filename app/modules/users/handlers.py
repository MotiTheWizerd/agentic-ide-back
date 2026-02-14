import logging

from app.core.events import Event, EventTypes, subscribe

logger = logging.getLogger(__name__)


@subscribe(EventTypes.USER_REGISTERED)
async def on_user_registered(event: Event) -> None:
    logger.info("Handle user.registered: %s", event.payload)


@subscribe(EventTypes.USER_DEACTIVATED)
async def on_user_deactivated(event: Event) -> None:
    logger.info("Handle user.deactivated: %s", event.payload)
