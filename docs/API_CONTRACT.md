# API Contract

## Purpose

This document defines the API contract between frontend and backend.

It focuses on response shape, error shape, pagination, task responses, naming, versioning, and contract stability.

## General Rules

1. Use REST-style HTTP APIs for MVP.
2. Use JSON for request and response bodies.
3. Keep resource names stable and predictable.
4. Do not expose raw database internals unless the frontend truly needs them.
5. Long-running operations should return a task or job reference instead of blocking.
6. The contract must remain explicit even when the backend implementation is still evolving.

## API Base Path

Business APIs should live under:

- `/api/v1/...`

Operational endpoints such as health checks may stay outside versioned business APIs when appropriate, for example:

- `/health`
- `/health/db`
- `/health/redis`

## Phase 1B Resource Endpoints

The minimum sources and knowledge slice exposes:

- `POST /api/v1/companies/{company_id}/sources`
- `GET /api/v1/companies/{company_id}/sources`
- `GET /api/v1/sources/{source_id}`
- `POST /api/v1/sources/{source_id}/knowledge-drafts`
- `GET /api/v1/companies/{company_id}/knowledge`
- `POST /api/v1/knowledge/{knowledge_id}/confirm`
- `POST /api/v1/knowledge/{knowledge_id}/reject`

Rules:

1. Source creation supports only `source_type = text` and `source_type = url` in Phase 1B.
2. Text sources require `raw_content`; URL sources require `url` and may omit `raw_content`.
3. Knowledge draft creation is synchronous and deterministic in this phase. It must not imply that a crawler or LLM processed a URL.
4. `GET /api/v1/companies/{company_id}/knowledge` accepts optional `status`, `limit`, and `offset` query parameters.
5. The `status` filter accepts `draft`, `confirmed`, or `rejected`, allowing confirmed knowledge to be retrieved separately.
6. Confirm and reject endpoints accept only knowledge items currently in `draft`; invalid transitions return HTTP `409` with `knowledge_not_draft`.
7. Missing company, source, or knowledge IDs return HTTP `404` with stable resource-specific error codes.

## Phase 2 Product Card Endpoints

The target Product Card contract exposes:

- `POST /api/v1/companies/{company_id}/product-cards` for generation from confirmed company knowledge
- `POST /api/v1/product-cards` for user-created Product Cards
- `GET /api/v1/product-cards`
- `GET /api/v1/product-cards/{product_card_id}`
- `PATCH /api/v1/product-cards/{product_card_id}`
- `POST /api/v1/product-cards/{product_card_id}/confirm`
- `DELETE /api/v1/product-cards/{product_card_id}`

Rules:

1. Product Cards have only `draft` and `confirmed` business statuses. `rejected` is not valid, and there is no Product Card reject endpoint.
2. Generation uses confirmed knowledge only, sets `source_type = ai_generated` and `status = draft`, and persists the exact confirmed knowledge IDs in `source_knowledge_item_ids`.
3. User-created Product Cards use `POST /api/v1/product-cards`, set `source_type = manual` and `status = draft`, and must belong to a company.
4. The manual Product Card creation path must remain available even when AI generation is available.
5. `GET /api/v1/product-cards` returns both `draft` and `confirmed` records by default, supports only `status=draft` or `status=confirmed`, and uses the standard `limit` and `offset` pagination contract. `status=rejected` is invalid.
6. `PATCH /api/v1/product-cards/{product_card_id}` is allowed for both statuses, saves editable fields only, and must not change `status`.
7. `POST /api/v1/product-cards/{product_card_id}/confirm` changes `draft` to `confirmed`. Repeating it for an already confirmed Product Card returns HTTP `200` with the current record and leaves the status unchanged.
8. `DELETE /api/v1/product-cards/{product_card_id}` deletes a draft directly. It may delete a confirmed Product Card only when no Campaign has ever referenced it; otherwise it returns HTTP `409`.
9. Only confirmed Product Cards may be selected by a Campaign.
10. Missing Product Card IDs return HTTP `404` with `product_card_not_found` for get, patch, confirm, and delete operations.
11. AI-backed generation may replace the current deterministic generator later, but it must preserve the same source, status, evidence, and human-confirmation rules.

### Product Card Scope Hardening (Planned)

The current MVP remains a single-user prototype. ID-only get, patch, confirm, and delete operations must not be treated as the final authorization model.

Target repository/service query semantics:

- get by `product_card_id + company_id`
- patch by `product_card_id + company_id`
- confirm by `product_card_id + company_id`
- delete by `product_card_id + company_id`
- later extend each lookup with `workspace_id`

Rules:

1. Product Cards must remain associated with their owning company.
2. Company-scoped lookup hardening should be incorporated before or alongside Phase 3 Campaign work.
3. Workspace-scoped lookup is a future multi-tenant constraint and is not implemented yet.
4. Account or workspace authorization must not be claimed until the corresponding implementation and tests exist.
5. Product Card deletion must check Campaign references before physical deletion and return HTTP `409` when the card is in use.

## Success Response Format

Business endpoints should return a consistent envelope:

```json
{
  "data": {},
  "message": "Success"
}
```

Rules:

1. `data` contains the actual payload.
2. `message` is a short human-readable summary.
3. Do not mix success payloads with error payloads.

## Error Response Format

Application-level errors should return:

```json
{
  "error": {
    "code": "resource_not_found",
    "message": "Resource not found."
  }
}
```

Rules:

1. `error.code` should be stable and machine-friendly.
2. `error.message` should be short and user-readable.
3. Do not leak secrets, connection strings, stack traces, or provider credentials.

## Validation Error Format

Request validation failures should use HTTP `422` and return structured details:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed.",
    "details": [
      {
        "loc": ["body", "name"],
        "msg": "Field required",
        "type": "missing"
      }
    ]
  }
}
```

Rules:

1. Validation errors must clearly point to the invalid field or location.
2. Frontend should treat validation failures differently from server failures.
3. Validation output should be stable enough for form error mapping.

## Pagination Format

List endpoints should use `limit` and `offset` query parameters for MVP unless a different scheme is explicitly documented.

Recommended response format:

```json
{
  "data": {
    "items": [],
    "pagination": {
      "total": 0,
      "limit": 20,
      "offset": 0
    }
  },
  "message": "Items fetched successfully."
}
```

Rules:

1. `items` contains the current page.
2. `total` is the total matching records before paging.
3. `limit` and `offset` echo the applied paging inputs.

## Task / Job Response Format

Long-running actions should return a task reference instead of pretending to finish synchronously.

Recommended response:

```json
{
  "data": {
    "task_id": "task_123",
    "status": "pending",
    "task_type": "lead_discovery"
  },
  "message": "Task created successfully."
}
```

Rules:

1. Task status values should be explicit, for example `pending`, `running`, `completed`, `failed`.
2. Task creation response must not imply that downstream work already finished.
3. If a task result is not ready, return the task status rather than partial fake business data.

## Naming Conventions

Rules:

1. Use plural nouns for collection resources, for example `/companies`, `/campaigns`, `/leads`.
2. Use snake_case for JSON field names unless a field is already standardized differently.
3. Keep enum values lowercase with underscores when possible.
4. Keep IDs stable once published.
5. Avoid mixing naming styles within the same payload.

## Status Code Rules

Recommended status codes:

- `200 OK`: successful read or update
- `201 Created`: successful creation
- `202 Accepted`: accepted async work if used
- `400 Bad Request`: malformed request not covered by schema validation
- `404 Not Found`: requested resource does not exist
- `409 Conflict`: invalid business state transition or uniqueness conflict
- `422 Unprocessable Entity`: request validation failure
- `500 Internal Server Error`: unexpected server failure
- `503 Service Unavailable`: dependency unavailable, such as database or Redis health failure

Rules:

1. Do not return `200` for real failures.
2. Do not hide dependency failures behind fake success messages.
3. Keep status codes consistent across modules.

## API Versioning Rule

Rules:

1. Version business APIs in the path, starting with `/api/v1`.
2. Do not change published response shapes silently.
3. If a breaking contract change is needed later, introduce a new version instead of mutating the old one without notice.

## LinkedIn API Boundary

Rules:

1. No API endpoint may trigger LinkedIn automation of any kind.
2. Do not expose endpoints that scrape LinkedIn, log in to LinkedIn, send LinkedIn messages, send connection requests, download LinkedIn contacts, or automatically enrich leads from LinkedIn.
3. Allowed endpoints may store a user-provided LinkedIn URL as a manual contact reference, return that LinkedIn URL for frontend human review, and mark `contact_type = linkedin`.
4. LinkedIn references must not be used as Gmail Draft recipients or as Gmail Draft eligibility.

## Frontend / Backend Contract Rule

Rules:

1. Frontend must rely only on documented fields.
2. Backend must not remove or rename fields casually once frontend depends on them.
3. If temporary placeholder fields are returned, label them clearly in implementation notes or docs.
4. Routes, schemas, and tests should reflect the same contract.
5. When the contract changes, update both the backend schemas and the related frontend usage together.
