"""Service placeholders for the tasks module."""

from app.modules.tasks.repository import TaskRepository


class TaskService:
    """Business service placeholder for tasks."""

    def __init__(self, repository: TaskRepository | None = None) -> None:
        self.repository = repository or TaskRepository()
