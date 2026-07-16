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
Backend Phase 5 Lead Validation + Intelligence first slice is implemented with
`MockCrawlerProvider`, `lead_validation` task runs, `input_url`,
`lead_intelligence`, service/repository/routes, migration, and focused tests.
It remains mock-crawler-only; independent local PostgreSQL migration/API smoke
verification has passed.
Frontend Phase 5 Lead Validation + Intelligence UI is implemented inside the
confirmed Campaign Lead Discovery workspace using the available Stitch Phase 5
corrected design screens and the verified backend Phase 5 APIs. Frontend build
verification and local PostgreSQL live-backend browser smoke have passed.

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
- Phase 5 first slice covers Lead Validation + Intelligence only. It does not
  include AI scoring, human review, contact discovery, Outreach Draft, Gmail
  Draft, auto-send, CRM behavior, LinkedIn crawling, or real crawler provider
  integration.

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
- Backend Phase 5 Lead Validation + Intelligence: First mock-crawler backend
  slice implemented; independent PostgreSQL migration/API smoke passed.
- Frontend Phase 5 Lead Validation + Intelligence: Implemented from Stitch
  corrected design context and backend Phase 5 APIs; build verification and
  local PostgreSQL live-backend browser smoke passed.

## Unified Phase Tracking

| Phase number | Backend scope | Backend status | Frontend scope | Frontend status | Notes / current next step |
|---|---|---|---|---|---|
| Foundation stabilization | Project scaffold, environment-driven config, Alembic baseline, health checks, company router, and rule-doc stabilization. | Completed | React + TypeScript + Vite shell and dashboard foundation. | Basic shell present; business workflow UI pending. | Foundation is complete, but this is not a full MVP. |
| Phase 1B | Minimum text/URL source records plus deterministic knowledge draft and review behavior. | Completed | Feeds Frontend Phase 1 company/source/knowledge screens. | Planned. | UI must not imply uploaded documents, crawling, or OCR support. |
| Phase 1: Sources + Knowledge | Source persistence, knowledge drafts, knowledge review transitions, models, schemas, repositories, services, routes, migrations, and tests for the MVP text/URL slice. | Completed | Frontend Phase 1: Company / Source / Knowledge basic UI alignment. | Planned. | Frontend should follow the current text/URL backend contract only. |
| Phase 2: Product Card | Product Card backend contract for AI-generated and manual cards, draft/confirmed lifecycle, edit, confirm, delete, source type, company ownership, and tests. | Completed for backend contract. | Frontend Phase 2: Product Card UI. | Implemented for the supported Product Card UI lifecycle. | PostgreSQL-backed browser smoke passed for create, edit, confirm, draft delete, and Campaign-linked 409 Chinese UI messaging. |
| Phase 3: Campaign | Campaign model, migration, schemas, repository, service, routes, API contract, lifecycle, confirmed Product Card linkage, `product_card_snapshot`, duplicate-as-draft behavior, and tests. | Completed for the minimum backend vertical slice. | Frontend Phase 3: Campaign UI synchronized with Backend Phase 3 Campaign. | Implemented for the supported Campaign UI lifecycle. | Campaign frontend live-backend browser smoke passed against local PostgreSQL for direct route reachability, create draft, confirm, status filters, and Product Card linkage. |
| Phase 4: Lead Discovery | Provider-driven candidate lead discovery from confirmed Campaign criteria, using `task_runs`, `leads`, and `MockSearchProvider` first. | Implemented for the first mock-provider backend vertical slice; local PostgreSQL migration / API smoke passed for the verified endpoints. | Lead discovery task/result UI. | Implemented and local PostgreSQL live-backend browser smoke passed for confirmed Campaign start, task status/history, candidate leads, duplicate conflict, and draft/archived action hiding. | Phase 4 remains limited to mock search candidate discovery. The UI must not imply validation, scoring, contacts, outreach, Gmail, real search, or real crawling. |
| Phase 5: Lead Validation + Intelligence | Lead normalization, duplicate handling, website availability checks, intelligence capture, evidence storage, and content sufficiency. | Implemented for the first mock-crawler backend slice; independent local PostgreSQL migration/API smoke passed. | Lead validation and lead intelligence UI states. | Implemented from Stitch corrected design screens and backend Phase 5 APIs; frontend build and local PostgreSQL live-backend browser smoke passed. | Backend uses `MockCrawlerProvider`, `input_url`, `lead_intelligence`, and task status APIs. UI must not imply real crawling, scoring, review, contacts, outreach, or Gmail Draft work. |
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
  the live backend. Frontend Phase 5 Lead Validation + Intelligence UI is
  implemented, build-verified, and locally smoke-verified against the live
  backend.
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
  `products`, the minimum `campaigns` vertical slice, the first
  mock-provider-backed Lead Discovery backend slice, and the first
  mock-crawler-backed Lead Validation + Intelligence slice; later modules
  beyond Phase 5 remain placeholders.
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
- Phase 5 Lead Validation + Intelligence first backend slice is implemented.
  Endpoints are `POST /api/v1/leads/{lead_id}/validation`,
  `GET /api/v1/leads/{lead_id}/validation/tasks`,
  `GET /api/v1/leads/{lead_id}/intelligence`, and the existing
  `GET /api/v1/tasks/{task_id}`.
- Phase 5 validation outcomes are `valid`, `invalid`, `duplicate`, and
  `insufficient_content`; provider/system failure remains task failure and does
  not change `leads.validation_status`.
- Phase 5 extends `task_runs` with `lead_validation` as `task_type`, `lead` as
  `related_entity_type`, and `input_url = lead.website`. The Lead Discovery
  `search_query` field is not reused to store website URLs.
- A Lead that exists but has no intelligence returns an empty
  `GET /api/v1/leads/{lead_id}/intelligence` collection.
- Phase 5 same-Campaign duplicate detection is based on canonical website
  normalization.
- Phase 5 remains out of scope for AI scoring, human review decisions, contact
  discovery, Outreach Draft, Gmail Draft, real crawler provider integration
  unless explicitly authorized, LinkedIn crawling, and CRM automation.
- The Phase 5 migration and API smoke were verified on 2026-07-14 against a
  disposable local PostgreSQL database on port `55434` and a live FastAPI
  backend on `127.0.0.1:8000`. The smoke migrated to Alembic head
  `20260714_0007`, created the upstream company/Product Card/Campaign/Lead
  Discovery data through live HTTP APIs, validated one discovered Lead, wrote
  one `lead_intelligence` record, confirmed `input_url` stores the Lead
  website while `search_query` stays empty, and confirmed duplicate Lead
  Validation returns HTTP `409`. This is local development proof, not staging
  or production proof.
- Frontend Phase 5 Lead Validation + Intelligence UI is implemented inside the
  confirmed Campaign Lead Discovery workspace. It extends the candidate Lead
  table with validation actions, selected Lead detail, validation task status,
  validation task history, factual `lead_intelligence` display, no-intelligence
  state, provider/task failure state, invalid URL state, duplicate state, and
  insufficient-content state. It was implemented from the Stitch corrected
  screens `待验证线索列表 + 详情面板 - 修正版`,
  `验证任务运行中 - 修正版`, `验证完成并展示网站情报 - 修正版`, and
  `异常状态预览：内容不足/失败/重复 - 修正版`.
- Frontend Phase 5 user-facing text is Chinese and the UI explicitly keeps
  scoring, human review, contacts, Outreach Draft, Gmail Draft, real crawler
  integration, LinkedIn crawling, and CRM automation out of scope.
- Frontend Phase 5 local PostgreSQL live-backend browser smoke passed on
  2026-07-16 against a disposable PostgreSQL database on port `55435`, live
  FastAPI on `127.0.0.1:8000`, and Vite on `127.0.0.1:5173`: a draft Campaign
  was confirmed in the browser, the confirmed Campaign entered Lead Discovery,
  three candidate Leads were displayed, Lead Validation created and displayed
  one `lead_intelligence` record, repeated validation returned backend HTTP
  `409` with `lead_already_validated`, `insufficient_content` displayed the
  content-insufficient state, and a mock provider failure displayed the failed
  validation task while leaving the Lead `pending`.
- Campaign-side Product Card same-company validation is implemented for
  Campaign creation and confirmation.
- Route-level Product Card get, patch, confirm, and delete company/workspace
  authorization remains planned hardening; repository/service company-scoped
  helpers exist but do not implement account or workspace authorization.

## Latest Codex Task Records

This section keeps compact records for the latest Codex tasks. Detailed task
history should be moved to `docs/DEVELOPMENT_LOG.md`.

### 2026-07-16 - Frontend Phase 5 Live-Backend Browser Smoke

Completed: Ran local PostgreSQL live-backend browser smoke for Frontend Phase 5
Lead Validation + Intelligence.

What changed:

- Started Docker Desktop and a disposable PostgreSQL 16 smoke container on
  `localhost:55435`.
- Ran the full Alembic migration chain to `20260714_0007 (head)`.
- Started live FastAPI on `127.0.0.1:8000` and Vite on `127.0.0.1:5173`.
- Seeded company, confirmed manual Product Card, and draft Campaign through
  live HTTP APIs.
- Used the browser UI to confirm the Campaign, enter the confirmed Campaign
  Lead Discovery workspace, start Lead Discovery, and display three candidate
  Leads.
- Used the browser UI to start Lead Validation for a discovered Lead and display
  the resulting factual `lead_intelligence`.
- Verified repeated validation against the same validated Lead returned backend
  HTTP `409` with `lead_already_validated`.
- Exercised abnormal Phase 5 states by updating smoke Lead URLs to mock crawler
  trigger URLs, then verified `insufficient_content` and provider-failure UI
  states in the browser.
- Stopped the live FastAPI process, Vite process, and disposable PostgreSQL
  container after the smoke run.

Files modified:

- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification commands:

- `docker run --name ai-b2b-sales-phase5-browser-smoke-postgres --rm ... postgres:16-alpine`
- `docker exec ai-b2b-sales-phase5-browser-smoke-postgres pg_isready -U phase5_browser_smoke -d ai_b2b_sales_phase5_browser_smoke`
- `.venv\Scripts\python.exe -m alembic upgrade head`
- `.venv\Scripts\python.exe -m alembic current`
- `.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000`
- `npm.cmd --prefix frontend run dev -- --host 127.0.0.1 --port 5173`
- Browser smoke at `http://127.0.0.1:5173/campaigns`
- Live API duplicate validation and status summary checks against
  `http://127.0.0.1:8000`

Test status:

- Alembic migration smoke passed against PostgreSQL and reached
  `20260714_0007 (head)`.
- Live FastAPI database health check passed.
- Browser smoke passed for Campaign confirmation, Lead Discovery candidate
  display, Lead Validation start, `lead_intelligence` display, repeated
  validation `409`, `insufficient_content`, and provider-failure task state.
- No automated tests were added or updated because this task was runtime smoke
  verification and documentation update only.

API contract alignment:

- Verified the UI used the implemented Backend Phase 5 APIs:
  `POST /api/v1/leads/{lead_id}/validation`,
  `GET /api/v1/leads/{lead_id}/validation/tasks`,
  `GET /api/v1/leads/{lead_id}/intelligence`, and
  `GET /api/v1/tasks/{task_id}`.
- Confirmed `task_runs.input_url` stores the Lead website for validation tasks.
- Confirmed provider failure leaves `leads.validation_status = pending`.
- Confirmed repeated validation of a terminal Lead returns HTTP `409` with
  `lead_already_validated`.

Stitch design alignment:

- Smoke verified the existing Stitch-aligned Frontend Phase 5 UI; no visual
  redesign was performed.

User-facing Chinese text verification:

- Browser-visible Phase 5 controls and states were Chinese, including Campaign
  confirmation, Lead Discovery, Lead Validation, website intelligence,
  content-insufficient, failed-task, retry, and scope-boundary copy.

Known limitations:

- This is local development proof only, not staging or production proof.
- The smoke used `MockSearchProvider` and `MockCrawlerProvider`; no real search
  API, real crawler API, AI scoring, human review, contact discovery, Outreach
  Draft, Gmail Draft, LinkedIn crawling, or CRM behavior was verified or
  implemented.
- No RQ worker runtime exists yet; mock providers still execute synchronously
  inside services.
- Abnormal-state Leads were adjusted directly in the disposable smoke database
  because the MVP has no public manual Lead creation endpoint.

Commit / push status:

- Not committed.
- Not pushed to GitHub.

Next recommended step:

- Move to Frontend Phase 1 company/source/knowledge screens or Phase 6 Lead
  Scoring contract planning, depending on whether the next priority is closing
  early frontend workflow gaps or continuing downstream lead qualification.

### 2026-07-15 - Frontend Phase 5 Lead Validation + Intelligence UI

Completed: Implemented Frontend Phase 5 Lead Validation + Intelligence UI
inside the confirmed Campaign Lead Discovery workspace.

What changed:

- Read the latest Stitch project `AI 获客任务管理系统` and used the corrected
  Phase 5 screens as design context:
  `待验证线索列表 + 详情面板 - 修正版`,
  `验证任务运行中 - 修正版`,
  `验证完成并展示网站情报 - 修正版`, and
  `异常状态预览：内容不足/失败/重复 - 修正版`.
- Extended the frontend Lead Discovery API client for Phase 5:
  `POST /api/v1/leads/{lead_id}/validation`,
  `GET /api/v1/leads/{lead_id}/validation/tasks`,
  `GET /api/v1/leads/{lead_id}/intelligence`, and the existing task status
  read.
- Updated task typing so `task_runs` supports `lead_validation`,
  `related_entity_type = lead`, nullable `search_query`, and `input_url`.
- Added selected Lead validation workflow in the existing Campaign detail Lead
  Discovery panel.
- Added validation start, retry-after-failed/cancelled UI behavior, validation
  task polling, validation task history, and refresh controls.
- Added factual website intelligence display for `website_summary`,
  `products_or_services`, `target_customers`, `business_model`, `pain_points`,
  and evidence.
- Added UI states for no intelligence, task/provider failure, invalid website,
  duplicate Lead, and insufficient content.
- Corrected Stitch sample-only/static details during implementation: no hardcoded
  page counts, elapsed times, fake crawl metrics, scoring, review decisions,
  contacts, Outreach Draft, Gmail Draft, real search, or real crawler behavior
  were added.

Files modified:

- `frontend/src/api/leadDiscovery.ts`
- `frontend/src/pages/campaigns/LeadDiscoveryPanel.tsx`
- `frontend/src/styles/global.css`
- `docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification commands:

- `npm.cmd --prefix frontend run build`

Test status:

- Frontend TypeScript and Vite production build passed.
- No backend tests were run because this task changed frontend UI and docs only.
- No local PostgreSQL live-backend browser smoke was run in this task.

API contract alignment:

- UI uses only the implemented Backend Phase 5 APIs and existing task status
  API.
- UI shows `leads.validation_status` as the business validation result and
  `task_runs.status` as execution state.
- UI reads factual intelligence only from backend `lead_intelligence`.
- UI keeps Phase 6+ concepts out of scope: scoring, human review decisions,
  contacts, Outreach Draft, Gmail Draft, auto-send, CRM behavior, LinkedIn
  crawling, and real crawler provider integration.

Stitch design alignment:

- Used Stitch as visual and interaction context only.
- Preserved the repo's existing Campaign / Lead Discovery workbench structure
  instead of introducing unsupported navigation or backend behavior.
- Corrected unsupported or sample-only Stitch details in code by binding the UI
  to real backend response fields.

User-facing Chinese text verification:

- Added Phase 5 UI text in Chinese.
- The only mentions of scoring, contacts, Gmail, real search, or real crawler
  in the UI are explicit negative-scope notices.

Known limitations:

- Build proof is complete, but live-browser smoke against local PostgreSQL and
  FastAPI is still pending.
- The UI remains mock-crawler-only because the backend first slice uses
  `MockCrawlerProvider`.
- No RQ worker runtime exists yet; validation tasks still complete
  synchronously inside the backend service.
- Frontend Phase 5 does not implement Phase 6 scoring, Phase 7 review, contacts,
  outreach, or Gmail Draft.

Commit / push status:

- Not committed.
- Not pushed to GitHub.

Next recommended step:

- Run local PostgreSQL live-backend browser smoke for Frontend Phase 5:
  confirmed Campaign -> Lead Discovery results -> select discovered Lead ->
  start Lead Validation -> display `lead_intelligence` -> verify duplicate /
  insufficient-content / provider-failure UI states where feasible.

### 2026-07-14 - Phase 5 Independent PostgreSQL Migration/API Smoke

Completed: Ran independent local PostgreSQL migration and live FastAPI API
smoke verification for Backend Phase 5 Lead Validation + Intelligence.

What changed:

- Started a disposable PostgreSQL 16 container on `localhost:55434`.
- Ran the full Alembic migration chain to head against the smoke database.
- Started a live FastAPI backend on `127.0.0.1:8000` using the smoke database.
- Seeded the required upstream workflow through live HTTP APIs:
  company, manual Product Card, confirmed Product Card, draft Campaign,
  confirmed Campaign, Lead Discovery task, and discovered Leads.
- Started Lead Validation for one discovered Lead through
  `POST /api/v1/leads/{lead_id}/validation`.
- Verified the validation task completed through `GET /api/v1/tasks/{task_id}`.
- Verified the Lead had one validation task through
  `GET /api/v1/leads/{lead_id}/validation/tasks`.
- Verified `GET /api/v1/leads/{lead_id}/intelligence` returned one
  `mock_crawler` intelligence record with completed crawl status and sufficient
  content quality.
- Verified the validated Lead changed to `validation_status = valid` while
  `review_status` stayed `unreviewed`.
- Verified Phase 5 stores the website in `task_runs.input_url` and does not
  reuse the Lead Discovery `search_query` field for website URLs.
- Verified duplicate Lead Validation returns HTTP `409`.
- Stopped the live FastAPI process and disposable PostgreSQL container after
  the smoke run.

Files modified:

- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification commands:

- `docker version`
- `docker run --name ai-b2b-sales-phase5-smoke-postgres --rm -e POSTGRES_DB=ai_b2b_sales_phase5_smoke -e POSTGRES_USER=phase5_smoke -e POSTGRES_PASSWORD=phase5_smoke_password -p 55434:5432 -d postgres:16-alpine`
- `docker exec ai-b2b-sales-phase5-smoke-postgres pg_isready -U phase5_smoke -d ai_b2b_sales_phase5_smoke`
- `.venv\Scripts\python.exe -m alembic upgrade head`
- `.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000`
- Live PowerShell API smoke against `http://127.0.0.1:8000`
- `.venv\Scripts\python.exe -m alembic current`
- `docker stop ai-b2b-sales-phase5-smoke-postgres`

Test status:

- Independent PostgreSQL migration smoke passed.
- Alembic current reached `20260714_0007 (head)`.
- Live FastAPI database health check passed.
- Live API smoke passed for the Phase 5 happy path and duplicate-validation
  conflict boundary.
- No automated tests were added or updated because this task was runtime smoke
  verification and documentation update only.

Known limitations:

- This is local development proof only, not staging or production proof.
- The smoke uses `MockSearchProvider` and `MockCrawlerProvider`; no real search
  API, real crawler API, AI scoring, human review, contact discovery, Outreach
  Draft, Gmail Draft, LinkedIn crawling, or CRM behavior was verified or
  implemented.
- No RQ worker runtime is implemented yet; mock providers still execute
  synchronously inside services.
- Frontend Phase 5 UI is not implemented.
- The disposable PostgreSQL container used a separate database and did not
  mutate existing local development data.

Commit / push status:

- Not committed.
- Not pushed to GitHub.

Next recommended step:

- Prepare Stitch or user-provided design context for Frontend Phase 5 Lead
  Validation + Intelligence before implementing any validation/intelligence UI.
