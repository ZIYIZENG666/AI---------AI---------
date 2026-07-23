from typing import Any

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.main import app
from app.modules.campaigns.repository import CampaignRepository
from app.modules.discovery.models import Lead
from app.modules.discovery.repository import DiscoveryRepository
from app.modules.intelligence.repository import IntelligenceRepository
from app.modules.qualification.models import LeadScore
from app.modules.qualification.repository import QualificationRepository
from app.modules.qualification.routes import get_qualification_service
from app.modules.qualification.service import QualificationService
from app.modules.tasks.models import TaskRun
from app.modules.tasks.repository import TaskRepository
from app.providers.llm_provider import MockLeadScoringProvider
from tests.test_lead_discovery import db_session_for_client
from tests.test_lead_validation import (
    create_discovered_leads,
    get_lead_from_db,
    update_lead,
)


class ErrorLeadScoringProvider(MockLeadScoringProvider):
    provider_name = "mock_llm"
    model_name = "mock_lead_scoring_error"

    def score_lead(self, payload: dict[str, Any]) -> dict[str, Any]:
        raise RuntimeError("mock scoring failed")


class InvalidLeadScoringProvider(MockLeadScoringProvider):
    provider_name = "mock_llm"
    model_name = "mock_lead_scoring_invalid"

    def score_lead(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "fit_score": 95,
            "recommendation": "recommended",
            "matching_reasons": [],
            "risk_notes": ["Invalid provider output for test."],
            "uncertainty_notes": ["Invalid provider output for test."],
            "evidence": [],
        }


def override_qualification_provider(provider) -> None:
    def override(db: Session = Depends(get_db)) -> QualificationService:
        return QualificationService(
            repository=QualificationRepository(db),
            discovery_repository=DiscoveryRepository(db),
            campaign_repository=CampaignRepository(db),
            intelligence_repository=IntelligenceRepository(db),
            task_repository=TaskRepository(db),
            scoring_provider=provider,
        )

    app.dependency_overrides[get_qualification_service] = override


def create_validated_lead(client) -> tuple[dict, dict, str]:
    setup, leads = create_discovered_leads(client)
    lead = leads[0]
    response = client.post(f"/api/v1/leads/{lead['id']}/validation")
    assert response.status_code == 201
    task_id = response.json()["data"]["task_id"]
    task_response = client.get(f"/api/v1/tasks/{task_id}")
    assert task_response.status_code == 200
    assert task_response.json()["data"]["status"] == "completed"
    return setup, lead, task_id


def insert_scoring_task(session: Session, lead_id: str, status: str) -> TaskRun:
    task = TaskRun(
        task_type="lead_scoring",
        related_entity_type="lead",
        related_entity_id=lead_id,
        provider_name="mock_llm",
        status=status,
        progress=100 if status in {"completed", "failed", "cancelled"} else 0,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def count_scores_for_lead(lead_id: str) -> int:
    with db_session_for_client() as session:
        return session.query(LeadScore).filter(LeadScore.lead_id == lead_id).count()


def test_valid_lead_starts_scoring_and_creates_score(client) -> None:
    setup, lead, _ = create_validated_lead(client)
    campaign_id = setup["campaign"]["id"]

    response = client.post(f"/api/v1/leads/{lead['id']}/scoring")
    body = response.json()
    task_id = body["data"]["task_id"]

    assert response.status_code == 201
    assert body == {
        "data": {
            "task_id": task_id,
            "status": "pending",
            "task_type": "lead_scoring",
            "lead_id": lead["id"],
        },
        "message": "Lead scoring task created successfully.",
    }

    task_response = client.get(f"/api/v1/tasks/{task_id}")
    task = task_response.json()["data"]
    assert task_response.status_code == 200
    assert task["status"] == "completed"
    assert task["task_type"] == "lead_scoring"
    assert task["related_entity_type"] == "lead"
    assert task["related_entity_id"] == lead["id"]
    assert task["search_query"] is None
    assert task["input_url"] is None
    assert task["provider_name"] == "mock_llm"

    tasks_response = client.get(f"/api/v1/leads/{lead['id']}/scoring/tasks")
    assert tasks_response.status_code == 200
    assert tasks_response.json()["data"]["pagination"]["total"] == 1

    scores_response = client.get(f"/api/v1/leads/{lead['id']}/scores")
    scores_body = scores_response.json()["data"]
    assert scores_response.status_code == 200
    assert scores_body["pagination"]["total"] == 1
    score = scores_body["items"][0]
    assert score["lead_id"] == lead["id"]
    assert score["campaign_id"] == campaign_id
    assert score["task_run_id"] == task_id
    assert 0 <= score["fit_score"] <= 100
    assert score["recommendation"] == "recommended"
    assert score["matching_reasons"]
    assert score["risk_notes"]
    assert score["uncertainty_notes"]
    assert score["evidence"]
    assert score["model_name"] == "mock_lead_scoring_v1"
    assert score["suggested_outreach_angle"]

    db_lead = get_lead_from_db(lead["id"])
    assert db_lead.validation_status == "valid"
    assert db_lead.review_status == "unreviewed"


def test_valid_lead_without_score_returns_empty_score_list(client) -> None:
    _, lead, _ = create_validated_lead(client)

    response = client.get(f"/api/v1/leads/{lead['id']}/scores")

    assert response.status_code == 200
    assert response.json()["data"] == {
        "items": [],
        "pagination": {
            "total": 0,
            "limit": 20,
            "offset": 0,
        },
    }


def test_missing_lead_scoring_returns_not_found(client) -> None:
    response = client.post("/api/v1/leads/missing-lead/scoring")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "lead_not_found"


def test_archived_campaign_lead_cannot_start_scoring(client) -> None:
    setup, lead, _ = create_validated_lead(client)
    campaign_id = setup["campaign"]["id"]
    archive_response = client.post(f"/api/v1/campaigns/{campaign_id}/archive")
    assert archive_response.status_code == 200

    response = client.post(f"/api/v1/leads/{lead['id']}/scoring")

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "campaign_archived"


def test_non_valid_leads_cannot_start_scoring(client) -> None:
    for validation_status in (
        "pending",
        "invalid",
        "duplicate",
        "insufficient_content",
    ):
        _, leads = create_discovered_leads(client)
        lead = leads[0]
        update_lead(lead["id"], {"validation_status": validation_status})

        response = client.post(f"/api/v1/leads/{lead['id']}/scoring")

        assert response.status_code == 409
        assert response.json()["error"]["code"] == "lead_not_validated"


def test_valid_lead_without_intelligence_evidence_cannot_start_scoring(client) -> None:
    _, leads = create_discovered_leads(client)
    lead = leads[0]
    update_lead(lead["id"], {"validation_status": "valid"})

    response = client.post(f"/api/v1/leads/{lead['id']}/scoring")

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "lead_intelligence_required"


def test_pending_running_and_completed_scoring_tasks_block_duplicate(client) -> None:
    for blocking_status in ("pending", "running", "completed"):
        _, lead, _ = create_validated_lead(client)
        with db_session_for_client() as session:
            insert_scoring_task(session, lead["id"], blocking_status)

        response = client.post(f"/api/v1/leads/{lead['id']}/scoring")

        assert response.status_code == 409
        assert response.json()["error"]["code"] == "lead_scoring_already_exists"


def test_failed_and_cancelled_scoring_tasks_can_be_retried(client) -> None:
    for retryable_status in ("failed", "cancelled"):
        _, lead, _ = create_validated_lead(client)
        with db_session_for_client() as session:
            insert_scoring_task(session, lead["id"], retryable_status)

        response = client.post(f"/api/v1/leads/{lead['id']}/scoring")
        task_response = client.get(f"/api/v1/tasks/{response.json()['data']['task_id']}")

        assert response.status_code == 201
        assert task_response.json()["data"]["status"] == "completed"


def test_existing_score_blocks_duplicate_first_slice_scoring(client) -> None:
    _, lead, _ = create_validated_lead(client)
    first_response = client.post(f"/api/v1/leads/{lead['id']}/scoring")
    assert first_response.status_code == 201

    second_response = client.post(f"/api/v1/leads/{lead['id']}/scoring")

    assert second_response.status_code == 409
    assert second_response.json()["error"]["code"] == "lead_already_scored"


def test_provider_failure_marks_task_failed_and_does_not_create_score(client) -> None:
    override_qualification_provider(ErrorLeadScoringProvider())
    _, lead, _ = create_validated_lead(client)

    response = client.post(f"/api/v1/leads/{lead['id']}/scoring")
    task_response = client.get(f"/api/v1/tasks/{response.json()['data']['task_id']}")
    scores_response = client.get(f"/api/v1/leads/{lead['id']}/scores")

    assert response.status_code == 201
    assert task_response.json()["data"]["status"] == "failed"
    assert task_response.json()["data"]["error_message"] == "mock scoring failed"
    assert scores_response.json()["data"]["pagination"]["total"] == 0
    assert count_scores_for_lead(lead["id"]) == 0
    assert get_lead_from_db(lead["id"]).review_status == "unreviewed"


def test_invalid_provider_output_fails_task_and_does_not_create_score(client) -> None:
    override_qualification_provider(InvalidLeadScoringProvider())
    _, lead, _ = create_validated_lead(client)

    response = client.post(f"/api/v1/leads/{lead['id']}/scoring")
    task_response = client.get(f"/api/v1/tasks/{response.json()['data']['task_id']}")
    scores_response = client.get(f"/api/v1/leads/{lead['id']}/scores")

    assert response.status_code == 201
    assert task_response.json()["data"]["status"] == "failed"
    assert scores_response.json()["data"]["pagination"]["total"] == 0
    assert count_scores_for_lead(lead["id"]) == 0
    assert get_lead_from_db(lead["id"]).review_status == "unreviewed"
