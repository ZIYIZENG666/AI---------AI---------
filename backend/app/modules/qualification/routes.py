"""HTTP routes for the qualification module."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.campaigns.repository import CampaignRepository
from app.modules.discovery.repository import DiscoveryRepository
from app.modules.intelligence.repository import IntelligenceRepository
from app.modules.qualification.repository import QualificationRepository
from app.modules.qualification.schemas import (
    LeadScoreListData,
    LeadScoreListResponse,
    LeadScoreRead,
    LeadScoringStartData,
    LeadScoringStartResponse,
    LeadScoringTaskListData,
    LeadScoringTaskListResponse,
)
from app.modules.qualification.service import QualificationService
from app.modules.tasks.repository import TaskRepository
from app.modules.tasks.schemas import PaginationMeta, TaskRunRead
from app.providers.llm_provider import MockLeadScoringProvider


router = APIRouter(tags=["qualification"])


def get_qualification_service(db: Session = Depends(get_db)) -> QualificationService:
    """Create a request-scoped Qualification service."""

    return QualificationService(
        repository=QualificationRepository(db),
        discovery_repository=DiscoveryRepository(db),
        campaign_repository=CampaignRepository(db),
        intelligence_repository=IntelligenceRepository(db),
        task_repository=TaskRepository(db),
        scoring_provider=MockLeadScoringProvider(),
    )


@router.post(
    "/leads/{lead_id}/scoring",
    response_model=LeadScoringStartResponse,
    status_code=status.HTTP_201_CREATED,
)
def start_lead_scoring(
    lead_id: str,
    service: QualificationService = Depends(get_qualification_service),
) -> LeadScoringStartResponse:
    data = service.start_lead_scoring(lead_id)
    return LeadScoringStartResponse(
        data=LeadScoringStartData(**data),
        message="Lead scoring task created successfully.",
    )


@router.get(
    "/leads/{lead_id}/scoring/tasks",
    response_model=LeadScoringTaskListResponse,
)
def list_lead_scoring_tasks(
    lead_id: str,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: QualificationService = Depends(get_qualification_service),
) -> LeadScoringTaskListResponse:
    result = service.list_tasks_for_lead(
        lead_id=lead_id,
        limit=limit,
        offset=offset,
    )
    return LeadScoringTaskListResponse(
        data=LeadScoringTaskListData(
            items=[TaskRunRead.model_validate(item) for item in result["items"]],
            pagination=PaginationMeta(
                total=result["total"],
                limit=result["limit"],
                offset=result["offset"],
            ),
        ),
        message="Lead scoring tasks fetched successfully.",
    )


@router.get(
    "/leads/{lead_id}/scores",
    response_model=LeadScoreListResponse,
)
def list_lead_scores(
    lead_id: str,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: QualificationService = Depends(get_qualification_service),
) -> LeadScoreListResponse:
    result = service.list_scores_for_lead(
        lead_id=lead_id,
        limit=limit,
        offset=offset,
    )
    return LeadScoreListResponse(
        data=LeadScoreListData(
            items=[LeadScoreRead.model_validate(item) for item in result["items"]],
            pagination=PaginationMeta(
                total=result["total"],
                limit=result["limit"],
                offset=result["offset"],
            ),
        ),
        message="Lead scores fetched successfully.",
    )
