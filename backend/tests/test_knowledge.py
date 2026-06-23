def create_company(client) -> str:
    response = client.post("/api/v1/companies", json={"name": "Knowledge Test Company"})
    assert response.status_code == 201
    return response.json()["data"]["id"]


def create_source(client, company_id: str, title: str = "Knowledge source") -> str:
    response = client.post(
        f"/api/v1/companies/{company_id}/sources",
        json={
            "source_type": "text",
            "title": title,
            "raw_content": "We help manufacturers reduce inspection downtime.",
        },
    )
    assert response.status_code == 201
    return response.json()["data"]["id"]


def create_knowledge_draft(client, source_id: str) -> dict:
    response = client.post(f"/api/v1/sources/{source_id}/knowledge-drafts")
    assert response.status_code == 201
    return response.json()["data"]


def test_create_knowledge_draft_from_source(client) -> None:
    company_id = create_company(client)
    source_id = create_source(client, company_id)

    response = client.post(f"/api/v1/sources/{source_id}/knowledge-drafts")
    body = response.json()

    assert response.status_code == 201
    assert body["message"] == "Knowledge draft created successfully."
    assert body["data"]["company_id"] == company_id
    assert body["data"]["source_id"] == source_id
    assert body["data"]["status"] == "draft"
    assert body["data"]["content"] == (
        "We help manufacturers reduce inspection downtime."
    )
    assert body["data"]["confidence"] is None


def test_confirm_draft_knowledge_item(client) -> None:
    company_id = create_company(client)
    draft = create_knowledge_draft(client, create_source(client, company_id))

    response = client.post(f"/api/v1/knowledge/{draft['id']}/confirm")

    assert response.status_code == 200
    assert response.json()["message"] == "Knowledge item confirmed successfully."
    assert response.json()["data"]["status"] == "confirmed"


def test_reject_draft_knowledge_item(client) -> None:
    company_id = create_company(client)
    draft = create_knowledge_draft(client, create_source(client, company_id))

    response = client.post(f"/api/v1/knowledge/{draft['id']}/reject")

    assert response.status_code == 200
    assert response.json()["message"] == "Knowledge item rejected successfully."
    assert response.json()["data"]["status"] == "rejected"


def test_list_knowledge_separates_confirmed_from_drafts(client) -> None:
    company_id = create_company(client)
    confirmed_draft = create_knowledge_draft(
        client,
        create_source(client, company_id, title="Confirmed source"),
    )
    remaining_draft = create_knowledge_draft(
        client,
        create_source(client, company_id, title="Draft source"),
    )
    client.post(f"/api/v1/knowledge/{confirmed_draft['id']}/confirm")

    confirmed_response = client.get(
        f"/api/v1/companies/{company_id}/knowledge?status=confirmed"
    )
    draft_response = client.get(
        f"/api/v1/companies/{company_id}/knowledge?status=draft"
    )

    assert confirmed_response.status_code == 200
    assert confirmed_response.json()["data"]["pagination"]["total"] == 1
    assert confirmed_response.json()["data"]["items"][0]["id"] == confirmed_draft["id"]
    assert draft_response.status_code == 200
    assert draft_response.json()["data"]["pagination"]["total"] == 1
    assert draft_response.json()["data"]["items"][0]["id"] == remaining_draft["id"]


def test_create_knowledge_draft_returns_not_found_for_invalid_source_id(client) -> None:
    response = client.post("/api/v1/sources/missing-source/knowledge-drafts")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "source_not_found",
            "message": "Company source not found.",
        }
    }


def test_review_returns_not_found_for_invalid_knowledge_id(client) -> None:
    response = client.post("/api/v1/knowledge/missing-knowledge/confirm")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "knowledge_not_found",
            "message": "Knowledge item not found.",
        }
    }


def test_confirm_rejects_non_draft_knowledge_item(client) -> None:
    company_id = create_company(client)
    draft = create_knowledge_draft(client, create_source(client, company_id))
    client.post(f"/api/v1/knowledge/{draft['id']}/confirm")

    response = client.post(f"/api/v1/knowledge/{draft['id']}/confirm")

    assert response.status_code == 409
    assert response.json() == {
        "error": {
            "code": "knowledge_not_draft",
            "message": "Only draft knowledge items can be reviewed.",
        }
    }
