"""Pydantic schemas for the tasks module."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


TaskStatus = Literal["pending", "running", "completed", "failed", "cancelled"]
TaskType = Literal["lead_discovery"]
RelatedEntityType = Literal["campaign"]


class PaginationMeta(BaseModel):
    """Pagination metadata for task lists."""

    total: int
    limit: int
    offset: int


class TaskRunRead(BaseModel):
    """Response schema for a task run."""

    id: str
    task_type: TaskType
    related_entity_type: RelatedEntityType
    related_entity_id: str
    search_query: str
    provider_name: str
    status: TaskStatus
    progress: int
    error_message: str | None
    started_at: datetime | None
    finished_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TaskRunResponse(BaseModel):
    """Envelope for a single task run response."""

    data: TaskRunRead
    message: str


class TaskRunListData(BaseModel):
    """Collection payload for task run list responses."""

    items: list[TaskRunRead]
    pagination: PaginationMeta


class TaskRunListResponse(BaseModel):
    """Envelope for task run list responses."""

    data: TaskRunListData
    message: str
