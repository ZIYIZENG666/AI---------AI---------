# API Contract

## Purpose

This document defines the API contract between frontend and backend.

It focuses on response shape, error shape, pagination, task responses, naming,
versioning, and contract stability.

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
3. Knowledge draft creation is synchronous and deterministic in this phase. It
   must not imply that a crawler or LLM processed a URL.
4. `GET /api/v1/companies/{company_id}/knowledge` accepts optional `status`, `limit`, and `offset` query parameters.
5. The `status` filter accepts `draft`, `confirmed`, or `rejected`, allowing confirmed knowledge to be retrieved separately.
6. Confirm and reject endpoints accept only knowledge items currently in `draft`;
   invalid transitions return HTTP `409` with `knowledge_not_draft`.
7. Missing company, source, or knowledge IDs return HTTP `404` with stable
   resource-specific error codes.
8. No current source endpoint accepts uploaded documents, PDF files, Word files,
   image OCR input, file storage payloads, document parsing jobs, or crawler
   processing requests.

## Phase 2 Product Card Endpoints

The current Product Card contract exposes:

- `POST /api/v1/companies/{company_id}/product-cards` for generation from confirmed company knowledge
- `POST /api/v1/product-cards` for user-created Product Cards
- `GET /api/v1/product-cards`
- `GET /api/v1/companies/{company_id}/product-cards`
- `GET /api/v1/product-cards/{product_card_id}`
- `PATCH /api/v1/product-cards/{product_card_id}`
- `POST /api/v1/product-cards/{product_card_id}/confirm`
- `DELETE /api/v1/product-cards/{product_card_id}`

Rules:

1. Product Cards have only `draft` and `confirmed` business statuses.
   `rejected` is not valid, and there is no Product Card reject endpoint.
2. Generation uses confirmed knowledge only, sets
   `source_type = ai_generated` and `status = draft`, and persists the exact
   confirmed knowledge IDs in `source_knowledge_item_ids`.
3. User-created Product Cards use `POST /api/v1/product-cards`, set
   `source_type = manual` and `status = draft`, and must belong to a company.
   The request body must include `company_id`, and the backend must verify that
   the company exists. Future company/workspace scope hardening may move manual
   creation into a company-scoped endpoint, but a Product Card must never exist
   without a company.
4. The manual Product Card creation path must remain available even when AI generation is available.
5. Product Card list has two read entry points:
   - `GET /api/v1/product-cards`: single-user MVP provisional global list
     across Product Cards. It returns both `draft` and `confirmed` records by
     default. This must not be treated as the long-term multi-company or
     multi-workspace ownership model.
   - `GET /api/v1/companies/{company_id}/product-cards`: company-scoped list for
     Product Cards belonging to the specified company. It returns both `draft`
     and `confirmed` records by default. Future frontend work should prefer
     this company-scoped list when a company context is available.
6. Both Product Card list endpoints support only `status=draft` or
   `status=confirmed`, and use the standard `limit` and `offset` pagination
   contract. `status=rejected` is invalid.
7. `PATCH /api/v1/product-cards/{product_card_id}` is allowed for both statuses,
   saves editable fields only, and must not change `status`, `source_type`,
   `source_knowledge_item_ids`, `company_id`, or company ownership.
8. `POST /api/v1/product-cards/{product_card_id}/confirm` changes `draft` to
   `confirmed`. Repeating it for an already confirmed Product Card returns HTTP
   `200` with the current record and leaves the status unchanged.
9. `DELETE /api/v1/product-cards/{product_card_id}` deletes a draft directly. It
   may delete a confirmed Product Card only when no Campaign has ever referenced
   it; otherwise it returns HTTP `409`.
10. Only confirmed Product Cards may be selected by a Campaign.
11. Missing Product Card IDs return HTTP `404` with `product_card_not_found` for get, patch, confirm, and delete operations.
12. AI-backed generation may replace the current deterministic generator later,
    but it must preserve the same source, status, evidence, and
    human-confirmation rules.

### Product Card Scope Hardening (Planned)

The current MVP remains a single-user prototype. ID-only get, patch, confirm,
and delete operations must not be treated as the final authorization model.

Implemented boundary:

- Campaign creation and confirmation already validate Product Card consumption
  with `product_card_id + company_id` semantics. A Campaign may use only a
  confirmed Product Card from the same company.
- Product Card deletion already checks whether a Campaign has referenced the
  Product Card before physical deletion.

Still planned hardening:

- Product Card route-level get, patch, confirm, and delete endpoints still use
  ID-only paths in the current single-user MVP contract.
- These Product Card route-level operations must not be described as having
  company/workspace authorization until company-scoped route semantics,
  service checks, and tests are implemented.

Target repository/service query semantics:

- get by `product_card_id + company_id`
- patch by `product_card_id + company_id`
- confirm by `product_card_id + company_id`
- delete by `product_card_id + company_id`
- later extend each lookup with `workspace_id`

Rules:

1. Product Cards must remain associated with their owning company.
2. Campaign-side same-company Product Card validation is implemented for the
   Phase 3 Campaign backend slice.
3. Product Card route-level company-scoped lookup hardening remains planned work
   for get, patch, confirm, and delete operations.
4. Workspace-scoped lookup is a future multi-tenant constraint and is not implemented yet.
5. Account or workspace authorization must not be claimed until the corresponding implementation and tests exist.
6. Product Card deletion must check Campaign references before physical deletion and return HTTP `409` when the card is in use.

## Phase 3 Campaign Endpoints

The current Campaign backend contract exposes the minimum Phase 3 vertical
slice with models, schemas, repository logic, service logic, routes, migration,
and focused tests.

Current endpoints:

- `POST /api/v1/companies/{company_id}/campaigns`
- `GET /api/v1/companies/{company_id}/campaigns`
- `GET /api/v1/campaigns/{campaign_id}`
- `PATCH /api/v1/campaigns/{campaign_id}`
- `DELETE /api/v1/campaigns/{campaign_id}`
- `POST /api/v1/campaigns/{campaign_id}/confirm`
- `POST /api/v1/campaigns/{campaign_id}/archive`
- `POST /api/v1/campaigns/{campaign_id}/duplicate`

Request fields for create:

- `product_card_id`
- `name`
- `target_country`
- `target_region`
- `target_industry`
- `target_company_type`
- `target_role`
- `search_keywords`
- `qualification_criteria`
- `outreach_angle`
- `lead_limit`

Editable request fields for patch:

- `name`
- `target_country`
- `target_region`
- `target_industry`
- `target_company_type`
- `target_role`
- `search_keywords`
- `qualification_criteria`
- `outreach_angle`
- `lead_limit`

Response-only or system-managed fields:

- `id`
- `company_id`
- `product_card_snapshot`
- `status`
- `created_at`
- `updated_at`

Rules:

1. A Campaign must belong to a company and must keep `product_card_id`.
2. A Campaign may be created from an AI suggestion or from user-entered fields,
   but it starts as `draft`.
3. AI suggestion fields such as `campaign_goal`,
   `target_customer_profile`, `exclusion_rules`, and `scoring_focus` are AI
   output fields until explicitly added to the data model. Services must map
   them into the Campaign draft fields above instead of treating them as
   database columns.
4. Campaign creation must verify that the referenced Product Card exists,
   belongs to the same company, and has `status = confirmed`.
5. A Campaign must not be created from a draft, deleted, or rejected Product
   Card. Product Cards do not have a current `rejected` status or reject
   endpoint.
6. Campaign status values are limited to `draft`, `confirmed`, and `archived`.
   `running`, `paused`, `completed`, `failed`, and `cancelled` are job or task
   execution states for future Lead Discovery / Campaign Job models, not
   Campaign status values.
7. `GET /api/v1/companies/{company_id}/campaigns` returns non-archived
   Campaigns by default. It may accept `status=draft`, `status=confirmed`, or
   `status=archived`; archived Campaigns are returned only when explicitly
   requested with `status=archived`.
8. `PATCH /api/v1/campaigns/{campaign_id}` may edit only `draft` Campaign
   fields. It must reject edits to `confirmed` or `archived` Campaigns and must
   not change `company_id`, `product_card_id`, `product_card_snapshot`, or
   status unless a later contract explicitly allows it.
9. `POST /api/v1/campaigns/{campaign_id}/confirm` changes `draft` to
   `confirmed` only after revalidating the current Product Card. The backend
   must verify that the Campaign exists, belongs to the current company /
   workspace scope, references an existing Product Card in the same company,
   and that the Product Card has `status = confirmed`.
10. Confirming a `draft` Campaign saves `product_card_snapshot`, a historical
    copy of Product Card business fields used by matching and outreach. The
    snapshot is not a foreign key and should include only core fields such as
    product name, description, target customer / ICP, value proposition, pain
    points, use cases, differentiators, industry / category, and any confirmed
    Product Card fields that directly affect lead matching or outreach
    generation.
11. Repeating confirm for an already `confirmed` Campaign is idempotent: return
    HTTP `200 OK` with the current Campaign and keep status `confirmed`.
12. Confirming an `archived` Campaign is invalid and should return HTTP `409`.
13. Only a `confirmed` Campaign may enter Lead Discovery. Lead Discovery must
    use the confirmed Campaign's `product_card_snapshot`, not a live reread of a
    later edited Product Card.
14. `POST /api/v1/campaigns/{campaign_id}/archive` changes `confirmed` to
    `archived`. Archived Campaigns are read-only history records; they cannot be
    edited, deleted, restored to `draft`, restored to `confirmed`, or used for
    new Lead Discovery.
15. `DELETE /api/v1/campaigns/{campaign_id}` is allowed only for `draft`
    Campaigns. Deleting `confirmed` or `archived` Campaigns is invalid and
    should return HTTP `409`.
16. `POST /api/v1/campaigns/{campaign_id}/duplicate` creates a new `draft`
    Campaign with a new `id` from a source Campaign. The new draft can be
    edited, and its later confirm must revalidate that the current Product Card
    is still usable. Duplicate / copy as draft must not modify the source
    Campaign and must not be treated as archived restore.
17. Campaign does not send email, does not create Gmail Drafts directly, and
    does not approve leads on behalf of the user.
18. Campaign is not a CRM sequence. It must not implement automatic follow-up,
    bulk sending, reply tracking, or any auto-send behavior.

Campaign error handling:

- Missing Campaign: HTTP `404` with `campaign_not_found`.
- Missing Product Card: HTTP `404` with `product_card_not_found`.
- Product Card from another company or workspace scope: HTTP `404` or `403`
  according to the future authorization model, but never allow confirmation.
- Product Card not confirmed: HTTP `409` with `product_card_not_confirmed`.
- Invalid status transition: HTTP `409` with `invalid_campaign_status_transition`.
- Unsupported status filter: HTTP `422` with validation details.

## Lead Recommendation and Review Status Contract

AI recommendation and human review status are separate concepts.

AI scoring writes `lead_scores.recommendation` with these values:

- `recommended`
- `maybe`
- `not_recommended`
- `needs_manual_review`

Human review writes `leads.review_status` with these values:

- `unreviewed`
- `approved`
- `rejected`
- `needs_manual_review`

Rules:

1. AI may produce only a recommendation. It must not approve or reject a lead.
2. User review produces `review_status`.
3. `needs_manual_review` may appear in both fields, but the meanings differ:
   in `lead_scores.recommendation` it is an AI uncertainty signal; in
   `leads.review_status` it is a human workflow state.
4. Only `review_status = approved` can proceed to Outreach Draft or Gmail Draft
   creation.

## Contact Selection and Gmail Draft Eligibility Contract

Gmail Draft eligibility must be based on a contact selected at draft creation
time. Do not add `contacts.selected` or any selected boolean to the contacts
table.

Rules:

1. When the user chooses a contact for Outreach Draft or Gmail Draft creation,
   the frontend passes `contact_id`.
2. The backend must verify:
   - `contact_id` exists.
   - The contact belongs to the current approved lead.
   - `contact.contact_type = email`.
   - `contact.status = valid`.
   - The contact is not `blocked`, `invalid`, or `unverified`.
   - The contact is not LinkedIn, phone, contact form, or manual-review-only.
3. After validation, `outreach_drafts.contact_id` stores the chosen contact for
   that draft.
4. "Selected valid email contact" means the valid email contact passed and
   verified for this Outreach Draft or Gmail Draft action. It does not mean
   `contacts.selected = true`.
5. A Gmail Draft can be created only when:
   - the lead `review_status` is `approved`;
   - the selected contact belongs to that lead;
   - the selected contact has `contact_type = email`;
   - the selected contact has `status = valid`;
   - an outreach draft exists or can be generated for that selected contact;
   - the same lead/contact/outreach draft has not already created a Gmail Draft.
6. Rejected, unreviewed, or needs-manual-review leads are not eligible for Gmail
   Draft creation.
7. Invalid, unverified, blocked, LinkedIn, phone, contact form, manual-only
   contacts, lead-level public-email fallback fields, and auto-sending email are
   forbidden for Gmail Draft eligibility.

## Gmail Draft Only Scope Contract

Gmail Draft creation is not email automation and not complete Gmail integration.

Rules:

1. The backend may only create Gmail drafts for eligible approved leads.
2. OAuth scope must be limited to the minimum draft-creation permission, such as
   `gmail.compose`.
3. The system must not request or use `gmail.send`, `gmail.modify`, mailbox
   read, inbox sync, move, delete, label, reply tracking, reply monitoring, or
   full Gmail access permissions.
4. The system must not read, sync, move, delete, label, or modify existing Gmail
   messages.
5. The user must review the draft in Gmail and manually send it.

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
2. Do not expose endpoints for LinkedIn scraping, LinkedIn crawler behavior,
   LinkedIn bot behavior, LinkedIn browser automation, LinkedIn browser
   extension automation, automated LinkedIn login, automated LinkedIn search,
   automated LinkedIn profile extraction, automated LinkedIn contact
   downloading, automated LinkedIn messaging, automated LinkedIn connection
   requests, or automatic lead enrichment from LinkedIn.
3. Allowed endpoints may store a user-provided LinkedIn URL as a manual contact
   reference, return that LinkedIn URL for frontend human review, and mark
   `contact_type = linkedin`.
4. LinkedIn references must not be used as Gmail Draft recipients or as Gmail
   Draft eligibility.
5. Gmail Draft eligibility must be based on a selected contact with
   `contacts.contact_type = email` and `contacts.status = valid`.

## Frontend / Backend Contract Rule

Rules:

1. Frontend must rely only on documented fields.
2. Backend must not remove or rename fields casually once frontend depends on them.
3. If temporary placeholder fields are returned, label them clearly in implementation notes or docs.
4. Routes, schemas, and tests should reflect the same contract.
5. When the contract changes, update both the backend schemas and the related frontend usage together.
