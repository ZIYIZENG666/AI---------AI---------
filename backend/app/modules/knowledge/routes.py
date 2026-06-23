"""HTTP routes for the knowledge module."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.company.repository import CompanyRepository
from app.modules.knowledge.repository import KnowledgeRepository
from app.modules.knowledge.schemas import (
    KnowledgeListData,
    KnowledgeListResponse,
    KnowledgeRead,
    KnowledgeResponse,
    KnowledgeStatus,
    PaginationMeta,
)
from app.modules.knowledge.service import KnowledgeService
from app.modules.sources.repository import SourceRepository


router = APIRouter(tags=["knowledge"])


def get_knowledge_service(db: Session = Depends(get_db)) -> KnowledgeService:
    """Create a request-scoped knowledge service."""

    return KnowledgeService(
        repository=KnowledgeRepository(db),
        source_repository=SourceRepository(db),
        company_repository=CompanyRepository(db),
    )


@router.post(
    "/sources/{source_id}/knowledge-drafts",
    response_model=KnowledgeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_knowledge_draft(
    source_id: str,
    service: KnowledgeService = Depends(get_knowledge_service),
) -> KnowledgeResponse:
    knowledge = service.create_draft_from_source(source_id)
    return KnowledgeResponse(
        data=KnowledgeRead.model_validate(knowledge),
        message="Knowledge draft created successfully.",
    )


@router.get(
    "/companies/{company_id}/knowledge",
    response_model=KnowledgeListResponse,
)
def list_knowledge(
    company_id: str,
    knowledge_status: KnowledgeStatus | None = Query(default=None, alias="status"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: KnowledgeService = Depends(get_knowledge_service),
) -> KnowledgeListResponse:
    result = service.list_knowledge(
        company_id=company_id,
        status_filter=knowledge_status,
        limit=limit,
        offset=offset,
    )
    return KnowledgeListResponse(
        data=KnowledgeListData(
            items=[KnowledgeRead.model_validate(item) for item in result["items"]],
            pagination=PaginationMeta(
                total=result["total"],
                limit=result["limit"],
                offset=result["offset"],
            ),
        ),
        message="Company knowledge fetched successfully.",
    )


@router.post(
    "/knowledge/{knowledge_id}/confirm",
    response_model=KnowledgeResponse,
)
def confirm_knowledge(
    knowledge_id: str,
    service: KnowledgeService = Depends(get_knowledge_service),
) -> KnowledgeResponse:
    knowledge = service.confirm_knowledge(knowledge_id)
    return KnowledgeResponse(
        data=KnowledgeRead.model_validate(knowledge),
        message="Knowledge item confirmed successfully.",
    )


@router.post(
    "/knowledge/{knowledge_id}/reject",
    response_model=KnowledgeResponse,
)
def reject_knowledge(
    knowledge_id: str,
    service: KnowledgeService = Depends(get_knowledge_service),
) -> KnowledgeResponse:
    knowledge = service.reject_knowledge(knowledge_id)
    return KnowledgeResponse(
        data=KnowledgeRead.model_validate(knowledge),
        message="Knowledge item rejected successfully.",
    )
