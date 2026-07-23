"""Service logic for the qualification module."""

from datetime import datetime, timezone
from typing import Any

from app.core.errors import AppError
from app.modules.campaigns.models import Campaign
from app.modules.campaigns.repository import CampaignRepository
from app.modules.discovery.models import Lead
from app.modules.discovery.repository import DiscoveryRepository
from app.modules.intelligence.models import LeadIntelligence
from app.modules.intelligence.repository import IntelligenceRepository
from app.modules.qualification.repository import QualificationRepository
from app.modules.qualification.schemas import LeadScoringProviderResult
from app.modules.tasks.models import TaskRun
from app.modules.tasks.repository import TaskRepository
from app.providers.llm_provider import LeadScoringProvider


class QualificationService:
    """Business service for Phase 6 Lead Scoring."""

    def __init__(
        self,
        repository: QualificationRepository,
        discovery_repository: DiscoveryRepository,
        campaign_repository: CampaignRepository,
        intelligence_repository: IntelligenceRepository,
        task_repository: TaskRepository,
        scoring_provider: LeadScoringProvider,
    ) -> None:
        self.repository = repository
        self.discovery_repository = discovery_repository
        self.campaign_repository = campaign_repository
        self.intelligence_repository = intelligence_repository
        self.task_repository = task_repository
        self.scoring_provider = scoring_provider

    def start_lead_scoring(self, lead_id: str) -> dict:
        lead = self._get_lead(lead_id)
        campaign = self._get_campaign(lead.campaign_id)
        self._ensure_campaign_allows_scoring(campaign)
        self._ensure_lead_can_start_scoring(lead)
        intelligence = self._get_scoring_intelligence(lead.id)

        if self.repository.has_score_for_lead(lead.id):
            raise AppError(
                message="Lead has already been scored.",
                status_code=409,
                code="lead_already_scored",
            )
        if self.task_repository.has_blocking_lead_scoring_task(lead.id):
            raise AppError(
                message="Lead Scoring already exists for this Lead.",
                status_code=409,
                code="lead_scoring_already_exists",
            )

        task_run = self.task_repository.create(
            {
                "task_type": "lead_scoring",
                "related_entity_type": "lead",
                "related_entity_id": lead.id,
                "provider_name": self.scoring_provider.provider_name,
                "status": "pending",
                "progress": 0,
            }
        )
        response_data = {
            "task_id": task_run.id,
            "status": "pending",
            "task_type": "lead_scoring",
            "lead_id": lead.id,
        }

        self._execute_mock_scoring(task_run, lead, campaign, intelligence)
        return response_data

    def list_tasks_for_lead(
        self,
        lead_id: str,
        limit: int,
        offset: int,
    ) -> dict:
        self._get_lead(lead_id)
        items, total = self.task_repository.list_lead_scoring_tasks_for_lead(
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

    def list_scores_for_lead(
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

    def _execute_mock_scoring(
        self,
        task_run: TaskRun,
        lead: Lead,
        campaign: Campaign,
        intelligence: LeadIntelligence,
    ) -> None:
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
            result = self._score_and_validate_provider_result(
                lead=lead,
                campaign=campaign,
                intelligence=intelligence,
            )
            self.repository.create(
                {
                    "lead_id": lead.id,
                    "campaign_id": campaign.id,
                    "task_run_id": task_run.id,
                    "fit_score": result.fit_score,
                    "recommendation": result.recommendation,
                    "matching_reasons": result.matching_reasons,
                    "risk_notes": result.risk_notes,
                    "uncertainty_notes": result.uncertainty_notes,
                    "evidence": result.evidence,
                    "suggested_outreach_angle": result.suggested_outreach_angle,
                    "model_name": self.scoring_provider.model_name,
                }
            )
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

    def _score_and_validate_provider_result(
        self,
        lead: Lead,
        campaign: Campaign,
        intelligence: LeadIntelligence,
    ) -> LeadScoringProviderResult:
        raw_result = self.scoring_provider.score_lead(
            self._build_scoring_payload(
                lead=lead,
                campaign=campaign,
                intelligence=intelligence,
            )
        )
        result = LeadScoringProviderResult.model_validate(raw_result)
        expected_recommendation = self._recommendation_for_score(result.fit_score)
        if result.recommendation != expected_recommendation:
            raise ValueError(
                "Lead scoring recommendation does not match the scoring rubric."
            )
        for evidence_item in result.evidence:
            source_url = str(evidence_item.get("source_url") or "").strip()
            evidence_text = str(
                evidence_item.get("evidence_text")
                or evidence_item.get("snippet")
                or ""
            ).strip()
            if not source_url or not evidence_text:
                raise ValueError(
                    "Lead scoring evidence must include source_url and evidence_text."
                )
        return result

    @staticmethod
    def _build_scoring_payload(
        lead: Lead,
        campaign: Campaign,
        intelligence: LeadIntelligence,
    ) -> dict[str, Any]:
        return {
            "lead": {
                "id": lead.id,
                "company_name": lead.company_name,
                "website": lead.website,
                "description": lead.description,
                "country": lead.country,
                "industry": lead.industry,
                "raw_snippet": lead.raw_snippet,
                "discovery_reason": lead.discovery_reason,
            },
            "campaign": {
                "id": campaign.id,
                "name": campaign.name,
                "target_country": campaign.target_country,
                "target_region": campaign.target_region,
                "target_industry": campaign.target_industry,
                "target_company_type": campaign.target_company_type,
                "target_role": campaign.target_role,
                "search_keywords": campaign.search_keywords,
                "qualification_criteria": campaign.qualification_criteria,
                "outreach_angle": campaign.outreach_angle,
                "product_card_snapshot": campaign.product_card_snapshot or {},
            },
            "intelligence": {
                "id": intelligence.id,
                "source_url": intelligence.source_url,
                "website_summary": intelligence.website_summary,
                "products_or_services": intelligence.products_or_services,
                "target_customers": intelligence.target_customers,
                "business_model": intelligence.business_model,
                "pain_points": intelligence.pain_points,
                "evidence": intelligence.evidence,
                "content_quality": intelligence.content_quality,
                "crawl_status": intelligence.crawl_status,
            },
        }

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

    def _get_scoring_intelligence(self, lead_id: str) -> LeadIntelligence:
        items, _ = self.intelligence_repository.list_by_lead(
            lead_id=lead_id,
            limit=20,
            offset=0,
        )
        for intelligence in items:
            if intelligence.crawl_status == "completed" and intelligence.evidence:
                return intelligence
        raise AppError(
            message="Completed Lead Intelligence with evidence is required before scoring.",
            status_code=409,
            code="lead_intelligence_required",
        )

    @staticmethod
    def _ensure_campaign_allows_scoring(campaign: Campaign) -> None:
        if campaign.status == "confirmed":
            return
        if campaign.status == "archived":
            raise AppError(
                message="Archived Campaign leads cannot start Lead Scoring.",
                status_code=409,
                code="campaign_archived",
            )
        raise AppError(
            message="Lead Campaign must be confirmed before Lead Scoring.",
            status_code=409,
            code="campaign_not_confirmed",
        )

    @staticmethod
    def _ensure_lead_can_start_scoring(lead: Lead) -> None:
        if lead.discovery_status != "discovered":
            raise AppError(
                message="Lead must be discovered before Lead Scoring.",
                status_code=409,
                code="lead_not_discovered",
            )
        if lead.validation_status == "valid":
            return
        raise AppError(
            message="Lead must be valid before Lead Scoring.",
            status_code=409,
            code="lead_not_validated",
        )

    @staticmethod
    def _recommendation_for_score(score: int) -> str:
        if score >= 80:
            return "recommended"
        if score >= 60:
            return "maybe"
        if score >= 40:
            return "needs_manual_review"
        return "not_recommended"
