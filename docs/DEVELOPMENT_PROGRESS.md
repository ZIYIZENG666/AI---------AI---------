# Development Progress

## Purpose

This file is the current high-level phase tracker for backend and frontend work.

Detailed historical task logs belong in `docs/DEVELOPMENT_LOG.md`. This file
should stay focused on the active phase, phase status, current known limits, and
the latest Codex task record required by `AGENTS.md`.

## Current Active Phase

Phase 4 Lead Discovery backend first implementation with mock provider-backed
search is implemented in code, covered by focused backend tests, and locally
smoke-verified against PostgreSQL through the live API. Frontend Phase 4 Lead
Discovery UI is implemented from the verified backend task and lead APIs plus
the available Stitch design context, and local PostgreSQL live-backend browser
smoke verification has passed for the confirmed Campaign discovery workflow.
The current active lane can move to Phase 5 contract planning, or to any
targeted Phase 4 hardening found during review.

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
- Frontend Phase 4 Lead Discovery UI: Implemented for the supported confirmed
  Campaign task/result workflow; build verification and local PostgreSQL
  live-backend browser smoke passed.

## Unified Phase Tracking

| Phase number | Backend scope | Backend status | Frontend scope | Frontend status | Notes / current next step |
|---|---|---|---|---|---|
| Foundation stabilization | Project scaffold, environment-driven config, Alembic baseline, health checks, company router, and rule-doc stabilization. | Completed | React + TypeScript + Vite shell and dashboard foundation. | Basic shell present; business workflow UI pending. | Foundation is complete, but this is not a full MVP. |
| Phase 1B | Minimum text/URL source records plus deterministic knowledge draft and review behavior. | Completed | Feeds Frontend Phase 1 company/source/knowledge screens. | Planned. | UI must not imply uploaded documents, crawling, or OCR support. |
| Phase 1: Sources + Knowledge | Source persistence, knowledge drafts, knowledge review transitions, models, schemas, repositories, services, routes, migrations, and tests for the MVP text/URL slice. | Completed | Frontend Phase 1: Company / Source / Knowledge basic UI alignment. | Planned. | Frontend should follow the current text/URL backend contract only. |
| Phase 2: Product Card | Product Card backend contract for AI-generated and manual cards, draft/confirmed lifecycle, edit, confirm, delete, source type, company ownership, and tests. | Completed for backend contract. | Frontend Phase 2: Product Card UI. | Implemented for the supported Product Card UI lifecycle. | PostgreSQL-backed browser smoke passed for create, edit, confirm, draft delete, and Campaign-linked 409 Chinese UI messaging. |
| Phase 3: Campaign | Campaign model, migration, schemas, repository, service, routes, API contract, lifecycle, confirmed Product Card linkage, `product_card_snapshot`, duplicate-as-draft behavior, and tests. | Completed for the minimum backend vertical slice. | Frontend Phase 3: Campaign UI synchronized with Backend Phase 3 Campaign. | Implemented for the supported Campaign UI lifecycle. | Campaign frontend live-backend browser smoke passed against local PostgreSQL for direct route reachability, create draft, confirm, status filters, and Product Card linkage. |
| Phase 4: Lead Discovery | Provider-driven candidate lead discovery from confirmed Campaign criteria, using `task_runs`, `leads`, and `MockSearchProvider` first. | Implemented for the first mock-provider backend vertical slice; local PostgreSQL migration / API smoke passed for the verified endpoints. | Lead discovery task/result UI. | Implemented and local PostgreSQL live-backend browser smoke passed for confirmed Campaign start, task status/history, candidate leads, duplicate conflict, and draft/archived action hiding. | Phase 4 remains limited to mock search candidate discovery. The UI must not imply validation, scoring, contacts, outreach, Gmail, real search, or real crawling. |
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
- Frontend Phase 2 Product Card UI, Frontend Phase 3 Campaign UI, and Frontend
  Phase 4 Lead Discovery UI are implemented and locally smoke-verified against
  the live backend.
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
- Frontend Phase 4 Lead Discovery UI is implemented inside confirmed Campaign
  detail using the verified task and lead APIs, with Chinese user-facing text,
  Stitch-aligned layout, task status/history, candidate lead list, zero-result
  state, duplicate/conflict handling, and provider-failure display. Local
  PostgreSQL live-backend browser smoke passed on 2026-07-14: a confirmed
  Campaign started discovery, showed one completed task, displayed three mock
  candidate leads, prevented duplicate discovery through UI state, returned
  backend HTTP `409` with `lead_discovery_already_exists`, and draft/archived
  Campaign detail views did not expose a start action.
- Campaign-side Product Card same-company validation is implemented for
  Campaign creation and confirmation.
- Route-level Product Card get, patch, confirm, and delete company/workspace
  authorization remains planned hardening; repository/service company-scoped
  helpers exist but do not implement account or workspace authorization.

## Latest Codex Task Records

This section keeps compact records for the latest Codex tasks. Detailed task
history should be moved to `docs/DEVELOPMENT_LOG.md`.

### 2026-07-14 - Frontend Phase 4 Live-Backend Browser Smoke

Completed: Ran local PostgreSQL live-backend browser smoke for the implemented
Frontend Phase 4 Lead Discovery UI.

What changed:

- Started an isolated disposable PostgreSQL database for the smoke run.
- Ran the Alembic migration chain to head against the smoke database.
- Started a live FastAPI backend on `127.0.0.1:8000`.
- Started the Vite frontend; port `5173` was unavailable, so Vite served the
  app on `127.0.0.1:5174`.
- Seeded a company, confirmed Product Card, draft Campaign, confirmed
  Campaign, and archived Campaign through live HTTP APIs.
- Opened the Campaign workspace in the in-app browser and verified the
  confirmed Campaign Lead Discovery workflow.
- Started Lead Discovery from the confirmed Campaign detail view.
- Verified the UI showed one completed task, task history, and three mock
  candidate leads with discovered / pending validation / unreviewed statuses.
- Verified the UI changed the start action to disabled `已有发现任务`.
- Verified duplicate start against the live backend returned HTTP `409` with
  `lead_discovery_already_exists`.
- Verified draft and archived Campaign detail views did not expose the Lead
  Discovery panel or `开始发现线索` action.
- Updated current progress/planning docs to mark Frontend Phase 4 live-backend
  browser smoke as passed.

Files modified:

- `docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification commands:

- `docker run --name ai-b2b-sales-phase4-browser-smoke-postgres --rm -e POSTGRES_DB=ai_b2b_sales_phase4_browser_smoke -e POSTGRES_USER=phase4_browser_smoke -e POSTGRES_PASSWORD=phase4_browser_smoke_password -p 55433:5432 -d postgres:16-alpine`
- `.venv\Scripts\python.exe -m alembic upgrade head`
- `.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000`
- `npm.cmd --prefix frontend run dev -- --host 127.0.0.1`
- Browser smoke at `http://127.0.0.1:5174/campaigns`
- `curl.exe -s -i -X POST http://127.0.0.1:8000/api/v1/campaigns/8d02da83-d011-4779-aff3-710e7e6c0f9c/lead-discovery -H "Content-Type: application/json" -d "{\"provider\":\"mock_search\"}"`
- `curl.exe -s http://127.0.0.1:8000/api/v1/campaigns/8d02da83-d011-4779-aff3-710e7e6c0f9c/lead-discovery/tasks`
- `curl.exe -s http://127.0.0.1:8000/api/v1/campaigns/8d02da83-d011-4779-aff3-710e7e6c0f9c/leads`

Test status:

- Local PostgreSQL migration smoke passed.
- Live FastAPI health and database health checks passed.
- Live browser smoke passed for the confirmed Campaign Lead Discovery happy
  path and state-based action visibility.
- Duplicate start returned backend HTTP `409` with
  `lead_discovery_already_exists`.
- No automated tests were added or updated because this task was runtime smoke
  verification and documentation update only.

Known limitations:

- This is local development proof only, not staging or production proof.
- The smoke uses `MockSearchProvider`; no real search API, crawler, validation,
  scoring, review, contacts, outreach, or Gmail Draft behavior was verified or
  implemented.
- The first backend implementation still executes the mock provider
  synchronously because no RQ worker runtime exists yet.
- The disposable PostgreSQL container used a separate database and did not
  mutate existing local development data.

Commit / push status:

- Not committed.
- Not pushed to GitHub.

Next recommended step:

- Move to Phase 5 Lead Validation + Intelligence contract planning, or do a
  targeted Phase 4 frontend/backend hardening pass if review finds specific
  UI or error-state polish items.

### 2026-07-14 - Frontend Phase 4 Lead Discovery UI Implementation

Completed: Implemented the Frontend Phase 4 Lead Discovery UI from the verified
backend APIs and available Stitch design context.

What changed:

- Read the relevant Stitch Phase 4 screens for Lead Discovery start, task
  status/history, candidate results, empty states, and conflict/error feedback.
- Added a frontend Lead Discovery API client for:
  - `POST /api/v1/campaigns/{campaign_id}/lead-discovery`
  - `GET /api/v1/tasks/{task_id}`
  - `GET /api/v1/campaigns/{campaign_id}/lead-discovery/tasks`
  - `GET /api/v1/campaigns/{campaign_id}/leads`
- Added a confirmed-Campaign-only Lead Discovery panel inside Campaign detail.
- Implemented start, refresh, task polling, task status/progress, task history,
  candidate lead list, search filtering, zero-result state, duplicate/conflict
  handling, provider-failure display, and source URL opening.
- Kept Phase 4 UI bounded to discovered candidate leads with pending validation
  and unreviewed human status; the UI does not add validation, scoring, review,
  contacts, outreach, Gmail Draft, real search, or real crawling behavior.
- Added Stitch-aligned layout and responsive styles using the existing
  Campaign/Product Card workbench visual language.

Files modified:

- `frontend/src/api/leadDiscovery.ts`
- `frontend/src/pages/campaigns/LeadDiscoveryPanel.tsx`
- `frontend/src/pages/campaigns/CampaignWorkspace.tsx`
- `frontend/src/styles/global.css`
- `docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification commands:

- `npm.cmd --prefix frontend run build`
- `rg -n "Frontend Phase|Gmail|Outreach|score|评分|审批|批准|拒绝|发送|真实搜索|爬虫|CRM|LinkedIn|Google Sheets|邮箱|email" frontend\src\pages\campaigns\LeadDiscoveryPanel.tsx frontend\src\api\leadDiscovery.ts`
- `git diff --check`

Test status:

- Frontend build passed.
- No automated tests were added because this task changed frontend integration
  UI only and the project currently has no frontend test harness.
- Backend tests were not rerun because no backend logic changed.

Known limitations:

- Live-backend browser smoke for the new Frontend Phase 4 UI was not run in
  this task.
- The UI depends on existing confirmed Campaign data and the already verified
  local backend APIs.
- The first backend implementation still executes `MockSearchProvider`
  synchronously because no RQ worker runtime exists yet.
- Lead Validation, website intelligence, scoring, review, contacts, outreach,
  Gmail Draft, real search APIs, and real crawling remain future phases.

Commit / push status:

- Not committed.
- Not pushed to GitHub.

Next recommended step:

- Run live-backend browser smoke against local PostgreSQL for the new Frontend
  Phase 4 UI: open a confirmed Campaign, start Lead Discovery, verify task
  status/history, verify candidate leads, verify duplicate-task conflict
  handling, and confirm draft/archived Campaigns do not expose a start action.

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
