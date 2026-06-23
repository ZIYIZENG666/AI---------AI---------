"""HTTP routes for the sources module."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.company.repository import CompanyRepository
from app.modules.sources.repository import SourceRepository
from app.modules.sources.schemas import (
    PaginationMeta,
    SourceCreate,
    SourceListData,
    SourceListResponse,
    SourceRead,
    SourceResponse,
)
from app.modules.sources.service import SourceService


router = APIRouter(tags=["sources"])


def get_source_service(db: Session = Depends(get_db)) -> SourceService:
    """Create a request-scoped source service."""

    return SourceService(
        repository=SourceRepository(db),
        company_repository=CompanyRepository(db),
    )


@router.post(
    "/companies/{company_id}/sources",
    response_model=SourceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_source(
    company_id: str,
    payload: SourceCreate,
    service: SourceService = Depends(get_source_service),
) -> SourceResponse:
    source = service.create_source(company_id=company_id, payload=payload)
    return SourceResponse(
        data=SourceRead.model_validate(source),
        message="Company source created successfully.",
    )


@router.get(
    "/companies/{company_id}/sources",
    response_model=SourceListResponse,
)
def list_sources(
    company_id: str,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: SourceService = Depends(get_source_service),
) -> SourceListResponse:
    result = service.list_sources(company_id=company_id, limit=limit, offset=offset)
    return SourceListResponse(
        data=SourceListData(
            items=[SourceRead.model_validate(item) for item in result["items"]],
            pagination=PaginationMeta(
                total=result["total"],
                limit=result["limit"],
                offset=result["offset"],
            ),
        ),
        message="Company sources fetched successfully.",
    )


@router.get("/sources/{source_id}", response_model=SourceResponse)
def get_source(
    source_id: str,
    service: SourceService = Depends(get_source_service),
) -> SourceResponse:
    source = service.get_source(source_id)
    return SourceResponse(
        data=SourceRead.model_validate(source),
        message="Company source fetched successfully.",
    )
