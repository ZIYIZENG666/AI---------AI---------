"""Pydantic schemas for the company module."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CompanyPayloadBase(BaseModel):
    """Shared writable fields for company payloads."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    owner_id: str | None = Field(default=None, max_length=36)
    workspace_id: str | None = Field(default=None, max_length=36)
    website: str | None = Field(default=None, max_length=500)
    industry: str | None = Field(default=None, max_length=255)
    description: str | None = None
    target_market: str | None = Field(default=None, max_length=255)
    value_proposition: str | None = None


class CompanyCreate(CompanyPayloadBase):
    """Request schema for creating a company profile."""

    name: str = Field(min_length=1, max_length=255)


class CompanyUpdate(CompanyPayloadBase):
    """Request schema for partial company profile updates."""

    name: str | None = Field(default=None, min_length=1, max_length=255)

    @model_validator(mode="after")
    def validate_has_changes(self) -> "CompanyUpdate":
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided for update.")
        return self


class CompanyRead(BaseModel):
    """Response schema for a company profile."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    owner_id: str | None
    workspace_id: str | None
    name: str
    website: str | None
    industry: str | None
    description: str | None
    target_market: str | None
    value_proposition: str | None
    created_at: datetime
    updated_at: datetime


class PaginationMeta(BaseModel):
    """Pagination metadata for list responses."""

    total: int
    limit: int
    offset: int


class CompanyListData(BaseModel):
    """Collection payload for company list responses."""

    items: list[CompanyRead]
    pagination: PaginationMeta


class CompanyResponse(BaseModel):
    """Envelope for single-company responses."""

    data: CompanyRead
    message: str


class CompanyListResponse(BaseModel):
    """Envelope for company collection responses."""

    data: CompanyListData
    message: str
