"""Pydantic schemas for the qualification module."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.modules.tasks.schemas import PaginationMeta, TaskRunRead


Recommendation = Literal[
    "recommended",
    "maybe",
    "not_recommended",
    "needs_manual_review",
]


class LeadScoringProviderResult(BaseModel):
    """Validated structured result returned by a Lead Scoring provider."""

    fit_score: int = Field(ge=0, le=100)
    recommendation: Recommendation
    matching_reasons: list[str] = Field(min_length=1)
    risk_notes: list[str] = Field(min_length=1)
    uncertainty_notes: list[str] = Field(min_length=1)
    evidence: list[dict] = Field(min_length=1)
    suggested_outreach_angle: str | None = None


class LeadScoringStartData(BaseModel):
    """Payload returned when a Lead Scoring task is accepted."""

    task_id: str
    status: Literal["pending"]
    task_type: Literal["lead_scoring"]
    lead_id: str


class LeadScoringStartResponse(BaseModel):
    """Envelope for Lead Scoring task creation."""

    data: LeadScoringStartData
    message: str


class LeadScoringTaskListData(BaseModel):
    """Collection payload for Lead Scoring task responses."""

    items: list[TaskRunRead]
    pagination: PaginationMeta


class LeadScoringTaskListResponse(BaseModel):
    """Envelope for Lead Scoring task list responses."""

    data: LeadScoringTaskListData
    message: str


class LeadScoreRead(BaseModel):
    """Response schema for AI Lead Scoring output."""

    id: str
    lead_id: str
    campaign_id: str
    task_run_id: str
    fit_score: int
    recommendation: Recommendation
    matching_reasons: list[str]
    risk_notes: list[str]
    uncertainty_notes: list[str]
    evidence: list[dict]
    suggested_outreach_angle: str | None
    model_name: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class LeadScoreListData(BaseModel):
    """Collection payload for Lead Score responses."""

    items: list[LeadScoreRead]
    pagination: PaginationMeta


class LeadScoreListResponse(BaseModel):
    """Envelope for Lead Score list responses."""

    data: LeadScoreListData
    message: str
