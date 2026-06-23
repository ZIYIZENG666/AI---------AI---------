"""HTTP routes for the company module."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.company.repository import CompanyRepository
from app.modules.company.schemas import (
    CompanyCreate,
    CompanyListData,
    CompanyListResponse,
    CompanyRead,
    CompanyResponse,
    CompanyUpdate,
    PaginationMeta,
)
from app.modules.company.service import CompanyService


router = APIRouter(prefix="/companies", tags=["company"])


def get_company_service(db: Session = Depends(get_db)) -> CompanyService:
    """Create a request-scoped company service."""

    repository = CompanyRepository(db)
    return CompanyService(repository)


@router.post("", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(
    payload: CompanyCreate,
    service: CompanyService = Depends(get_company_service),
) -> CompanyResponse:
    company = service.create_company(payload)
    return CompanyResponse(
        data=CompanyRead.model_validate(company),
        message="Company profile created successfully.",
    )


@router.get("", response_model=CompanyListResponse)
def list_companies(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: CompanyService = Depends(get_company_service),
) -> CompanyListResponse:
    result = service.list_companies(limit=limit, offset=offset)
    return CompanyListResponse(
        data=CompanyListData(
            items=[CompanyRead.model_validate(item) for item in result["items"]],
            pagination=PaginationMeta(
                total=result["total"],
                limit=result["limit"],
                offset=result["offset"],
            ),
        ),
        message="Company profiles fetched successfully.",
    )


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: str,
    service: CompanyService = Depends(get_company_service),
) -> CompanyResponse:
    company = service.get_company(company_id)
    return CompanyResponse(
        data=CompanyRead.model_validate(company),
        message="Company profile fetched successfully.",
    )


@router.patch("/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: str,
    payload: CompanyUpdate,
    service: CompanyService = Depends(get_company_service),
) -> CompanyResponse:
    company = service.update_company(company_id=company_id, payload=payload)
    return CompanyResponse(
        data=CompanyRead.model_validate(company),
        message="Company profile updated successfully.",
    )
