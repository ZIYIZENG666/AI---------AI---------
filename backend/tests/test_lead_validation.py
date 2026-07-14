from typing import Any

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.main import app
from app.modules.campaigns.repository import CampaignRepository
from app.modules.discovery.models import Lead
from app.modules.discovery.repository import DiscoveryRepository
from app.modules.intelligence.repository import IntelligenceRepository
from app.modules.intelligence.routes import get_intelligence_service
from app.modules.intelligence.service import IntelligenceService
from app.modules.tasks.models import TaskRun
from app.modules.tasks.repository import TaskRepository
from tests.test_lead_discovery import create_confirmed_campaign, db_session_for_client


class ErrorCrawlerProvider:
    provider_name = "mock_crawler"

    def fetch(self, url: str) -> dict[str, Any]:
        raise RuntimeError("mock crawler failed")


class CanonicalDuplicateCrawlerProvider:
    provider_name = "mock_crawler"

    def __init__(self, final_url: str) -> None:
        self.final_url = final_url

    def fetch(self, url: str) -> dict[str, Any]:
        return {
            "final_url": self.final_url,
            "website_summary": "Duplicate canonical website.",
            "products_or_services": ["Duplicate product"],
            "target_customers": ["Duplicate customer"],
            "business_model": "B2B",
            "pain_points": ["Duplicate pain point"],
            "evidence": [{"source_url": self.final_url, "snippet": "Duplicate."}],
            "content_quality": "sufficient",
            "crawl_status": "completed",
        }


def override_intelligence_provider(provider) -> None:
    def override(db: Session = Depends(get_db)) -> IntelligenceService:
        return IntelligenceService(
            repository=IntelligenceRepository(db),
            discovery_repository=DiscoveryRepository(db),
            campaign_repository=CampaignRepository(db),
            task_repository=TaskRepository(db),
            crawler_provider=provider,
        )

    app.dependency_overrides[get_intelligence_service] = override


def create_discovered_leads(client) -> tuple[dict, list[dict]]:
    setup = create_confirmed_campaign(client)
    campaign_id = setup["campaign"]["id"]
    response = client.post(f"/api/v1/campaigns/{campaign_id}/lead-discovery")
    assert response.status_code == 201
    leads_response = client.get(f"/api/v1/campaigns/{campaign_id}/leads")
    assert leads_response.status_code == 200
    leads = leads_response.json()["data"]["items"]
    assert leads
    return setup, leads


def get_lead_from_db(lead_id: str) -> Lead:
    with db_session_for_client() as session:
        lead = session.get(Lead, lead_id)
        assert lead is not None
        session.expunge(lead)
        return lead


def update_lead(lead_id: str, data: dict) -> None:
    with db_session_for_client() as session:
        lead = session.get(Lead, lead_id)
        assert lead is not None
        for field_name, value in data.items():
            setattr(lead, field_name, value)
        session.commit()


def insert_validation_task(session: Session, lead_id: str, status: str) -> TaskRun:
    task = TaskRun(
        task_type="lead_validation",
        related_entity_type="lead",
        related_entity_id=lead_id,
        input_url="https://existing-validation.example.com",
        provider_name="mock_crawler",
        status=status,
        progress=100 if status in {"completed", "failed", "cancelled"} else 0,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def test_discovered_lead_starts_validation_and_creates_intelligence(client) -> None:
    _, leads = create_discovered_leads(client)
    lead = leads[0]

    response = client.post(f"/api/v1/leads/{lead['id']}/validation")
    body = response.json()
    task_id = body["data"]["task_id"]

    assert response.status_code == 201
    assert body == {
        "data": {
            "task_id": task_id,
            "status": "pending",
            "task_type": "lead_validation",
            "lead_id": lead["id"],
        },
        "message": "Lead validation task created successfully.",
    }

    task_response = client.get(f"/api/v1/tasks/{task_id}")
    task = task_response.json()["data"]
    assert task_response.status_code == 200
    assert task["status"] == "completed"
    assert task["task_type"] == "lead_validation"
    assert task["related_entity_type"] == "lead"
    assert task["related_entity_id"] == lead["id"]
    assert task["input_url"] == lead["website"]
    assert task["search_query"] is None
    assert task["provider_name"] == "mock_crawler"

    tasks_response = client.get(f"/api/v1/leads/{lead['id']}/validation/tasks")
    assert tasks_response.status_code == 200
    assert tasks_response.json()["data"]["pagination"]["total"] == 1

    intelligence_response = client.get(f"/api/v1/leads/{lead['id']}/intelligence")
    intelligence_body = intelligence_response.json()["data"]
    assert intelligence_response.status_code == 200
    assert intelligence_body["pagination"]["total"] == 1
    intelligence = intelligence_body["items"][0]
    assert intelligence["lead_id"] == lead["id"]
    assert intelligence["task_run_id"] == task_id
    assert intelligence["provider_name"] == "mock_crawler"
    assert intelligence["crawl_status"] == "completed"
    assert intelligence["content_quality"] == "sufficient"
    assert intelligence["evidence"]

    db_lead = get_lead_from_db(lead["id"])
    assert db_lead.validation_status == "valid"
    assert db_lead.review_status == "unreviewed"


def test_existing_lead_without_intelligence_returns_empty_list(client) -> None:
    _, leads = create_discovered_leads(client)
    lead = leads[0]

    response = client.get(f"/api/v1/leads/{lead['id']}/intelligence")

    assert response.status_code == 200
    assert response.json()["data"] == {
        "items": [],
        "pagination": {
            "total": 0,
            "limit": 20,
            "offset": 0,
        },
    }


def test_archived_campaign_lead_cannot_start_validation(client) -> None:
    setup, leads = create_discovered_leads(client)
    campaign_id = setup["campaign"]["id"]
    lead = leads[0]
    archive_response = client.post(f"/api/v1/campaigns/{campaign_id}/archive")
    assert archive_response.status_code == 200

    response = client.post(f"/api/v1/leads/{lead['id']}/validation")

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "campaign_archived"


def test_terminal_validation_status_cannot_start_again(client) -> None:
    for validation_status in ("valid", "invalid", "duplicate", "insufficient_content"):
        _, leads = create_discovered_leads(client)
        lead = leads[0]
        update_lead(lead["id"], {"validation_status": validation_status})

        response = client.post(f"/api/v1/leads/{lead['id']}/validation")

        assert response.status_code == 409
        assert response.json()["error"]["code"] == "lead_already_validated"


def test_pending_running_and_completed_validation_tasks_block_duplicate(client) -> None:
    for blocking_status in ("pending", "running", "completed"):
        _, leads = create_discovered_leads(client)
        lead = leads[0]
        with db_session_for_client() as session:
            insert_validation_task(session, lead["id"], blocking_status)

        response = client.post(f"/api/v1/leads/{lead['id']}/validation")

        assert response.status_code == 409
        assert response.json()["error"]["code"] == "lead_validation_already_exists"


def test_failed_and_cancelled_validation_tasks_can_be_retried(client) -> None:
    for retryable_status in ("failed", "cancelled"):
        _, leads = create_discovered_leads(client)
        lead = leads[0]
        with db_session_for_client() as session:
            insert_validation_task(session, lead["id"], retryable_status)

        response = client.post(f"/api/v1/leads/{lead['id']}/validation")
        task_response = client.get(f"/api/v1/tasks/{response.json()['data']['task_id']}")

        assert response.status_code == 201
        assert task_response.json()["data"]["status"] == "completed"


def test_provider_failure_marks_task_failed_and_keeps_validation_pending(client) -> None:
    override_intelligence_provider(ErrorCrawlerProvider())
    _, leads = create_discovered_leads(client)
    lead = leads[0]

    response = client.post(f"/api/v1/leads/{lead['id']}/validation")
    task_response = client.get(f"/api/v1/tasks/{response.json()['data']['task_id']}")
    intelligence_response = client.get(f"/api/v1/leads/{lead['id']}/intelligence")

    assert response.status_code == 201
    assert task_response.json()["data"]["status"] == "failed"
    assert task_response.json()["data"]["error_message"] == "mock crawler failed"
    assert intelligence_response.json()["data"]["pagination"]["total"] == 0
    assert get_lead_from_db(lead["id"]).validation_status == "pending"


def test_malformed_or_unsupported_url_marks_lead_invalid(client) -> None:
    _, leads = create_discovered_leads(client)
    lead = leads[0]
    update_lead(lead["id"], {"website": "not a url"})

    response = client.post(f"/api/v1/leads/{lead['id']}/validation")
    task_response = client.get(f"/api/v1/tasks/{response.json()['data']['task_id']}")
    intelligence_response = client.get(f"/api/v1/leads/{lead['id']}/intelligence")
    intelligence = intelligence_response.json()["data"]["items"][0]

    assert response.status_code == 201
    assert task_response.json()["data"]["status"] == "completed"
    assert intelligence["crawl_status"] == "skipped"
    assert intelligence["error_message"] == "Unsupported or invalid website URL."
    assert get_lead_from_db(lead["id"]).validation_status == "invalid"


def test_insufficient_content_marks_lead_insufficient_content(client) -> None:
    _, leads = create_discovered_leads(client)
    lead = leads[0]
    update_lead(lead["id"], {"website": "https://insufficient.example.com"})

    response = client.post(f"/api/v1/leads/{lead['id']}/validation")
    task_response = client.get(f"/api/v1/tasks/{response.json()['data']['task_id']}")
    intelligence_response = client.get(f"/api/v1/leads/{lead['id']}/intelligence")
    intelligence = intelligence_response.json()["data"]["items"][0]

    assert response.status_code == 201
    assert task_response.json()["data"]["status"] == "completed"
    assert intelligence["crawl_status"] == "insufficient_content"
    assert intelligence["content_quality"] == "insufficient"
    assert get_lead_from_db(lead["id"]).validation_status == "insufficient_content"


def test_same_campaign_canonical_duplicate_marks_lead_duplicate(client) -> None:
    _, leads = create_discovered_leads(client)
    lead_to_validate = leads[0]
    existing_lead = leads[1]
    override_intelligence_provider(
        CanonicalDuplicateCrawlerProvider(final_url=existing_lead["website"])
    )

    response = client.post(f"/api/v1/leads/{lead_to_validate['id']}/validation")
    task_response = client.get(f"/api/v1/tasks/{response.json()['data']['task_id']}")
    intelligence_response = client.get(
        f"/api/v1/leads/{lead_to_validate['id']}/intelligence"
    )

    assert response.status_code == 201
    assert task_response.json()["data"]["status"] == "completed"
    assert intelligence_response.json()["data"]["pagination"]["total"] == 0
    assert get_lead_from_db(lead_to_validate["id"]).validation_status == "duplicate"
