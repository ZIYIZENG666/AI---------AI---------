"""Pydantic schemas for the discovery module."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from app.modules.tasks.schemas import PaginationMeta, TaskRunRead


DiscoveryStatus = Literal["discovered"]
ValidationStatus = Literal[
    "pending",
    "valid",
    "invalid",
    "duplicate",
    "insufficient_content",
]
ReviewStatus = Literal["unreviewed", "approved", "rejected", "needs_manual_review"]


class LeadDiscoveryStartData(BaseModel):
    """Payload returned when a Lead Discovery task is accepted."""

    task_id: str
    status: Literal["pending"]
    task_type: Literal["lead_discovery"]
    campaign_id: str


class LeadDiscoveryStartResponse(BaseModel):
    """Envelope for Lead Discovery task creation."""

    data: LeadDiscoveryStartData
    message: str


class LeadRead(BaseModel):
    """Response schema for a discovered candidate lead."""

    id: str
    campaign_id: str
    task_run_id: str
    company_name: str
    website: str
    normalized_name: str
    normalized_website: str
    description: str | None
    country: str | None
    industry: str | None
    source_url: str
    search_query: str
    raw_snippet: str | None
    discovery_reason: str | None
    provider_name: str
    discovery_status: DiscoveryStatus
    validation_status: ValidationStatus
    review_status: ReviewStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class LeadListData(BaseModel):
    """Collection payload for Lead list responses."""

    items: list[LeadRead]
    pagination: PaginationMeta


class LeadListResponse(BaseModel):
    """Envelope for Lead list responses."""

    data: LeadListData
    message: str


class LeadDiscoveryTaskListData(BaseModel):
    """Collection payload for Campaign Lead Discovery task responses."""

    items: list[TaskRunRead]
    pagination: PaginationMeta


class LeadDiscoveryTaskListResponse(BaseModel):
    """Envelope for Campaign Lead Discovery task responses."""

    data: LeadDiscoveryTaskListData
    message: str
