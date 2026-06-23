"""Repository logic for the sources module."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.sources.models import CompanySource


class SourceRepository:
    """Database access for company sources."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, data: dict) -> CompanySource:
        source = CompanySource(**data)
        self.session.add(source)
        self.session.commit()
        self.session.refresh(source)
        return source

    def list_by_company(
        self,
        company_id: str,
        limit: int,
        offset: int,
    ) -> tuple[list[CompanySource], int]:
        filters = (CompanySource.company_id == company_id,)
        total = self.session.scalar(
            select(func.count()).select_from(CompanySource).where(*filters)
        ) or 0
        items = list(
            self.session.scalars(
                select(CompanySource)
                .where(*filters)
                .order_by(CompanySource.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
        )
        return items, total

    def get_by_id(self, source_id: str) -> CompanySource | None:
        return self.session.get(CompanySource, source_id)
