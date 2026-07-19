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
Frontend Phase 1 Company / Sources / Knowledge UI is implemented from the
Stitch Phase 1 final corrected screens and the Backend Phase 1B API contract.
Frontend build verification and local PostgreSQL live-backend browser smoke
verification have passed.
An integrated local PostgreSQL live-backend browser smoke from Frontend Phase 1
through Frontend Phase 5 has passed for demo-readiness proof.

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
- Frontend Phase 1: Implemented for the supported company/source/knowledge
  workflow; frontend build verification and local PostgreSQL live-backend
  browser smoke passed.
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
- Integrated Phase 1 through Phase 5 workflow smoke: Passed locally against
  PostgreSQL, live FastAPI, Vite, and the browser UI.

## Unified Phase Tracking

| Phase number | Backend scope | Backend status | Frontend scope | Frontend status | Notes / current next step |
|---|---|---|---|---|---|
| Foundation stabilization | Project scaffold, environment-driven config, Alembic baseline, health checks, company router, and rule-doc stabilization. | Completed | React + TypeScript + Vite shell and dashboard foundation. | Basic shell present; business workflow UI pending. | Foundation is complete, but this is not a full MVP. |
| Phase 1B | Minimum text/URL source records plus deterministic knowledge draft and review behavior. | Completed | Feeds Frontend Phase 1 company/source/knowledge screens. | Implemented. | UI explicitly says URL records are saved only and not crawled, parsed, or read. |
| Phase 1: Sources + Knowledge | Source persistence, knowledge drafts, knowledge review transitions, models, schemas, repositories, services, routes, migrations, and tests for the MVP text/URL slice. | Completed | Frontend Phase 1: Company / Source / Knowledge basic UI alignment. | Implemented; frontend build and local PostgreSQL live-backend browser smoke passed. | Frontend follows the current text/URL backend contract only and does not imply uploads, OCR, crawling, or file parsing. |
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
- Frontend Phase 1 Company / Sources / Knowledge UI is implemented,
  build-verified, and locally smoke-verified against the live backend.
  Frontend Phase 2 Product Card UI, Frontend Phase 3 Campaign UI, and Frontend
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
- Frontend Phase 1 is implemented as a three-tab Company / Sources / Knowledge
  workspace at `/knowledge` and `#knowledge`. It supports company create/edit,
  text and URL source creation, source detail review, deterministic knowledge
  draft generation, and draft knowledge confirm/reject. It uses the Stitch
  Phase 1 final corrected screens as visual context and corrects unsupported
  design details by avoiding uploads, OCR, crawler/file parsing, settings/help
  navigation, fake static business data, and any claim that URL content was
  crawled or read.
- Frontend Phase 1 local PostgreSQL live-backend browser smoke passed on
  2026-07-19 against a disposable PostgreSQL database on port `55436`, live
  FastAPI on `127.0.0.1:8000`, and Vite on `127.0.0.1:5173`: the browser
  created and updated a company profile, added one text source and one URL
  source, generated one knowledge draft from each source, confirmed the text
  draft, rejected the URL draft, and the live API returned two ready sources
  plus one `confirmed` and one `rejected` knowledge item.
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
- Integrated Phase 1 through Phase 5 local PostgreSQL live-backend browser
  smoke passed on 2026-07-19 against a disposable PostgreSQL database on port
  `55437`, live FastAPI on `127.0.0.1:8000`, and Vite on
  `127.0.0.1:5173`: the browser created and updated a company, added text and
  URL sources, generated and reviewed knowledge drafts, generated and confirmed
  an AI Product Card from confirmed knowledge, created and confirmed a Campaign
  from that Product Card, started Lead Discovery, displayed three mock
  candidate Leads, validated `Helio Factory Automation`, and displayed one
  factual `lead_intelligence` record from `mock_crawler`.
- Campaign-side Product Card same-company validation is implemented for
  Campaign creation and confirmation.
- Route-level Product Card get, patch, confirm, and delete company/workspace
  authorization remains planned hardening; repository/service company-scoped
  helpers exist but do not implement account or workspace authorization.

## Latest Codex Task Records

This section keeps compact records for the latest Codex tasks. Detailed task
history should be moved to `docs/DEVELOPMENT_LOG.md`.

### 2026-07-19 - Integrated Phase 1 Through Phase 5 Browser Smoke

Completed: Ran an integrated local PostgreSQL live-backend browser smoke for
demo readiness across Frontend Phase 1 through Frontend Phase 5.

What changed:

- Started a disposable PostgreSQL 16 smoke container on `localhost:55437`.
- Ran the full Alembic migration chain to `20260714_0007 (head)`.
- Started live FastAPI on `127.0.0.1:8000` and Vite on `127.0.0.1:5173`.
- Used the browser UI to create and update a company profile.
- Added one text source and one URL source.
- Generated one knowledge draft from each source, confirmed the text-source
  draft, and rejected the URL-source draft.
- Generated one AI Product Card from confirmed knowledge and confirmed it.
- Created one Campaign from the confirmed Product Card and confirmed the
  Campaign, locking a Product Card snapshot.
- Started Lead Discovery from the confirmed Campaign and displayed three mock
  candidate Leads.
- Started Lead Validation for `Helio Factory Automation` and displayed one
  factual website intelligence record.
- Verified the live API final state across company, sources, knowledge,
  Product Card, Campaign, Lead Discovery task, Leads, Lead Validation task, and
  Lead Intelligence.
- Verified the browser console had no captured errors.

Files modified:

- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification commands:

- `docker run --name ai-b2b-sales-integrated-smoke-postgres-20260719 --rm ... postgres:16-alpine`
- `docker exec ai-b2b-sales-integrated-smoke-postgres-20260719 pg_isready -U integrated_smoke -d ai_b2b_sales_integrated_smoke`
- `.venv\Scripts\python.exe -m alembic upgrade head`
- `.venv\Scripts\python.exe -m alembic current`
- `.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000`
- `npm.cmd --prefix frontend run dev -- --host 127.0.0.1 --port 5173`
- Browser smoke across `http://127.0.0.1:5173/#knowledge`,
  `#products`, and `#campaigns`
- Live API final state checks against `http://127.0.0.1:8000`

Test status:

- Alembic migration smoke passed against PostgreSQL and reached
  `20260714_0007 (head)`.
- Live FastAPI health check passed.
- Browser smoke passed across Phase 1 company/source/knowledge, Phase 2 Product
  Card, Phase 3 Campaign, Phase 4 Lead Discovery, and Phase 5 Lead Validation +
  Intelligence.
- Browser console error check returned no errors.
- No automated tests were added or updated because this task was runtime smoke
  verification and documentation update only.

API contract alignment:

- Phase 1 used only text and URL sources and draft-only knowledge
  confirm/reject transitions.
- Phase 2 generated the Product Card from confirmed knowledge only and confirmed
  the draft Product Card.
- Phase 3 created the Campaign from a confirmed same-company Product Card and
  confirmed the Campaign with a saved Product Card snapshot.
- Phase 4 used `MockSearchProvider` and saved three discovered candidate Leads.
- Phase 5 used `MockCrawlerProvider`, created a completed `lead_validation`
  task with `input_url`, marked one Lead `valid`, and saved one
  `lead_intelligence` record.

Stitch design alignment:

- Smoke verified the existing Stitch-aligned frontend workflow screens; no
  visual redesign was performed.

User-facing Chinese text verification:

- Browser-visible workflow controls, form labels, status labels, confirmation
  dialogs, scope-boundary copy, Lead Discovery states, and Lead Validation
  states were Chinese.

Known limitations:

- This is local development proof only, not staging or production proof.
- The integrated smoke remains limited to implemented Phases 1 through 5.
- The run used deterministic/mock providers only: no real LLM, real search API,
  real crawler, AI scoring, human lead review, contact discovery, Outreach
  Draft, Gmail Draft, LinkedIn crawling, or CRM automation was performed.
- No RQ worker runtime exists yet; mock provider tasks still complete
  synchronously in service logic.

Commit / push status:

- Not committed.
- Not pushed to GitHub.

Next recommended step:

- Start Phase 6 Lead Scoring contract planning and implementation, keeping AI
  recommendation separate from human review status.

### 2026-07-19 - Frontend Phase 1 Live-Backend Browser Smoke

Completed: Ran local PostgreSQL live-backend browser smoke for Frontend Phase 1
Company / Sources / Knowledge.

What changed:

- Started Docker Desktop and a disposable PostgreSQL 16 smoke container on
  `localhost:55436`.
- Ran the full Alembic migration chain to `20260714_0007 (head)`.
- Started live FastAPI on `127.0.0.1:8000` and Vite on `127.0.0.1:5173`.
- Used the browser UI at `/knowledge` to create a company profile and then
  update its industry and website.
- Added one text source and one URL source through the browser UI.
- Verified the URL-source boundary copy remained visible: URL records are saved
  only and are not crawled, parsed, or read in this phase.
- Generated one knowledge draft from each source.
- Confirmed the text-source draft and rejected the URL-source draft.
- Verified the live API returned two ready sources and two knowledge items with
  final statuses `confirmed` and `rejected`.
- Stopped the live FastAPI process, Vite process, and disposable PostgreSQL
  container after the smoke run.

Files modified:

- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification commands:

- `docker run --name ai-b2b-sales-phase1-smoke-postgres-20260719 --rm ... postgres:16-alpine`
- `docker exec ai-b2b-sales-phase1-smoke-postgres-20260719 pg_isready -U phase1_smoke -d ai_b2b_sales_phase1_smoke`
- `.venv\Scripts\python.exe -m alembic upgrade head`
- `.venv\Scripts\python.exe -m alembic current`
- `.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000`
- `npm.cmd --prefix frontend run dev -- --host 127.0.0.1 --port 5173`
- Browser smoke at `http://127.0.0.1:5173/knowledge`
- Live API final state checks against `http://127.0.0.1:8000`

Test status:

- Alembic migration smoke passed against PostgreSQL and reached
  `20260714_0007 (head)`.
- Live FastAPI health check passed.
- Browser smoke passed for company create/update, text source creation, URL
  source creation, source-to-knowledge draft generation, draft confirmation,
  and draft rejection.
- No automated tests were added or updated because this task was runtime smoke
  verification and documentation update only.

API contract alignment:

- Verified the UI used the supported Backend Phase 1B APIs for company
  create/update, source create/list, knowledge draft creation, knowledge list,
  knowledge confirm, and knowledge reject.
- Verified only `source_type = text` and `source_type = url` were used.
- Verified the final knowledge statuses were `confirmed` and `rejected`, with
  no unsupported knowledge edit/retry workflow.

Stitch design alignment:

- Smoke verified the existing Stitch-aligned Frontend Phase 1 UI; no visual
  redesign was performed.

User-facing Chinese text verification:

- Browser-visible Phase 1 controls, tabs, form labels, source/knowledge states,
  confirmation dialogs, rejection dialogs, success messages, and scope-boundary
  copy were Chinese.

Known limitations:

- This is local development proof only, not staging or production proof.
- The backend Phase 1B generator remains deterministic and synchronous; no real
  LLM or crawler provider was used.
- URL source handling remains saved-record-only; no webpage crawling, parsing,
  or reading was performed.

Commit / push status:

- Not committed.
- Not pushed to GitHub.

Next recommended step:

- Continue with Phase 6 Lead Scoring contract planning, or run an integrated
  frontend workflow smoke across Phase 1 through Phase 5 if the next priority
  is demo readiness.

### 2026-07-17 - Frontend Phase 1 Company / Sources / Knowledge UI

Completed: Implemented Frontend Phase 1 for company profile, source input, and
knowledge review from Stitch Phase 1 final corrected screens and the Backend
Phase 1B contract.

What changed:

- Read the Stitch project `AI 获客任务管理系统` and used these Phase 1 final
  corrected screens as visual context:
  `公司资料维护 - Phase 1 最终修正版`,
  `资料来源管理 - Phase 1 最终修正版`, and
  `知识审核工作台 - Phase 1 最终修正版`.
- Added a Phase 1 API client for company list/create/update, source
  list/create, source-to-knowledge draft creation, knowledge list, confirm, and
  reject.
- Added a new `/knowledge` / `#knowledge` workspace with tabs for company
  profile, sources, and knowledge review.
- Added company create/edit drawer, source text/URL create drawer, source
  detail modal, knowledge detail modal, and knowledge confirm/reject modals.
- Corrected Stitch design issues during implementation: removed unsupported
  settings/help navigation from the new Phase 1 workspace, replaced static
  sample rows with backend-bound state, and made the URL source boundary
  explicit as saved-only with no crawling, parsing, or webpage reading.

Files modified:

- `frontend/src/api/knowledgeBase.ts`
- `frontend/src/pages/knowledge/KnowledgeWorkspace.tsx`
- `frontend/src/app/App.tsx`
- `frontend/src/styles/global.css`
- `docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification commands:

- `npm.cmd --prefix frontend run build`
- `rg -n "上传|文件|PDF|Word|OCR|爬|抓取|解析|读取网页|发送邮件|自动发送|LinkedIn|Google Sheets|系统设置" frontend/src/pages/knowledge frontend/src/api/knowledgeBase.ts frontend/src/app/App.tsx`

Test status:

- Frontend TypeScript and Vite production build passed.
- No backend tests were run because this task changed frontend UI and docs only.
- No local PostgreSQL live-backend browser smoke was run in this task.

API contract alignment:

- UI uses only the documented Backend Phase 1B endpoints:
  `POST /api/v1/companies`, `PATCH /api/v1/companies/{company_id}`,
  `GET /api/v1/companies`, `POST /api/v1/companies/{company_id}/sources`,
  `GET /api/v1/companies/{company_id}/sources`,
  `POST /api/v1/sources/{source_id}/knowledge-drafts`,
  `GET /api/v1/companies/{company_id}/knowledge`,
  `POST /api/v1/knowledge/{knowledge_id}/confirm`, and
  `POST /api/v1/knowledge/{knowledge_id}/reject`.
- UI supports only `source_type = text` and `source_type = url`.
- Knowledge confirmation and rejection actions are shown only for `draft`
  knowledge items.
- UI does not expose upload, OCR, file parsing, crawler, Gmail, LinkedIn,
  Google Sheets, scoring, review, contact, or outreach behavior.

Stitch design alignment:

- Preserved the Stitch Phase 1 three-tab layout, table/list direction, drawer
  forms, status badges, detail modals, and confirm/reject review flow.
- Used Stitch as visual and interaction context only; backend contract and
  project rules remained authoritative.

User-facing Chinese text verification:

- New Phase 1 page titles, tabs, buttons, labels, empty states, errors,
  success toasts, detail modals, and confirmation dialogs are Chinese.
- Scope-boundary copy explicitly says URL records are not crawled, parsed, or
  read in the current phase.

Known limitations:

- This is build proof only, not live-backend browser smoke, staging, or
  production proof.
- The backend Phase 1B generator remains deterministic and synchronous; no real
  LLM or crawler provider is used.
- Sources cannot be edited or deleted because the current backend contract does
  not expose source edit/delete endpoints.
- Knowledge content cannot be edited because the current backend contract only
  supports confirm/reject transitions.

Commit / push status:

- Not committed.
- Not pushed to GitHub.

Next recommended step:

- Run local live-backend browser smoke for Frontend Phase 1:
  create/update company -> add text and URL sources -> generate knowledge draft
  -> confirm and reject draft knowledge.
