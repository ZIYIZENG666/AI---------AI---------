"""Service logic for the company module."""

from app.core.errors import AppError
from app.modules.company.repository import CompanyRepository
from app.modules.company.schemas import CompanyCreate, CompanyUpdate


class CompanyService:
    """Business service for company profiles."""

    def __init__(self, repository: CompanyRepository) -> None:
        self.repository = repository

    def create_company(self, payload: CompanyCreate):
        return self.repository.create(payload.model_dump())

    def list_companies(self, limit: int, offset: int) -> dict:
        items, total = self.repository.list(limit=limit, offset=offset)
        return {
            "items": items,
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    def get_company(self, company_id: str):
        company = self.repository.get_by_id(company_id)
        if company is None:
            raise AppError(
                message="Company profile not found.",
                status_code=404,
                code="company_not_found",
            )
        return company

    def update_company(self, company_id: str, payload: CompanyUpdate):
        company = self.get_company(company_id)
        return self.repository.update(company, payload.model_dump(exclude_unset=True))
