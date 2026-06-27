"""Pydantic schemas for the product card module."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


ProductCardStatus = Literal["draft", "confirmed"]
ProductCardSourceType = Literal["ai_generated", "manual"]


class ProductCardCreate(BaseModel):
    """Request schema for user-created product cards."""

    model_config = ConfigDict(extra="forbid")

    company_id: str
    name: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    target_customer: str = Field(min_length=1)
    pain_points: list[str] = Field(default_factory=list)
    value_proposition: str = Field(min_length=1)
    use_cases: list[str] = Field(default_factory=list)
    differentiators: list[str] = Field(default_factory=list)


class ProductCardUpdate(BaseModel):
    """Request schema for editable product card fields."""

    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1)
    target_customer: str | None = Field(default=None, min_length=1)
    pain_points: list[str] | None = None
    value_proposition: str | None = Field(default=None, min_length=1)
    use_cases: list[str] | None = None
    differentiators: list[str] | None = None

    @model_validator(mode="after")
    def reject_explicit_nulls(self) -> "ProductCardUpdate":
        """Keep nullable patch fields from becoming nullable database writes."""

        for field_name in self.model_fields_set:
            if getattr(self, field_name) is None:
                raise ValueError(f"{field_name} cannot be null.")
        return self


class ProductCardRead(BaseModel):
    """Response schema for a product card."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    company_id: str
    name: str
    description: str
    target_customer: str
    pain_points: list[str]
    value_proposition: str
    use_cases: list[str]
    differentiators: list[str]
    source_knowledge_item_ids: list[str]
    source_type: ProductCardSourceType
    status: ProductCardStatus
    created_at: datetime
    updated_at: datetime


class PaginationMeta(BaseModel):
    """Pagination metadata for product card lists."""

    total: int
    limit: int
    offset: int


class ProductCardListData(BaseModel):
    """Collection payload for product card list responses."""

    items: list[ProductCardRead]
    pagination: PaginationMeta


class ProductCardResponse(BaseModel):
    """Envelope for single-product-card responses."""

    data: ProductCardRead
    message: str


class ProductCardListResponse(BaseModel):
    """Envelope for product card collection responses."""

    data: ProductCardListData
    message: str


class ProductCardDeleteData(BaseModel):
    """Payload returned after a product card is deleted."""

    id: str
    deleted: bool


class ProductCardDeleteResponse(BaseModel):
    """Envelope for product card deletion responses."""

    data: ProductCardDeleteData
    message: str
