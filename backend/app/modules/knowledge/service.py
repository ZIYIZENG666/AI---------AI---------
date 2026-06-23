"""Service logic for the knowledge module."""

from app.core.errors import AppError
from app.modules.company.repository import CompanyRepository
from app.modules.knowledge.repository import KnowledgeRepository
from app.modules.sources.models import CompanySource
from app.modules.sources.repository import SourceRepository


class DeterministicKnowledgeDraftGenerator:
    """Build a transparent draft without calling an external AI provider."""

    def generate(self, source: CompanySource) -> dict:
        if source.raw_content:
            content = source.raw_content
        else:
            content = f"Manual review required for source URL: {source.url}"

        return {
            "company_id": source.company_id,
            "source_id": source.id,
            "category": "source_summary",
            "title": f"Draft: {source.title}",
            "content": content,
            "status": "draft",
            "confidence": None,
        }


class KnowledgeService:
    """Business service for reviewable company knowledge."""

    def __init__(
        self,
        repository: KnowledgeRepository,
        source_repository: SourceRepository,
        company_repository: CompanyRepository,
        generator: DeterministicKnowledgeDraftGenerator | None = None,
    ) -> None:
        self.repository = repository
        self.source_repository = source_repository
        self.company_repository = company_repository
        self.generator = generator or DeterministicKnowledgeDraftGenerator()

    def create_draft_from_source(self, source_id: str):
        source = self.source_repository.get_by_id(source_id)
        if source is None:
            raise AppError(
                message="Company source not found.",
                status_code=404,
                code="source_not_found",
            )

        return self.repository.create(self.generator.generate(source))

    def list_knowledge(
        self,
        company_id: str,
        status_filter: str | None,
        limit: int,
        offset: int,
    ) -> dict:
        self._require_company(company_id)
        items, total = self.repository.list_by_company(
            company_id=company_id,
            status_filter=status_filter,
            limit=limit,
            offset=offset,
        )
        return {
            "items": items,
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    def confirm_knowledge(self, knowledge_id: str):
        knowledge = self._get_knowledge(knowledge_id)
        self._require_draft(knowledge.status)
        return self.repository.update_status(knowledge, "confirmed")

    def reject_knowledge(self, knowledge_id: str):
        knowledge = self._get_knowledge(knowledge_id)
        self._require_draft(knowledge.status)
        return self.repository.update_status(knowledge, "rejected")

    def _get_knowledge(self, knowledge_id: str):
        knowledge = self.repository.get_by_id(knowledge_id)
        if knowledge is None:
            raise AppError(
                message="Knowledge item not found.",
                status_code=404,
                code="knowledge_not_found",
            )
        return knowledge

    def _require_company(self, company_id: str) -> None:
        if self.company_repository.get_by_id(company_id) is None:
            raise AppError(
                message="Company profile not found.",
                status_code=404,
                code="company_not_found",
            )

    @staticmethod
    def _require_draft(current_status: str) -> None:
        if current_status != "draft":
            raise AppError(
                message="Only draft knowledge items can be reviewed.",
                status_code=409,
                code="knowledge_not_draft",
            )
