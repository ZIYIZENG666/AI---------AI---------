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
        review_response = client.post(
            f"/api/v1/knowledge/{knowledge['id']}/{action}"
        )
        assert review_response.status_code == 200
        return review_response.json()["data"]

    return knowledge


def create_product_card(client, company_id: str) -> dict:
    response = client.post(f"/api/v1/companies/{company_id}/product-cards")
    assert response.status_code == 201
    return response.json()["data"]


def test_create_product_card_from_confirmed_knowledge(client) -> None:
    company_id = create_company(client)
    confirmed = create_knowledge_item(
        client,
        company_id,
        title="Inspection platform",
        content="A robotic platform for automated industrial inspection.",
    )

    response = client.post(f"/api/v1/companies/{company_id}/product-cards")
    body = response.json()

    assert response.status_code == 201
    assert body["message"] == "Product card created successfully."
    assert body["data"]["company_id"] == company_id
    assert body["data"]["name"] == "Product Test Company Product Card"
    assert body["data"]["description"] == (
        "A robotic platform for automated industrial inspection."
    )
    assert body["data"]["target_customer"] == "Industrial manufacturers"
    assert body["data"]["value_proposition"] == "Reduce inspection downtime."
    assert body["data"]["pain_points"] == []
    assert body["data"]["use_cases"] == []
    assert body["data"]["differentiators"] == []
    assert body["data"]["source_knowledge_item_ids"] == [confirmed["id"]]
    assert body["data"]["status"] == "draft"


def test_create_product_card_fails_without_confirmed_knowledge(client) -> None:
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


def test_product_card_ignores_draft_and_rejected_knowledge(client) -> None:
    company_id = create_company(client)
    confirmed = create_knowledge_item(
        client,
        company_id,
        title="Confirmed knowledge",
        content="Only confirmed content is eligible.",
    )
    draft = create_knowledge_item(
        client,
        company_id,
        title="Draft knowledge",
        content="Draft content must not be used.",
        review_status="draft",
    )
    rejected = create_knowledge_item(
        client,
        company_id,
        title="Rejected knowledge",
        content="Rejected content must not be used.",
        review_status="rejected",
    )

    product_card = create_product_card(client, company_id)

    assert product_card["source_knowledge_item_ids"] == [confirmed["id"]]
    assert draft["id"] not in product_card["source_knowledge_item_ids"]
    assert rejected["id"] not in product_card["source_knowledge_item_ids"]
    assert product_card["description"] == "Only confirmed content is eligible."


def test_list_product_cards_by_company(client) -> None:
    company_id = create_company(client)
    other_company_id = create_company(client, name="Other Product Company")
    create_knowledge_item(
        client,
        company_id,
        title="Primary knowledge",
        content="Primary company product information.",
    )
    create_knowledge_item(
        client,
        other_company_id,
        title="Other knowledge",
        content="Other company product information.",
    )
    first = create_product_card(client, company_id)
    second = create_product_card(client, company_id)
    create_product_card(client, other_company_id)

    response = client.get(
        f"/api/v1/companies/{company_id}/product-cards?limit=10&offset=0"
    )
    body = response.json()

    assert response.status_code == 200
    assert body["data"]["pagination"] == {"total": 2, "limit": 10, "offset": 0}
    assert {item["id"] for item in body["data"]["items"]} == {
        first["id"],
        second["id"],
    }


def test_get_product_card_by_id(client) -> None:
    company_id = create_company(client)
    create_knowledge_item(
        client,
        company_id,
        title="Lookup knowledge",
        content="Product information for lookup.",
    )
    created = create_product_card(client, company_id)

    response = client.get(f"/api/v1/product-cards/{created['id']}")

    assert response.status_code == 200
    assert response.json()["message"] == "Product card fetched successfully."
    assert response.json()["data"] == created


def test_confirm_product_card(client) -> None:
    company_id = create_company(client)
    create_knowledge_item(
        client,
        company_id,
        title="Confirm knowledge",
        content="Product information ready for confirmation.",
    )
    product_card = create_product_card(client, company_id)

    response = client.post(f"/api/v1/product-cards/{product_card['id']}/confirm")

    assert response.status_code == 200
    assert response.json()["message"] == "Product card confirmed successfully."
    assert response.json()["data"]["status"] == "confirmed"


def test_reject_product_card(client) -> None:
    company_id = create_company(client)
    create_knowledge_item(
        client,
        company_id,
        title="Reject knowledge",
        content="Product information to reject.",
    )
    product_card = create_product_card(client, company_id)

    response = client.post(f"/api/v1/product-cards/{product_card['id']}/reject")

    assert response.status_code == 200
    assert response.json()["message"] == "Product card rejected successfully."
    assert response.json()["data"]["status"] == "rejected"


def test_get_product_card_returns_not_found_for_invalid_id(client) -> None:
    response = client.get("/api/v1/product-cards/missing-product-card")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "product_card_not_found",
            "message": "Product card not found.",
        }
    }


def test_confirm_rejects_non_draft_product_card(client) -> None:
    company_id = create_company(client)
    create_knowledge_item(
        client,
        company_id,
        title="Transition knowledge",
        content="Product information for transition testing.",
    )
    product_card = create_product_card(client, company_id)
    client.post(f"/api/v1/product-cards/{product_card['id']}/confirm")

    response = client.post(f"/api/v1/product-cards/{product_card['id']}/confirm")

    assert response.status_code == 409
    assert response.json() == {
        "error": {
            "code": "product_card_not_draft",
            "message": "Only draft product cards can be reviewed.",
        }
    }
