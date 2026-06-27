"""HTTP routes for the product card module."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.campaigns.repository import CampaignRepository
from app.modules.company.repository import CompanyRepository
from app.modules.knowledge.repository import KnowledgeRepository
from app.modules.products.repository import ProductRepository
from app.modules.products.schemas import (
    PaginationMeta,
    ProductCardCreate,
    ProductCardDeleteData,
    ProductCardDeleteResponse,
    ProductCardListData,
    ProductCardListResponse,
    ProductCardRead,
    ProductCardResponse,
    ProductCardStatus,
    ProductCardUpdate,
)
from app.modules.products.service import ProductService


router = APIRouter(tags=["products"])


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    """Create a request-scoped product card service."""

    return ProductService(
        repository=ProductRepository(db),
        company_repository=CompanyRepository(db),
        knowledge_repository=KnowledgeRepository(db),
        campaign_repository=CampaignRepository(db),
    )


@router.post(
    "/companies/{company_id}/product-cards",
    response_model=ProductCardResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product_card(
    company_id: str,
    service: ProductService = Depends(get_product_service),
) -> ProductCardResponse:
    product_card = service.create_product_card(company_id)
    return ProductCardResponse(
        data=ProductCardRead.model_validate(product_card),
        message="Product card created successfully.",
    )


@router.post(
    "/product-cards",
    response_model=ProductCardResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_manual_product_card(
    payload: ProductCardCreate,
    service: ProductService = Depends(get_product_service),
) -> ProductCardResponse:
    product_card = service.create_manual_product_card(payload.model_dump())
    return ProductCardResponse(
        data=ProductCardRead.model_validate(product_card),
        message="Product card created successfully.",
    )


@router.get(
    "/product-cards",
    response_model=ProductCardListResponse,
)
def list_all_product_cards(
    status_filter: ProductCardStatus | None = Query(default=None, alias="status"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: ProductService = Depends(get_product_service),
) -> ProductCardListResponse:
    result = service.list_product_cards(
        status_filter=status_filter,
        limit=limit,
        offset=offset,
    )
    return ProductCardListResponse(
        data=ProductCardListData(
            items=[ProductCardRead.model_validate(item) for item in result["items"]],
            pagination=PaginationMeta(
                total=result["total"],
                limit=result["limit"],
                offset=result["offset"],
            ),
        ),
        message="Product cards fetched successfully.",
    )


@router.get(
    "/companies/{company_id}/product-cards",
    response_model=ProductCardListResponse,
)
def list_product_cards(
    company_id: str,
    status_filter: ProductCardStatus | None = Query(default=None, alias="status"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: ProductService = Depends(get_product_service),
) -> ProductCardListResponse:
    result = service.list_product_cards(
        company_id=company_id,
        status_filter=status_filter,
        limit=limit,
        offset=offset,
    )
    return ProductCardListResponse(
        data=ProductCardListData(
            items=[ProductCardRead.model_validate(item) for item in result["items"]],
            pagination=PaginationMeta(
                total=result["total"],
                limit=result["limit"],
                offset=result["offset"],
            ),
        ),
        message="Product cards fetched successfully.",
    )


@router.get(
    "/product-cards/{product_card_id}",
    response_model=ProductCardResponse,
)
def get_product_card(
    product_card_id: str,
    service: ProductService = Depends(get_product_service),
) -> ProductCardResponse:
    product_card = service.get_product_card(product_card_id)
    return ProductCardResponse(
        data=ProductCardRead.model_validate(product_card),
        message="Product card fetched successfully.",
    )


@router.patch(
    "/product-cards/{product_card_id}",
    response_model=ProductCardResponse,
)
def update_product_card(
    product_card_id: str,
    payload: ProductCardUpdate,
    service: ProductService = Depends(get_product_service),
) -> ProductCardResponse:
    product_card = service.update_product_card(
        product_card_id,
        payload.model_dump(exclude_unset=True),
    )
    return ProductCardResponse(
        data=ProductCardRead.model_validate(product_card),
        message="Product card updated successfully.",
    )


@router.post(
    "/product-cards/{product_card_id}/confirm",
    response_model=ProductCardResponse,
)
def confirm_product_card(
    product_card_id: str,
    service: ProductService = Depends(get_product_service),
) -> ProductCardResponse:
    product_card = service.confirm_product_card(product_card_id)
    return ProductCardResponse(
        data=ProductCardRead.model_validate(product_card),
        message="Product card confirmed successfully.",
    )


@router.delete(
    "/product-cards/{product_card_id}",
    response_model=ProductCardDeleteResponse,
)
def delete_product_card(
    product_card_id: str,
    service: ProductService = Depends(get_product_service),
) -> ProductCardDeleteResponse:
    deleted_id = service.delete_product_card(product_card_id)
    return ProductCardDeleteResponse(
        data=ProductCardDeleteData(id=deleted_id, deleted=True),
        message="Product card deleted successfully.",
    )
