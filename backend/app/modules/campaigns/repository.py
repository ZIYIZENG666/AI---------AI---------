"""Repository logic for the campaigns module."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.campaigns.models import Campaign


class CampaignRepository:
    """Database access for Campaigns."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, data: dict) -> Campaign:
        campaign = Campaign(**data)
        self.session.add(campaign)
        self.session.commit()
        self.session.refresh(campaign)
        return campaign

    def list_by_company(
        self,
        company_id: str,
        limit: int,
        offset: int,
        status_filter: str | None = None,
    ) -> tuple[list[Campaign], int]:
        filters = [Campaign.company_id == company_id]
        if status_filter is None:
            filters.append(Campaign.status.in_(("draft", "confirmed")))
        else:
            filters.append(Campaign.status == status_filter)

        total = self.session.scalar(
            select(func.count()).select_from(Campaign).where(*filters)
        ) or 0
        items = list(
            self.session.scalars(
                select(Campaign)
                .where(*filters)
                .order_by(Campaign.created_at.desc(), Campaign.id.desc())
                .limit(limit)
                .offset(offset)
            )
        )
        return items, total

    def get_by_id(self, campaign_id: str) -> Campaign | None:
        return self.session.get(Campaign, campaign_id)

    def update(self, campaign: Campaign, data: dict) -> Campaign:
        for field_name, value in data.items():
            setattr(campaign, field_name, value)

        self.session.add(campaign)
        self.session.commit()
        self.session.refresh(campaign)
        return campaign

    def delete(self, campaign: Campaign) -> None:
        self.session.delete(campaign)
        self.session.commit()

    def is_product_card_referenced(self, product_card_id: str) -> bool:
        """Return whether any existing Campaign references a Product Card."""

        count = self.session.scalar(
            select(func.count())
            .select_from(Campaign)
            .where(Campaign.product_card_id == product_card_id)
        )
        return bool(count)
