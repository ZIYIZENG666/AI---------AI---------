"""Pydantic schemas for the intelligence module."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from app.modules.tasks.schemas import PaginationMeta, TaskRunRead


CrawlStatus = Literal["completed", "failed", "insufficient_content", "skipped"]


class LeadValidationStartData(BaseModel):
    """Payload returned when a Lead Validation task is accepted."""

    task_id: str
    status: Literal["pending"]
    task_type: Literal["lead_validation"]
    lead_id: str


class LeadValidationStartResponse(BaseModel):
    """Envelope for Lead Validation task creation."""

    data: LeadValidationStartData
    message: str


class LeadValidationTaskListData(BaseModel):
    """Collection payload for Lead Validation task responses."""

    items: list[TaskRunRead]
    pagination: PaginationMeta


class LeadValidationTaskListResponse(BaseModel):
    """Envelope for Lead Validation task list responses."""

    data: LeadValidationTaskListData
    message: str


class LeadIntelligenceRead(BaseModel):
    """Response schema for factual Lead Intelligence."""

    id: str
    lead_id: str
    task_run_id: str
    source_url: str
    provider_name: str
    website_summary: str | None
    products_or_services: list[str]
    target_customers: list[str]
    business_model: str | None
    pain_points: list[str]
    evidence: list[dict]
    content_quality: str
    crawl_status: CrawlStatus
    error_message: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class LeadIntelligenceListData(BaseModel):
    """Collection payload for Lead Intelligence responses."""

    items: list[LeadIntelligenceRead]
    pagination: PaginationMeta


class LeadIntelligenceListResponse(BaseModel):
    """Envelope for Lead Intelligence list responses."""

    data: LeadIntelligenceListData
    message: str
