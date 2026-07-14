"""Service logic for the intelligence module."""

from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

from app.core.errors import AppError
from app.modules.campaigns.models import Campaign
from app.modules.campaigns.repository import CampaignRepository
from app.modules.discovery.models import Lead
from app.modules.discovery.repository import DiscoveryRepository
from app.modules.intelligence.repository import IntelligenceRepository
from app.modules.tasks.models import TaskRun
from app.modules.tasks.repository import TaskRepository
from app.providers.crawler_provider import CrawlerProvider


class IntelligenceService:
    """Business service for Phase 5 Lead Validation + Intelligence."""

    def __init__(
        self,
        repository: IntelligenceRepository,
        discovery_repository: DiscoveryRepository,
        campaign_repository: CampaignRepository,
        task_repository: TaskRepository,
        crawler_provider: CrawlerProvider,
    ) -> None:
        self.repository = repository
        self.discovery_repository = discovery_repository
        self.campaign_repository = campaign_repository
        self.task_repository = task_repository
        self.crawler_provider = crawler_provider

    def start_lead_validation(self, lead_id: str) -> dict:
        lead = self._get_lead(lead_id)
        campaign = self._get_campaign(lead.campaign_id)
        self._ensure_campaign_allows_validation(campaign)
        self._ensure_lead_can_start_validation(lead)
        if self.task_repository.has_blocking_lead_validation_task(lead_id):
            raise AppError(
                message="Lead Validation already exists for this Lead.",
                status_code=409,
                code="lead_validation_already_exists",
            )

        task_run = self.task_repository.create(
            {
                "task_type": "lead_validation",
                "related_entity_type": "lead",
                "related_entity_id": lead.id,
                "input_url": lead.website,
                "provider_name": self.crawler_provider.provider_name,
                "status": "pending",
                "progress": 0,
            }
        )
        response_data = {
            "task_id": task_run.id,
            "status": "pending",
            "task_type": "lead_validation",
            "lead_id": lead.id,
        }

        self._execute_mock_validation(task_run, lead)
        return response_data

    def list_tasks_for_lead(
        self,
        lead_id: str,
        limit: int,
        offset: int,
    ) -> dict:
        self._get_lead(lead_id)
        items, total = self.task_repository.list_lead_validation_tasks_for_lead(
            lead_id=lead_id,
            limit=limit,
            offset=offset,
        )
        return {
            "items": items,
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    def list_intelligence_for_lead(
        self,
        lead_id: str,
        limit: int,
        offset: int,
    ) -> dict:
        self._get_lead(lead_id)
        items, total = self.repository.list_by_lead(
            lead_id=lead_id,
            limit=limit,
            offset=offset,
        )
        return {
            "items": items,
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    def _execute_mock_validation(self, task_run: TaskRun, lead: Lead) -> None:
        self.task_repository.update(
            task_run,
            {
                "status": "running",
                "progress": 10,
                "started_at": datetime.now(timezone.utc),
                "error_message": None,
            },
        )
        try:
            if not self._is_supported_website_url(lead.website):
                self._complete_with_invalid_url(task_run, lead)
                return

            result = self.crawler_provider.fetch(lead.website)
            final_url = str(result.get("final_url") or lead.website).strip()
            normalized_website = self._normalize_website(final_url)
            if self.discovery_repository.has_other_lead_with_normalized_website(
                campaign_id=lead.campaign_id,
                normalized_website=normalized_website,
                exclude_lead_id=lead.id,
            ):
                self._complete_with_status(task_run, lead, "duplicate")
                return

            if self._is_insufficient_content(result):
                self._create_intelligence(
                    task_run=task_run,
                    lead=lead,
                    result=result,
                    validation_status="insufficient_content",
                    error_message=None,
                )
                self._complete_with_status(task_run, lead, "insufficient_content")
                return

            self._create_intelligence(
                task_run=task_run,
                lead=lead,
                result=result,
                validation_status="valid",
                error_message=None,
            )
            self._complete_with_status(task_run, lead, "valid")
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

    def _complete_with_invalid_url(self, task_run: TaskRun, lead: Lead) -> None:
        result = {
            "final_url": lead.website,
            "website_summary": None,
            "products_or_services": [],
            "target_customers": [],
            "business_model": None,
            "pain_points": [],
            "evidence": [],
            "content_quality": "invalid",
            "crawl_status": "skipped",
        }
        self._create_intelligence(
            task_run=task_run,
            lead=lead,
            result=result,
            validation_status="invalid",
            error_message="Unsupported or invalid website URL.",
        )
        self._complete_with_status(task_run, lead, "invalid")

    def _complete_with_status(
        self,
        task_run: TaskRun,
        lead: Lead,
        validation_status: str,
    ) -> None:
        self.discovery_repository.update(lead, {"validation_status": validation_status})
        self.task_repository.update(
            task_run,
            {
                "status": "completed",
                "progress": 100,
                "finished_at": datetime.now(timezone.utc),
                "error_message": None,
            },
        )

    def _create_intelligence(
        self,
        task_run: TaskRun,
        lead: Lead,
        result: dict[str, Any],
        validation_status: str,
        error_message: str | None,
    ) -> None:
        source_url = str(result.get("final_url") or lead.website).strip()
        self.repository.create(
            {
                "lead_id": lead.id,
                "task_run_id": task_run.id,
                "source_url": source_url,
                "provider_name": self.crawler_provider.provider_name,
                "website_summary": result.get("website_summary"),
                "products_or_services": list(result.get("products_or_services") or []),
                "target_customers": list(result.get("target_customers") or []),
                "business_model": result.get("business_model"),
                "pain_points": list(result.get("pain_points") or []),
                "evidence": list(result.get("evidence") or []),
                "content_quality": str(
                    result.get("content_quality") or validation_status
                ),
                "crawl_status": str(result.get("crawl_status") or "completed"),
                "error_message": error_message,
            }
        )

    def _get_lead(self, lead_id: str) -> Lead:
        lead = self.discovery_repository.get_by_id(lead_id)
        if lead is None:
            raise AppError(
                message="Lead not found.",
                status_code=404,
                code="lead_not_found",
            )
        return lead

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
    def _ensure_campaign_allows_validation(campaign: Campaign) -> None:
        if campaign.status == "confirmed":
            return
        if campaign.status == "archived":
            raise AppError(
                message="Archived Campaign leads cannot start Lead Validation.",
                status_code=409,
                code="campaign_archived",
            )
        raise AppError(
            message="Lead Campaign must be confirmed before Lead Validation.",
            status_code=409,
            code="campaign_not_confirmed",
        )

    @staticmethod
    def _ensure_lead_can_start_validation(lead: Lead) -> None:
        if lead.discovery_status != "discovered":
            raise AppError(
                message="Lead must be discovered before Lead Validation.",
                status_code=409,
                code="lead_not_discovered",
            )
        if lead.validation_status == "pending":
            return
        raise AppError(
            message="Lead has already completed validation.",
            status_code=409,
            code="lead_already_validated",
        )

    @staticmethod
    def _is_insufficient_content(result: dict[str, Any]) -> bool:
        return (
            result.get("crawl_status") == "insufficient_content"
            or result.get("content_quality") == "insufficient"
        )

    @staticmethod
    def _is_supported_website_url(website: str) -> bool:
        clean = website.strip()
        if not clean or any(character.isspace() for character in clean):
            return False

        parsed = urlparse(clean if "://" in clean else f"https://{clean}")
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            return False

        host = parsed.netloc.lower()
        blocked_hosts = (
            "linkedin.com",
            "facebook.com",
            "instagram.com",
            "twitter.com",
            "x.com",
        )
        return not any(host == blocked or host.endswith(f".{blocked}") for blocked in blocked_hosts)

    @staticmethod
    def _normalize_website(website: str) -> str:
        parsed = urlparse(website if "://" in website else f"https://{website}")
        netloc = parsed.netloc.lower()
        if netloc.startswith("www."):
            netloc = netloc[4:]
        path = parsed.path.rstrip("/")
        return f"{netloc}{path}".lower()
