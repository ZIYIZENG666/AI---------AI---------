"""Service logic for the tasks module."""

from app.core.errors import AppError
from app.modules.tasks.repository import TaskRepository


class TaskService:
    """Business service for generic task lookup."""

    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def get_task(self, task_id: str):
        task_run = self.repository.get_by_id(task_id)
        if task_run is None:
            raise AppError(
                message="Task not found.",
                status_code=404,
                code="task_not_found",
            )
        return task_run
