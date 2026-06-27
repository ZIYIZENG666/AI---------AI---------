import pytest
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.main import app
from app.modules.campaigns.repository import CampaignRepository
from app.modules.company.repository import CompanyRepository
from app.modules.knowledge.repository import KnowledgeRepository
from app.modules.products.repository import ProductRepository
from app.modules.products.routes import get_product_service
from app.modules.products.service import ProductService


def create_company(client, name: str = "Product Test Company") -> str:
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


def create_knowledge_item(
    client,
    company_id: str,
    title: str,
    content: str,
    review_status: str = "confirmed",
) -> dict:
    source_response = client.post(
        f"/api/v1/companies/{company_id}/sources",
        json={
            "source_type": "text",
            "title": title,
            "raw_content": content,
        },
    )
    assert source_response.status_code == 201
    source_id = source_response.json()["data"]["id"]

    draft_response = client.post(f"/api/v1/sources/{source_id}/knowledge-drafts")
    assert draft_response.status_code == 201
    knowledge = draft_response.json()["data"]

    if review_status in {"confirmed", "rejected"}:
        action = "confirm" if review_status == "confirmed" else "reject"
        review_response = client.post(f"/api/v1/knowledge/{knowledge['id']}/{action}")
        assert review_response.status_code == 200
        return review_response.json()["data"]

    return knowledge


def manual_product_card_payload(company_id: str, name: str = "Manual Inspection AI") -> dict:
    return {
        "company_id": company_id,
        "name": name,
        "description": "A manually entered inspection automation product.",
        "target_customer": "Quality teams at manufacturers",
        "pain_points": ["Manual inspection is slow"],
        "value_proposition": "Find defects faster with less downtime.",
        "use_cases": ["Factory quality assurance"],
        "differentiators": ["Evidence-first recommendations"],
    }


def create_manual_product_card(
    client,
    company_id: str,
    name: str = "Manual Inspection AI",
) -> dict:
    response = client.post(
        "/api/v1/product-cards",
        json=manual_product_card_payload(company_id, name=name),
    )
    assert response.status_code == 201
    return response.json()["data"]


def create_ai_product_card(client, company_id: str) -> dict:
    response = client.post(f"/api/v1/companies/{company_id}/product-cards")
    assert response.status_code == 201
    return response.json()["data"]


def assert_product_card_not_found(response) -> None:
    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "product_card_not_found",
            "message": "Product card not found.",
        }
    }


def test_ai_generated_product_card_uses_confirmed_knowledge_only(client) -> None:
    company_id = create_company(client)
    confirmed = create_knowledge_item(
        client,
        company_id,
        title="Confirmed product knowledge",
        content="Only this confirmed product content should be used.",
    )
    draft = create_knowledge_item(
        client,
        company_id,
        title="Draft product knowledge",
        content="Draft content must not be used.",
        review_status="draft",
    )
    rejected = create_knowledge_item(
        client,
        company_id,
        title="Rejected product knowledge",
        content="Rejected content must not be used.",
        review_status="rejected",
    )

    response = client.post(f"/api/v1/companies/{company_id}/product-cards")
    body = response.json()

    assert response.status_code == 201
    assert body["message"] == "Product card created successfully."
    assert body["data"]["company_id"] == company_id
    assert body["data"]["source_type"] == "ai_generated"
    assert body["data"]["status"] == "draft"
    assert body["data"]["source_knowledge_item_ids"] == [confirmed["id"]]
    assert draft["id"] not in body["data"]["source_knowledge_item_ids"]
    assert rejected["id"] not in body["data"]["source_knowledge_item_ids"]
    assert body["data"]["description"] == (
        "Only this confirmed product content should be used."
    )


def test_ai_generated_product_card_fails_without_confirmed_knowledge(client) -> None:
    company_id = create_company(client)
    create_knowledge_item(
        client,
        company_id,
        title="Unreviewed knowledge",
        content="This remains a draft.",
        review_status="draft",
    )
    create_knowledge_item(
        client,
        company_id,
        title="Rejected knowledge",
        content="This was rejected.",
        review_status="rejected",
    )

    response = client.post(f"/api/v1/companies/{company_id}/product-cards")

    assert response.status_code == 409
    assert response.json() == {
        "error": {
            "code": "confirmed_knowledge_required",
            "message": "At least one confirmed knowledge item is required.",
        }
    }


def test_manual_product_card_creation_requires_company_and_defaults_source_ids(
    client,
) -> None:
    company_id = create_company(client)

    response = client.post(
        "/api/v1/product-cards",
        json={
            "company_id": company_id,
            "name": "Manual Product",
            "description": "User-authored product card.",
            "target_customer": "Operations teams",
            "value_proposition": "A clear manually entered value proposition.",
        },
    )
    body = response.json()

    assert response.status_code == 201
    assert body["data"]["company_id"] == company_id
    assert body["data"]["source_type"] == "manual"
    assert body["data"]["status"] == "draft"
    assert body["data"]["source_knowledge_item_ids"] == []
    assert body["data"]["pain_points"] == []
    assert body["data"]["use_cases"] == []
    assert body["data"]["differentiators"] == []


def test_manual_product_card_requires_company_id(client) -> None:
    payload = manual_product_card_payload("placeholder-company-id")
    payload.pop("company_id")

    response = client.post("/api/v1/product-cards", json=payload)

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


def test_product_card_source_type_values_for_ai_and_manual_cards(client) -> None:
    company_id = create_company(client)
    create_knowledge_item(
        client,
        company_id,
        title="Confirmed AI source",
        content="Confirmed source for AI-generated product card.",
    )

    ai_generated = create_ai_product_card(client, company_id)
    manual = create_manual_product_card(client, company_id)

    assert ai_generated["source_type"] == "ai_generated"
    assert manual["source_type"] == "manual"


def test_rejected_product_card_status_is_not_supported(client) -> None:
    company_id = create_company(client)
    payload = manual_product_card_payload(company_id)
    payload["status"] = "rejected"

    create_response = client.post("/api/v1/product-cards", json=payload)
    list_response = client.get("/api/v1/product-cards?status=rejected")

    assert create_response.status_code == 422
    assert create_response.json()["error"]["code"] == "validation_error"
    assert list_response.status_code == 422
    assert list_response.json()["error"]["code"] == "validation_error"


def test_reject_endpoint_is_not_available(client) -> None:
    company_id = create_company(client)
    product_card = create_manual_product_card(client, company_id)

    response = client.post(f"/api/v1/product-cards/{product_card['id']}/reject")

    assert response.status_code == 404


def test_list_product_cards_filters_by_draft_and_confirmed(client) -> None:
    company_id = create_company(client)
    draft = create_manual_product_card(client, company_id, name="Draft Card")
    confirmed = create_manual_product_card(client, company_id, name="Confirmed Card")
    client.post(f"/api/v1/product-cards/{confirmed['id']}/confirm")

    default_response = client.get("/api/v1/product-cards?limit=10&offset=0")
    draft_response = client.get("/api/v1/product-cards?status=draft&limit=10&offset=0")
    confirmed_response = client.get(
        "/api/v1/product-cards?status=confirmed&limit=10&offset=0"
    )

    assert default_response.status_code == 200
    assert default_response.json()["data"]["pagination"] == {
        "total": 2,
        "limit": 10,
        "offset": 0,
    }
    assert {
        item["id"] for item in default_response.json()["data"]["items"]
    } == {draft["id"], confirmed["id"]}

    assert draft_response.status_code == 200
    assert [item["id"] for item in draft_response.json()["data"]["items"]] == [
        draft["id"]
    ]
    assert confirmed_response.status_code == 200
    assert [item["id"] for item in confirmed_response.json()["data"]["items"]] == [
        confirmed["id"]
    ]


def test_company_product_card_list_uses_same_status_filter(client) -> None:
    company_id = create_company(client)
    other_company_id = create_company(client, name="Other Product Company")
    draft = create_manual_product_card(client, company_id, name="Company Draft")
    confirmed = create_manual_product_card(client, company_id, name="Company Confirmed")
    create_manual_product_card(client, other_company_id, name="Other Draft")
    client.post(f"/api/v1/product-cards/{confirmed['id']}/confirm")

    response = client.get(
        f"/api/v1/companies/{company_id}/product-cards?status=draft&limit=10&offset=0"
    )

    assert response.status_code == 200
    assert response.json()["data"]["pagination"] == {
        "total": 1,
        "limit": 10,
        "offset": 0,
    }
    assert [item["id"] for item in response.json()["data"]["items"]] == [draft["id"]]


def test_get_product_card_by_id(client) -> None:
    company_id = create_company(client)
    created = create_manual_product_card(client, company_id)

    response = client.get(f"/api/v1/product-cards/{created['id']}")

    assert response.status_code == 200
    assert response.json()["message"] == "Product card fetched successfully."
    assert response.json()["data"] == created


def test_patch_edits_draft_and_confirmed_without_changing_status(client) -> None:
    company_id = create_company(client)
    product_card = create_manual_product_card(client, company_id)

    draft_update = client.patch(
        f"/api/v1/product-cards/{product_card['id']}",
        json={
            "name": "Updated Draft Product",
            "pain_points": ["Inspection evidence is scattered"],
        },
    )
    confirmed = client.post(f"/api/v1/product-cards/{product_card['id']}/confirm")
    confirmed_update = client.patch(
        f"/api/v1/product-cards/{product_card['id']}",
        json={
            "description": "Updated after user confirmation.",
            "use_cases": ["Confirmed card editing"],
        },
    )
    status_update = client.patch(
        f"/api/v1/product-cards/{product_card['id']}",
        json={"status": "draft"},
    )

    assert draft_update.status_code == 200
    assert draft_update.json()["data"]["name"] == "Updated Draft Product"
    assert draft_update.json()["data"]["status"] == "draft"
    assert draft_update.json()["data"]["pain_points"] == [
        "Inspection evidence is scattered"
    ]

    assert confirmed.status_code == 200
    assert confirmed.json()["data"]["status"] == "confirmed"

    assert confirmed_update.status_code == 200
    assert confirmed_update.json()["data"]["description"] == (
        "Updated after user confirmation."
    )
    assert confirmed_update.json()["data"]["use_cases"] == [
        "Confirmed card editing"
    ]
    assert confirmed_update.json()["data"]["status"] == "confirmed"

    assert status_update.status_code == 422
    assert status_update.json()["error"]["code"] == "validation_error"


def test_confirm_product_card_is_idempotent(client) -> None:
    company_id = create_company(client)
    product_card = create_manual_product_card(client, company_id)

    first_response = client.post(f"/api/v1/product-cards/{product_card['id']}/confirm")
    second_response = client.post(f"/api/v1/product-cards/{product_card['id']}/confirm")

    assert first_response.status_code == 200
    assert first_response.json()["data"]["status"] == "confirmed"
    assert second_response.status_code == 200
    assert second_response.json()["data"]["status"] == "confirmed"
    assert second_response.json()["data"]["id"] == product_card["id"]


def test_delete_draft_product_card(client) -> None:
    company_id = create_company(client)
    product_card = create_manual_product_card(client, company_id)

    response = client.delete(f"/api/v1/product-cards/{product_card['id']}")
    get_response = client.get(f"/api/v1/product-cards/{product_card['id']}")

    assert response.status_code == 200
    assert response.json() == {
        "data": {"id": product_card["id"], "deleted": True},
        "message": "Product card deleted successfully.",
    }
    assert_product_card_not_found(get_response)


def test_delete_confirmed_product_card_when_not_referenced(client) -> None:
    company_id = create_company(client)
    product_card = create_manual_product_card(client, company_id)
    client.post(f"/api/v1/product-cards/{product_card['id']}/confirm")

    response = client.delete(f"/api/v1/product-cards/{product_card['id']}")
    get_response = client.get(f"/api/v1/product-cards/{product_card['id']}")

    assert response.status_code == 200
    assert response.json()["data"] == {"id": product_card["id"], "deleted": True}
    assert_product_card_not_found(get_response)


def test_delete_confirmed_product_card_checks_campaign_reference_boundary(
    client,
) -> None:
    class ReferencedCampaignRepository(CampaignRepository):
        def is_product_card_referenced(self, product_card_id: str) -> bool:
            return True

    def override_product_service(db: Session = Depends(get_db)) -> ProductService:
        return ProductService(
            repository=ProductRepository(db),
            company_repository=CompanyRepository(db),
            knowledge_repository=KnowledgeRepository(db),
            campaign_repository=ReferencedCampaignRepository(db),
        )

    company_id = create_company(client)
    product_card = create_manual_product_card(client, company_id)
    client.post(f"/api/v1/product-cards/{product_card['id']}/confirm")
    app.dependency_overrides[get_product_service] = override_product_service

    response = client.delete(f"/api/v1/product-cards/{product_card['id']}")

    assert response.status_code == 409
    assert response.json() == {
        "error": {
            "code": "product_card_in_use",
            "message": "Product card is already referenced by a campaign.",
        }
    }


@pytest.mark.parametrize(
    ("method_name", "path", "payload"),
    [
        ("get", "/api/v1/product-cards/missing-product-card", None),
        ("patch", "/api/v1/product-cards/missing-product-card", {}),
        ("post", "/api/v1/product-cards/missing-product-card/confirm", None),
        ("delete", "/api/v1/product-cards/missing-product-card", None),
    ],
)
def test_missing_product_card_returns_product_card_not_found(
    client,
    method_name: str,
    path: str,
    payload: dict | None,
) -> None:
    request = getattr(client, method_name)
    kwargs = {"json": payload} if payload is not None else {}

    response = request(path, **kwargs)

    assert_product_card_not_found(response)
