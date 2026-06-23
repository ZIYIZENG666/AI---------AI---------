"""Pydantic schemas for the sources module."""

from datetime import datetime
from typing import Literal

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, model_validator


SourceType = Literal["text", "url"]
SourceStatus = Literal["ready"]


class SourceCreate(BaseModel):
    """Request schema for adding a company source."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    source_type: SourceType
    title: str = Field(min_length=1, max_length=255)
    url: AnyHttpUrl | None = None
    raw_content: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_content_for_source_type(self) -> "SourceCreate":
        if self.source_type == "text":
            if self.raw_content is None:
                raise ValueError("raw_content is required for text sources.")
            if self.url is not None:
                raise ValueError("url is only allowed for URL sources.")
        elif self.url is None:
            raise ValueError("url is required for URL sources.")

        return self


class SourceRead(BaseModel):
    """Response schema for a company source."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    company_id: str
    source_type: SourceType
    title: str
    url: str | None
    raw_content: str | None
    status: SourceStatus
    created_at: datetime
    updated_at: datetime


class PaginationMeta(BaseModel):
    """Pagination metadata for source lists."""

    total: int
    limit: int
    offset: int


class SourceListData(BaseModel):
    """Collection payload for source list responses."""

    items: list[SourceRead]
    pagination: PaginationMeta


class SourceResponse(BaseModel):
    """Envelope for single-source responses."""

    data: SourceRead
    message: str


class SourceListResponse(BaseModel):
    """Envelope for source collection responses."""

    data: SourceListData
    message: str
