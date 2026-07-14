"""Repository logic for the intelligence module."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.intelligence.models import LeadIntelligence


class IntelligenceRepository:
    """Database access for Lead Intelligence records."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, data: dict) -> LeadIntelligence:
        intelligence = LeadIntelligence(**data)
        self.session.add(intelligence)
        self.session.commit()
        self.session.refresh(intelligence)
        return intelligence

    def list_by_lead(
        self,
        lead_id: str,
        limit: int,
        offset: int,
    ) -> tuple[list[LeadIntelligence], int]:
        filters = [LeadIntelligence.lead_id == lead_id]
        total = self.session.scalar(
            select(func.count()).select_from(LeadIntelligence).where(*filters)
        ) or 0
        items = list(
            self.session.scalars(
                select(LeadIntelligence)
                .where(*filters)
                .order_by(LeadIntelligence.created_at.desc(), LeadIntelligence.id.desc())
                .limit(limit)
                .offset(offset)
            )
        )
        return items, total
