"""Repository logic for the tasks module."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.tasks.models import TaskRun


class TaskRepository:
    """Database access for task runs."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, data: dict) -> TaskRun:
        task_run = TaskRun(**data)
        self.session.add(task_run)
        self.session.commit()
        self.session.refresh(task_run)
        return task_run

    def get_by_id(self, task_id: str) -> TaskRun | None:
        return self.session.get(TaskRun, task_id)

    def update(self, task_run: TaskRun, data: dict) -> TaskRun:
        for field_name, value in data.items():
            setattr(task_run, field_name, value)

        self.session.add(task_run)
        self.session.commit()
        self.session.refresh(task_run)
        return task_run

    def list_lead_discovery_tasks_for_campaign(
        self,
        campaign_id: str,
        limit: int,
        offset: int,
    ) -> tuple[list[TaskRun], int]:
        filters = [
            TaskRun.task_type == "lead_discovery",
            TaskRun.related_entity_type == "campaign",
            TaskRun.related_entity_id == campaign_id,
        ]
        total = self.session.scalar(
            select(func.count()).select_from(TaskRun).where(*filters)
        ) or 0
        items = list(
            self.session.scalars(
                select(TaskRun)
                .where(*filters)
                .order_by(TaskRun.created_at.desc(), TaskRun.id.desc())
                .limit(limit)
                .offset(offset)
            )
        )
        return items, total

    def has_blocking_lead_discovery_task(self, campaign_id: str) -> bool:
        count = self.session.scalar(
            select(func.count())
            .select_from(TaskRun)
            .where(
                TaskRun.task_type == "lead_discovery",
                TaskRun.related_entity_type == "campaign",
                TaskRun.related_entity_id == campaign_id,
                TaskRun.status.in_(("pending", "running", "completed")),
            )
        )
        return bool(count)

    def list_lead_validation_tasks_for_lead(
        self,
        lead_id: str,
        limit: int,
        offset: int,
    ) -> tuple[list[TaskRun], int]:
        filters = [
            TaskRun.task_type == "lead_validation",
            TaskRun.related_entity_type == "lead",
            TaskRun.related_entity_id == lead_id,
        ]
        total = self.session.scalar(
            select(func.count()).select_from(TaskRun).where(*filters)
        ) or 0
        items = list(
            self.session.scalars(
                select(TaskRun)
                .where(*filters)
                .order_by(TaskRun.created_at.desc(), TaskRun.id.desc())
                .limit(limit)
                .offset(offset)
            )
        )
        return items, total

    def has_blocking_lead_validation_task(self, lead_id: str) -> bool:
        count = self.session.scalar(
            select(func.count())
            .select_from(TaskRun)
            .where(
                TaskRun.task_type == "lead_validation",
                TaskRun.related_entity_type == "lead",
                TaskRun.related_entity_id == lead_id,
                TaskRun.status.in_(("pending", "running", "completed")),
            )
        )
        return bool(count)

    def list_lead_scoring_tasks_for_lead(
        self,
        lead_id: str,
        limit: int,
        offset: int,
    ) -> tuple[list[TaskRun], int]:
        filters = [
            TaskRun.task_type == "lead_scoring",
            TaskRun.related_entity_type == "lead",
            TaskRun.related_entity_id == lead_id,
        ]
        total = self.session.scalar(
            select(func.count()).select_from(TaskRun).where(*filters)
        ) or 0
        items = list(
            self.session.scalars(
                select(TaskRun)
                .where(*filters)
                .order_by(TaskRun.created_at.desc(), TaskRun.id.desc())
                .limit(limit)
                .offset(offset)
            )
        )
        return items, total

    def has_blocking_lead_scoring_task(self, lead_id: str) -> bool:
        count = self.session.scalar(
            select(func.count())
            .select_from(TaskRun)
            .where(
                TaskRun.task_type == "lead_scoring",
                TaskRun.related_entity_type == "lead",
                TaskRun.related_entity_id == lead_id,
                TaskRun.status.in_(("pending", "running", "completed")),
            )
        )
        return bool(count)
