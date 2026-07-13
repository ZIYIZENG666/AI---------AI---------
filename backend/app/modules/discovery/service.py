"""Service logic for the discovery module."""

from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

from app.core.errors import AppError
from app.modules.campaigns.models import Campaign
from app.modules.campaigns.repository import CampaignRepository
from app.modules.discovery.repository import DiscoveryRepository
from app.modules.tasks.models import TaskRun
from app.modules.tasks.repository import TaskRepository
from app.providers.search_provider import SearchProvider


class DiscoveryService:
    """Business service for Phase 4 Lead Discovery."""

    def __init__(
        self,
        repository: DiscoveryRepository,
        campaign_repository: CampaignRepository,
        task_repository: TaskRepository,
        search_provider: SearchProvider,
    ) -> None:
        self.repository = repository
        self.campaign_repository = campaign_repository
        self.task_repository = task_repository
        self.search_provider = search_provider

    def start_lead_discovery(self, campaign_id: str) -> dict:
        campaign = self._get_campaign(campaign_id)
        self._ensure_campaign_can_start_discovery(campaign)
        if self.task_repository.has_blocking_lead_discovery_task(campaign_id):
            raise AppError(
                message="Lead Discovery already exists for this Campaign.",
                status_code=409,
                code="lead_discovery_already_exists",
            )

        search_query = self._build_search_query(campaign)
        task_run = self.task_repository.create(
            {
                "task_type": "lead_discovery",
                "related_entity_type": "campaign",
                "related_entity_id": campaign.id,
                "search_query": search_query,
                "provider_name": self.search_provider.provider_name,
                "status": "pending",
                "progress": 0,
            }
        )
        response_data = {
            "task_id": task_run.id,
            "status": "pending",
            "task_type": "lead_discovery",
            "campaign_id": campaign.id,
        }

        self._execute_mock_discovery(task_run, campaign, search_query)
        return response_data

    def list_tasks_for_campaign(
        self,
        campaign_id: str,
        limit: int,
        offset: int,
    ) -> dict:
        self._get_campaign(campaign_id)
        items, total = self.task_repository.list_lead_discovery_tasks_for_campaign(
            campaign_id=campaign_id,
            limit=limit,
            offset=offset,
        )
        return {
            "items": items,
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    def list_leads_for_campaign(
        self,
        campaign_id: str,
        limit: int,
        offset: int,
    ) -> dict:
        self._get_campaign(campaign_id)
        items, total = self.repository.list_by_campaign(
            campaign_id=campaign_id,
            limit=limit,
            offset=offset,
        )
        return {
            "items": items,
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    def _execute_mock_discovery(
        self,
        task_run: TaskRun,
        campaign: Campaign,
        search_query: str,
    ) -> None:
        started_at = datetime.now(timezone.utc)
        self.task_repository.update(
            task_run,
            {
                "status": "running",
                "progress": 10,
                "started_at": started_at,
                "error_message": None,
            },
        )
        try:
            results = self.search_provider.search(search_query, limit=campaign.lead_limit)
            leads_data = self._build_leads_data(
                results=results,
                campaign=campaign,
                task_run=task_run,
                search_query=search_query,
            )
            if leads_data:
                self.repository.create_many(leads_data)
            self.task_repository.update(
                task_run,
                {
                    "status": "completed",
                    "progress": 100,
                    "finished_at": datetime.now(timezone.utc),
                    "error_message": None,
                },
            )
        except Exception as exc:
            self.task_repository.update(
                task_run,
                {
                    "status": "failed",
                    "progress": 100,
                    "finished_at": datetime.now(timezone.utc),
                    "error_message": str(exc),
                },
            )

    def _build_leads_data(
        self,
        results: list[dict[str, Any]],
        campaign: Campaign,
        task_run: TaskRun,
        search_query: str,
    ) -> list[dict]:
        existing_websites = self.repository.existing_normalized_websites(campaign.id)
        leads_data: list[dict] = []

        for result in results:
            company_name = str(result.get("company_name") or "").strip()
            website = str(result.get("website") or "").strip()
            source_url = str(result.get("source_url") or "").strip()
            if not company_name or not website or not source_url:
                raise ValueError(
                    "Mock search results must include company_name, website, and source_url."
                )

            normalized_website = self._normalize_website(website)
            if normalized_website in existing_websites:
                continue

            existing_websites.add(normalized_website)
            leads_data.append(
                {
                    "campaign_id": campaign.id,
                    "task_run_id": task_run.id,
                    "company_name": company_name,
                    "website": website,
                    "normalized_name": self._normalize_name(company_name),
                    "normalized_website": normalized_website,
                    "description": result.get("description"),
                    "country": result.get("country"),
                    "industry": result.get("industry"),
                    "source_url": source_url,
                    "search_query": search_query,
                    "raw_snippet": result.get("raw_snippet"),
                    "discovery_reason": result.get("discovery_reason"),
                    "provider_name": self.search_provider.provider_name,
                    "discovery_status": "discovered",
                    "validation_status": "pending",
                    "review_status": "unreviewed",
                }
            )

        return leads_data

    def _get_campaign(self, campaign_id: str) -> Campaign:
        campaign = self.campaign_repository.get_by_id(campaign_id)
        if campaign is None:
            raise AppError(
                message="Campaign not found.",
                status_code=404,
                code="campaign_not_found",
            )
        return campaign

    @staticmethod
    def _ensure_campaign_can_start_discovery(campaign: Campaign) -> None:
        if campaign.status == "confirmed":
            return
        if campaign.status == "archived":
            raise AppError(
                message="Archived Campaigns cannot start Lead Discovery.",
                status_code=409,
                code="campaign_archived",
            )
        raise AppError(
            message="Campaign must be confirmed before Lead Discovery.",
            status_code=409,
            code="campaign_not_confirmed",
        )

    @staticmethod
    def _build_search_query(campaign: Campaign) -> str:
        snapshot = campaign.product_card_snapshot or {}
        parts = [
            campaign.name,
            snapshot.get("name"),
            snapshot.get("target_customer"),
            snapshot.get("value_proposition"),
            campaign.target_country,
            campaign.target_region,
            campaign.target_industry,
            campaign.target_company_type,
            campaign.target_role,
            " ".join(campaign.search_keywords or []),
            " ".join(campaign.qualification_criteria or []),
        ]
        return " ".join(str(part).strip() for part in parts if str(part or "").strip())

    @staticmethod
    def _normalize_name(company_name: str) -> str:
        return " ".join(company_name.lower().strip().split())

    @staticmethod
    def _normalize_website(website: str) -> str:
        parsed = urlparse(website if "://" in website else f"https://{website}")
        netloc = parsed.netloc.lower()
        if netloc.startswith("www."):
            netloc = netloc[4:]
        path = parsed.path.rstrip("/")
        return f"{netloc}{path}".lower()
