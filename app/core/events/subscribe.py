from typing import Callable


def subscribe(*event_types: str) -> Callable:
    def decorator(fn: Callable) -> Callable:
        fn._event_subscriptions = list(event_types)
        return fn
    return decorator
