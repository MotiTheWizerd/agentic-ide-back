import logging
from typing import Any, Callable

logger = logging.getLogger(__name__)


class ServiceRegistry:
    def __init__(self) -> None:
        self._instances: dict[type, Any] = {}

    def register(self, cls: type, instance: Any) -> None:
        self._instances[cls] = instance
        logger.info("Registered service: %s", cls.__name__)

    def resolve(self, cls: type) -> Any:
        instance = self._instances.get(cls)
        if instance is None:
            raise KeyError(f"Service not registered: {cls.__name__}")
        return instance

    def get(self, cls: type) -> Callable:
        def _provider() -> Any:
            return self.resolve(cls)
        return _provider


registry = ServiceRegistry()
