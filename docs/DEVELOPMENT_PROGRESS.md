# Development Progress

## Purpose

This file is the current high-level phase tracker for backend and frontend work.

Detailed historical task logs belong in `docs/DEVELOPMENT_LOG.md`. This file
should stay focused on the active phase, phase status, current known limits, and
the latest Codex task record required by `AGENTS.md`.

## Current Active Phase

Frontend Phase 2: Product Card UI gap-filling is the current active
implementation lane before Phase 4 Lead Discovery.

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
- Current verification priority is to run a real backend/PostgreSQL Product
  Card browser smoke check and then verify the Product Card to Campaign flow
  before starting Phase 4 Lead Discovery work.

## Required Status Alignment

- Foundation stabilization: Completed.
- Phase 1B: Completed.
- Phase 1 Sources + Knowledge: Completed.
- Phase 2 Product Card backend contract: Completed.
- Frontend Foundation: Basic shell present; Product Card and Campaign workflow
  UI implemented.
- Frontend Phase 1: Planned / pending UI implementation.
- Frontend Phase 2 Product Card UI: Implemented for the supported Product Card
  lifecycle; real full-stack browser verification remains pending.
- Phase 3 Campaign backend: Minimum backend vertical slice implemented.
- Phase 3 Campaign frontend: Implemented for the supported Campaign UI
  lifecycle.

## Unified Phase Tracking

| Phase number | Backend scope | Backend status | Frontend scope | Frontend status | Notes / current next step |
|---|---|---|---|---|---|
| Foundation stabilization | Project scaffold, environment-driven config, Alembic baseline, health checks, company router, and rule-doc stabilization. | Completed | React + TypeScript + Vite shell and dashboard foundation. | Basic shell present; business workflow UI pending. | Foundation is complete, but this is not a full MVP. |
| Phase 1B | Minimum text/URL source records plus deterministic knowledge draft and review behavior. | Completed | Feeds Frontend Phase 1 company/source/knowledge screens. | Planned. | UI must not imply uploaded documents, crawling, or OCR support. |
| Phase 1: Sources + Knowledge | Source persistence, knowledge drafts, knowledge review transitions, models, schemas, repositories, services, routes, migrations, and tests for the MVP text/URL slice. | Completed | Frontend Phase 1: Company / Source / Knowledge basic UI alignment. | Planned. | Frontend should follow the current text/URL backend contract only. |
| Phase 2: Product Card | Product Card backend contract for AI-generated and manual cards, draft/confirmed lifecycle, edit, confirm, delete, source type, company ownership, and tests. | Completed for backend contract. | Frontend Phase 2: Product Card UI. | Implemented for the supported Product Card UI lifecycle. | Real full-stack browser verification against the live backend and PostgreSQL remains pending. |
| Phase 3: Campaign | Campaign model, migration, schemas, repository, service, routes, API contract, lifecycle, confirmed Product Card linkage, `product_card_snapshot`, duplicate-as-draft behavior, and tests. | Completed for the minimum backend vertical slice. | Frontend Phase 3: Campaign UI synchronized with Backend Phase 3 Campaign. | Implemented for the supported Campaign UI lifecycle. | Real backend runtime integration verification remains pending; Product Card to Campaign integration should be checked before Phase 4. |
| Phase 4: Lead Discovery | Provider-driven candidate lead discovery from confirmed Campaign criteria. | Planned / future. | Lead discovery task/result UI. | Planned / future. | Start only after Product Card UI is verified in a real full-stack smoke check and Phase 4 backend contract, data model, business rules, validation rules, and provider boundaries are clarified. |
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
- Frontend Phase 2 Product Card UI is implemented; Phase 4 Lead Discovery
  remains future work until Product Card real full-stack verification and the
  Phase 4 backend contract are clarified.
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
- Product Card real full-stack browser verification against the live backend and
  PostgreSQL data remains pending.
- Campaign frontend UI is implemented for the Phase 3 supported lifecycle:
  list/filter, create draft, edit draft, delete draft, confirm, duplicate
  confirmed Campaign as draft, archive confirmed Campaign, and read-only
  archived Campaign detail.
- The Campaign frontend was browser-checked with a temporary local mock API.
  A real full-stack browser smoke test against the live backend and PostgreSQL
  data remains pending.
- Source support is limited to text and URL records. Uploaded documents,
  document parsing, OCR, file storage, and crawling are not implemented.
- No real provider implementations exist yet for LLM, search, crawler, Gmail,
  storage, or task queue behavior.
- No RQ worker runtime is implemented yet.
- The migration chain has not been executed against a live isolated PostgreSQL
  test database.
- Campaign-side Product Card same-company validation is implemented for
  Campaign creation and confirmation.
- Route-level Product Card get, patch, confirm, and delete company/workspace
  authorization remains planned hardening; repository/service company-scoped
  helpers exist but do not implement account or workspace authorization.

## Latest Codex Task Records

This section keeps compact records for the latest Codex tasks. Detailed task
history should be moved to `docs/DEVELOPMENT_LOG.md`.

### 2026-07-07 - Frontend Phase 2 Product Card UI Implementation

Completed: Implemented the Frontend Phase 2 Product Card UI against the
finalized Product Card backend contract and the Stitch Product Card visual
reference.

What changed:

- Added a Product Card API client for company lists, company-scoped Product Card
  lists, manual Product Card creation, AI generation from confirmed knowledge,
  edit, confirm, and delete.
- Added a Product Card workspace with sidebar navigation, summary metrics,
  company selector, status filter, Product Card table, detail/edit dialog, and
  confirmation/delete modals.
- Implemented Product Card lifecycle actions aligned to the backend contract:
  draft cards can be edited, confirmed, or deleted; confirmed cards can be
  edited or deleted, with backend 409 handling when already used by Campaigns.
- Kept Product Card user-facing text Chinese-only and limited statuses to
  `待确认` and `已确认`.
- Replaced the frontend shell entry view with the Product Card workspace for
  this phase.
- Updated frontend styles to support the Product Card layout, table, form, and
  modal structure while reusing the existing dashboard visual language.
- Updated this progress tracker to mark Frontend Phase 2 Product Card UI as
  implemented and to keep real full-stack smoke verification as pending.

Files modified:

- `frontend/src/api/productCards.ts`
- `frontend/src/pages/products/ProductCardWorkspace.tsx`
- `frontend/src/app/App.tsx`
- `frontend/src/styles/global.css`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification commands:

- `npm.cmd run build`
- `rg -n "Product Card|Frontend Phase 2|reject|rejected|拒绝|已拒绝|待业务审核|确认生效|新建产品卡片" frontend\src\pages\products frontend\src\api\productCards.ts`
- `rg -n "待确认|已确认|手动添加产品|确认产品卡片|保存修改|取消|已被获客任务使用" frontend\src\pages\products\ProductCardWorkspace.tsx`
- `Invoke-WebRequest -Uri http://127.0.0.1:8000/health -UseBasicParsing`
- `git diff --check`
- `git status --short`

Test status:

- Frontend build passed.
- Product Card UI text scan found no disallowed `reject` / `rejected` /
  `拒绝` / `已拒绝` Product Card wording, no `Product Card` visible English
  copy, and no `Frontend Phase 2` visible English copy in the Product Card
  implementation files.
- Required Product Card Chinese UI terms were present in the Product Card
  workspace.
- No automated frontend tests were added because this frontend currently only
  defines the Vite build script and no UI test runner.
- Backend health check failed because no backend server was reachable at
  `http://127.0.0.1:8000/health` during this task.
- In-app browser verification was attempted, but the Browser MCP DOM snapshot
  call failed and a follow-up evaluation timed out; live UI behavior still needs
  a browser smoke check after the backend is running.

Known limitations:

- Real full-stack Product Card browser verification against the live backend and
  PostgreSQL data remains pending.
- Product Card to Campaign integrated workflow verification remains pending.
- Frontend Phase 1 company/source/knowledge screens remain planned.

Commit / push status:

- Not committed.
- Not pushed to GitHub.

Next recommended step:

- Start the FastAPI backend with PostgreSQL data, run a Product Card browser
  smoke check for create/edit/confirm/delete, then verify the Product Card to
  Campaign flow before starting Phase 4 Lead Discovery.

### 2026-07-07 - Frontend Phase Priority Documentation Alignment

Completed: Documentation-only alignment of frontend phase status and next-step
priority.

What changed:

- Updated the frontend plan so Frontend Phase 3 Campaign UI is no longer marked
  blocked or unimplemented.
- Marked Frontend Phase 2 Product Card UI as the current next frontend
  implementation priority before Phase 4 Lead Discovery.
- Clarified that Campaign real full-stack verification remains useful and
  pending, but it does not replace the Product Card UI implementation priority.
- Clarified that Phase 4 Lead Discovery should start only after the Product Card
  UI gap is closed and the Phase 4 backend contract, data model, business
  rules, validation rules, and provider boundaries are clarified.
- Kept this task documentation-only; no backend code, frontend code, migrations,
  package files, or runtime configuration were changed.

Files modified:

- `docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `docs/DEVELOPMENT_PROGRESS.md`
- `docs/DEVELOPMENT_LOG.md`

Verification commands:

- `rg -n "Campaign frontend UI is implemented|current next frontend implementation priority|Frontend Phase 2 Product Card UI|Phase 4 Lead Discovery" docs`
- `rg -n "^### [0-9]{4}-[0-9]{2}-[0-9]{2} -" docs\DEVELOPMENT_PROGRESS.md`
- `git diff --check`
- `git diff --name-only`
- `git status --short --branch`

Test status:

- Documentation-only task; backend tests, frontend tests, migrations, compile
  checks, package checks, and runtime checks were not run.

Known limitations:

- At the time of this documentation-only task, Product Card frontend UI had not
  yet been implemented.
- Campaign real full-stack browser verification against live backend and
  PostgreSQL data remains pending.
- Phase 4 Lead Discovery remains future work.

Commit / push status:

- Not committed.
- Not pushed to GitHub.

Next recommended step:

- At the time of this documentation-only task, the recommended next step was to
  discuss and implement the Frontend Phase 2 Product Card UI before starting
  Phase 4 Lead Discovery. This is superseded by the Product Card UI
  implementation record above.

### 2026-07-06 - Frontend Phase 3 Campaign UI Implementation

Completed: Implemented the Frontend Phase 3 Campaign UI against the current
Campaign backend contract and Stitch Campaign visual reference.

What changed:

- Added a Campaign API client for company Campaign lists, confirmed Product Card
  selection, draft creation/update/delete, confirm, archive, and duplicate as
  draft.
- Replaced the frontend shell body with a Campaign workspace that supports
  `全部` / `草稿` / `已确认` / `已归档` filtering.
- Implemented status-based actions aligned to the backend contract:
  draft Campaigns can be edited, confirmed, or deleted; confirmed Campaigns can
  be duplicated as draft or archived; archived Campaigns are read-only.
- Added Chinese-only user-facing text for buttons, labels, empty states, error
  states, confirmation dialogs, and lifecycle hints.
- Added a Vite `/api` proxy to the FastAPI backend at `http://127.0.0.1:8000`.
- Kept Lead Discovery, Contacts, Outreach, Gmail Draft, execution queues,
  automatic sending, LinkedIn API, and Google Sheets out of the Campaign UI.
- Updated this progress tracker to reflect that Campaign frontend UI is no
  longer blocked by missing Stitch context.

Files modified:

- `frontend/src/api/campaigns.ts`
- `frontend/src/pages/campaigns/CampaignWorkspace.tsx`
- `frontend/src/app/App.tsx`
- `frontend/src/styles/global.css`
- `frontend/vite.config.ts`
- `frontend/package-lock.json`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification commands:

- `npm.cmd install`
- `npm.cmd run build`
- `.\.venv\Scripts\python.exe -m pytest tests\test_campaigns.py -q`
- `rg -n "United States|California|cloud cost optimization|B2B 企业客户|CTO、运营|官网展示 B2B SaaS 产品|Lead Discovery|执行队列|运行中|Gmail|发送|退回|启动|LinkedIn|Google Sheets" frontend/src`
- Browser UI check at `http://127.0.0.1:5173/` with a temporary local mock API
  for Campaign and Product Card responses.
- Desktop and mobile viewport checks through the in-app browser.

Test status:

- Frontend build passed.
- Campaign backend tests passed: 16 passed.
- Browser interaction checks passed for list filtering, create draft, confirm,
  duplicate as draft, archive, archived read-only detail, and archived list
  actions.
- Browser console error/warning check returned no errors or warnings during the
  mock-backed UI verification.

Known limitations:

- Real full-stack browser verification against a live backend server and live
  PostgreSQL data remains pending.
- At the time of this Campaign task, Product Card frontend UI had not yet been
  implemented; Campaign creation depended on existing confirmed Product Card
  data from the backend.
- `npm.cmd install` reported npm audit vulnerabilities: 1 moderate and 1 high.
  No forced dependency update was applied in this task.
- Lead Discovery and later phases remain out of scope.

Commit / push status:

- Later committed and pushed to `origin/main` as commit
  `452262f campaign前端已完成`.

Next recommended step:

- At the time of this Campaign task, the recommended next step was to implement
  Frontend Phase 2 Product Card UI before continuing to Phase 4 Lead Discovery.
  Campaign real full-stack verification remains pending and should be included
  in a later integration check.
