"""Repository logic for the company module."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.company.models import CompanyProfile


class CompanyRepository:
    """Database access for company profiles."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, data: dict) -> CompanyProfile:
        company = CompanyProfile(**data)
        self.session.add(company)
        self.session.commit()
        self.session.refresh(company)
        return company

    def list(self, limit: int, offset: int) -> tuple[list[CompanyProfile], int]:
        total = self.session.scalar(
            select(func.count()).select_from(CompanyProfile)
        ) or 0
        items = list(
            self.session.scalars(
                select(CompanyProfile)
                .order_by(CompanyProfile.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
        )
        return items, total

    def get_by_id(self, company_id: str) -> CompanyProfile | None:
        return self.session.get(CompanyProfile, company_id)

    def update(self, company: CompanyProfile, data: dict) -> CompanyProfile:
        for field_name, value in data.items():
            setattr(company, field_name, value)

        self.session.add(company)
        self.session.commit()
        self.session.refresh(company)
        return company
