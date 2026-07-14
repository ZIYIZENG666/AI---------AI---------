"""HTTP routes for the intelligence module."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.campaigns.repository import CampaignRepository
from app.modules.discovery.repository import DiscoveryRepository
from app.modules.intelligence.repository import IntelligenceRepository
from app.modules.intelligence.schemas import (
    LeadIntelligenceListData,
    LeadIntelligenceListResponse,
    LeadIntelligenceRead,
    LeadValidationStartData,
    LeadValidationStartResponse,
    LeadValidationTaskListData,
    LeadValidationTaskListResponse,
)
from app.modules.intelligence.service import IntelligenceService
from app.modules.tasks.repository import TaskRepository
from app.modules.tasks.schemas import PaginationMeta, TaskRunRead
from app.providers.crawler_provider import MockCrawlerProvider


router = APIRouter(tags=["intelligence"])


def get_intelligence_service(db: Session = Depends(get_db)) -> IntelligenceService:
    """Create a request-scoped Intelligence service."""

    return IntelligenceService(
        repository=IntelligenceRepository(db),
        discovery_repository=DiscoveryRepository(db),
        campaign_repository=CampaignRepository(db),
        task_repository=TaskRepository(db),
        crawler_provider=MockCrawlerProvider(),
    )


@router.post(
    "/leads/{lead_id}/validation",
    response_model=LeadValidationStartResponse,
    status_code=status.HTTP_201_CREATED,
)
def start_lead_validation(
    lead_id: str,
    service: IntelligenceService = Depends(get_intelligence_service),
) -> LeadValidationStartResponse:
    data = service.start_lead_validation(lead_id)
    return LeadValidationStartResponse(
        data=LeadValidationStartData(**data),
        message="Lead validation task created successfully.",
    )


@router.get(
    "/leads/{lead_id}/validation/tasks",
    response_model=LeadValidationTaskListResponse,
)
def list_lead_validation_tasks(
    lead_id: str,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: IntelligenceService = Depends(get_intelligence_service),
) -> LeadValidationTaskListResponse:
    result = service.list_tasks_for_lead(
        lead_id=lead_id,
        limit=limit,
        offset=offset,
    )
    return LeadValidationTaskListResponse(
        data=LeadValidationTaskListData(
            items=[TaskRunRead.model_validate(item) for item in result["items"]],
            pagination=PaginationMeta(
                total=result["total"],
                limit=result["limit"],
                offset=result["offset"],
            ),
        ),
        message="Lead validation tasks fetched successfully.",
    )


@router.get(
    "/leads/{lead_id}/intelligence",
    response_model=LeadIntelligenceListResponse,
)
def list_lead_intelligence(
    lead_id: str,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: IntelligenceService = Depends(get_intelligence_service),
) -> LeadIntelligenceListResponse:
    result = service.list_intelligence_for_lead(
        lead_id=lead_id,
        limit=limit,
        offset=offset,
    )
    return LeadIntelligenceListResponse(
        data=LeadIntelligenceListData(
            items=[
                LeadIntelligenceRead.model_validate(item) for item in result["items"]
            ],
            pagination=PaginationMeta(
                total=result["total"],
                limit=result["limit"],
                offset=result["offset"],
            ),
        ),
        message="Lead intelligence fetched successfully.",
    )
