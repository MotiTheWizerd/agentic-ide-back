class EventTypes:
    # Project
    PROJECT_CREATED = "project.created"
    PROJECT_DELETED = "project.deleted"

    # User
    USER_REGISTERED = "user.registered"
    USER_DEACTIVATED = "user.deactivated"

    # Execution — run level
    EXECUTION_STARTED = "execution.started"
    EXECUTION_COMPLETED = "execution.completed"
    EXECUTION_FAILED = "execution.failed"

    # Execution — node level
    NODE_PENDING = "execution.node.pending"
    NODE_RUNNING = "execution.node.running"
    NODE_COMPLETED = "execution.node.completed"
    NODE_FAILED = "execution.node.failed"
    NODE_SKIPPED = "execution.node.skipped"
