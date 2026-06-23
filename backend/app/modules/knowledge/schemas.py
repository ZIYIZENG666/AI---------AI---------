"""Pydantic schemas for the knowledge module."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


KnowledgeStatus = Literal["draft", "confirmed", "rejected"]


class KnowledgeRead(BaseModel):
    """Response schema for a knowledge item."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    company_id: str
    source_id: str | None
    category: str
    title: str
    content: str
    status: KnowledgeStatus
    confidence: float | None
    created_at: datetime
    updated_at: datetime


class PaginationMeta(BaseModel):
    """Pagination metadata for knowledge lists."""

    total: int
    limit: int
    offset: int


class KnowledgeListData(BaseModel):
    """Collection payload for knowledge list responses."""

    items: list[KnowledgeRead]
    pagination: PaginationMeta


class KnowledgeResponse(BaseModel):
    """Envelope for single-knowledge responses."""

    data: KnowledgeRead
    message: str


class KnowledgeListResponse(BaseModel):
    """Envelope for knowledge collection responses."""

    data: KnowledgeListData
    message: str
