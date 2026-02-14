"""Executor function type definition."""

from __future__ import annotations

from typing import Awaitable, Callable

from app.modules.execution.models import NodeExecutionContext, NodeOutput

ExecutorFn = Callable[[NodeExecutionContext], Awaitable[NodeOutput]]
