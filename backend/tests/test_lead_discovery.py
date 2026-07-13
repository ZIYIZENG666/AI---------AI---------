from contextlib import contextmanager
from typing import Any

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.main import app
from app.modules.campaigns.models import Campaign
from app.modules.campaigns.repository import CampaignRepository
from app.modules.discovery.models import Lead
from app.modules.discovery.repository import DiscoveryRepository
from app.modules.discovery.routes import get_discovery_service
from app.modules.discovery.service import DiscoveryService
from app.modules.products.models import ProductCard
from app.modules.tasks.models import TaskRun
from app.modules.tasks.repository import TaskRepository


@contextmanager
def db_session_for_client():
    override_get_db = app.dependency_overrides[get_db]
    session_generator = override_get_db()
    session = next(session_generator)
    try:
        yield session
    finally:
        try:
            next(session_generator)
        except StopIteration:
            pass


def create_company(client, name: str = "Lead Discovery Company") -> str:
    response = client.post(
        "/api/v1/companies",
        json={
            "name": name,
            "target_market": "Industrial manufacturers",
            "value_proposition": "Reduce inspection downtime.",
        },
    )
    assert response.status_code == 201
    return response.json()["data"]["id"]


def create_product_card(client, company_id: str, name: str = "Snapshot Product") -> dict:
    response = client.post(
        "/api/v1/product-cards",
        json={
            "company_id": company_id,
            "name": name,
            "description": "AI inspection workflow for manufacturing quality teams.",
            "target_customer": "Quality leaders at industrial manufacturers",
            "pain_points": ["Manual inspection is slow"],
            "value_proposition": "Find defects faster with traceable evidence.",
            "use_cases": ["Factory quality assurance"],
            "differentiators": ["Evidence-first matching"],
        },
    )
    assert response.status_code == 201
    return response.json()["data"]


def create_confirmed_product_card(
    client,
    company_id: str,
    name: str = "Snapshot Product",
) -> dict:
    product_card = create_product_card(client, company_id, name=name)
    response = client.post(f"/api/v1/product-cards/{product_card['id']}/confirm")
    assert response.status_code == 200
    return response.json()["data"]


def campaign_payload(product_card_id: str, name: str = "Lead Discovery Campaign") -> dict:
    return {
        "product_card_id": product_card_id,
        "name": name,
        "target_country": "Germany",
        "target_region": "DACH",
        "target_industry": "Manufacturing",
        "target_company_type": "Mid-market factories",
        "target_role": "Head of Quality",
        "search_keywords": ["factory quality inspection", "industrial AI QA"],
        "qualification_criteria": ["Has in-house production"],
        "outreach_angle": "Reduce manual QA review time.",
        "lead_limit": 25,
    }


def create_campaign(client, company_id: str, product_card_id: str) -> dict:
    response = client.post(
        f"/api/v1/companies/{company_id}/campaigns",
        json=campaign_payload(product_card_id),
    )
    assert response.status_code == 201
    return response.json()["data"]


def create_confirmed_campaign(client, product_name: str = "Snapshot Product") -> dict:
    company_id = create_company(client)
    product_card = create_confirmed_product_card(client, company_id, name=product_name)
    campaign = create_campaign(client, company_id, product_card["id"])
    response = client.post(f"/api/v1/campaigns/{campaign['id']}/confirm")
    assert response.status_code == 200
    return {
        "company_id": company_id,
        "product_card": product_card,
        "campaign": response.json()["data"],
    }


class EmptySearchProvider:
    provider_name = "mock_search"

    def search(self, query: str, limit: int) -> list[dict[str, Any]]:
        return []


class ErrorSearchProvider:
    provider_name = "mock_search"

    def search(self, query: str, limit: int) -> list[dict[str, Any]]:
        raise RuntimeError("mock provider failed")


class DuplicateWebsiteProvider:
    provider_name = "mock_search"

    def search(self, query: str, limit: int) -> list[dict[str, Any]]:
        return [
            {
                "company_name": "Duplicate Candidate",
                "website": "https://www.duplicate.example.com/",
                "source_url": "https://mock-search.example.com/duplicate-a",
                "raw_snippet": f"Matched {query}",
                "discovery_reason": "First duplicate candidate.",
            },
            {
                "company_name": "Duplicate Candidate Again",
                "website": "http://duplicate.example.com",
                "source_url": "https://mock-search.example.com/duplicate-b",
                "raw_snippet": f"Matched {query}",
                "discovery_reason": "Same normalized website.",
            },
        ]


def override_discovery_provider(provider):
    def override(db: Session = Depends(get_db)) -> DiscoveryService:
        return DiscoveryService(
            repository=DiscoveryRepository(db),
            campaign_repository=CampaignRepository(db),
            task_repository=TaskRepository(db),
            search_provider=provider,
        )

    app.dependency_overrides[get_discovery_service] = override


def insert_task_run(session: Session, campaign_id: str, status: str) -> TaskRun:
    task = TaskRun(
        task_type="lead_discovery",
        related_entity_type="campaign",
        related_entity_id=campaign_id,
        search_query="existing task query",
        provider_name="mock_search",
        status=status,
        progress=100 if status in {"completed", "failed", "cancelled"} else 0,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def test_confirmed_campaign_starts_discovery_and_saves_candidate_leads(client) -> None:
    setup = create_confirmed_campaign(client)
    campaign_id = setup["campaign"]["id"]

    response = client.post(f"/api/v1/campaigns/{campaign_id}/lead-discovery")
    body = response.json()
    task_id = body["data"]["task_id"]

    assert response.status_code == 201
    assert body == {
        "data": {
            "task_id": task_id,
            "status": "pending",
            "task_type": "lead_discovery",
            "campaign_id": campaign_id,
        },
        "message": "Lead Discovery task created successfully.",
    }

    task_response = client.get(f"/api/v1/tasks/{task_id}")
    task = task_response.json()["data"]
    assert task_response.status_code == 200
    assert task["status"] == "completed"
    assert task["task_type"] == "lead_discovery"
    assert task["related_entity_type"] == "campaign"
    assert task["related_entity_id"] == campaign_id
    assert task["provider_name"] == "mock_search"
    assert "Snapshot Product" in task["search_query"]

    campaign_response = client.get(f"/api/v1/campaigns/{campaign_id}")
    assert campaign_response.json()["data"]["status"] == "confirmed"

    leads_response = client.get(f"/api/v1/campaigns/{campaign_id}/leads")
    leads_body = leads_response.json()["data"]
    assert leads_response.status_code == 200
    assert leads_body["pagination"]["total"] == 3
    first_lead = leads_body["items"][0]
    assert first_lead["campaign_id"] == campaign_id
    assert first_lead["task_run_id"] == task_id
    assert first_lead["website"]
    assert first_lead["source_url"]
    assert first_lead["search_query"] == task["search_query"]
    assert first_lead["provider_name"] == "mock_search"
    assert first_lead["discovery_status"] == "discovered"
    assert first_lead["validation_status"] == "pending"
    assert first_lead["review_status"] == "unreviewed"


def test_draft_and_archived_campaigns_cannot_start_lead_discovery(client) -> None:
    company_id = create_company(client)
    product_card = create_confirmed_product_card(client, company_id)
    draft_campaign = create_campaign(client, company_id, product_card["id"])
    archived_setup = create_confirmed_campaign(client)
    archived_campaign_id = archived_setup["campaign"]["id"]
    archive_response = client.post(f"/api/v1/campaigns/{archived_campaign_id}/archive")
    assert archive_response.status_code == 200

    draft_response = client.post(
        f"/api/v1/campaigns/{draft_campaign['id']}/lead-discovery"
    )
    archived_response = client.post(
        f"/api/v1/campaigns/{archived_campaign_id}/lead-discovery"
    )

    assert draft_response.status_code == 409
    assert draft_response.json()["error"]["code"] == "campaign_not_confirmed"
    assert archived_response.status_code == 409
    assert archived_response.json()["error"]["code"] == "campaign_archived"


def test_pending_running_and_completed_tasks_block_duplicate_discovery(client) -> None:
    for blocking_status in ("pending", "running", "completed"):
        setup = create_confirmed_campaign(client, product_name=f"{blocking_status} Product")
        campaign_id = setup["campaign"]["id"]
        with db_session_for_client() as session:
            insert_task_run(session, campaign_id, blocking_status)

        response = client.post(f"/api/v1/campaigns/{campaign_id}/lead-discovery")

        assert response.status_code == 409
        assert response.json()["error"]["code"] == "lead_discovery_already_exists"


def test_failed_and_cancelled_tasks_can_be_retried(client) -> None:
    for retryable_status in ("failed", "cancelled"):
        setup = create_confirmed_campaign(client, product_name=f"{retryable_status} Product")
        campaign_id = setup["campaign"]["id"]
        with db_session_for_client() as session:
            insert_task_run(session, campaign_id, retryable_status)

        response = client.post(f"/api/v1/campaigns/{campaign_id}/lead-discovery")

        assert response.status_code == 201
        task_response = client.get(f"/api/v1/tasks/{response.json()['data']['task_id']}")
        assert task_response.json()["data"]["status"] == "completed"


def test_zero_result_mock_search_marks_task_completed_without_leads(client) -> None:
    override_discovery_provider(EmptySearchProvider())
    setup = create_confirmed_campaign(client)
    campaign_id = setup["campaign"]["id"]

    response = client.post(f"/api/v1/campaigns/{campaign_id}/lead-discovery")
    task_response = client.get(f"/api/v1/tasks/{response.json()['data']['task_id']}")
    leads_response = client.get(f"/api/v1/campaigns/{campaign_id}/leads")

    assert response.status_code == 201
    assert task_response.json()["data"]["status"] == "completed"
    assert task_response.json()["data"]["error_message"] is None
    assert leads_response.json()["data"]["pagination"]["total"] == 0


def test_provider_failure_marks_task_failed_and_records_error(client) -> None:
    override_discovery_provider(ErrorSearchProvider())
    setup = create_confirmed_campaign(client)
    campaign_id = setup["campaign"]["id"]

    response = client.post(f"/api/v1/campaigns/{campaign_id}/lead-discovery")
    task_response = client.get(f"/api/v1/tasks/{response.json()['data']['task_id']}")
    task = task_response.json()["data"]

    assert response.status_code == 201
    assert task["status"] == "failed"
    assert task["error_message"] == "mock provider failed"


def test_discovery_query_uses_confirmed_campaign_snapshot_not_live_product_card(
    client,
) -> None:
    setup = create_confirmed_campaign(client, product_name="Snapshot Product")
    campaign_id = setup["campaign"]["id"]
    product_card_id = setup["product_card"]["id"]

    with db_session_for_client() as session:
        product_card = session.get(ProductCard, product_card_id)
        product_card.name = "Mutated Live Product"
        session.commit()

    response = client.post(f"/api/v1/campaigns/{campaign_id}/lead-discovery")
    task_response = client.get(f"/api/v1/tasks/{response.json()['data']['task_id']}")
    search_query = task_response.json()["data"]["search_query"]

    assert "Snapshot Product" in search_query
    assert "Mutated Live Product" not in search_query


def test_discovery_deduplicates_websites_per_campaign_but_not_across_campaigns(
    client,
) -> None:
    override_discovery_provider(DuplicateWebsiteProvider())
    first_setup = create_confirmed_campaign(client, product_name="First Product")
    second_setup = create_confirmed_campaign(client, product_name="Second Product")
    first_campaign_id = first_setup["campaign"]["id"]
    second_campaign_id = second_setup["campaign"]["id"]

    first_response = client.post(
        f"/api/v1/campaigns/{first_campaign_id}/lead-discovery"
    )
    second_response = client.post(
        f"/api/v1/campaigns/{second_campaign_id}/lead-discovery"
    )
    first_leads = client.get(f"/api/v1/campaigns/{first_campaign_id}/leads").json()
    second_leads = client.get(f"/api/v1/campaigns/{second_campaign_id}/leads").json()

    assert first_response.status_code == 201
    assert second_response.status_code == 201
    assert first_leads["data"]["pagination"]["total"] == 1
    assert second_leads["data"]["pagination"]["total"] == 1

    with db_session_for_client() as session:
        total_leads = session.query(Lead).count()
        first_campaign = session.get(Campaign, first_campaign_id)
        second_campaign = session.get(Campaign, second_campaign_id)

    assert total_leads == 2
    assert first_campaign.status == "confirmed"
    assert second_campaign.status == "confirmed"
