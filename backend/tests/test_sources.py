def create_company(client, name: str = "Source Test Company") -> str:
    response = client.post("/api/v1/companies", json={"name": name})
    assert response.status_code == 201
    return response.json()["data"]["id"]


def test_create_text_source_for_existing_company(client) -> None:
    company_id = create_company(client)

    response = client.post(
        f"/api/v1/companies/{company_id}/sources",
        json={
            "source_type": "text",
            "title": "Company overview",
            "raw_content": "We build industrial inspection robots.",
        },
    )
    body = response.json()

    assert response.status_code == 201
    assert body["message"] == "Company source created successfully."
    assert body["data"]["company_id"] == company_id
    assert body["data"]["source_type"] == "text"
    assert body["data"]["raw_content"] == "We build industrial inspection robots."
    assert body["data"]["status"] == "ready"


def test_create_url_source_for_existing_company(client) -> None:
    company_id = create_company(client)

    response = client.post(
        f"/api/v1/companies/{company_id}/sources",
        json={
            "source_type": "url",
            "title": "Public website",
            "url": "https://example.com/about",
        },
    )

    assert response.status_code == 201
    assert response.json()["data"]["url"] == "https://example.com/about"
    assert response.json()["data"]["raw_content"] is None


def test_create_source_rejects_missing_company(client) -> None:
    response = client.post(
        "/api/v1/companies/missing-company/sources",
        json={
            "source_type": "text",
            "title": "Orphan source",
            "raw_content": "This source has no company.",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "company_not_found",
            "message": "Company profile not found.",
        }
    }


def test_list_sources_for_company(client) -> None:
    company_id = create_company(client)
    other_company_id = create_company(client, name="Other Company")

    client.post(
        f"/api/v1/companies/{company_id}/sources",
        json={
            "source_type": "text",
            "title": "First source",
            "raw_content": "First source content.",
        },
    )
    client.post(
        f"/api/v1/companies/{company_id}/sources",
        json={
            "source_type": "url",
            "title": "Second source",
            "url": "https://example.com/products",
        },
    )
    client.post(
        f"/api/v1/companies/{other_company_id}/sources",
        json={
            "source_type": "text",
            "title": "Other source",
            "raw_content": "Should not appear in the first company list.",
        },
    )

    response = client.get(
        f"/api/v1/companies/{company_id}/sources?limit=10&offset=0"
    )
    body = response.json()

    assert response.status_code == 200
    assert body["data"]["pagination"] == {"total": 2, "limit": 10, "offset": 0}
    assert {item["title"] for item in body["data"]["items"]} == {
        "First source",
        "Second source",
    }


def test_get_source_by_id(client) -> None:
    company_id = create_company(client)
    created = client.post(
        f"/api/v1/companies/{company_id}/sources",
        json={
            "source_type": "text",
            "title": "Lookup source",
            "raw_content": "Content for lookup.",
        },
    ).json()

    response = client.get(f"/api/v1/sources/{created['data']['id']}")

    assert response.status_code == 200
    assert response.json()["data"]["title"] == "Lookup source"


def test_get_source_returns_not_found_for_invalid_id(client) -> None:
    response = client.get("/api/v1/sources/missing-source")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "source_not_found",
            "message": "Company source not found.",
        }
    }
