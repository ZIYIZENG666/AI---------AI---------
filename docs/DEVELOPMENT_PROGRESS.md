# Development Progress

## Purpose

This file is the current high-level phase tracker for backend and frontend work.

Detailed historical task logs belong in `docs/DEVELOPMENT_LOG.md`. This file
should stay focused on the active phase, phase status, current known limits, and
the latest Codex task record required by `AGENTS.md`.

## Current Active Phase

Phase 4 Lead Discovery backend contract clarification is the next active lane
after closing the Product Card / Campaign live-backend frontend verification
gap.

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
  PostgreSQL live-backend browser smoke. The next recommended work is to
  clarify the Phase 4 Lead Discovery backend contract before implementation.

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
| Phase 4: Lead Discovery | Provider-driven candidate lead discovery from confirmed Campaign criteria. | Planned / future. | Lead discovery task/result UI. | Planned / future. | Start after the Phase 4 backend contract, data model, business rules, validation rules, and provider boundaries are clarified. |
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
  implemented and locally smoke-verified against the live backend; Phase 4 Lead
  Discovery remains future work until its backend contract is clarified.
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
  `products`, and the minimum `campaigns` vertical slice; most later modules
  remain placeholders.
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
- No RQ worker runtime is implemented yet.
- The migration chain was executed against a local Docker PostgreSQL test
  database on 2026-07-08. Broader deployment/staging PostgreSQL verification
  remains a future stabilization task.
- Campaign-side Product Card same-company validation is implemented for
  Campaign creation and confirmation.
- Route-level Product Card get, patch, confirm, and delete company/workspace
  authorization remains planned hardening; repository/service company-scoped
  helpers exist but do not implement account or workspace authorization.

## Latest Codex Task Records

This section keeps compact records for the latest Codex tasks. Detailed task
history should be moved to `docs/DEVELOPMENT_LOG.md`.

### 2026-07-09 - Build Verification And Progress Documentation Reconciliation

Completed: Rechecked the Product Card / Campaign progress audit findings,
reran frontend/backend verification, and reconciled stale documentation wording.

What changed:

- Reran the frontend build after a one-time Vite build failure was observed
  during the audit; the final full `npm.cmd run build` passed.
- Updated `docs/FRONTEND_DEVELOPMENT_PLAN.md` so Frontend Phase 3 Campaign no
  longer describes itself as the current active phase after Phase 4 became the
  next contract-planning lane.
- Updated `docs/DEVELOPMENT_LOG.md` so the current summary no longer says
  Product Card UI, Campaign live-backend verification, or the local migration
  chain are pending.
- Added this compact progress record and kept only the three latest Codex task
  records in this file.
- Kept the task limited to verification and documentation reconciliation; no
  backend API, schema, data model, business rule, or frontend workflow behavior
  changed.

Files modified:

- `docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `docs/DEVELOPMENT_LOG.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification commands:

- `npx.cmd vite build --debug`
- `npm.cmd run build`
- `.venv\Scripts\python.exe -m pytest -q`
- `git diff --check`
- `git status --short --branch`

Test status:

- Frontend Vite debug build passed.
- Frontend production build passed.
- Backend full test suite passed: 57 passed, 1 warning.
- `git diff --check` passed with LF-to-CRLF working-copy warnings only.

Known limitations:

- No automated frontend test runner was added.
- No browser smoke test was rerun in this task because no frontend workflow
  behavior changed.
- A one-time Vite build failure was observed during the audit but did not
  reproduce after rerunning `npx.cmd vite build --debug` and `npm.cmd run
  build`; if it recurs, investigate the Windows path / Node / Vite combination.
- The local PostgreSQL smoke evidence is still development-environment proof,
  not staging or production database proof.

Commit / push status:

- Not committed.
- Not pushed to GitHub.

Next recommended step:

- Clarify the Phase 4 Lead Discovery backend contract, data model, business
  rules, validation rules, status boundaries, and provider interfaces before
  implementation.

### 2026-07-08 - Product Card and Campaign Workspace Switch Smoke

Completed: Added a local Product Card / Campaign workspace switch entry and
reran the Campaign live-backend browser smoke plus the Product Card 409 UI
screenshot check.

What changed:

- Added a tiny frontend workspace router in `frontend/src/app/App.tsx` so
  `/campaigns`, `/products`, `#campaigns`, and `#products` can render the
  correct local workspace.
- Made hash-based switching override the current path so `/campaigns#products`
  returns to the Product Card workspace and `/campaigns#campaigns` returns to
  Campaign.
- Added a `产品卡片` side-nav entry to the Campaign workspace, matching the
  existing Product Card to Campaign side-nav entry.
- Kept the change limited to local frontend reachability; no backend API,
  schema, data model, or business rule changed.
- Verified Campaign create and confirm through the browser against the live
  FastAPI backend and local PostgreSQL data.
- Verified the linked Product Card delete path returns HTTP 409 behavior in the
  frontend and captured the Chinese UI prompt screenshot.
- Updated this progress tracker and the frontend plan to record the closed
  Product Card / Campaign verification gap.

Files modified:

- `frontend/src/app/App.tsx`
- `frontend/src/pages/campaigns/CampaignWorkspace.tsx`
- `docs/DEVELOPMENT_PROGRESS.md`
- `docs/FRONTEND_DEVELOPMENT_PLAN.md`

Verification commands:

- `npm.cmd run build`
- `Invoke-WebRequest -Uri http://127.0.0.1:8000/health -UseBasicParsing`
- `Invoke-WebRequest -Uri http://127.0.0.1:8000/health/db -UseBasicParsing`
- `Invoke-WebRequest -Uri http://127.0.0.1:8000/health/redis -UseBasicParsing`
- `Invoke-WebRequest -Uri http://127.0.0.1:5173/ -UseBasicParsing`
- In-app Browser check at `http://127.0.0.1:5173/campaigns`.
- In-app Browser Product Card / Campaign switch checks through `#products` and
  `#campaigns`.
- In-app Browser Campaign live-backend smoke: create draft Campaign, confirm
  Campaign, verify status badge/actions, and verify `全部` / `草稿` / `已确认`
  filters.
- In-app Browser Product Card 409 UI check: attempt to delete a confirmed
  Product Card referenced by Campaign and verify
  `已被获客任务使用，无法删除。`.

Test status:

- Frontend build passed.
- Backend health passed: `/health`, `/health/db`, and `/health/redis`.
- Vite dev server responded at `http://127.0.0.1:5173/`.
- Campaign direct route `/campaigns` rendered the Campaign workspace.
- Product Card / Campaign local switching passed in both directions.
- Campaign live-backend browser smoke passed against local PostgreSQL for
  confirmed Product Card selection, draft creation, confirmation, rendered
  confirmed status, and status filters.
- Product Card 409 frontend prompt screenshot was captured at
  `C:\Users\33351\AppData\Local\Temp\ai-b2b-campaign-smoke-20260708\03-product-card-409.png`.
- Browser console error/warning checks returned no app errors or warnings.

Known limitations:

- The browser `domSnapshot()` helper still fails in this environment, so the
  browser proof used the same Browser plugin with page evaluation, DOM click,
  console logs, and screenshots instead of DOM snapshots.
- The smoke data used local PostgreSQL dev data and is not staging or
  production database proof.
- No new automated frontend test runner was added; the frontend currently uses
  build plus browser smoke for this check.

Commit / push status:

- Not committed.
- Not pushed to GitHub.

Next recommended step:

- Clarify the Phase 4 Lead Discovery backend contract, data model, business
  rules, validation rules, status boundaries, and provider interfaces before
  implementing Lead Discovery.

### 2026-07-08 - PostgreSQL Product Card and Campaign Integration Smoke

Completed: Corrected the frontend plan Product Card status and ran a real local
PostgreSQL integration smoke for the implemented Product Card and Campaign
contracts.

What changed:

- Updated `docs/FRONTEND_DEVELOPMENT_PLAN.md` so Frontend Phase 2 Product Card
  UI is no longer marked pending.
- Changed the frontend priority wording to real PostgreSQL integration
  verification before Phase 4 Lead Discovery.
- Started Docker Desktop, PostgreSQL, Redis, local FastAPI, and local Vite for
  a real backend/PostgreSQL smoke run.
- Ran Alembic `upgrade head` against local Docker PostgreSQL.
- Verified `/health`, `/health/db`, and `/health/redis`.
- Created a PostgreSQL-backed smoke company and verified Product Card UI create,
  edit, confirm, and draft delete through the browser.
- Verified Product Card to Campaign backend/API flow: create draft Campaign,
  confirm Campaign, capture `product_card_snapshot`, archive, duplicate as
  draft, and filter `全部` / `草稿` / `已确认` / `已归档` through live API calls.
- Verified Campaign-linked Product Card delete protection returns HTTP 409
  `product_card_in_use`, and confirmed the Product Card frontend maps HTTP 409
  to Chinese delete-blocking copy.

Files modified:

- `docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification commands:

- `Start-Process -FilePath "C:\Program Files\Docker\Docker\Docker Desktop.exe"`
- `docker compose up -d postgres redis`
- `.venv\Scripts\python.exe -m alembic -c alembic.ini upgrade head`
- `.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000`
- `Invoke-WebRequest -Uri http://127.0.0.1:8000/health -UseBasicParsing`
- `Invoke-WebRequest -Uri http://127.0.0.1:8000/health/db -UseBasicParsing`
- `Invoke-WebRequest -Uri http://127.0.0.1:8000/health/redis -UseBasicParsing`
- `npm.cmd run dev -- --host 127.0.0.1 --port 5173`
- Product Card browser smoke through the in-app Browser.
- Campaign integration API calls against `http://127.0.0.1:8000/api/v1`.
- `curl.exe -s -i -X DELETE http://127.0.0.1:8000/api/v1/product-cards/<id>`
- `rg -n "product_card_in_use|已被获客任务使用|无法删除|409|ApiError" frontend\src\pages\products\ProductCardWorkspace.tsx frontend\src\api\productCards.ts backend\app\modules\products\service.py`

Test status:

- Alembic migration chain passed against local Docker PostgreSQL.
- Backend health passed: `/health`, `/health/db`, and `/health/redis`.
- Frontend dev server responded at `http://127.0.0.1:5173/`.
- Product Card browser smoke passed for create, edit, confirm, and draft delete.
- Campaign backend/API integration passed against PostgreSQL with expected
  statuses and `product_card_snapshot`.
- Campaign-linked Product Card delete returned HTTP 409 with
  `product_card_in_use`.
- Final browser confirmation of the 409 delete message was blocked because the
  in-app Browser timed out and reset while reopening/reloading the Product Card
  page.

Known limitations:

- The current app entry renders the Product Card workspace, so Campaign frontend
  live-backend browser verification is still not directly reachable without a
  route, switcher, or temporary test harness.
- The linked Product Card delete 409 frontend message is verified by backend
  response plus frontend error mapping, but not by a final browser screenshot
  because of the Browser reconnect timeout.
- The smoke data used local Docker PostgreSQL with temporary dev credentials;
  it is not staging or production database proof.

Commit / push status:

- Not committed.
- Not pushed to GitHub.

Next recommended step:

- Add or expose a small frontend route/switcher for Campaign workspace
  verification, then rerun the linked Product Card 409 UI check and the Campaign
  frontend live-backend browser smoke before starting Phase 4 Lead Discovery
  contract work.
