"""Repository logic for the discovery module."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.discovery.models import Lead


class DiscoveryRepository:
    """Database access for discovered leads."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create_many(self, leads_data: list[dict]) -> list[Lead]:
        leads = [Lead(**data) for data in leads_data]
        self.session.add_all(leads)
        self.session.commit()
        for lead in leads:
            self.session.refresh(lead)
        return leads

    def get_by_id(self, lead_id: str) -> Lead | None:
        return self.session.get(Lead, lead_id)

    def update(self, lead: Lead, data: dict) -> Lead:
        for field_name, value in data.items():
            setattr(lead, field_name, value)

        self.session.add(lead)
        self.session.commit()
        self.session.refresh(lead)
        return lead

    def list_by_campaign(
        self,
        campaign_id: str,
        limit: int,
        offset: int,
    ) -> tuple[list[Lead], int]:
        filters = [Lead.campaign_id == campaign_id]
        total = self.session.scalar(
            select(func.count()).select_from(Lead).where(*filters)
        ) or 0
        items = list(
            self.session.scalars(
                select(Lead)
                .where(*filters)
                .order_by(Lead.created_at.desc(), Lead.id.desc())
                .limit(limit)
                .offset(offset)
            )
        )
        return items, total

    def existing_normalized_websites(self, campaign_id: str) -> set[str]:
        return set(
            self.session.scalars(
                select(Lead.normalized_website).where(Lead.campaign_id == campaign_id)
            )
        )

    def has_other_lead_with_normalized_website(
        self,
        campaign_id: str,
        normalized_website: str,
        exclude_lead_id: str,
    ) -> bool:
        count = self.session.scalar(
            select(func.count())
            .select_from(Lead)
            .where(
                Lead.campaign_id == campaign_id,
                Lead.normalized_website == normalized_website,
                Lead.id != exclude_lead_id,
            )
        )
        return bool(count)
