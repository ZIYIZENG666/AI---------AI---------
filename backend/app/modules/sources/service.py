"""Service logic for the sources module."""

from app.core.errors import AppError
from app.modules.company.repository import CompanyRepository
from app.modules.sources.repository import SourceRepository
from app.modules.sources.schemas import SourceCreate


class SourceService:
    """Business service for company sources."""

    def __init__(
        self,
        repository: SourceRepository,
        company_repository: CompanyRepository,
    ) -> None:
        self.repository = repository
        self.company_repository = company_repository

    def create_source(self, company_id: str, payload: SourceCreate):
        self._require_company(company_id)
        data = payload.model_dump(mode="json")
        data.update(company_id=company_id, status="ready")
        return self.repository.create(data)

    def list_sources(self, company_id: str, limit: int, offset: int) -> dict:
        self._require_company(company_id)
        items, total = self.repository.list_by_company(
            company_id=company_id,
            limit=limit,
            offset=offset,
        )
        return {
            "items": items,
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    def get_source(self, source_id: str):
        source = self.repository.get_by_id(source_id)
        if source is None:
            raise AppError(
                message="Company source not found.",
                status_code=404,
                code="source_not_found",
            )
        return source

    def _require_company(self, company_id: str) -> None:
        if self.company_repository.get_by_id(company_id) is None:
            raise AppError(
                message="Company profile not found.",
                status_code=404,
                code="company_not_found",
            )
