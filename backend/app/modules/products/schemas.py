"""Pydantic schemas for the product card module."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


ProductCardStatus = Literal["draft", "confirmed", "rejected"]


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
