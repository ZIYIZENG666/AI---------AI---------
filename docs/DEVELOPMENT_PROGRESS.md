# Development Progress

## Purpose

This file is the current high-level phase tracker for backend and frontend work.

Detailed historical task logs belong in `docs/DEVELOPMENT_LOG.md`. This file
should stay focused on the active phase, phase status, current known limits, and
the latest Codex task record required by `AGENTS.md`.

## Current Active Phase

Phase 4 Lead Discovery backend first implementation with mock provider-backed
search is implemented in code, covered by focused backend tests, and locally
smoke-verified against PostgreSQL through the live API. The current active lane
is Frontend Phase 4 Lead Discovery planning from the verified backend task and
lead APIs before UI implementation.

- Backend Phase 2 = Product Card backend/API/data contract work. The Product
  Card backend contract is implemented.
- Frontend Phase 2 = Product Card UI implementation for the supported Product
  Card lifecycle is implemented.
- Backend Phase 3 = Campaign backend/API/data contract work. The minimum
  Campaign backend vertical slice is implemented.
- Frontend Phase 3 = Campaign frontend UI implementation for the supported
  Campaign lifecycle is implemented.
- Campaign Phase 3 final documentation contract uses only `draft`,
  `confirmed`, and `archived` Campaign statuses.
- Product Card confirmed-only validation and `product_card_snapshot` capture are
  required parts of the Campaign Phase 3 contract.
- Frontend Phase 3 and Backend Phase 3 use the same phase number and should be
  tracked together.
- Campaign frontend implementation depends on the backend contract, data model,
  business rules, validation rules, allowed status transitions,
  `docs/UI_REQUIREMENTS.md`, and Stitch Campaign design context.
- Human UI design is created manually in Stitch. Stitch is a visual and
  interaction reference, not a backend business logic source.
- Current verification priority for Product Card / Campaign is closed for local
  PostgreSQL live-backend browser smoke. The Phase 4 Lead Discovery contract is
  clarified, the first backend slice is implemented with `MockSearchProvider`,
  and local PostgreSQL migration / API smoke verification has passed for the
  new `task_runs` / `leads` tables and endpoints.

## Required Status Alignment

- Foundation stabilization: Completed.
- Phase 1B: Completed.
- Phase 1 Sources + Knowledge: Completed.
- Phase 2 Product Card backend contract: Completed.
- Frontend Foundation: Basic shell present; Product Card and Campaign workflow
  UI implemented.
- Frontend Phase 1: Planned / pending UI implementation.
- Frontend Phase 2 Product Card UI: Implemented for the supported Product Card
  lifecycle; PostgreSQL-backed browser smoke passed for create, edit, confirm,
  draft delete, and Campaign-linked 409 delete messaging.
- Phase 3 Campaign backend: Minimum backend vertical slice implemented.
- Phase 3 Campaign frontend: Implemented for the supported Campaign UI
  lifecycle.

## Unified Phase Tracking

| Phase number | Backend scope | Backend status | Frontend scope | Frontend status | Notes / current next step |
|---|---|---|---|---|---|
| Foundation stabilization | Project scaffold, environment-driven config, Alembic baseline, health checks, company router, and rule-doc stabilization. | Completed | React + TypeScript + Vite shell and dashboard foundation. | Basic shell present; business workflow UI pending. | Foundation is complete, but this is not a full MVP. |
| Phase 1B | Minimum text/URL source records plus deterministic knowledge draft and review behavior. | Completed | Feeds Frontend Phase 1 company/source/knowledge screens. | Planned. | UI must not imply uploaded documents, crawling, or OCR support. |
| Phase 1: Sources + Knowledge | Source persistence, knowledge drafts, knowledge review transitions, models, schemas, repositories, services, routes, migrations, and tests for the MVP text/URL slice. | Completed | Frontend Phase 1: Company / Source / Knowledge basic UI alignment. | Planned. | Frontend should follow the current text/URL backend contract only. |
| Phase 2: Product Card | Product Card backend contract for AI-generated and manual cards, draft/confirmed lifecycle, edit, confirm, delete, source type, company ownership, and tests. | Completed for backend contract. | Frontend Phase 2: Product Card UI. | Implemented for the supported Product Card UI lifecycle. | PostgreSQL-backed browser smoke passed for create, edit, confirm, draft delete, and Campaign-linked 409 Chinese UI messaging. |
| Phase 3: Campaign | Campaign model, migration, schemas, repository, service, routes, API contract, lifecycle, confirmed Product Card linkage, `product_card_snapshot`, duplicate-as-draft behavior, and tests. | Completed for the minimum backend vertical slice. | Frontend Phase 3: Campaign UI synchronized with Backend Phase 3 Campaign. | Implemented for the supported Campaign UI lifecycle. | Campaign frontend live-backend browser smoke passed against local PostgreSQL for direct route reachability, create draft, confirm, status filters, and Product Card linkage. |
| Phase 4: Lead Discovery | Provider-driven candidate lead discovery from confirmed Campaign criteria, using `task_runs`, `leads`, and `MockSearchProvider` first. | Implemented for the first mock-provider backend vertical slice; local PostgreSQL migration / API smoke passed for the verified endpoints. | Lead discovery task/result UI. | Planning from verified backend APIs; implementation pending. | Frontend Phase 4 should use only the verified task and lead APIs and must not imply validation, scoring, contacts, outreach, Gmail, real search, or real crawling. |
| Phase 5: Lead Validation + Intelligence | Lead normalization, duplicate handling, website availability checks, intelligence capture, evidence storage, and content sufficiency. | Planned / future. | Lead validation and lead intelligence UI states. | Planned / future. | Must not pretend validation or crawling has completed before implementation exists. |
| Phase 6: Lead Scoring | Evidence-based customer-fit scoring, recommendations, risk notes, uncertainty, and provider-mocked tests. | Planned / future. | Lead score, evidence, risk, and recommendation UI. | Planned / future. | AI recommendation remains separate from human review status. |
| Phase 7: Lead Review | User approval, rejection, and manual-review workflow. | Planned / future. | Lead review pages and decision controls. | Planned / future. | AI must not approve leads for the user. |
| Phase 8: Contacts | Contact records, contact type/status, manual LinkedIn reference storage, and selected valid email contact boundary. | Planned / future. | Contact selection and contact validation UI. | Planned / future. | Gmail Draft eligibility requires a selected valid email contact. |
| Phase 9: Outreach Draft + Gmail Draft | Outreach draft records, Gmail Draft provider boundary, duplicate prevention, and draft-only Gmail behavior. | Planned / future. | Outreach draft status and Gmail Draft review UI. | Planned / future. | Gmail behavior must remain draft-only and user-reviewed. |
| Phase 10: Frontend MVP Workflow | Backend phases 1-9 should provide the APIs that the frontend workflow consumes. | Planned / future integration. | End-to-end frontend workflow across company, source, knowledge, product, campaign, lead, contact, and outreach screens. | Planned / future. | Frontend must follow `docs/UI_REQUIREMENTS.md`, `docs/API_CONTRACT.md`, and required Stitch design context for user-designed workflow screens. |
| Phase 11: Background Jobs + Deployment | Background workers, task execution, deployment alignment, and real PostgreSQL migration smoke verification. | Planned / future. | Task progress, runtime health, and deployment-aware frontend states. | Planned / future. | Worker runtime is not implemented yet. |
| Phase 12: MVP Stabilization | Contract gaps, validation, error handling, test coverage, docs accuracy, and production-readiness checks. | Planned / future. | Frontend stabilization, smoke checks, and demo readiness. | Planned / future. | Real PostgreSQL schema validation remains an exit gate. |

## Frontend / Backend Phase Alignment

- Frontend phase numbering follows backend phase numbering where possible.
- Frontend Phase 3 corresponds to Backend Phase 3 Campaign.
- Frontend Phase 2 Product Card UI and Frontend Phase 3 Campaign UI are
  implemented and locally smoke-verified against the live backend; Frontend
  Phase 4 Lead Discovery UI planning has started from the smoke-verified
  backend task and lead APIs.
- A backend phase being completed does not automatically mean the matching
  frontend phase is implemented.
- At the start of each phase, backend work should define the API contract, data
  model, business rules, validation rules, and allowed status transitions.
- Frontend implementation must follow backend API contracts, data model,
  business rules, validation rules, and allowed status transitions. It must not
  invent unsupported backend behavior.
- The user manually creates UI designs in Stitch.
- Stitch is a design reference for layout, visual direction, and interaction
  intent. `AGENTS.md`, `docs/API_CONTRACT.md`, `docs/DATA_MODEL.md`, and
  `docs/UI_REQUIREMENTS.md` remain authoritative for project rules and behavior.
- Campaign and Product Card frontend implementation used the available Stitch
  design context as visual and interaction reference.
- Codex must not freely redesign UI unless explicitly requested.
- All user-facing frontend text must be Chinese.

## Current Known Limits

- Backend implementation is real through `company`, `sources`, `knowledge`,
  `products`, the minimum `campaigns` vertical slice, and the first
  mock-provider-backed Lead Discovery backend slice; most later modules remain
  placeholders.
- Campaign persistence and APIs are implemented for the Phase 3 minimum backend
  contract: `draft` / `confirmed` / `archived`, same-company confirmed Product
  Card validation, `product_card_snapshot`, archive, and duplicate-as-draft.
- Campaign default company list behavior now matches the current rule documents:
  default Campaign lists / `全部` include archived Campaigns alongside draft and
  confirmed Campaigns, while status-specific filters remain available.
- Product Card frontend UI is implemented for the finalized backend contract:
  list by company, status filter, manual create, AI generation trigger, edit,
  confirm draft, delete, detail dialog, and 409 delete messaging for confirmed
  cards used by Campaigns.
- Product Card browser verification against the live backend and PostgreSQL data
  passed for create, edit, confirm, and draft delete. Campaign-linked confirmed
  Product Card deletion protection returned backend HTTP 409 and the Product
  Card frontend displayed the Chinese blocking copy
  `已被获客任务使用，无法删除。` in the browser.
- Campaign frontend UI is implemented for the Phase 3 supported lifecycle:
  list/filter, create draft, edit draft, delete draft, confirm, duplicate
  confirmed Campaign as draft, archive confirmed Campaign, and read-only
  archived Campaign detail.
- Campaign frontend live-backend browser smoke passed against local PostgreSQL:
  `/campaigns` renders the Campaign workspace, a draft Campaign can be created
  from a confirmed Product Card, confirmation saves the linked Product Card
  state, and `全部` / `草稿` / `已确认` filters update rendered UI state.
- Source support is limited to text and URL records. Uploaded documents,
  document parsing, OCR, file storage, and crawling are not implemented.
- No real provider implementations exist yet for LLM, search, crawler, Gmail,
  storage, or task queue behavior.
- Phase 4 Lead Discovery first implementation uses `MockSearchProvider`,
  creates `task_runs`, stores candidate `leads`, records `search_query` and
  `provider_name`, blocks duplicate `pending` / `running` / `completed` tasks,
  allows retry after `failed` / `cancelled`, and keeps Campaign status unchanged.
- The Phase 4 create endpoint returns a `pending` task reference; until an RQ
  worker runtime exists, the service executes the mock provider immediately and
  clients should poll `GET /api/v1/tasks/{task_id}` for the terminal state.
- Phase 4 Lead Discovery remains contractually limited to mock search. It must
  not call a real search API, self-build full-web search, or perform real
  website crawling.
- No RQ worker runtime is implemented yet.
- The Phase 4 migration and API smoke were verified on 2026-07-13 against a
  disposable local PostgreSQL database on port `55432` and a live FastAPI
  backend on `127.0.0.1:8000`. This is local development proof, not staging or
  production proof.
- The migration chain was executed against a local Docker PostgreSQL test
  database on 2026-07-08. Broader deployment/staging PostgreSQL verification
  remains a future stabilization task.
- Frontend Phase 4 Lead Discovery planning has started from the verified
  backend APIs, but no Frontend Phase 4 UI has been implemented yet.
- Campaign-side Product Card same-company validation is implemented for
  Campaign creation and confirmation.
- Route-level Product Card get, patch, confirm, and delete company/workspace
  authorization remains planned hardening; repository/service company-scoped
  helpers exist but do not implement account or workspace authorization.

## Latest Codex Task Records

This section keeps compact records for the latest Codex tasks. Detailed task
history should be moved to `docs/DEVELOPMENT_LOG.md`.

### 2026-07-13 - Phase 4 PostgreSQL Smoke And Frontend Planning Start

Completed: Ran local PostgreSQL migration / API smoke verification for the
Phase 4 Lead Discovery endpoints, then started Frontend Phase 4 planning from
the verified backend APIs.

What changed:

- Verified the full Alembic chain through
  `20260712_0006_create_lead_discovery.py` against a disposable local
  PostgreSQL database.
- Verified the `task_runs` and `leads` tables and key Phase 4 constraint names
  in PostgreSQL.
- Started a live FastAPI backend against the smoke database and verified:
  - `/health`
  - `/health/db`
  - `POST /api/v1/campaigns/{campaign_id}/lead-discovery`
  - `GET /api/v1/tasks/{task_id}`
  - `GET /api/v1/campaigns/{campaign_id}/lead-discovery/tasks`
  - `GET /api/v1/campaigns/{campaign_id}/leads`
- Confirmed draft Campaign rejection, confirmed Campaign task creation,
  pending create response, completed mock-provider task status, three saved
  candidate leads, duplicate task blocking, and Campaign status separation.
- Updated frontend planning and UI requirements so Frontend Phase 4 is planned
  from the verified task/lead APIs only.

Files modified:

- `docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `docs/UI_REQUIREMENTS.md`
- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification commands:

- `docker run --name ai-b2b-sales-phase4-smoke-postgres --rm -e POSTGRES_DB=ai_b2b_sales_phase4_smoke -e POSTGRES_USER=phase4_smoke -e POSTGRES_PASSWORD=phase4_smoke_password -p 55432:5432 -d postgres:16-alpine`
- `.venv\Scripts\python.exe -m alembic upgrade head`
- `.venv\Scripts\python.exe -m alembic upgrade head`
- PostgreSQL schema inspection for `task_runs`, `leads`, and key constraints.
- `.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000`
- Live HTTP smoke script against the verified Phase 4 endpoints.

Test status:

- No automated tests were added or updated in this task.
- Local PostgreSQL migration smoke passed.
- Live FastAPI API smoke passed against local PostgreSQL.

Known limitations:

- The existing Docker Compose `postgres` volume was not used because it was
  initialized with credentials that did not match `.env.example`; the smoke used
  a separate disposable PostgreSQL container to avoid mutating existing data.
- This is local development proof only, not staging or production proof.
- The first implementation still executes `MockSearchProvider` synchronously
  because no RQ worker runtime exists yet.
- Frontend Phase 4 planning has started, but no Frontend Phase 4 UI was
  implemented.
- Lead Validation, website intelligence, scoring, review, contacts, outreach,
  Gmail Draft, real search APIs, and real crawling remain future phases.

Commit / push status:

- Not committed.
- Not pushed to GitHub.

Next recommended step:

- Provide or authorize the required Lead Discovery UI design context, then
  implement Frontend Phase 4 using only the verified task/lead APIs and
  Chinese user-facing text.

### 2026-07-12 - Backend Phase 4 Lead Discovery First Implementation

Completed: Implemented the first backend Lead Discovery vertical slice using
`MockSearchProvider`.

What changed:

- Added real `task_runs` and `leads` ORM models, repositories, schemas, service
  logic, HTTP routes, and Alembic migration for Phase 4.
- Added `MockSearchProvider` behind the existing Search Provider abstraction;
  no real search API, crawler, website parsing, scoring, contacts, outreach, or
  Gmail behavior was introduced.
- Implemented `POST /api/v1/campaigns/{campaign_id}/lead-discovery`,
  `GET /api/v1/campaigns/{campaign_id}/lead-discovery/tasks`,
  `GET /api/v1/campaigns/{campaign_id}/leads`, and
  `GET /api/v1/tasks/{task_id}`.
- Enforced confirmed-Campaign-only start, archived/draft rejection, duplicate
  blocking for `pending` / `running` / `completed` task runs, retry after
  `failed` / `cancelled`, zero-result completion, provider failure recording,
  Campaign-status separation, and per-Campaign normalized website de-duplication.
- Stored generated `search_query` and `provider_name` on both task/lead
  traceability surfaces where appropriate.
- Added focused backend tests for the Phase 4 contract and updated current docs
  to reflect the implemented first slice and remaining PostgreSQL smoke gap.

Files modified:

- `backend/app/main.py`
- `backend/app/models.py`
- `backend/app/providers/search_provider.py`
- `backend/app/modules/tasks/models.py`
- `backend/app/modules/tasks/repository.py`
- `backend/app/modules/tasks/schemas.py`
- `backend/app/modules/tasks/service.py`
- `backend/app/modules/tasks/routes.py`
- `backend/app/modules/discovery/models.py`
- `backend/app/modules/discovery/repository.py`
- `backend/app/modules/discovery/schemas.py`
- `backend/app/modules/discovery/service.py`
- `backend/app/modules/discovery/routes.py`
- `backend/alembic/versions/20260712_0006_create_lead_discovery.py`
- `backend/tests/test_lead_discovery.py`
- `docs/API_CONTRACT.md`
- `docs/DATA_MODEL.md`
- `docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification commands:

- `.venv\Scripts\python.exe -m pytest tests\test_lead_discovery.py -q`
- `.venv\Scripts\python.exe -m pytest -q`

Test status:

- Phase 4 focused backend tests passed: 8 passed, 1 warning.
- Full backend test suite passed: 65 passed, 1 warning.

Known limitations:

- The new Alembic migration has not yet been run against local PostgreSQL in
  this task.
- The first implementation executes the mock provider synchronously after
  creating a pending task reference because no RQ worker runtime exists yet.
- Lead Validation, website intelligence, scoring, review, contacts, outreach,
  Gmail Draft, real search APIs, and real crawling remain future phases.
- No Frontend Phase 4 Lead Discovery UI was implemented.

Commit / push status:

- Not committed.
- Not pushed to GitHub.

Next recommended step:

- Run local PostgreSQL Alembic migration and API smoke verification for
  `POST /api/v1/campaigns/{campaign_id}/lead-discovery`,
  `GET /api/v1/tasks/{task_id}`, and
  `GET /api/v1/campaigns/{campaign_id}/leads`; after that, plan Frontend Phase
  4 UI from the verified backend APIs and required design context.

### 2026-07-12 - Phase 4 Lead Discovery Contract Documentation Pass

Completed: Clarified the Phase 4 Lead Discovery contract before backend
implementation.

What changed:

- Updated the Phase 4 scope so the first implementation is confirmed Campaign
  -> Lead Discovery task -> mock search results -> saved candidate leads.
- Documented that Phase 4 first implementation uses `MockSearchProvider`, does
  not call real search APIs, does not self-build full-web search, and does not
  perform real website crawling.
- Clarified that real website crawling, website parsing, content sufficiency,
  and evidence extraction belong to later Lead Validation / Intelligence work.
- Added Lead Discovery API contract details for task creation, task listing,
  lead listing, task lookup, error handling, duplicate-start blocking, retry
  behavior, and zero-result completion.
- Added data model guidance for `task_runs`, saved lead traceability fields,
  required `website` / `source_url`, `search_query`, and per-Campaign normalized
  website de-duplication.
- Added Lead Discovery contract tests and updated frontend planning so Lead
  Discovery UI waits for backend task and lead APIs.
- Updated AI rules so mock provider results are treated as development/test data
  and not real external customer evidence.
- Updated the detailed development log and this progress tracker.
- Kept the task documentation-only; no backend code, frontend UI, database
  migration, provider implementation, or runtime behavior changed.

Files modified:

- `docs/API_CONTRACT.md`
- `docs/DATA_MODEL.md`
- `docs/MODULE_BOUNDARIES.md`
- `docs/MVP_SCOPE.md`
- `docs/WORKFLOW.md`
- `docs/TESTING_STRATEGY.md`
- `docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `docs/AI_RULES.md`
- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification commands:

- `rg -n "MockSearchProvider|lead_discovery|search_query|zero leads|full-web|real search API|website crawling" docs`
- `rg -n "^### 2026" docs\DEVELOPMENT_PROGRESS.md`
- `rg -n "^## [0-9]+\." docs\TESTING_STRATEGY.md`
- `git diff --check`
- `git diff --name-only`
- `git status --short --branch`

Test status:

- No automated tests were run because this was a documentation-only contract
  alignment task with no application code changes.

Known limitations at the time of that documentation-only task:

- Phase 4 backend implementation was still pending then; this has been
  superseded by the later Backend Phase 4 implementation record above.
- No database migration or model change was made yet.
- No real search API, real crawler, task queue runtime, or frontend Lead
  Discovery UI exists yet.

Commit / push status:

- Not committed.
- Not pushed to GitHub.

Next recommended step at the time:

- Implement Backend Phase 4 Lead Discovery using `task_runs`, `leads`,
  `MockSearchProvider`, the documented duplicate-start rules, and focused tests.
  This recommendation has been completed by the later implementation record
  above.
