"""HTTP routes for the campaigns module."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.campaigns.repository import CampaignRepository
from app.modules.campaigns.schemas import (
    CampaignCreate,
    CampaignDeleteData,
    CampaignDeleteResponse,
    CampaignListData,
    CampaignListResponse,
    CampaignRead,
    CampaignResponse,
    CampaignStatus,
    CampaignUpdate,
    PaginationMeta,
)
from app.modules.campaigns.service import CampaignService
from app.modules.company.repository import CompanyRepository
from app.modules.products.repository import ProductRepository


router = APIRouter(tags=["campaigns"])


def get_campaign_service(db: Session = Depends(get_db)) -> CampaignService:
    """Create a request-scoped Campaign service."""

    return CampaignService(
        repository=CampaignRepository(db),
        company_repository=CompanyRepository(db),
        product_repository=ProductRepository(db),
    )


@router.post(
    "/companies/{company_id}/campaigns",
    response_model=CampaignResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_campaign(
    company_id: str,
    payload: CampaignCreate,
    service: CampaignService = Depends(get_campaign_service),
) -> CampaignResponse:
    campaign = service.create_campaign(company_id, payload.model_dump())
    return CampaignResponse(
        data=CampaignRead.model_validate(campaign),
        message="Campaign created successfully.",
    )


@router.get(
    "/companies/{company_id}/campaigns",
    response_model=CampaignListResponse,
)
def list_campaigns(
    company_id: str,
    status_filter: CampaignStatus | None = Query(default=None, alias="status"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: CampaignService = Depends(get_campaign_service),
) -> CampaignListResponse:
    result = service.list_campaigns(
        company_id=company_id,
        status_filter=status_filter,
        limit=limit,
        offset=offset,
    )
    return CampaignListResponse(
        data=CampaignListData(
            items=[CampaignRead.model_validate(item) for item in result["items"]],
            pagination=PaginationMeta(
                total=result["total"],
                limit=result["limit"],
                offset=result["offset"],
            ),
        ),
        message="Campaigns fetched successfully.",
    )


@router.get(
    "/campaigns/{campaign_id}",
    response_model=CampaignResponse,
)
def get_campaign(
    campaign_id: str,
    service: CampaignService = Depends(get_campaign_service),
) -> CampaignResponse:
    campaign = service.get_campaign(campaign_id)
    return CampaignResponse(
        data=CampaignRead.model_validate(campaign),
        message="Campaign fetched successfully.",
    )


@router.patch(
    "/campaigns/{campaign_id}",
    response_model=CampaignResponse,
)
def update_campaign(
    campaign_id: str,
    payload: CampaignUpdate,
    service: CampaignService = Depends(get_campaign_service),
) -> CampaignResponse:
    campaign = service.update_campaign(
        campaign_id,
        payload.model_dump(exclude_unset=True),
    )
    return CampaignResponse(
        data=CampaignRead.model_validate(campaign),
        message="Campaign updated successfully.",
    )


@router.delete(
    "/campaigns/{campaign_id}",
    response_model=CampaignDeleteResponse,
)
def delete_campaign(
    campaign_id: str,
    service: CampaignService = Depends(get_campaign_service),
) -> CampaignDeleteResponse:
    deleted_id = service.delete_campaign(campaign_id)
    return CampaignDeleteResponse(
        data=CampaignDeleteData(id=deleted_id, deleted=True),
        message="Campaign deleted successfully.",
    )


@router.post(
    "/campaigns/{campaign_id}/confirm",
    response_model=CampaignResponse,
)
def confirm_campaign(
    campaign_id: str,
    service: CampaignService = Depends(get_campaign_service),
) -> CampaignResponse:
    campaign = service.confirm_campaign(campaign_id)
    return CampaignResponse(
        data=CampaignRead.model_validate(campaign),
        message="Campaign confirmed successfully.",
    )


@router.post(
    "/campaigns/{campaign_id}/archive",
    response_model=CampaignResponse,
)
def archive_campaign(
    campaign_id: str,
    service: CampaignService = Depends(get_campaign_service),
) -> CampaignResponse:
    campaign = service.archive_campaign(campaign_id)
    return CampaignResponse(
        data=CampaignRead.model_validate(campaign),
        message="Campaign archived successfully.",
    )


@router.post(
    "/campaigns/{campaign_id}/duplicate",
    response_model=CampaignResponse,
    status_code=status.HTTP_201_CREATED,
)
def duplicate_campaign(
    campaign_id: str,
    service: CampaignService = Depends(get_campaign_service),
) -> CampaignResponse:
    campaign = service.duplicate_campaign(campaign_id)
    return CampaignResponse(
        data=CampaignRead.model_validate(campaign),
        message="Campaign duplicated successfully.",
    )
