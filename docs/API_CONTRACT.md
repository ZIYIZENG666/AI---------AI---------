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

## Frontend / Backend Contract Rule

Rules:

1. Frontend must rely only on documented fields.
2. Backend must not remove or rename fields casually once frontend depends on them.
3. If temporary placeholder fields are returned, label them clearly in implementation notes or docs.
4. Routes, schemas, and tests should reflect the same contract.
5. When the contract changes, update both the backend schemas and the related frontend usage together.
