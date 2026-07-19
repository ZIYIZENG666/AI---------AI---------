# Development Log

## Purpose

This file records detailed development history and task-level completion logs
for the AI Sales Knowledge Base + AI Customer Matching Judgment System.

Use this file when you need historical context, prior task details, or a record
of documentation-only work that no longer belongs in the high-level progress
tracker.

## Relationship To `DEVELOPMENT_PROGRESS.md`

- `docs/DEVELOPMENT_PROGRESS.md` is the current high-level phase status file.
- `docs/DEVELOPMENT_PROGRESS.md` should show the active phase, phase table,
  current known limits, and compact latest Codex task records.
- `docs/DEVELOPMENT_LOG.md` is the detailed historical log.
- Documentation-only changes should be recorded here as documentation-only
  entries.
- Do not treat a log entry as completed code work unless the entry explicitly
  says the relevant models, schemas, repositories, services, routes, migrations,
  and tests exist where appropriate.

## Current Progress Summary

This summary reflects the current high-level backend and frontend implementation
state.

| Area | Status | Summary |
|---|---|---|
| Foundation stabilization | Completed | Project scaffold, environment-driven backend config, Alembic foundation, health checks, company router, and rule-doc stabilization were completed. |
| Phase 1B | Completed | The minimum source and knowledge slice supports text/URL source records and deterministic source-to-knowledge draft creation. |
| Phase 1: Sources + Knowledge | Completed | Source persistence, knowledge draft creation, review transitions, filtering, migrations, routes, services, repositories, schemas, and tests exist for the MVP text/URL slice. |
| Phase 2: Product Card backend contract | Completed | Product Card backend supports AI-generated and manual cards, `draft` and `confirmed` lifecycle, edit, confirm, delete, `source_type`, and tests under the finalized contract. |
| Phase 3: Campaign | Backend and supported frontend lifecycle completed | Campaign backend supports the minimum Phase 3 contract: `draft`, `confirmed`, and `archived`; confirmed same-company Product Card validation; `product_card_snapshot`; archive; duplicate-as-draft; routes; migration; and tests. Frontend Phase 3 Campaign UI is implemented for the supported lifecycle. |
| Phase 4: Lead Discovery | Backend implemented and frontend UI live-smoke verified | Phase 4 now has models, schemas, repositories, services, routes, migration, `MockSearchProvider`, focused tests, local PostgreSQL / live API smoke proof, and a Frontend Phase 4 UI that passed local PostgreSQL live-backend browser smoke for confirmed Campaign -> Lead Discovery task -> mock search results -> saved candidate leads. It does not call real search APIs, self-build full-web search, perform real website crawling, score leads, approve leads, find contacts, or create outreach/Gmail drafts. |
| Phase 5: Lead Validation + Intelligence | Backend first slice and frontend UI live-smoke verified | Phase 5 now has `lead_validation` task runs, `input_url`, `lead_intelligence`, `MockCrawlerProvider`, service/repository/routes, migration, focused tests, independent local PostgreSQL / live FastAPI smoke proof, a build-verified Frontend Phase 5 UI, and local PostgreSQL live-backend browser smoke proof for the supported UI workflow. It remains mock-crawler-only and does not perform AI scoring, human review, contact discovery, Outreach Draft, Gmail Draft, LinkedIn crawling, or real crawler integration. |
| Frontend business workflow | Partially implemented | Frontend Phase 1 Company / Sources / Knowledge UI, Product Card UI, Campaign UI, Frontend Phase 4 Lead Discovery UI, and Frontend Phase 5 Lead Validation + Intelligence UI are implemented for their supported lifecycles. Product Card, Campaign, Frontend Phase 1, Phase 4, Frontend Phase 5, and an integrated Phase 1 through Phase 5 workflow are locally smoke-verified against the live backend. |

## 2026-07-19 - Integrated Phase 1 Through Phase 5 Browser Smoke

Type: Local PostgreSQL live-backend browser smoke verification and progress
documentation update.

Completed:

- Started a disposable PostgreSQL 16 container on `localhost:55437`.
- Ran the full Alembic migration chain against the smoke database and reached
  `20260714_0007 (head)`.
- Started a live FastAPI backend on `127.0.0.1:8000` against the smoke
  database.
- Verified `GET /health` returned HTTP `200`.
- Started Vite on `127.0.0.1:5173`.
- Used the browser UI to create a company profile, then update its industry and
  website.
- Added one text source and one URL source through the browser UI.
- Verified the URL-source boundary remained visible: URL records are saved only
  and are not crawled, parsed, or read in Phase 1.
- Generated one knowledge draft from each source.
- Confirmed the text-source draft and rejected the URL-source draft.
- Opened Product Card management, generated one AI Product Card from confirmed
  knowledge, and confirmed the Product Card.
- Opened Campaign management, created one Campaign from the confirmed Product
  Card, and confirmed the Campaign.
- Verified Campaign confirmation exposed the Lead Discovery workspace and
  locked a Product Card snapshot.
- Started Lead Discovery through the browser UI.
- Verified the completed `lead_discovery` task used `mock_search` and displayed
  three candidate Leads.
- Started Lead Validation for `Helio Factory Automation`.
- Verified the completed `lead_validation` task used `mock_crawler`,
  preserved `input_url = https://helio-factory.example.com`, marked the Lead
  `valid`, and displayed one factual `lead_intelligence` record with
  `content_quality = sufficient`.
- Verified browser-visible Phase 4 and Phase 5 scope-boundary copy: mock search
  only, no real crawler/search, no scoring, no human review, no contacts, and
  no Gmail Draft.
- Verified the browser console had no captured errors.
- Verified the live API final state:
  - one updated company
  - two ready sources: one `text`, one `url`
  - two knowledge items: one `confirmed`, one `rejected`
  - one confirmed AI-generated Product Card with one source knowledge ID
  - one confirmed Campaign with `product_card_snapshot`
  - one completed `lead_discovery` task from `mock_search`
  - three discovered Leads, all still `review_status = unreviewed`
  - one valid Lead with a completed `lead_validation` task from `mock_crawler`
  - one `lead_intelligence` record with `crawl_status = completed`
- Updated `docs/DEVELOPMENT_PROGRESS.md` to mark the integrated Phase 1 through
  Phase 5 smoke as passed and to keep only the latest three task records.

Files modified:

- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification:

- `docker run --name ai-b2b-sales-integrated-smoke-postgres-20260719 --rm -e POSTGRES_DB=ai_b2b_sales_integrated_smoke -e POSTGRES_USER=integrated_smoke -e POSTGRES_PASSWORD=integrated_smoke -p 55437:5432 -d postgres:16-alpine`
- `docker exec ai-b2b-sales-integrated-smoke-postgres-20260719 pg_isready -U integrated_smoke -d ai_b2b_sales_integrated_smoke`
- `.venv\Scripts\python.exe -m alembic upgrade head`
- `.venv\Scripts\python.exe -m alembic current`
- `.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000`
- `Invoke-WebRequest -UseBasicParsing -Uri http://127.0.0.1:8000/health`
- `npm.cmd --prefix frontend run dev -- --host 127.0.0.1 --port 5173`
- Browser smoke across `http://127.0.0.1:5173/#knowledge`, `#products`, and
  `#campaigns`
- Browser console error check
- Live API final state checks against `http://127.0.0.1:8000`

Results:

- PostgreSQL migration smoke passed.
- Alembic current reached `20260714_0007 (head)`.
- FastAPI health check passed.
- Vite served the browser workflow.
- Integrated browser smoke passed across Phase 1 company/source/knowledge,
  Phase 2 Product Card, Phase 3 Campaign, Phase 4 Lead Discovery, and Phase 5
  Lead Validation + Intelligence.
- Browser console error check returned no errors.
- No automated tests were added or updated because this was runtime smoke
  verification and documentation update only.

API contract alignment:

- Phase 1 used only supported text/URL sources and draft-only knowledge
  confirm/reject transitions.
- Phase 2 generated a Product Card only from confirmed company knowledge,
  stored `source_type = ai_generated`, and confirmed the draft Product Card.
- Phase 3 created a Campaign only from a confirmed same-company Product Card and
  confirmed the Campaign with a saved Product Card snapshot.
- Phase 4 created a `lead_discovery` task, used `MockSearchProvider`, and saved
  discovered candidate Leads without validation, scoring, review, contacts, or
  outreach.
- Phase 5 created a `lead_validation` task, used `MockCrawlerProvider`, stored
  the Lead website in `input_url`, marked one Lead `valid`, and saved factual
  `lead_intelligence`.

Stitch design alignment:

- Smoke verified the existing Stitch-aligned frontend screens for the supported
  lifecycle; no visual redesign was performed.

User-facing Chinese text verification:

- Browser-visible workflow navigation, form labels, buttons, empty states,
  confirmation dialogs, status labels, Lead Discovery states, Lead Validation
  states, and scope-boundary copy were Chinese.

Known limits:

- This is local development proof only, not staging or production proof.
- The integrated smoke covers the implemented Phase 1 through Phase 5 workflow
  only.
- The run used deterministic/mock providers only. It did not use a real LLM,
  real search API, real crawler, AI scoring, human lead review, contact
  discovery, Outreach Draft, Gmail Draft, LinkedIn crawling, or CRM automation.
- No RQ worker runtime exists yet; mock provider tasks still complete
  synchronously in service logic.

Next recommended step:

- Start Phase 6 Lead Scoring contract planning and implementation, keeping AI
  recommendation separate from human review status.

## 2026-07-19 - Frontend Phase 1 Live-Backend Browser Smoke

Type: Local PostgreSQL live-backend browser smoke verification and progress
documentation update.

Completed:

- Started Docker Desktop and a disposable PostgreSQL 16 container on
  `localhost:55436`.
- Ran the full Alembic migration chain against the smoke database and reached
  `20260714_0007 (head)`.
- Started a live FastAPI backend on `127.0.0.1:8000` against the smoke
  database.
- Verified `GET /health` returned HTTP `200`.
- Started Vite on `127.0.0.1:5173`.
- Opened `/knowledge` in the browser and verified the empty company state.
- Created a company profile through the browser UI.
- Updated the company industry and website through the browser UI.
- Added one text source and one URL source through the browser UI.
- Verified the browser-visible source scope boundary remained clear: URL
  records are saved only and are not crawled, parsed, or read in Phase 1.
- Generated one knowledge draft from the URL source and one knowledge draft
  from the text source.
- Confirmed the text-source draft through the browser confirmation dialog.
- Rejected the URL-source draft through the browser rejection dialog.
- Verified the browser counters showed two sources, zero remaining drafts, one
  confirmed knowledge item, and one rejected knowledge item.
- Verified the live API returned:
  - one company with the updated website and industry
  - two ready sources, one `url` and one `text`
  - two knowledge items with statuses `confirmed` and `rejected`
- Updated `docs/DEVELOPMENT_PROGRESS.md` to mark Frontend Phase 1
  live-backend browser smoke as passed and to keep only the latest three task
  records.

Files modified:

- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification:

- `docker run --name ai-b2b-sales-phase1-smoke-postgres-20260719 --rm -e POSTGRES_DB=ai_b2b_sales_phase1_smoke -e POSTGRES_USER=phase1_smoke -e POSTGRES_PASSWORD=phase1_smoke -p 55436:5432 -d postgres:16-alpine`
- `docker exec ai-b2b-sales-phase1-smoke-postgres-20260719 pg_isready -U phase1_smoke -d ai_b2b_sales_phase1_smoke`
- `.venv\Scripts\python.exe -m alembic upgrade head`
- `.venv\Scripts\python.exe -m alembic current`
- `.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000`
- `Invoke-WebRequest -UseBasicParsing -Uri http://127.0.0.1:8000/health`
- `npm.cmd --prefix frontend run dev -- --host 127.0.0.1 --port 5173`
- Browser smoke at `http://127.0.0.1:5173/knowledge`
- Live API final state checks against `http://127.0.0.1:8000`

Results:

- PostgreSQL migration smoke passed.
- Alembic current reached `20260714_0007 (head)`.
- FastAPI health check passed.
- Vite served `/knowledge`.
- Browser smoke passed for company create/update, text source creation, URL
  source creation, source-to-knowledge draft generation, draft confirmation,
  and draft rejection.
- No automated tests were added or updated because this was runtime smoke
  verification and documentation update only.

API contract alignment:

- The smoke used the documented Backend Phase 1B source and knowledge workflow:
  company create/update, text/URL source creation, deterministic
  source-to-knowledge draft generation, draft confirm, and draft reject.
- Only `source_type = text` and `source_type = url` were used.
- Confirm and reject were performed only on `draft` knowledge items.
- The UI did not expose uploads, OCR, file parsing, crawler behavior, source
  edit/delete, knowledge edit, Gmail, LinkedIn, Google Sheets, scoring,
  contacts, outreach, or CRM behavior.

Stitch design alignment:

- Smoke verified the existing Stitch-aligned Frontend Phase 1 UI; no visual
  redesign was performed.

User-facing Chinese text verification:

- Browser-visible controls, page titles, tabs, form labels, empty/source states,
  knowledge review states, confirmation/rejection dialogs, success messages,
  and scope-boundary copy were Chinese.

Known limits:

- This is local development proof only, not staging or production proof.
- The smoke used the deterministic Phase 1B generator; no real LLM, crawler, or
  webpage reading was used.
- URL source records remained saved-link records only.

Next recommended step:

- Continue with Phase 6 Lead Scoring contract planning, or run an integrated
  frontend workflow smoke across Phase 1 through Phase 5 if demo readiness is
  the next priority.

## 2026-07-17 - Frontend Phase 1 Company / Sources / Knowledge UI

Type: Frontend implementation, Stitch design alignment, and progress
documentation update.

Completed:

- Read the current Stitch project `AI 获客任务管理系统`.
- Used the Phase 1 final corrected Stitch screens as design context:
  - `公司资料维护 - Phase 1 最终修正版`
  - `资料来源管理 - Phase 1 最终修正版`
  - `知识审核工作台 - Phase 1 最终修正版`
- Added `frontend/src/api/knowledgeBase.ts` with API client methods for:
  - company list/create/update
  - source list/create
  - source-to-knowledge draft creation
  - knowledge list
  - knowledge confirm/reject
- Added a new `KnowledgeWorkspace` with three tabs:
  - company profile create/edit and read view
  - text/URL source creation, list, detail, and knowledge-draft generation
  - knowledge list, status filters, detail, confirm, and reject
- Updated app routing so `/knowledge` and `#knowledge` open the Phase 1
  workspace, while `/products`, `#products`, `/campaigns`, and `#campaigns`
  continue to route to their existing workspaces.
- Added CSS for the Phase 1 tabs, summary cards, company profile layout,
  source/knowledge tables, right-side drawers, detail modals, and review
  modals.
- Corrected Stitch design issues during implementation:
  - Removed unsupported settings/help navigation from the new Phase 1 workspace.
  - Replaced static sample-only table data with backend-bound state.
  - Kept only text and URL source creation.
  - Added explicit copy that URL records are saved only and are not crawled,
    parsed, or read in the current phase.
  - Did not add upload, OCR, file parsing, crawler, Gmail, LinkedIn, Google
    Sheets, scoring, contact, outreach, or CRM behavior.
- Updated `docs/FRONTEND_DEVELOPMENT_PLAN.md` and
  `docs/DEVELOPMENT_PROGRESS.md` to mark Frontend Phase 1 implemented and
  build-verified.

Files modified:

- `frontend/src/api/knowledgeBase.ts`
- `frontend/src/pages/knowledge/KnowledgeWorkspace.tsx`
- `frontend/src/app/App.tsx`
- `frontend/src/styles/global.css`
- `docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification:

- `npm.cmd --prefix frontend run build`
- `rg -n "上传|文件|PDF|Word|OCR|爬|抓取|解析|读取网页|发送邮件|自动发送|LinkedIn|Google Sheets|系统设置" frontend/src/pages/knowledge frontend/src/api/knowledgeBase.ts frontend/src/app/App.tsx`

Results:

- Frontend TypeScript compilation passed.
- Vite production build passed.
- Unsupported-scope search found only explicit negative-scope copy for
  crawling/parsing/webpage reading.
- No backend tests were run because this task changed frontend UI and docs only.
- No live-backend browser smoke was run in this task.

API contract alignment:

- UI uses only documented Backend Phase 1B endpoints and fields.
- Source creation supports only `source_type = text` and `source_type = url`.
- Text sources require raw content; URL sources require a URL.
- Knowledge confirm/reject controls are shown only for `draft` items.
- Confirmed and rejected knowledge items are read-only in the UI because the
  backend does not expose edit or retry transitions for them.

Stitch design alignment:

- Preserved the Phase 1 Stitch visual direction: tabbed knowledge-base
  workspace, source list table, right-side create drawers, status badges, detail
  modals, and confirm/reject modals.
- Treated Stitch as design context only; API contract and project rules remained
  authoritative.

User-facing Chinese text verification:

- New Phase 1 visible text is Chinese, including navigation, page titles, form
  labels, buttons, empty states, error text, success toasts, modals, and scope
  notices.

Known limits:

- This is build proof only, not local PostgreSQL live-backend browser smoke,
  staging proof, or production proof.
- The backend Phase 1B knowledge draft generator is deterministic and
  synchronous; no real LLM or crawler is used.
- Source edit/delete and knowledge edit are not implemented because the current
  backend contract does not expose those endpoints.

Next recommended step:

- Run local live-backend browser smoke for Frontend Phase 1:
  create/update company -> add text and URL sources -> generate knowledge draft
  -> confirm and reject draft knowledge.

## 2026-07-16 - Frontend Phase 5 Live-Backend Browser Smoke

Type: Local PostgreSQL live-backend browser smoke verification and progress
documentation update.

Completed:

- Started Docker Desktop and a disposable PostgreSQL 16 container on
  `localhost:55435`.
- Ran the full Alembic migration chain against the smoke database and reached
  `20260714_0007 (head)`.
- Started a live FastAPI backend on `127.0.0.1:8000` against the smoke
  database.
- Verified `GET /health/db` returned `status = ok`.
- Started Vite on `127.0.0.1:5173`.
- Seeded the prerequisite company, confirmed manual Product Card, and draft
  Campaign through live HTTP APIs.
- Opened `/campaigns` in the browser and verified the draft Campaign rendered.
- Confirmed the Campaign through the browser UI and verified the confirmed
  detail view exposed the Lead Discovery workspace.
- Started Lead Discovery through the browser UI and verified three candidate
  Leads rendered from the live backend.
- Updated two smoke Lead URLs directly in the disposable database to exercise
  mock crawler abnormal states, because the MVP has no public manual Lead
  creation endpoint.
- Started Lead Validation for the valid discovered Lead through the browser UI
  and verified the UI displayed:
  - completed `lead_validation` task
  - `mock_crawler`
  - `input_url`
  - factual `lead_intelligence`
  - website summary, business model, products/services, target customers,
    pain points, and evidence
- Verified repeated validation for the terminal Lead returned HTTP `409` with
  `lead_already_validated`.
- Started Lead Validation for a smoke Lead with
  `https://phase5-insufficient.example.com` and verified the browser displayed
  the `insufficient_content` / website-content-insufficient state.
- Started Lead Validation for a smoke Lead with
  `https://provider-failure.example.com` and verified the browser displayed a
  failed validation task with `mock crawler failed`, no intelligence record, and
  the Lead still `pending`.
- Verified the live API summary matched browser observations:
  - Helio Factory Automation: `validation_status = valid`, task `completed`,
    one `lead_intelligence` record with `content_quality = sufficient`
  - Acme Quality Systems: `validation_status = insufficient_content`, task
    `completed`, one `lead_intelligence` record with
    `crawl_status = insufficient_content`
  - Northstar Inspection Group: `validation_status = pending`, task `failed`,
    `error_message = mock crawler failed`, zero intelligence records
- Stopped the live FastAPI process, Vite process, and disposable PostgreSQL
  container after the smoke run.
- Updated `docs/DEVELOPMENT_PROGRESS.md` to mark Frontend Phase 5
  live-backend browser smoke as passed and to keep only the latest three task
  records.

Files modified:

- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification:

- `docker ps --format "table {{.Names}}\t{{.Ports}}\t{{.Status}}"`
- `docker run --name ai-b2b-sales-phase5-browser-smoke-postgres --rm -e POSTGRES_DB=ai_b2b_sales_phase5_browser_smoke -e POSTGRES_USER=phase5_browser_smoke -e POSTGRES_PASSWORD=phase5_browser_smoke_password -p 55435:5432 -d postgres:16-alpine`
- `docker exec ai-b2b-sales-phase5-browser-smoke-postgres pg_isready -U phase5_browser_smoke -d ai_b2b_sales_phase5_browser_smoke`
- `.venv\Scripts\python.exe -m alembic upgrade head`
- `.venv\Scripts\python.exe -m alembic current`
- `.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000`
- `Invoke-RestMethod -Uri http://127.0.0.1:8000/health/db`
- `npm.cmd --prefix frontend run dev -- --host 127.0.0.1 --port 5173`
- Browser smoke at `http://127.0.0.1:5173/campaigns`
- Live API duplicate validation and final status summary checks

Results:

- PostgreSQL migration smoke passed.
- Alembic current reached `20260714_0007 (head)`.
- FastAPI database health check passed.
- Frontend Phase 5 live-backend browser smoke passed for the requested path:
  confirmed Campaign -> candidate Leads -> start validation -> display
  `lead_intelligence` -> duplicate validation `409` -> abnormal states.
- User-facing browser-visible Phase 5 text was Chinese.
- No automated tests were added or updated because this task was runtime smoke
  verification and documentation update only.

API contract alignment:

- The browser workflow used the implemented Backend Phase 5 APIs and existing
  task API only.
- The UI displayed `leads.validation_status` as business validation result and
  `task_runs.status` as execution state.
- The UI displayed website intelligence only from backend `lead_intelligence`.
- Repeated validation of a terminal Lead returned HTTP `409` with
  `lead_already_validated`.
- Provider failure remained an execution failure and did not change the Lead
  business validation status from `pending`.

Known limits:

- This is local development proof only, not staging or production proof.
- The smoke used `MockSearchProvider` and `MockCrawlerProvider`; no real search
  API, real crawler API, AI scoring, human review, contact discovery, Outreach
  Draft, Gmail Draft, LinkedIn crawling, or CRM behavior was verified or
  implemented.
- No RQ worker runtime exists yet; mock providers still execute synchronously
  inside services.
- Abnormal-state setup used direct updates in the disposable smoke database
  because the MVP does not expose manual Lead creation.

Next recommended step:

- Move to Frontend Phase 1 company/source/knowledge screens or Phase 6 Lead
  Scoring contract planning, depending on the chosen project priority.

## 2026-07-15 - Frontend Phase 5 Lead Validation + Intelligence UI

Type: Frontend implementation, Stitch design alignment, and progress
documentation update.

Completed:

- Read the current Stitch project `AI 获客任务管理系统`.
- Used the corrected Phase 5 Stitch screens as design context:
  - `待验证线索列表 + 详情面板 - 修正版`
  - `验证任务运行中 - 修正版`
  - `验证完成并展示网站情报 - 修正版`
  - `异常状态预览：内容不足/失败/重复 - 修正版`
- Extended the frontend Lead Discovery API client for Backend Phase 5:
  - `POST /api/v1/leads/{lead_id}/validation`
  - `GET /api/v1/leads/{lead_id}/validation/tasks`
  - `GET /api/v1/leads/{lead_id}/intelligence`
  - existing `GET /api/v1/tasks/{task_id}`
- Updated frontend task typing for `lead_validation`, `related_entity_type =
  lead`, nullable `search_query`, and `input_url`.
- Implemented selected Lead validation UI inside the existing confirmed
  Campaign Lead Discovery workspace.
- Added validation start behavior, validation task refresh/polling, validation
  task history, and retry after failed/cancelled validation tasks when the Lead
  remains pending.
- Added factual website intelligence display for website summary,
  products/services, target customers, business model, pain points, and evidence.
- Added no-intelligence, provider/task failure, invalid website, duplicate Lead,
  and insufficient-content states.
- Kept the UI bound to backend response fields instead of using Stitch's static
  sample-only values such as fake page counts or elapsed times.
- Updated `docs/DEVELOPMENT_PROGRESS.md` to mark Frontend Phase 5 implemented
  with build proof and live-browser smoke still pending.

Files modified:

- `frontend/src/api/leadDiscovery.ts`
- `frontend/src/pages/campaigns/LeadDiscoveryPanel.tsx`
- `frontend/src/styles/global.css`
- `docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification:

- `npm.cmd --prefix frontend run build`

Results:

- Frontend TypeScript compilation passed.
- Vite production build passed.
- User-facing Phase 5 UI text is Chinese.
- Scope wording was checked so the UI only mentions scoring, contacts, Gmail,
  real search, or real crawling as explicit negative-scope notices.

API contract alignment:

- The UI uses only the implemented Phase 5 backend APIs.
- `leads.validation_status` is shown as the business validation result.
- `task_runs.status` is shown as execution state.
- Website intelligence is shown only from backend `lead_intelligence`.
- Phase 5 UI does not imply AI scoring, human approval/rejection, contact
  discovery, Outreach Draft, Gmail Draft, auto-send, CRM behavior, LinkedIn
  crawling, or real crawler provider integration.

Known limits:

- This task did not run local PostgreSQL live-backend browser smoke.
- The backend remains mock-crawler-only through `MockCrawlerProvider`.
- No RQ worker runtime exists yet; backend task execution remains synchronous in
  the first slice.
- Frontend Phase 5 does not include Phase 6 scoring, Phase 7 review, contacts,
  outreach, or Gmail Draft.

Next recommended step:

- Run local PostgreSQL live-backend browser smoke for Frontend Phase 5:
  confirmed Campaign -> Lead Discovery results -> select discovered Lead ->
  start Lead Validation -> display `lead_intelligence` -> verify duplicate /
  insufficient-content / provider-failure UI states where feasible.

## 2026-07-14 - Phase 5 Independent PostgreSQL Migration/API Smoke

Type: Independent local PostgreSQL migration and live API smoke verification.

Completed:

- Started a disposable PostgreSQL 16 container on `localhost:55434` for an
  isolated Phase 5 smoke database.
- Ran the full Alembic migration chain against the smoke database and reached
  `20260714_0007_create_lead_intelligence`.
- Confirmed Alembic current was `20260714_0007 (head)`.
- Started a live FastAPI backend on `127.0.0.1:8000` against the smoke
  database.
- Verified `GET /health/db` returned `status = ok`.
- Seeded the prerequisite workflow through live HTTP APIs:
  - `POST /api/v1/companies`
  - `POST /api/v1/product-cards`
  - `POST /api/v1/product-cards/{product_card_id}/confirm`
  - `POST /api/v1/companies/{company_id}/campaigns`
  - `POST /api/v1/campaigns/{campaign_id}/confirm`
  - `POST /api/v1/campaigns/{campaign_id}/lead-discovery`
  - `GET /api/v1/campaigns/{campaign_id}/leads`
- Verified Lead Discovery created three mock candidate Leads.
- Verified an existing discovered Lead returned an empty intelligence list
  before validation.
- Started Phase 5 Lead Validation through
  `POST /api/v1/leads/{lead_id}/validation`.
- Verified the Lead Validation task through `GET /api/v1/tasks/{task_id}`:
  - `status = completed`
  - `task_type = lead_validation`
  - `related_entity_type = lead`
  - `input_url = lead.website`
  - `search_query = null`
  - `provider_name = mock_crawler`
- Verified `GET /api/v1/leads/{lead_id}/validation/tasks` returned one
  validation task for the Lead.
- Verified `GET /api/v1/leads/{lead_id}/intelligence` returned one factual
  intelligence record linked to the validation task.
- Verified the intelligence record used `provider_name = mock_crawler`,
  `crawl_status = completed`, and `content_quality = sufficient`.
- Verified the Lead changed to `validation_status = valid` while
  `review_status` remained `unreviewed`.
- Verified duplicate Lead Validation returned HTTP `409`.
- Stopped the live FastAPI process and removed the disposable PostgreSQL
  container after the smoke run.
- Updated `docs/DEVELOPMENT_PROGRESS.md` to mark Backend Phase 5 PostgreSQL
  migration/API smoke as passed and to keep only the latest three task records.

Files modified:

- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification:

- `docker version`
- `docker ps -a --filter name=ai-b2b-sales-phase5-smoke-postgres`
- `docker run --name ai-b2b-sales-phase5-smoke-postgres --rm -e POSTGRES_DB=ai_b2b_sales_phase5_smoke -e POSTGRES_USER=phase5_smoke -e POSTGRES_PASSWORD=phase5_smoke_password -p 55434:5432 -d postgres:16-alpine`
- `docker exec ai-b2b-sales-phase5-smoke-postgres pg_isready -U phase5_smoke -d ai_b2b_sales_phase5_smoke`
- `.venv\Scripts\python.exe -m alembic upgrade head`
- `.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000`
- Live PowerShell API smoke against `http://127.0.0.1:8000`.
- `.venv\Scripts\python.exe -m alembic current`
- `docker stop ai-b2b-sales-phase5-smoke-postgres`

Results:

- Docker Desktop was available after running commands with the required Docker
  approval boundary.
- PostgreSQL readiness passed.
- Alembic migration smoke passed on the isolated PostgreSQL database.
- Alembic current reached `20260714_0007 (head)`.
- Live FastAPI database health passed.
- Live API smoke passed for the Phase 5 happy path.
- Duplicate validation returned HTTP `409`.
- Disposable PostgreSQL cleanup completed.

Known limits:

- This is local development proof only, not staging or production proof.
- The smoke uses `MockSearchProvider` and `MockCrawlerProvider`; it does not
  verify real search, real crawling, AI scoring, human review, contact
  discovery, Outreach Draft, Gmail Draft, LinkedIn crawling, or CRM behavior.
- No RQ worker runtime is implemented; mock providers still execute
  synchronously inside the service layer.
- Frontend Phase 5 UI is not implemented.

Next recommended step:

- Prepare Stitch or user-provided design context for Frontend Phase 5 Lead
  Validation + Intelligence before implementing any validation/intelligence UI.

## 2026-07-14 - Backend Phase 5 Lead Validation + Intelligence First Slice

Type: Backend implementation, focused tests, and progress documentation update.

Completed:

- Implemented Backend Phase 5 first slice for Lead Validation + factual website
  intelligence.
- Extended `task_runs` to support `task_type = lead_validation`,
  `related_entity_type = lead`, and `input_url = lead.website`; `search_query`
  remains Lead Discovery-specific and is not used for website URLs.
- Added `lead_intelligence` ORM model and Alembic migration for factual website
  intelligence, source traceability, provider name, content quality, crawl
  status, and evidence.
- Implemented `MockCrawlerProvider` through the Crawler Provider interface.
- Implemented Phase 5 service/repository/routes for:
  - `POST /api/v1/leads/{lead_id}/validation`
  - `GET /api/v1/leads/{lead_id}/validation/tasks`
  - `GET /api/v1/leads/{lead_id}/intelligence`
  - existing `GET /api/v1/tasks/{task_id}`
- Kept the first slice synchronous inside the service until RQ worker runtime is
  implemented, while preserving the task-reference API contract.
- Implemented allowed validation outcomes:
  - `pending -> valid`
  - `pending -> invalid`
  - `pending -> duplicate`
  - `pending -> insufficient_content`
- Implemented same-Campaign duplicate detection after canonical website
  normalization.
- Made existing leads with no intelligence return an empty intelligence list.
- Kept provider/system failure as task failure without changing
  `leads.validation_status`.
- Kept Phase 5 out of AI scoring, human review decisions, contact discovery,
  Outreach Draft, Gmail Draft, real crawler integration, LinkedIn crawling, and
  CRM automation.

Files modified:

- `backend/app/main.py`
- `backend/app/models.py`
- `backend/app/providers/crawler_provider.py`
- `backend/app/modules/discovery/repository.py`
- `backend/app/modules/intelligence/models.py`
- `backend/app/modules/intelligence/repository.py`
- `backend/app/modules/intelligence/routes.py`
- `backend/app/modules/intelligence/schemas.py`
- `backend/app/modules/intelligence/service.py`
- `backend/app/modules/tasks/models.py`
- `backend/app/modules/tasks/repository.py`
- `backend/app/modules/tasks/schemas.py`
- `backend/alembic/versions/20260714_0007_create_lead_intelligence.py`
- `backend/tests/test_lead_validation.py`
- `docs/API_CONTRACT.md`
- `docs/DATA_MODEL.md`
- `docs/MODULE_BOUNDARIES.md`
- `docs/TESTING_STRATEGY.md`
- `docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification:

- `.venv\Scripts\python.exe -m pytest`
- `.venv\Scripts\python.exe -m compileall app`
- `git diff --check`
- `.venv\Scripts\python.exe -m alembic upgrade head --sql`
- Attempted disposable Docker PostgreSQL smoke with
  `docker run --name ai-b2b-sales-phase5-smoke-postgres ... postgres:16-alpine`,
  but Docker daemon was not running.

Test status:

- Backend test suite passed: 75 tests.
- Python compile check passed.
- `git diff --check` passed with only line-ending warnings.
- Alembic PostgreSQL offline SQL generation passed.
- Added focused Phase 5 tests for valid validation, empty intelligence list,
  archived Campaign rejection, terminal validation blocking, duplicate task
  blocking, failed/cancelled retry, provider failure, invalid URL,
  insufficient content, and same-Campaign canonical duplicate handling.

Known limits:

- This is mock-crawler-only. No real website crawling or paid crawler API is
  integrated.
- No RQ worker runtime is implemented; the mock provider still runs
  synchronously inside the service after returning a task reference.
- Frontend Phase 5 UI is not implemented.
- At the time of that implementation task, real PostgreSQL migration/API smoke
  still needed a live PostgreSQL verification pass because Docker daemon was
  unavailable. The later Phase 5 smoke entry above resolves that verification
  gap.

Next recommended step:

- Run real PostgreSQL migration/API smoke for Phase 5, then prepare Frontend
  Phase 5 design context before implementing any validation/intelligence UI.

## 2026-07-14 - Phase 5 Lead Validation + Intelligence Contract Planning

Type: Documentation-only contract planning before backend implementation.

Completed:

- Formally moved the active planning lane from completed Phase 4 local smoke
  verification into Phase 5 Lead Validation + Intelligence contract planning.
- Documented Phase 5 scope as validation and factual website intelligence from
  existing discovered leads.
- Added the planned Phase 5 endpoints:
  - `POST /api/v1/leads/{lead_id}/validation`
  - `GET /api/v1/leads/{lead_id}/validation/tasks`
  - `GET /api/v1/leads/{lead_id}/intelligence`
  - `GET /api/v1/tasks/{task_id}`
- Documented allowed first-slice validation transitions:
  - `pending -> valid`
  - `pending -> invalid`
  - `pending -> duplicate`
  - `pending -> insufficient_content`
- Clarified that provider/system failures should fail the task and should not
  be recorded as completed validation outcomes.
- Documented `lead_intelligence` as factual website intelligence with source
  traceability, provider name, content quality, crawl status, and evidence.
- Documented that Phase 5 backend implementation must extend `task_runs` for
  `task_type = lead_validation`, `related_entity_type = lead`, and a generic
  website input field; it must not reuse Lead Discovery `search_query` to store
  website URLs.
- Updated module boundaries so the intelligence module owns Phase 5 validation
  and website intelligence while qualification, reviews, contacts, and outreach
  remain separate phases.
- Added Phase 5 testing expectations for mock Crawler Provider behavior,
  validation outcomes, intelligence evidence traceability, and strict
  out-of-scope boundaries.
- Updated frontend planning/UI requirements to keep Frontend Phase 5 pending
  backend implementation and Stitch or user-provided design context.

Files modified:

- `docs/MVP_SCOPE.md`
- `docs/API_CONTRACT.md`
- `docs/DATA_MODEL.md`
- `docs/MODULE_BOUNDARIES.md`
- `docs/WORKFLOW.md`
- `docs/TESTING_STRATEGY.md`
- `docs/UI_REQUIREMENTS.md`
- `docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification:

- `rg -n "Phase 5|lead_validation|lead_intelligence|search_query|Gmail Draft|LinkedIn|Outreach Draft|lead_scores|review_status" docs`
- `git diff --check`

Known limits:

- This was a documentation-only contract planning task.
- No Phase 5 backend models, schemas, repositories, services, routes,
  migrations, or tests were implemented.
- No frontend Phase 5 UI was implemented.
- No automated tests were run because no implementation code changed.
- Real crawler provider integration remains future work and was not authorized
  by this task.

Next recommended step:

- Implement Backend Phase 5 first slice with a mock Crawler Provider, extend
  `task_runs`, add `lead_intelligence`, implement service/repository/routes,
  add focused tests, then run PostgreSQL migration and live API smoke
  verification.

## 2026-07-14 - Frontend Phase 4 Live-Backend Browser Smoke

Type: Local PostgreSQL live-backend browser smoke verification and progress
documentation update.

Completed:

- Started a disposable PostgreSQL 16 container on `localhost:55433` for an
  isolated Phase 4 browser smoke database.
- Ran the Alembic migration chain to head against the smoke database.
- Started a live FastAPI backend on `127.0.0.1:8000`.
- Started the Vite frontend; port `5173` was already occupied, so Vite served
  the app on `127.0.0.1:5174`.
- Seeded the smoke database through live HTTP APIs with:
  - one company,
  - one confirmed manual Product Card,
  - one draft Campaign,
  - one confirmed Campaign,
  - one archived Campaign.
- Opened `/campaigns` in the in-app browser and verified the seeded Campaigns
  rendered from the live backend through the Vite proxy.
- Opened the confirmed Campaign detail view and verified the Lead Discovery
  panel showed the `开始发现线索` entry point.
- Started Lead Discovery from the browser UI.
- Verified the browser UI showed:
  - one completed `mock_search` Lead Discovery task,
  - one task history row,
  - three candidate leads,
  - candidate lead states as discovered, pending validation, and unreviewed,
  - a disabled `已有发现任务` action after the first run.
- Verified duplicate start against the live backend returned HTTP `409` with
  `lead_discovery_already_exists`.
- Opened the draft Campaign detail view and verified no Lead Discovery panel or
  `开始发现线索` action was displayed.
- Opened the archived Campaign detail view and verified no Lead Discovery panel
  or `开始发现线索` action was displayed.
- Updated `docs/FRONTEND_DEVELOPMENT_PLAN.md` and
  `docs/DEVELOPMENT_PROGRESS.md` to mark Frontend Phase 4 live-backend browser
  smoke as passed.

Verification:

- `docker run --name ai-b2b-sales-phase4-browser-smoke-postgres --rm -e POSTGRES_DB=ai_b2b_sales_phase4_browser_smoke -e POSTGRES_USER=phase4_browser_smoke -e POSTGRES_PASSWORD=phase4_browser_smoke_password -p 55433:5432 -d postgres:16-alpine`
- `.venv\Scripts\python.exe -m alembic upgrade head`
- `.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000`
- `npm.cmd --prefix frontend run dev -- --host 127.0.0.1`
- Browser smoke at `http://127.0.0.1:5174/campaigns`
- `curl.exe -s -i -X POST http://127.0.0.1:8000/api/v1/campaigns/8d02da83-d011-4779-aff3-710e7e6c0f9c/lead-discovery -H "Content-Type: application/json" -d "{\"provider\":\"mock_search\"}"`
- `curl.exe -s http://127.0.0.1:8000/api/v1/campaigns/8d02da83-d011-4779-aff3-710e7e6c0f9c/lead-discovery/tasks`
- `curl.exe -s http://127.0.0.1:8000/api/v1/campaigns/8d02da83-d011-4779-aff3-710e7e6c0f9c/leads`

Known limits:

- This is local development proof only, not staging or production proof.
- The smoke used `MockSearchProvider`; it did not verify real search, crawling,
  validation, scoring, review, contacts, outreach, or Gmail Draft behavior.
- No automated tests were added or updated in this task because this was a
  runtime smoke verification and documentation update.
- No RQ worker runtime exists yet; the first backend implementation still
  executes the mock provider synchronously after task creation.
- The smoke used a disposable PostgreSQL database and did not mutate existing
  local development data.

Next recommended step:

- Move to Phase 5 Lead Validation + Intelligence contract planning, or do a
  targeted Phase 4 hardening pass if review finds specific UI or error-state
  polish items.

## 2026-07-14 - Frontend Phase 4 Lead Discovery UI Implementation

Type: Frontend implementation from Stitch design context and verified backend
API contract.

Completed:

- Read the available Stitch Phase 4 Lead Discovery screens for:
  - start entry from a confirmed Campaign,
  - task status and task history,
  - candidate lead results,
  - completed zero-result state,
  - duplicate/conflict and provider-failure states.
- Added `frontend/src/api/leadDiscovery.ts` with typed API methods for the
  verified Phase 4 endpoints:
  - `POST /api/v1/campaigns/{campaign_id}/lead-discovery`
  - `GET /api/v1/tasks/{task_id}`
  - `GET /api/v1/campaigns/{campaign_id}/lead-discovery/tasks`
  - `GET /api/v1/campaigns/{campaign_id}/leads`
- Added `frontend/src/pages/campaigns/LeadDiscoveryPanel.tsx`.
- Mounted the Lead Discovery panel only inside confirmed Campaign detail.
- Implemented start, refresh, polling, task progress/status, task history,
  candidate lead table, result search, zero-result state, duplicate/conflict
  error messaging, provider failure display, and source URL opening.
- Added responsive styles in `frontend/src/styles/global.css` to match the
  Stitch light workbench direction while staying close to the existing
  Product Card / Campaign UI language.
- Kept the UI contract-bound: discovered candidate leads are displayed as
  pending validation and unreviewed; no validation, scoring, review actions,
  contact discovery, outreach, Gmail Draft, real search, or real crawling UI was
  added.
- Updated `docs/FRONTEND_DEVELOPMENT_PLAN.md` and
  `docs/DEVELOPMENT_PROGRESS.md` to reflect the new implementation boundary.

Verification:

- `npm.cmd --prefix frontend run build` passed.
- Searched the new Phase 4 frontend files for unsupported out-of-scope wording
  such as Gmail, outreach, scoring, approval/rejection, email sending, CRM,
  LinkedIn, and Google Sheets. The remaining real-search/crawler words appear
  only in negative boundary copy.
- `git diff --check` passed with only existing CRLF normalization warnings for
  touched frontend files.

Known limitations:

- Live-backend browser smoke was not run for the new UI in this task.
- No frontend test harness exists yet, so no automated frontend tests were
  added.
- No backend logic changed; backend tests were not rerun.
- The first backend implementation still executes `MockSearchProvider`
  synchronously because no RQ worker runtime exists yet.

Next recommended step:

- Run live-backend browser smoke against local PostgreSQL: open a confirmed
  Campaign, start Lead Discovery, verify task status/history, verify candidate
  leads, verify duplicate-task conflict handling, and confirm draft/archived
  Campaigns do not expose a start action.

## 2026-07-13 - Phase 4 PostgreSQL Migration/API Smoke And Frontend Planning Start

Type: Local runtime verification and frontend planning documentation.

Completed:

- Started a disposable PostgreSQL 16 container on `localhost:55432` for an
  isolated Phase 4 smoke database, leaving the existing Docker Compose
  PostgreSQL volume untouched.
- Ran `alembic upgrade head` against the smoke database and reached
  `20260712_0006_create_lead_discovery.py`.
- Ran `alembic upgrade head` a second time to verify idempotent head state.
- Inspected PostgreSQL schema presence for `campaigns`, `product_cards`,
  `task_runs`, and `leads`, including key Phase 4 constraints such as
  `ck_task_runs_task_type`, `ck_task_runs_status`,
  `ck_leads_discovery_status`, `ck_leads_validation_status`,
  `ck_leads_review_status`, and
  `uq_leads_campaign_id_normalized_website`.
- Started a live FastAPI backend on `127.0.0.1:8000` against the smoke
  database.
- Verified `/health` and `/health/db`.
- Created a company, manual Product Card, confirmed Product Card, draft
  Campaign, and confirmed Campaign through live HTTP APIs.
- Verified draft Campaign Lead Discovery rejection with HTTP `409` and
  `campaign_not_confirmed`.
- Verified `POST /api/v1/campaigns/{campaign_id}/lead-discovery` returned HTTP
  `201` with a `pending` task reference.
- Verified `GET /api/v1/tasks/{task_id}` returned `completed`,
  `task_type = lead_discovery`, `provider_name = mock_search`, and a
  `search_query` containing the confirmed Product Card snapshot name.
- Verified `GET /api/v1/campaigns/{campaign_id}/lead-discovery/tasks` returned
  one Lead Discovery task.
- Verified `GET /api/v1/campaigns/{campaign_id}/leads` returned three mock
  candidate leads with `discovery_status = discovered`,
  `validation_status = pending`, `review_status = unreviewed`,
  `provider_name = mock_search`, and matching `search_query`.
- Verified Campaign status remained `confirmed` after discovery.
- Verified duplicate Lead Discovery start returned HTTP `409` with
  `lead_discovery_already_exists`.
- Updated frontend planning and UI requirements to start Frontend Phase 4 from
  the verified task/lead API surfaces only.

Files modified:

- `docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `docs/UI_REQUIREMENTS.md`
- `docs/DEVELOPMENT_PROGRESS.md`
- `docs/DEVELOPMENT_LOG.md`

Verification:

- Local PostgreSQL readiness check against the disposable smoke database passed.
- Alembic migration smoke passed.
- Idempotent second Alembic head check passed.
- PostgreSQL schema inspection passed for the Phase 4 tables and constraints.
- Live FastAPI API smoke passed for the Phase 4 endpoint path.

Known limits:

- The existing Docker Compose `postgres` volume was not used because it was
  initialized with credentials that did not match `.env.example`; this task
  avoided mutating existing local data by using a separate disposable PostgreSQL
  container.
- This is local development proof, not staging or production proof.
- No automated tests were added or updated in this task.
- No Frontend Phase 4 UI was implemented.
- No RQ worker runtime exists yet; the first implementation still executes the
  mock provider synchronously after creating a pending task reference.
- Lead Validation, website intelligence, scoring, human review, contacts,
  outreach, Gmail Draft, real search APIs, and real crawling remain future
  phases.

## 2026-07-12 - Backend Phase 4 Lead Discovery First Implementation

Implemented the first backend Lead Discovery vertical slice.

Completed:

- Added `task_runs` and `leads` ORM models with status/check constraints,
  traceability fields, timestamps, foreign keys, and per-Campaign normalized
  website uniqueness.
- Added Alembic revision `20260712_0006_create_lead_discovery.py`.
- Replaced `tasks` and `discovery` placeholders with repositories, schemas,
  services, and routes.
- Registered the new Discovery and Task routers in `backend/app/main.py`.
- Added `MockSearchProvider` through the Search Provider abstraction.
- Implemented:
  - `POST /api/v1/campaigns/{campaign_id}/lead-discovery`
  - `GET /api/v1/campaigns/{campaign_id}/lead-discovery/tasks`
  - `GET /api/v1/campaigns/{campaign_id}/leads`
  - `GET /api/v1/tasks/{task_id}`
- Enforced confirmed-Campaign-only start, archived/draft rejection, duplicate
  task blocking, retry after failed/cancelled tasks, zero-result completion,
  provider failure recording, Campaign-status separation, and per-Campaign lead
  website de-duplication.
- Added `backend/tests/test_lead_discovery.py` with focused Phase 4 coverage.
- Updated current docs to reflect that the first backend slice was implemented
  and that local PostgreSQL migration / API smoke was still pending at that
  time.

Verification:

- `.venv\Scripts\python.exe -m pytest tests\test_lead_discovery.py -q` passed:
  8 passed, 1 warning.
- `.venv\Scripts\python.exe -m pytest -q` passed: 65 passed, 1 warning.

Known limits:

- The first implementation executes `MockSearchProvider` synchronously after
  returning a pending task reference because no RQ worker runtime exists yet.
- The new Alembic migration was not smoke-verified against local PostgreSQL in
  this task.
- Lead Validation, website intelligence, scoring, human review, contacts,
  outreach, Gmail Draft, real search APIs, and real crawling remain future
  phases.

## 2026-07-12 - Phase 4 Lead Discovery Contract Documentation Pass

Documentation-only alignment before backend implementation.

Completed:

- Clarified Phase 4 as confirmed Campaign -> Lead Discovery task -> mock search
  results -> saved candidate leads.
- Documented that Phase 4 first implementation uses `MockSearchProvider` and
  does not call a real search API or self-build full-web search.
- Documented that real website crawling, website parsing, content sufficiency,
  and evidence extraction are reserved for later Lead Validation / Intelligence
  work.
- Added Lead Discovery API contract details for task creation, task listing,
  lead listing, task lookup, error handling, duplicate-start blocking, retry
  behavior, and zero-result completion.
- Added data model guidance for `task_runs`, saved lead traceability fields,
  required `website` / `source_url`, `search_query`, and per-Campaign normalized
  website de-duplication.
- Added Lead Discovery contract tests covering confirmed-only start, task status
  separation, mock provider behavior, duplicate blocking, retry rules, zero
  results, provider failure, required fields, and non-eligibility for later
  phases.
- Clarified in AI rules that mock provider results are development/test data and
  must not be presented as real external customer evidence.

No backend code, frontend UI, database migration, provider implementation, or
runtime behavior changed in this task.

## Historical Implementation Summary

### Foundation Stabilization

Completed work summarized from the prior progress file:

- Repaired truncated rule documents in `docs/API_CONTRACT.md` and
  `docs/CODING_STANDARDS.md`.
- Added Alembic foundation files and an initial baseline migration.
- Moved database and Redis settings to environment-based configuration.
- Registered the first working business router in `backend/app/main.py`.
- Implemented a minimal `company` vertical slice with model, schemas,
  repository, service, routes, and tests.
- Added `/health/db` and `/health/redis` checks with honest dependency probing.
- Aligned AI, data model, deployment, and planning documents with the current
  repository state.

### Phase 1B And Phase 1 Sources + Knowledge

Completed work summarized from the prior progress file:

- Implemented company-owned text and URL source records with create, list, and
  get APIs.
- Implemented deterministic source-to-knowledge draft creation without crawler
  or LLM dependency.
- Implemented knowledge review transitions for `draft`, `confirmed`, and
  `rejected` knowledge items.
- Added status-filtered company knowledge lists.
- Added the `company_sources` and `knowledge_items` tables through Alembic.
- Added focused API tests for ownership, listing, draft generation, review
  transitions, status separation, invalid IDs, and invalid repeat review.

### Phase 2 Product Card Backend Contract

Completed work summarized from the prior progress file:

- Implemented deterministic Product Card generation from confirmed company
  knowledge only.
- Added Product Card persistence and API behavior for the finalized backend
  contract.
- Limited Product Card statuses to `draft` and `confirmed`.
- Added `source_type` values `ai_generated` and `manual`.
- Kept AI-generated card creation under
  `POST /api/v1/companies/{company_id}/product-cards`.
- Kept manual Product Card creation under `POST /api/v1/product-cards` with a
  required `company_id`.
- Added Product Card list, detail, patch, confirm, and delete behavior.
- Made Product Card confirmation idempotent for already confirmed cards.
- Added a minimal Campaign reference-check boundary for Product Card deletion.
- Added Alembic revision `20260627_0004` for Product Card source type and
  status constraint cleanup.
- Rewrote Product Card API tests for the finalized backend contract.

### Phase 3 Campaign Backend Contract

Completed work summarized from the 2026-07-03 Campaign implementation:

- Added Campaign persistence and API behavior for the minimum Phase 3 backend
  contract.
- Limited Campaign statuses to `draft`, `confirmed`, and `archived`.
- Added create, company-scoped list, get, patch, delete, confirm, archive, and
  duplicate endpoints.
- Enforced confirmed same-company Product Card validation at creation and
  confirmation.
- Captured `product_card_snapshot` at confirmation.
- Made repeated confirm idempotent for already confirmed Campaigns.
- Initially kept archived Campaigns read-only and hidden from the default list
  under the then-current implementation contract. The default-list behavior was
  later superseded by the 2026-07-06 documentation rule update and synchronized
  in backend code and tests on 2026-07-06.
- Added Alembic revision `20260703_0005` for Campaign persistence.
- Added focused Campaign API tests for lifecycle and validation behavior.

### Remaining Product Card / Campaign Hardening Items

Planned or pending work:

- Keep future Campaign UI changes backed by the backend contract and available
  Stitch Campaign design context.
- Extend Product Card route-level scoping when API context supports company or
  future workspace ownership.
- Audit non-Product-Card ORM and Alembic check constraints for consistent
  `ck_<table_name>_<column_name>` naming.
- Run broader deployment or staging PostgreSQL verification during later
  stabilization.
- Clarify the Phase 4 Lead Discovery backend contract before implementing Lead
  Discovery or its frontend UI.

## Dated Task Entries

### 2026-07-09 - Build Verification And Progress Documentation Reconciliation

Type: Documentation and verification cleanup.

Completed:

- Rechecked the current Product Card and Campaign implementation status against
  the active progress docs.
- Reran frontend build verification after a one-time Vite build failure was
  observed during the audit; the final `npm.cmd run build` passed.
- Updated the frontend plan so Frontend Phase 3 Campaign is no longer described
  as the current active phase after Phase 4 became the next contract-planning
  lane.
- Updated this log's current summary and remaining hardening list so it no
  longer says Product Card UI, Campaign live-backend verification, or the local
  migration chain are pending.
- Updated `docs/DEVELOPMENT_PROGRESS.md` with a compact latest task record.

Files modified:

- `docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification:

- `npx.cmd vite build --debug`
- `npm.cmd run build`
- `.venv\Scripts\python.exe -m pytest -q`
- `git diff --check`
- `git status --short --branch`

Known limitations:

- No backend API behavior, frontend workflow behavior, migration, or data model
  changed in this cleanup task.
- No browser smoke test was rerun in this task because the code behavior under
  review had already been smoke-verified and this task only reconciled build
  verification and documentation.
- The smoke evidence remains local development proof, not staging or production
  database proof.

Next recommended step:

- Clarify the Phase 4 Lead Discovery backend contract, data model, business
  rules, validation rules, status boundaries, and provider interfaces before
  implementation.

### 2026-07-07 - Frontend Phase Priority Documentation Alignment

Type: Documentation-only.

Completed:

- Updated the frontend planning document so Frontend Phase 3 Campaign UI is no
  longer described as blocked or unimplemented.
- Marked Frontend Phase 2 Product Card UI as the current next frontend
  implementation priority before Phase 4 Lead Discovery.
- Clarified that Campaign real full-stack verification remains pending and
  useful, but it does not replace the Product Card UI implementation priority.
- Clarified that Phase 4 Lead Discovery should start only after the Product Card
  UI gap is closed and the Phase 4 backend contract, data model, business
  rules, validation rules, and provider boundaries are clarified.
- Kept this task documentation-only.

Files modified:

- `docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `docs/DEVELOPMENT_PROGRESS.md`
- `docs/DEVELOPMENT_LOG.md`

Verification:

- `rg -n "Campaign frontend UI is implemented|current next frontend implementation priority|Frontend Phase 2 Product Card UI|Phase 4 Lead Discovery" docs`
- `rg -n "^### [0-9]{4}-[0-9]{2}-[0-9]{2} -" docs\DEVELOPMENT_PROGRESS.md`
- `git diff --check`
- `git diff --name-only`
- `git status --short --branch`

Known limitations:

- No backend code, frontend code, migrations, package files, or runtime
  configuration were changed.
- Product Card frontend UI is still not implemented.
- Campaign real full-stack browser verification against live backend and
  PostgreSQL data remains pending.
- Phase 4 Lead Discovery remains future work.

Next recommended step:

- Discuss and confirm the Frontend Phase 2 Product Card UI workflow, then
  implement Product Card UI before starting Phase 4 Lead Discovery.

### 2026-07-06 - Campaign Backend Archived List Runtime Sync

Type: Backend behavior and tests.

Completed:

- Removed the Campaign repository default-list filter that excluded archived
  Campaigns when no `status` query parameter was supplied.
- Updated the Campaign list test so the default company Campaign list includes
  both draft and archived Campaigns.
- Verified that `status=archived` and `status=draft` still return
  status-specific lists.
- Updated backend README and progress notes so they no longer describe backend
  archived-list synchronization as pending.
- Kept archived Campaign lifecycle restrictions unchanged.

Files modified:

- `backend/app/modules/campaigns/repository.py`
- `backend/tests/test_campaigns.py`
- `backend/README.md`
- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification:

- `.\.venv\Scripts\python.exe -m pytest tests\test_campaigns.py -q`
- `git diff --check`
- `git status --short`

Known limitations:

- No frontend UI was implemented.
- The migration chain still has not been executed against a live isolated
  PostgreSQL test database in this task.

### 2026-07-06 - Campaign Archived List Visibility Rule Update

Type: Documentation-only.

Completed:

- Updated the Campaign list visibility rule so the default Campaign list /
  `全部` view may include archived Campaigns alongside draft and confirmed
  Campaigns.
- Kept archived Campaigns as read-only history records that cannot be edited,
  deleted, restored, confirmed, or used for new Lead Discovery.
- Kept `status=archived` / `已归档` as an allowed status-specific filter, but no
  longer the only way to view archived Campaigns.
- Updated API, data model, workflow, MVP scope, product, frontend plan, UI, and
  testing rule documents.
- Added explicit follow-up notes that backend implementation and tests still
  needed synchronization from the earlier default-hidden behavior. That
  follow-up was completed later on 2026-07-06.

Files modified:

- `backend/README.md`
- `docs/API_CONTRACT.md`
- `docs/DATA_MODEL.md`
- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`
- `docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `docs/MVP_SCOPE.md`
- `docs/PRODUCT_REQUIREMENTS.md`
- `docs/TESTING_STRATEGY.md`
- `docs/UI_REQUIREMENTS.md`
- `docs/WORKFLOW.md`

Verification:

- `rg -n "default Campaign list|hide archived|hidden from default|explicit archived|status=archived|全部|已归档|归档" docs backend/README.md`
- `git diff --check`
- `git diff --name-only`
- `git status --short`

Known limitations:

- The task was documentation-only.
- Backend repository logic and Campaign tests still implement the earlier
  default-hidden behavior and require a follow-up code/test update. This was
  resolved by the later 2026-07-06 Campaign backend archived list runtime sync.
- No frontend UI was implemented.

### 2026-07-05 - Stitch-Gated Campaign Frontend Documentation Cleanup

Type: Documentation-only.

Completed:

- Updated Campaign frontend planning to state that the Campaign backend minimum
  vertical slice is complete.
- Marked Frontend Phase 3 Campaign UI as blocked until Stitch Campaign design
  context is provided or authorized.
- Documented that Codex must not implement a conservative Campaign UI fallback
  without Stitch Campaign screens or authorized Stitch context.
- Clarified that Campaign-side Product Card same-company validation is
  implemented for Campaign creation and confirmation.
- Clarified that Product Card route-level get, patch, confirm, and delete
  company/workspace authorization remains planned hardening.
- Kept Lead Discovery, Contacts, Outreach, Gmail Draft, backend code, frontend
  code, migrations, package files, and runtime behavior out of scope.

Files modified:

- `docs/API_CONTRACT.md`
- `docs/CODING_STANDARDS.md`
- `docs/DATA_MODEL.md`
- `docs/WORKFLOW.md`
- `docs/SYSTEM_ARCHITECTURE.md`
- `docs/UI_REQUIREMENTS.md`
- `docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `docs/DEVELOPMENT_PROGRESS.md`
- `docs/DEVELOPMENT_LOG.md`

Verification:

- `git diff --check`
- `git diff --name-only`
- `rg -n "Campaign backend and frontend must not be marked complete yet|when available|without waiting for Stitch|Product Card Scope Hardening|Route-level Product Card" docs`
- `rg -n "^### [0-9]{4}-[0-9]{2}-[0-9]{2} -" docs\DEVELOPMENT_PROGRESS.md`

Known limitations:

- No backend tests, frontend tests, migrations, compile checks, package checks,
  or runtime checks were run because this was documentation-only.
- Stitch Campaign screens and Stitch MCP design context still need to be
  provided or authorized before Campaign frontend implementation can begin.
- Product Card route-level company/workspace authorization remains planned
  hardening.

Next recommended step:

- Provide or authorize Stitch Campaign screens for Frontend Phase 3. After that,
  implement only the supported Campaign UI actions from the current backend
  contract, without starting Lead Discovery, Contacts, Outreach, or Gmail Draft
  work.

### 2026-07-03 - Campaign Phase 3 Minimum Backend Vertical Slice

Type: Backend implementation.

Completed:

- Implemented the Campaign Phase 3 minimum backend vertical slice.
- Added the `campaigns` ORM model with documented Campaign fields and
  `ck_campaigns_status`.
- Added Alembic revision `20260703_0005` to create the `campaigns` table,
  foreign keys, indexes, and status check constraint.
- Added Campaign schemas for create, patch, read, list, and delete envelopes.
- Added Campaign repository create, list, get, update, delete, and Product Card
  reference-check behavior.
- Added Campaign service rules for create, edit, delete, confirm, archive, and
  duplicate.
- Registered Campaign routes under `/api/v1`.
- Implemented endpoints:
  - `POST /api/v1/companies/{company_id}/campaigns`
  - `GET /api/v1/companies/{company_id}/campaigns`
  - `GET /api/v1/campaigns/{campaign_id}`
  - `PATCH /api/v1/campaigns/{campaign_id}`
  - `DELETE /api/v1/campaigns/{campaign_id}`
  - `POST /api/v1/campaigns/{campaign_id}/confirm`
  - `POST /api/v1/campaigns/{campaign_id}/archive`
  - `POST /api/v1/campaigns/{campaign_id}/duplicate`
- Enforced Campaign status values as only `draft`, `confirmed`, and
  `archived`.
- Enforced confirmed Product Card validation in the same company on Campaign
  creation and confirmation.
- Saved a Product Card business-field snapshot when confirming a draft Campaign.
- Kept repeated confirm on confirmed Campaigns idempotent.
- Rejected edits and deletes for confirmed and archived Campaigns.
- Rejected archive for non-confirmed Campaigns.
- Hid archived Campaigns from the default company Campaign list and allowed
  explicit `status=archived` listing.
- Added focused Campaign tests for the required lifecycle and validation paths.
- Updated backend and API/progress documentation to stop describing Campaign
  backend as unimplemented.

Files added:

- `backend/alembic/versions/20260703_0005_create_campaigns.py`
- `backend/tests/test_campaigns.py`

Files modified:

- `backend/README.md`
- `backend/app/main.py`
- `backend/app/models.py`
- `backend/app/modules/campaigns/models.py`
- `backend/app/modules/campaigns/repository.py`
- `backend/app/modules/campaigns/routes.py`
- `backend/app/modules/campaigns/schemas.py`
- `backend/app/modules/campaigns/service.py`
- `docs/API_CONTRACT.md`
- `docs/DEVELOPMENT_PROGRESS.md`
- `docs/DEVELOPMENT_LOG.md`

Verification:

- `.\.venv\Scripts\python.exe -m pytest tests\test_campaigns.py -q` passed:
  16 passed.
- `.\.venv\Scripts\python.exe -m pytest tests\test_products.py -q` passed:
  19 passed.
- `.\.venv\Scripts\python.exe -m pytest -q` passed: 57 passed.
- `git diff --check` passed.
- `git status --short` and `git diff --name-only` were used for final handoff
  inspection.

Known limitations:

- No frontend UI, Lead Discovery, Gmail, outreach, contacts, provider calls, or
  background jobs were implemented.
- The migration chain was not executed against a live isolated PostgreSQL test
  database in this task.
- SQLite in-memory tests validated API behavior, but they do not replace
  PostgreSQL migration smoke validation.
- Campaign does not add an `archived_at` column; the current docs define
  archived state through `status = archived` and `updated_at`.

Next recommended step:

- Provide or authorize Stitch Campaign screens before implementing Frontend
  Phase 3 Campaign UI. Codex must not implement a conservative fallback UI
  without Stitch Campaign context.

### 2026-07-02 - Campaign Phase 3 Final Rule Documentation Alignment

Type: Documentation-only.

Completed:

- Synchronized the finalized Campaign Phase 3 rules into the project rule
  documents.
- Documented that Campaign status values are limited to `draft`, `confirmed`,
  and `archived`.
- Documented that `running`, `paused`, `completed`, `failed`, and `cancelled`
  are future LeadDiscoveryJob / CampaignJob / background task execution states,
  not Campaign configuration states.
- Documented draft, confirmed, and archived Campaign lifecycle rules.
- Documented idempotent repeated confirm for already confirmed Campaigns.
- Documented that Campaign creation and confirmation must validate a same-company
  / workspace-scope `confirmed` Product Card.
- Documented that confirming a draft Campaign saves `product_card_snapshot` as
  a historical copy of Product Card business fields used by matching and
  outreach generation.
- Documented duplicate / copy as draft as the reuse path, instead of editing
  confirmed Campaigns or restoring archived Campaigns.
- Documented the then-current rule that archived Campaigns were read-only
  history, hidden from default lists, not restorable, and not usable for new
  Lead Discovery. The default-list visibility portion was superseded by the
  2026-07-06 documentation rule update.
- Added Campaign UI status/action rules and Chinese user-facing text
  requirements.
- Kept Phase 3 Campaign active / in progress and did not mark backend or
  frontend Campaign implementation complete.

Files modified:

- `docs/API_CONTRACT.md`
- `docs/DATA_MODEL.md`
- `docs/WORKFLOW.md`
- `docs/MODULE_BOUNDARIES.md`
- `docs/PRODUCT_REQUIREMENTS.md`
- `docs/MVP_SCOPE.md`
- `docs/AI_RULES.md`
- `docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `docs/UI_REQUIREMENTS.md`
- `docs/TESTING_STRATEGY.md`
- `docs/DEVELOPMENT_PROGRESS.md`
- `docs/DEVELOPMENT_LOG.md`
- `backend/README.md`

Verification:

- `git diff --check`
- `git diff --name-only`
- `rg "running|paused|completed|restore|product_card_snapshot|archived|confirmed|draft" docs`
- `git status --short`

Known limitations:

- No backend business code, frontend business code, migrations, package files,
  or runtime configuration were changed.
- Backend tests, frontend tests, migrations, compile checks, package checks, and
  runtime checks were not run because this was a documentation-only update.
- Campaign implementation remains pending: model, migration, schemas,
  repository, service, routes, and tests still need to be built.

Next recommended step:

- Implement the minimal Campaign backend vertical slice for the final
  `draft` / `confirmed` / `archived` contract, including same-company Product
  Card validation, `product_card_snapshot`, archive, duplicate-as-draft, and
  focused tests.

### 2026-07-02 - Frontend Backend Stitch Workflow Governance Update

Type: Documentation-only.

Completed:

- Updated the frontend/backend workflow rules to state that backend API
  contract, data model, business rules, validation rules, and allowed status
  transitions come first for each phase.
- Reworked `docs/FRONTEND_DEVELOPMENT_PLAN.md` so Human Stitch design tasks and
  Codex frontend implementation tasks are separate sections.
- Documented that the user manually creates UI designs in Stitch.
- Documented that Codex reads Stitch MCP design context when available.
- Documented that Stitch is a visual and interaction reference only, not a
  backend business logic source and not a production runtime dependency.
- Reinforced that Codex must not freely redesign UI unless explicitly requested.
- Reinforced that Codex must not implement or imply frontend features that the
  current backend API contract does not support.
- Reinforced that all user-facing frontend text must be Chinese.
- Kept frontend and backend phases synchronized by phase number.
- Kept the current active phase as Phase 3 Campaign without marking Campaign
  backend or Campaign frontend complete.

Files modified:

- `AGENTS.md`
- `README.md`
- `docs/README.md`
- `docs/WORKFLOW.md`
- `docs/UI_REQUIREMENTS.md`
- `docs/SYSTEM_ARCHITECTURE.md`
- `docs/CODING_STANDARDS.md`
- `docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `docs/DEVELOPMENT_PROGRESS.md`
- `docs/DEVELOPMENT_LOG.md`

Verification:

- `git diff --name-only`
- `git diff --check`
- `git status --short`
- `rg` search for Stitch
- `rg` search for `FRONTEND_DEVELOPMENT_PLAN`
- `rg` search for `UI_REQUIREMENTS`
- `rg` search for Campaign
- `rg` search for rejected and reject
- `rg` search for upload and OCR
- `rg` search for Google Sheets and LinkedIn

Known limitations:

- No backend business code or frontend business code was changed.
- Backend tests, frontend tests, migrations, compile checks, package checks, and
  runtime checks were not run because this was a Markdown-only governance update.
- Campaign remains the current active phase but is not implemented yet.
- Campaign frontend remains in active planning until backend contract alignment
  and Stitch MCP design context are available.

Next recommended step:

- Continue Phase 3 Campaign by implementing the minimal Campaign backend
  vertical slice after confirming API contract, data model, business rules,
  validation rules, and allowed status transitions.

### 2026-06-30 - Unified Phase Tracking And Frontend Plan Documentation

Type: Documentation-only.

Completed:

- Added this detailed development log.
- Added `docs/FRONTEND_DEVELOPMENT_PLAN.md`.
- Converted `docs/DEVELOPMENT_PROGRESS.md` into a unified backend/frontend
  phase tracking table.
- Marked Phase 3 Campaign as the current active phase.
- Documented that Backend Phase 3 and Frontend Phase 3 are synchronized in
  numbering.
- Documented that frontend work may require manual Google Stitch design before
  Codex implementation.
- Added the new docs to project documentation indexes.

Files added:

- `docs/DEVELOPMENT_LOG.md`
- `docs/FRONTEND_DEVELOPMENT_PLAN.md`

Files modified:

- `README.md`
- `docs/README.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification:

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `rg` search for new doc references in `README.md`, `docs/README.md`, and the
  new/updated progress docs.
- `rg` search for rejected legacy wording in the new phase-tracking docs.

Results:

- `git status --short` listed modified tracked docs and the two new untracked
  docs.
- `git diff --name-only` listed the tracked Markdown files changed in this task.
- `git diff --check` passed; Git printed LF-to-CRLF working-copy warnings only.
- New-document reference search found the new docs from the project indexes and
  progress docs.
- Rejected legacy wording search returned no matches in the new phase-tracking
  docs.
- Trailing-whitespace search returned no matches in the new/updated progress
  docs.

Known limitations:

- No backend code, frontend code, tests, migrations, package files, or runtime
  configuration were changed.
- Campaign remains active but not implemented.
- Frontend Phase 3 remains a plan until Stitch context and Codex implementation
  work are provided.

Next recommended step:

- Begin Phase 3 Campaign backend implementation with model, migration, schemas,
  repository, service, routes, and tests.

### 2026-06-29 - Development Progress Retention Cleanup

Type: Documentation-only.

Completed:

- Clarified that `docs/DEVELOPMENT_PROGRESS.md` should keep only recent Codex
  task records.
- Updated project document descriptions to match the retention policy.
- Removed older detailed task records from the progress file while keeping the
  project-stage summary, completed-work summary, long-term plan, known issues,
  and next recommended step.

Files modified:

- `AGENTS.md`
- `README.md`
- `docs/README.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification recorded in the prior progress file:

- `git status --short`
- `rg` search for recent task headings
- `git diff --check`
- `rg` search for retention wording

Known limitations:

- The task was documentation-only.
- Backend tests, frontend tests, migrations, compile checks, package checks, and
  runtime checks were not run.

### 2026-06-29 - Gmail Draft Only Scope Wording Repair

Type: Documentation-only.

Completed:

- Clarified that Gmail Draft creation is not complete email automation.
- Documented minimum draft-creation OAuth scope with `gmail.compose` as the
  example.
- Prohibited send, modify, mailbox read, inbox sync, move, delete, label, reply
  tracking, and reply monitoring permissions or behavior.
- Expanded selected valid email contact wording across project docs.
- Documented that the frontend passes `contact_id`, the backend verifies
  ownership and validity, and `outreach_drafts.contact_id` stores the selected
  contact after validation.

Files modified:

- `AGENTS.md`
- `README.md`
- `docs/AI_RULES.md`
- `docs/API_CONTRACT.md`
- `docs/CODING_STANDARDS.md`
- `docs/DATA_MODEL.md`
- `docs/DEPLOYMENT_GUIDE.md`
- `docs/DEVELOPMENT_PROGRESS.md`
- `docs/MODULE_BOUNDARIES.md`
- `docs/MVP_SCOPE.md`
- `docs/PRODUCT_REQUIREMENTS.md`
- `docs/SYSTEM_ARCHITECTURE.md`
- `docs/TESTING_STRATEGY.md`
- `docs/WORKFLOW.md`

Verification recorded in the prior progress file:

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `rg` searches for Gmail scope, old reply-tracking wording, contact selection,
  and selected valid email contact wording

Known limitations:

- The task was documentation-only.
- No OAuth implementation exists yet.

### 2026-06-29 - Rule Document Self-Check And Progress Catch-Up

Type: Documentation-only.

Completed:

- Verified that rule document entry points exist and remain discoverable.
- Confirmed `README.md` tells Codex to read `docs/DEVELOPMENT_PROGRESS.md`
  before development.
- Confirmed `docs/README.md` indexes `docs/UI_REQUIREMENTS.md` and
  `docs/DEVELOPMENT_PROGRESS.md`.
- Updated the progress file after local rule-document changes.
- Recorded that planned Phase 3 Campaign endpoints and fields were future
  contract boundaries, not current implementation.
- Recorded that AI lead recommendation and human review status are separate.
- Recorded that Gmail Draft eligibility uses a user-selected `contact_id`
  verified by the backend.

Files modified:

- `docs/DEVELOPMENT_PROGRESS.md`

Known limitations:

- The task was documentation-only.
- The self-check verified local repository state only.

## Future Log Rule

When a new Codex task is completed:

1. Update `docs/DEVELOPMENT_PROGRESS.md` with the current phase status and a
   compact latest task record.
2. Add a dated detailed entry to this file when the task has historical value or
   when old task detail would otherwise be removed from the progress tracker.
3. Keep documentation-only work clearly labeled as documentation-only.
4. Do not claim a module is complete unless the implementation has the expected
   models, schemas, repository and service logic, routes, migrations, and tests
   where appropriate.
