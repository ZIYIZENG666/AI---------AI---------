"""Pydantic schemas for the campaigns module."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


CampaignStatus = Literal["draft", "confirmed", "archived"]


class CampaignPayloadBase(BaseModel):
    """Shared Campaign draft fields accepted from clients."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    target_country: str | None = Field(default=None, max_length=255)
    target_region: str | None = Field(default=None, max_length=255)
    target_industry: str | None = Field(default=None, max_length=255)
    target_company_type: str | None = Field(default=None, max_length=255)
    target_role: str | None = Field(default=None, max_length=255)
    search_keywords: list[str] = Field(default_factory=list)
    qualification_criteria: list[str] = Field(default_factory=list)
    outreach_angle: str | None = None
    lead_limit: int = Field(default=20, ge=1, le=1000)


class CampaignCreate(CampaignPayloadBase):
    """Request schema for creating a Campaign draft."""

    product_card_id: str
    name: str = Field(min_length=1, max_length=255)


class CampaignUpdate(BaseModel):
    """Request schema for editable Campaign draft fields."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=1, max_length=255)
    target_country: str | None = Field(default=None, max_length=255)
    target_region: str | None = Field(default=None, max_length=255)
    target_industry: str | None = Field(default=None, max_length=255)
    target_company_type: str | None = Field(default=None, max_length=255)
    target_role: str | None = Field(default=None, max_length=255)
    search_keywords: list[str] | None = None
    qualification_criteria: list[str] | None = None
    outreach_angle: str | None = None
    lead_limit: int | None = Field(default=None, ge=1, le=1000)

    @model_validator(mode="after")
    def validate_patch_payload(self) -> "CampaignUpdate":
        """Reject empty patches and nulls for non-nullable fields."""

        if not self.model_fields_set:
            raise ValueError("At least one field must be provided for update.")

        non_nullable_fields = {
            "name",
            "search_keywords",
            "qualification_criteria",
            "lead_limit",
        }
        for field_name in non_nullable_fields.intersection(self.model_fields_set):
            if getattr(self, field_name) is None:
                raise ValueError(f"{field_name} cannot be null.")

        return self


class CampaignRead(BaseModel):
    """Response schema for a Campaign."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    company_id: str
    product_card_id: str
    product_card_snapshot: dict | None
    name: str
    target_country: str | None
    target_region: str | None
    target_industry: str | None
    target_company_type: str | None
    target_role: str | None
    search_keywords: list[str]
    qualification_criteria: list[str]
    outreach_angle: str | None
    lead_limit: int
    status: CampaignStatus
    created_at: datetime
    updated_at: datetime


class PaginationMeta(BaseModel):
    """Pagination metadata for Campaign lists."""

    total: int
    limit: int
    offset: int


class CampaignListData(BaseModel):
    """Collection payload for Campaign list responses."""

    items: list[CampaignRead]
    pagination: PaginationMeta


class CampaignResponse(BaseModel):
    """Envelope for a single-Campaign response."""

    data: CampaignRead
    message: str


class CampaignListResponse(BaseModel):
    """Envelope for Campaign collection responses."""

    data: CampaignListData
    message: str


class CampaignDeleteData(BaseModel):
    """Payload returned after a Campaign is deleted."""

    id: str
    deleted: bool


class CampaignDeleteResponse(BaseModel):
    """Envelope for Campaign deletion responses."""

    data: CampaignDeleteData
    message: str
