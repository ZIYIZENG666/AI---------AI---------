from contextlib import contextmanager

from app.core.database import get_db
from app.main import app
from app.modules.campaigns.models import Campaign
from app.modules.products.models import ProductCard


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


def create_company(client, name: str = "Campaign Test Company") -> str:
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


def product_card_payload(
    company_id: str,
    name: str = "Confirmed Inspection AI",
) -> dict:
    return {
        "company_id": company_id,
        "name": name,
        "description": "AI inspection workflow for manufacturing quality teams.",
        "target_customer": "Quality leaders at industrial manufacturers",
        "pain_points": ["Manual inspection is slow", "Defect evidence is scattered"],
        "value_proposition": "Find defects faster with traceable evidence.",
        "use_cases": ["Factory quality assurance", "Incoming goods inspection"],
        "differentiators": ["Evidence-first matching", "Operator-friendly workflow"],
    }


def create_product_card(
    client,
    company_id: str,
    name: str = "Confirmed Inspection AI",
) -> dict:
    response = client.post(
        "/api/v1/product-cards",
        json=product_card_payload(company_id, name=name),
    )
    assert response.status_code == 201
    return response.json()["data"]


def create_confirmed_product_card(
    client,
    company_id: str,
    name: str = "Confirmed Inspection AI",
) -> dict:
    product_card = create_product_card(client, company_id, name=name)
    response = client.post(f"/api/v1/product-cards/{product_card['id']}/confirm")
    assert response.status_code == 200
    return response.json()["data"]


def campaign_payload(product_card_id: str, name: str = "DACH Factory QA Campaign") -> dict:
    return {
        "product_card_id": product_card_id,
        "name": name,
        "target_country": "Germany",
        "target_region": "DACH",
        "target_industry": "Manufacturing",
        "target_company_type": "Mid-market factories",
        "target_role": "Head of Quality",
        "search_keywords": ["factory quality inspection", "industrial AI QA"],
        "qualification_criteria": ["Has in-house production", "Mentions QA team"],
        "outreach_angle": "Reduce manual QA review time with traceable evidence.",
        "lead_limit": 25,
    }


def create_campaign(
    client,
    company_id: str,
    product_card_id: str,
    name: str = "DACH Factory QA Campaign",
) -> dict:
    response = client.post(
        f"/api/v1/companies/{company_id}/campaigns",
        json=campaign_payload(product_card_id, name=name),
    )
    assert response.status_code == 201
    return response.json()["data"]


def assert_campaign_not_found(response) -> None:
    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "campaign_not_found",
            "message": "Campaign not found.",
        }
    }


def assert_invalid_campaign_transition(response) -> None:
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "invalid_campaign_status_transition"


def test_create_campaign_defaults_to_draft(client) -> None:
    company_id = create_company(client)
    product_card = create_confirmed_product_card(client, company_id)

    response = client.post(
        f"/api/v1/companies/{company_id}/campaigns",
        json=campaign_payload(product_card["id"]),
    )
    body = response.json()

    assert response.status_code == 201
    assert body["message"] == "Campaign created successfully."
    assert body["data"]["company_id"] == company_id
    assert body["data"]["product_card_id"] == product_card["id"]
    assert body["data"]["product_card_snapshot"] is None
    assert body["data"]["status"] == "draft"
    assert body["data"]["search_keywords"] == [
        "factory quality inspection",
        "industrial AI QA",
    ]


def test_create_campaign_requires_confirmed_product_card_in_same_company(client) -> None:
    company_id = create_company(client)
    other_company_id = create_company(client, name="Other Campaign Company")
    draft_product_card = create_product_card(client, company_id, name="Draft Product")
    other_product_card = create_confirmed_product_card(
        client,
        other_company_id,
        name="Other Company Product",
    )

    missing_response = client.post(
        f"/api/v1/companies/{company_id}/campaigns",
        json=campaign_payload("missing-product-card"),
    )
    draft_response = client.post(
        f"/api/v1/companies/{company_id}/campaigns",
        json=campaign_payload(draft_product_card["id"]),
    )
    other_company_response = client.post(
        f"/api/v1/companies/{company_id}/campaigns",
        json=campaign_payload(other_product_card["id"]),
    )

    assert missing_response.status_code == 404
    assert missing_response.json()["error"]["code"] == "product_card_not_found"
    assert draft_response.status_code == 409
    assert draft_response.json()["error"]["code"] == "product_card_not_confirmed"
    assert other_company_response.status_code == 404
    assert other_company_response.json()["error"]["code"] == "product_card_not_found"


def test_edit_draft_campaign_works(client) -> None:
    company_id = create_company(client)
    product_card = create_confirmed_product_card(client, company_id)
    campaign = create_campaign(client, company_id, product_card["id"])

    response = client.patch(
        f"/api/v1/campaigns/{campaign['id']}",
        json={
            "name": "Updated Campaign",
            "search_keywords": ["machine vision QA"],
            "lead_limit": 10,
        },
    )
    body = response.json()

    assert response.status_code == 200
    assert body["data"]["id"] == campaign["id"]
    assert body["data"]["name"] == "Updated Campaign"
    assert body["data"]["search_keywords"] == ["machine vision QA"]
    assert body["data"]["lead_limit"] == 10
    assert body["data"]["status"] == "draft"


def test_delete_draft_campaign_works(client) -> None:
    company_id = create_company(client)
    product_card = create_confirmed_product_card(client, company_id)
    campaign = create_campaign(client, company_id, product_card["id"])

    response = client.delete(f"/api/v1/campaigns/{campaign['id']}")
    get_response = client.get(f"/api/v1/campaigns/{campaign['id']}")

    assert response.status_code == 200
    assert response.json() == {
        "data": {"id": campaign["id"], "deleted": True},
        "message": "Campaign deleted successfully.",
    }
    assert_campaign_not_found(get_response)


def test_confirm_draft_campaign_saves_product_card_snapshot(client) -> None:
    company_id = create_company(client)
    product_card = create_confirmed_product_card(client, company_id)
    campaign = create_campaign(client, company_id, product_card["id"])

    response = client.post(f"/api/v1/campaigns/{campaign['id']}/confirm")
    body = response.json()
    snapshot = body["data"]["product_card_snapshot"]

    assert response.status_code == 200
    assert body["data"]["status"] == "confirmed"
    assert snapshot["product_card_id"] == product_card["id"]
    assert snapshot["company_id"] == company_id
    assert snapshot["name"] == product_card["name"]
    assert snapshot["target_customer"] == product_card["target_customer"]
    assert snapshot["pain_points"] == product_card["pain_points"]
    assert snapshot["value_proposition"] == product_card["value_proposition"]


def test_confirm_already_confirmed_campaign_is_idempotent(client) -> None:
    company_id = create_company(client)
    product_card = create_confirmed_product_card(client, company_id)
    campaign = create_campaign(client, company_id, product_card["id"])

    first_response = client.post(f"/api/v1/campaigns/{campaign['id']}/confirm")
    second_response = client.post(f"/api/v1/campaigns/{campaign['id']}/confirm")

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert second_response.json()["data"]["id"] == campaign["id"]
    assert second_response.json()["data"]["status"] == "confirmed"
    assert second_response.json()["data"]["product_card_snapshot"] == (
        first_response.json()["data"]["product_card_snapshot"]
    )


def test_confirm_fails_if_product_card_is_missing(client) -> None:
    company_id = create_company(client)
    product_card = create_confirmed_product_card(client, company_id)
    campaign = create_campaign(client, company_id, product_card["id"])

    with db_session_for_client() as session:
        persisted_campaign = session.get(Campaign, campaign["id"])
        persisted_campaign.product_card_id = "missing-product-card"
        session.commit()

    response = client.post(f"/api/v1/campaigns/{campaign['id']}/confirm")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "product_card_not_found"


def test_confirm_fails_if_product_card_belongs_to_another_company(client) -> None:
    company_id = create_company(client)
    other_company_id = create_company(client, name="Other Scope Company")
    product_card = create_confirmed_product_card(client, company_id)
    campaign = create_campaign(client, company_id, product_card["id"])

    with db_session_for_client() as session:
        persisted_product_card = session.get(ProductCard, product_card["id"])
        persisted_product_card.company_id = other_company_id
        session.commit()

    response = client.post(f"/api/v1/campaigns/{campaign['id']}/confirm")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "product_card_not_found"


def test_confirm_fails_if_product_card_is_not_confirmed(client) -> None:
    company_id = create_company(client)
    product_card = create_confirmed_product_card(client, company_id)
    campaign = create_campaign(client, company_id, product_card["id"])

    with db_session_for_client() as session:
        persisted_product_card = session.get(ProductCard, product_card["id"])
        persisted_product_card.status = "draft"
        session.commit()

    response = client.post(f"/api/v1/campaigns/{campaign['id']}/confirm")

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "product_card_not_confirmed"


def test_edit_confirmed_campaign_is_rejected(client) -> None:
    company_id = create_company(client)
    product_card = create_confirmed_product_card(client, company_id)
    campaign = create_campaign(client, company_id, product_card["id"])
    client.post(f"/api/v1/campaigns/{campaign['id']}/confirm")

    response = client.patch(
        f"/api/v1/campaigns/{campaign['id']}",
        json={"name": "Should Not Edit"},
    )

    assert_invalid_campaign_transition(response)


def test_delete_confirmed_campaign_is_rejected(client) -> None:
    company_id = create_company(client)
    product_card = create_confirmed_product_card(client, company_id)
    campaign = create_campaign(client, company_id, product_card["id"])
    client.post(f"/api/v1/campaigns/{campaign['id']}/confirm")

    response = client.delete(f"/api/v1/campaigns/{campaign['id']}")

    assert_invalid_campaign_transition(response)


def test_archive_confirmed_campaign_works(client) -> None:
    company_id = create_company(client)
    product_card = create_confirmed_product_card(client, company_id)
    campaign = create_campaign(client, company_id, product_card["id"])
    client.post(f"/api/v1/campaigns/{campaign['id']}/confirm")

    response = client.post(f"/api/v1/campaigns/{campaign['id']}/archive")

    assert response.status_code == 200
    assert response.json()["data"]["status"] == "archived"


def test_archived_campaign_is_read_only_and_not_restorable(client) -> None:
    company_id = create_company(client)
    product_card = create_confirmed_product_card(client, company_id)
    campaign = create_campaign(client, company_id, product_card["id"])
    client.post(f"/api/v1/campaigns/{campaign['id']}/confirm")
    client.post(f"/api/v1/campaigns/{campaign['id']}/archive")

    edit_response = client.patch(
        f"/api/v1/campaigns/{campaign['id']}",
        json={"name": "Archived Should Not Edit"},
    )
    delete_response = client.delete(f"/api/v1/campaigns/{campaign['id']}")
    confirm_response = client.post(f"/api/v1/campaigns/{campaign['id']}/confirm")
    archive_again_response = client.post(f"/api/v1/campaigns/{campaign['id']}/archive")
    restore_response = client.post(f"/api/v1/campaigns/{campaign['id']}/restore")
    status_patch_response = client.patch(
        f"/api/v1/campaigns/{campaign['id']}",
        json={"status": "draft"},
    )

    assert_invalid_campaign_transition(edit_response)
    assert_invalid_campaign_transition(delete_response)
    assert_invalid_campaign_transition(confirm_response)
    assert_invalid_campaign_transition(archive_again_response)
    assert restore_response.status_code == 404
    assert status_patch_response.status_code == 422
    assert status_patch_response.json()["error"]["code"] == "validation_error"


def test_archived_campaign_is_hidden_from_default_list_and_explicitly_listed(
    client,
) -> None:
    company_id = create_company(client)
    product_card = create_confirmed_product_card(client, company_id)
    draft_campaign = create_campaign(
        client,
        company_id,
        product_card["id"],
        name="Visible Draft Campaign",
    )
    archived_campaign = create_campaign(
        client,
        company_id,
        product_card["id"],
        name="Archived Campaign",
    )
    client.post(f"/api/v1/campaigns/{archived_campaign['id']}/confirm")
    client.post(f"/api/v1/campaigns/{archived_campaign['id']}/archive")

    default_response = client.get(
        f"/api/v1/companies/{company_id}/campaigns?limit=10&offset=0"
    )
    archived_response = client.get(
        f"/api/v1/companies/{company_id}/campaigns"
        "?status=archived&limit=10&offset=0"
    )

    assert default_response.status_code == 200
    assert default_response.json()["data"]["pagination"]["total"] == 1
    assert [item["id"] for item in default_response.json()["data"]["items"]] == [
        draft_campaign["id"]
    ]

    assert archived_response.status_code == 200
    assert archived_response.json()["data"]["pagination"]["total"] == 1
    assert [item["id"] for item in archived_response.json()["data"]["items"]] == [
        archived_campaign["id"]
    ]


def test_duplicate_campaign_creates_new_draft_without_confirmed_snapshot(
    client,
) -> None:
    company_id = create_company(client)
    product_card = create_confirmed_product_card(client, company_id)
    campaign = create_campaign(client, company_id, product_card["id"])
    confirmed = client.post(f"/api/v1/campaigns/{campaign['id']}/confirm").json()[
        "data"
    ]

    response = client.post(f"/api/v1/campaigns/{campaign['id']}/duplicate")
    body = response.json()
    source_response = client.get(f"/api/v1/campaigns/{campaign['id']}")

    assert response.status_code == 201
    assert body["data"]["id"] != campaign["id"]
    assert body["data"]["status"] == "draft"
    assert body["data"]["product_card_id"] == product_card["id"]
    assert body["data"]["product_card_snapshot"] is None
    assert body["data"]["name"] == campaign["name"]
    assert source_response.json()["data"]["status"] == "confirmed"
    assert source_response.json()["data"]["product_card_snapshot"] == (
        confirmed["product_card_snapshot"]
    )


def test_unsupported_campaign_status_values_are_rejected(client) -> None:
    company_id = create_company(client)
    product_card = create_confirmed_product_card(client, company_id)
    payload = campaign_payload(product_card["id"])
    payload["status"] = "running"

    create_response = client.post(
        f"/api/v1/companies/{company_id}/campaigns",
        json=payload,
    )
    list_response = client.get(
        f"/api/v1/companies/{company_id}/campaigns?status=running"
    )

    assert create_response.status_code == 422
    assert create_response.json()["error"]["code"] == "validation_error"
    assert list_response.status_code == 422
    assert list_response.json()["error"]["code"] == "validation_error"
