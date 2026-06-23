"""HTTP routes for the product card module."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.company.repository import CompanyRepository
from app.modules.knowledge.repository import KnowledgeRepository
from app.modules.products.repository import ProductRepository
from app.modules.products.schemas import (
    PaginationMeta,
    ProductCardListData,
    ProductCardListResponse,
    ProductCardRead,
    ProductCardResponse,
)
from app.modules.products.service import ProductService


router = APIRouter(tags=["products"])


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    """Create a request-scoped product card service."""

    return ProductService(
        repository=ProductRepository(db),
        company_repository=CompanyRepository(db),
        knowledge_repository=KnowledgeRepository(db),
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


@router.get(
    "/companies/{company_id}/product-cards",
    response_model=ProductCardListResponse,
)
def list_product_cards(
    company_id: str,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: ProductService = Depends(get_product_service),
) -> ProductCardListResponse:
    result = service.list_product_cards(
        company_id=company_id,
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


@router.post(
    "/product-cards/{product_card_id}/reject",
    response_model=ProductCardResponse,
)
def reject_product_card(
    product_card_id: str,
    service: ProductService = Depends(get_product_service),
) -> ProductCardResponse:
    product_card = service.reject_product_card(product_card_id)
    return ProductCardResponse(
        data=ProductCardRead.model_validate(product_card),
        message="Product card rejected successfully.",
    )
