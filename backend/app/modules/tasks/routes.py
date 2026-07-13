"""HTTP routes for the tasks module."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.tasks.repository import TaskRepository
from app.modules.tasks.schemas import TaskRunRead, TaskRunResponse
from app.modules.tasks.service import TaskService


router = APIRouter(tags=["tasks"])


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    """Create a request-scoped task service."""

    return TaskService(repository=TaskRepository(db))


@router.get(
    "/tasks/{task_id}",
    response_model=TaskRunResponse,
)
def get_task(
    task_id: str,
    service: TaskService = Depends(get_task_service),
) -> TaskRunResponse:
    task_run = service.get_task(task_id)
    return TaskRunResponse(
        data=TaskRunRead.model_validate(task_run),
        message="Task fetched successfully.",
    )
