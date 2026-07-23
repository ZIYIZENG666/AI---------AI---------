"""Repository logic for the qualification module."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.qualification.models import LeadScore


class QualificationRepository:
    """Database access for Lead Score records."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, data: dict) -> LeadScore:
        lead_score = LeadScore(**data)
        self.session.add(lead_score)
        self.session.commit()
        self.session.refresh(lead_score)
        return lead_score

    def has_score_for_lead(self, lead_id: str) -> bool:
        count = self.session.scalar(
            select(func.count())
            .select_from(LeadScore)
            .where(LeadScore.lead_id == lead_id)
        )
        return bool(count)

    def list_by_lead(
        self,
        lead_id: str,
        limit: int,
        offset: int,
    ) -> tuple[list[LeadScore], int]:
        filters = [LeadScore.lead_id == lead_id]
        total = self.session.scalar(
            select(func.count()).select_from(LeadScore).where(*filters)
        ) or 0
        items = list(
            self.session.scalars(
                select(LeadScore)
                .where(*filters)
                .order_by(LeadScore.created_at.desc(), LeadScore.id.desc())
                .limit(limit)
                .offset(offset)
            )
        )
        return items, total
