import importlib
import inspect
import logging
import pkgutil
from pathlib import Path

from fastapi import APIRouter

from app.core.bus import event_bus
from app.core.di.registry import registry

logger = logging.getLogger(__name__)


def discover_routers(endpoints_package: str) -> list[APIRouter]:
    package = importlib.import_module(endpoints_package)
    package_path = Path(package.__file__).parent
    routers: list[APIRouter] = []

    for module_info in pkgutil.iter_modules([str(package_path)]):
        module_name = f"{endpoints_package}.{module_info.name}"
        module = importlib.import_module(module_name)
        router = getattr(module, "router", None)
        if isinstance(router, APIRouter):
            routers.append(router)
            logger.info("Discovered router: %s", module_name)

    return routers


def discover_managers(modules_package: str) -> None:
    package = importlib.import_module(modules_package)
    package_path = Path(package.__file__).parent

    for subdir in sorted(package_path.iterdir()):
        if not subdir.is_dir() or subdir.name.startswith(("_", ".")):
            continue

        manager_file = subdir / "manager.py"
        if not manager_file.exists():
            continue

        module_name = f"{modules_package}.{subdir.name}.manager"
        module = importlib.import_module(module_name)

        for name, cls in inspect.getmembers(module, inspect.isclass):
            if name.endswith("Manager") and cls.__module__ == module_name:
                instance = cls()
                registry.register(cls, instance)


def discover_handlers(modules_package: str) -> None:
    package = importlib.import_module(modules_package)
    package_path = Path(package.__file__).parent

    for subdir in sorted(package_path.iterdir()):
        if not subdir.is_dir() or subdir.name.startswith(("_", ".")):
            continue

        handlers_file = subdir / "handlers.py"
        if not handlers_file.exists():
            continue

        module_name = f"{modules_package}.{subdir.name}.handlers"
        module = importlib.import_module(module_name)

        for name, fn in inspect.getmembers(module, inspect.isfunction):
            event_types = getattr(fn, "_event_subscriptions", None)
            if not event_types:
                continue
            for event_type in event_types:
                event_bus.on(event_type, fn)
                logger.info("Subscribed %s to '%s'", name, event_type)
