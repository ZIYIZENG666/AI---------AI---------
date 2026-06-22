"""Placeholder interface for background task queue integrations."""


class TaskQueueProvider:
    """Provider contract for scheduling async background work."""

    def enqueue(self, task_name: str, payload: dict) -> str:
        raise NotImplementedError("Task queue integration is not implemented in the skeleton.")
