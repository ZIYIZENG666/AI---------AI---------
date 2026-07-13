"""HTTP routes for the discovery module."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.campaigns.repository import CampaignRepository
from app.modules.discovery.repository import DiscoveryRepository
from app.modules.discovery.schemas import (
    LeadDiscoveryStartData,
    LeadDiscoveryStartResponse,
    LeadDiscoveryTaskListData,
    LeadDiscoveryTaskListResponse,
    LeadListData,
    LeadListResponse,
    LeadRead,
)
from app.modules.discovery.service import DiscoveryService
from app.modules.tasks.repository import TaskRepository
from app.modules.tasks.schemas import PaginationMeta, TaskRunRead
from app.providers.search_provider import MockSearchProvider


router = APIRouter(tags=["discovery"])


def get_discovery_service(db: Session = Depends(get_db)) -> DiscoveryService:
    """Create a request-scoped Discovery service."""

    return DiscoveryService(
        repository=DiscoveryRepository(db),
        campaign_repository=CampaignRepository(db),
        task_repository=TaskRepository(db),
        search_provider=MockSearchProvider(),
    )


@router.post(
    "/campaigns/{campaign_id}/lead-discovery",
    response_model=LeadDiscoveryStartResponse,
    status_code=status.HTTP_201_CREATED,
)
def start_lead_discovery(
    campaign_id: str,
    service: DiscoveryService = Depends(get_discovery_service),
) -> LeadDiscoveryStartResponse:
    data = service.start_lead_discovery(campaign_id)
    return LeadDiscoveryStartResponse(
        data=LeadDiscoveryStartData(**data),
        message="Lead Discovery task created successfully.",
    )


@router.get(
    "/campaigns/{campaign_id}/lead-discovery/tasks",
    response_model=LeadDiscoveryTaskListResponse,
)
def list_lead_discovery_tasks(
    campaign_id: str,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: DiscoveryService = Depends(get_discovery_service),
) -> LeadDiscoveryTaskListResponse:
    result = service.list_tasks_for_campaign(
        campaign_id=campaign_id,
        limit=limit,
        offset=offset,
    )
    return LeadDiscoveryTaskListResponse(
        data=LeadDiscoveryTaskListData(
            items=[TaskRunRead.model_validate(item) for item in result["items"]],
            pagination=PaginationMeta(
                total=result["total"],
                limit=result["limit"],
                offset=result["offset"],
            ),
        ),
        message="Lead Discovery tasks fetched successfully.",
    )


@router.get(
    "/campaigns/{campaign_id}/leads",
    response_model=LeadListResponse,
)
def list_campaign_leads(
    campaign_id: str,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: DiscoveryService = Depends(get_discovery_service),
) -> LeadListResponse:
    result = service.list_leads_for_campaign(
        campaign_id=campaign_id,
        limit=limit,
        offset=offset,
    )
    return LeadListResponse(
        data=LeadListData(
            items=[LeadRead.model_validate(item) for item in result["items"]],
            pagination=PaginationMeta(
                total=result["total"],
                limit=result["limit"],
                offset=result["offset"],
            ),
        ),
        message="Leads fetched successfully.",
    )
