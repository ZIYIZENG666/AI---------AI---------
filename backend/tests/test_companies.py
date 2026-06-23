def test_create_company(client) -> None:
    response = client.post(
        "/api/v1/companies",
        json={
            "name": "Acme Robotics",
            "website": "https://acme.example",
            "industry": "Industrial Automation",
            "workspace_id": "workspace-001",
        },
    )

    body = response.json()

    assert response.status_code == 201
    assert body["message"] == "Company profile created successfully."
    assert body["data"]["name"] == "Acme Robotics"
    assert body["data"]["workspace_id"] == "workspace-001"
    assert body["data"]["id"]


def test_list_companies(client) -> None:
    client.post("/api/v1/companies", json={"name": "Alpha Manufacturing"})
    client.post("/api/v1/companies", json={"name": "Beta Systems"})

    response = client.get("/api/v1/companies?limit=10&offset=0")
    body = response.json()

    assert response.status_code == 200
    assert body["message"] == "Company profiles fetched successfully."
    assert body["data"]["pagination"] == {
        "total": 2,
        "limit": 10,
        "offset": 0,
    }
    assert {item["name"] for item in body["data"]["items"]} == {
        "Alpha Manufacturing",
        "Beta Systems",
    }


def test_get_company(client) -> None:
    created = client.post("/api/v1/companies", json={"name": "Northwind Exports"}).json()

    response = client.get(f"/api/v1/companies/{created['data']['id']}")
    body = response.json()

    assert response.status_code == 200
    assert body["data"]["name"] == "Northwind Exports"


def test_update_company(client) -> None:
    created = client.post(
        "/api/v1/companies",
        json={"name": "Original Name", "industry": "Manufacturing"},
    ).json()

    response = client.patch(
        f"/api/v1/companies/{created['data']['id']}",
        json={
            "name": "Updated Name",
            "value_proposition": "Shorter sales cycles through AI research.",
        },
    )
    body = response.json()

    assert response.status_code == 200
    assert body["message"] == "Company profile updated successfully."
    assert body["data"]["name"] == "Updated Name"
    assert body["data"]["value_proposition"] == "Shorter sales cycles through AI research."


def test_get_company_returns_not_found_for_missing_id(client) -> None:
    response = client.get("/api/v1/companies/non-existent-id")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "company_not_found",
            "message": "Company profile not found.",
        }
    }
