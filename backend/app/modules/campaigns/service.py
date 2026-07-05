"""Service logic for the campaigns module."""

from app.core.errors import AppError
from app.modules.campaigns.models import Campaign
from app.modules.campaigns.repository import CampaignRepository
from app.modules.company.repository import CompanyRepository
from app.modules.products.models import ProductCard
from app.modules.products.repository import ProductRepository


class CampaignService:
    """Business service for Campaign lifecycle operations."""

    editable_fields = {
        "name",
        "target_country",
        "target_region",
        "target_industry",
        "target_company_type",
        "target_role",
        "search_keywords",
        "qualification_criteria",
        "outreach_angle",
        "lead_limit",
    }

    def __init__(
        self,
        repository: CampaignRepository,
        company_repository: CompanyRepository,
        product_repository: ProductRepository,
    ) -> None:
        self.repository = repository
        self.company_repository = company_repository
        self.product_repository = product_repository

    def create_campaign(self, company_id: str, data: dict) -> Campaign:
        self._get_company(company_id)
        product_card = self._get_product_card_for_campaign(
            product_card_id=data["product_card_id"],
            company_id=company_id,
        )
        self._ensure_product_card_confirmed(product_card)

        create_data = {
            **data,
            "company_id": company_id,
            "product_card_snapshot": None,
            "status": "draft",
        }
        return self.repository.create(create_data)

    def list_campaigns(
        self,
        company_id: str,
        limit: int,
        offset: int,
        status_filter: str | None = None,
    ) -> dict:
        self._get_company(company_id)
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

    def get_campaign(self, campaign_id: str) -> Campaign:
        campaign = self.repository.get_by_id(campaign_id)
        if campaign is None:
            raise AppError(
                message="Campaign not found.",
                status_code=404,
                code="campaign_not_found",
            )
        return campaign

    def update_campaign(self, campaign_id: str, data: dict) -> Campaign:
        campaign = self.get_campaign(campaign_id)
        self._ensure_status(
            campaign,
            allowed_statuses={"draft"},
            message="Only draft Campaigns can be edited.",
        )

        editable_data = {
            field_name: value
            for field_name, value in data.items()
            if field_name in self.editable_fields
        }
        if not editable_data:
            return campaign

        return self.repository.update(campaign, editable_data)

    def delete_campaign(self, campaign_id: str) -> str:
        campaign = self.get_campaign(campaign_id)
        self._ensure_status(
            campaign,
            allowed_statuses={"draft"},
            message="Only draft Campaigns can be deleted.",
        )
        deleted_id = campaign.id
        self.repository.delete(campaign)
        return deleted_id

    def confirm_campaign(self, campaign_id: str) -> Campaign:
        campaign = self.get_campaign(campaign_id)
        if campaign.status == "confirmed":
            return campaign

        self._ensure_status(
            campaign,
            allowed_statuses={"draft"},
            message="Only draft Campaigns can be confirmed.",
        )
        product_card = self._get_product_card_for_campaign(
            product_card_id=campaign.product_card_id,
            company_id=campaign.company_id,
        )
        self._ensure_product_card_confirmed(product_card)

        return self.repository.update(
            campaign,
            {
                "status": "confirmed",
                "product_card_snapshot": self._snapshot_product_card(product_card),
            },
        )

    def archive_campaign(self, campaign_id: str) -> Campaign:
        campaign = self.get_campaign(campaign_id)
        self._ensure_status(
            campaign,
            allowed_statuses={"confirmed"},
            message="Only confirmed Campaigns can be archived.",
        )
        return self.repository.update(campaign, {"status": "archived"})

    def duplicate_campaign(self, campaign_id: str) -> Campaign:
        source = self.get_campaign(campaign_id)
        duplicate_data = {
            "company_id": source.company_id,
            "product_card_id": source.product_card_id,
            "product_card_snapshot": None,
            "name": source.name,
            "target_country": source.target_country,
            "target_region": source.target_region,
            "target_industry": source.target_industry,
            "target_company_type": source.target_company_type,
            "target_role": source.target_role,
            "search_keywords": list(source.search_keywords or []),
            "qualification_criteria": list(source.qualification_criteria or []),
            "outreach_angle": source.outreach_angle,
            "lead_limit": source.lead_limit,
            "status": "draft",
        }
        return self.repository.create(duplicate_data)

    def _get_company(self, company_id: str):
        company = self.company_repository.get_by_id(company_id)
        if company is None:
            raise AppError(
                message="Company profile not found.",
                status_code=404,
                code="company_not_found",
            )
        return company

    def _get_product_card_for_campaign(
        self,
        product_card_id: str,
        company_id: str,
    ) -> ProductCard:
        product_card = self.product_repository.get_by_id_and_company(
            product_card_id,
            company_id,
        )
        if product_card is None:
            raise AppError(
                message="Product card not found.",
                status_code=404,
                code="product_card_not_found",
            )
        return product_card

    @staticmethod
    def _ensure_product_card_confirmed(product_card: ProductCard) -> None:
        if product_card.status != "confirmed":
            raise AppError(
                message="Product card must be confirmed before Campaign use.",
                status_code=409,
                code="product_card_not_confirmed",
            )

    @staticmethod
    def _ensure_status(
        campaign: Campaign,
        allowed_statuses: set[str],
        message: str,
    ) -> None:
        if campaign.status not in allowed_statuses:
            raise AppError(
                message=message,
                status_code=409,
                code="invalid_campaign_status_transition",
            )

    @staticmethod
    def _snapshot_product_card(product_card: ProductCard) -> dict:
        return {
            "product_card_id": product_card.id,
            "company_id": product_card.company_id,
            "name": product_card.name,
            "description": product_card.description,
            "target_customer": product_card.target_customer,
            "pain_points": list(product_card.pain_points or []),
            "value_proposition": product_card.value_proposition,
            "use_cases": list(product_card.use_cases or []),
            "differentiators": list(product_card.differentiators or []),
            "source_type": product_card.source_type,
        }
