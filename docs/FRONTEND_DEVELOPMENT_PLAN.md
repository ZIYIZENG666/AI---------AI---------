# Frontend Development Plan

## Purpose

This document tracks frontend development planning for the AI Sales Knowledge
Base + AI Customer Matching Judgment System.

Frontend phase numbers align with backend phase numbers. Frontend work must be
planned from the current backend API contract, data model, business rules,
validation rules, allowed status transitions, `docs/UI_REQUIREMENTS.md`, and
Stitch MCP design context. Frontend Phase 3 Campaign UI used Stitch Campaign
design context as a required input. Future Campaign UI changes must continue to
use the backend contract and available Stitch Campaign design context.

## Frontend Development Principles

- Frontend phase number should align with backend phase number.
- Frontend implementation must follow backend contract and business rules.
- Frontend must not invent business workflows that are not backed by the current
  backend API contract.
- Stitch design is a visual and interaction reference.
- The user manually creates UI designs in Stitch.
- For Campaign UI, Codex must read Stitch Campaign design context before
  implementation. Without Stitch Campaign screens or authorized Stitch context,
  Codex must not implement a conservative fallback UI. This requirement was
  satisfied for the implemented Frontend Phase 3 Campaign UI.
- Codex must not freely redesign UI unless explicitly requested.
- All user-facing text must be Chinese.
- Unsupported backend features must not be shown or implied in UI.
- Backend implementation does not need to wait for Stitch UI design once the API
  contract, data model, and business rules are clear.
- Campaign frontend implementation required Stitch Campaign design context, and
  future Campaign UI changes still require the same contract-first treatment.
- For Campaign UI, the frontend must use only the backend Campaign statuses
  `draft`, `confirmed`, and `archived`. It must not invent execution statuses or
  action buttons that the API contract does not support.

## Current Frontend Priority

The current frontend verification priority for Product Card and Campaign is
closed for local PostgreSQL live-backend browser smoke.

Phase 4 Lead Discovery backend smoke verification has passed against a clean
local PostgreSQL smoke database and live FastAPI API. Frontend Phase 4 Lead
Discovery UI is implemented from the verified backend API surfaces and the
available Stitch design context, and local PostgreSQL live-backend browser
smoke verification has passed for the confirmed Campaign discovery workflow.
Backend Phase 5 Lead Validation + Intelligence first slice is implemented with
`MockCrawlerProvider`. Frontend Phase 5 Lead Validation + Intelligence UI is
implemented from the corrected Stitch Phase 5 screens and the verified backend
Phase 5 API surfaces. Frontend build verification has passed; local PostgreSQL
live-backend browser smoke remains pending.

Lead Discovery UI is implemented only from the verified backend task and lead
APIs. It does not use frontend-only fake data and must not imply Lead
Validation, website intelligence, scoring, review, contact discovery, Outreach
Draft, Gmail Draft, real search, or real crawling behavior.

Lead Validation + Intelligence UI is implemented only from the verified backend
Phase 5 task and intelligence APIs. It does not use frontend-only fake
intelligence data and must not imply scoring, review, contact discovery,
Outreach Draft, Gmail Draft, real crawler integration, LinkedIn crawling, or CRM
automation.

The completed verification covered:

1. Product Card create, edit, confirm, draft delete, and Campaign-linked 409
   deletion protection against a live FastAPI backend and local PostgreSQL data.
2. Product Card to Campaign flow against the live backend: confirmed Product
   Card selection, Campaign create/confirm, `product_card_snapshot`, and
   `全部` / `草稿` / `已确认` filters.
3. Local workspace reachability through `/campaigns`, `/products`,
   `#campaigns`, and `#products`.
4. Phase 4 migration and API smoke against a disposable local PostgreSQL
   database: `alembic upgrade head`, idempotent second upgrade, schema presence
   for `task_runs` / `leads`, `POST /api/v1/campaigns/{campaign_id}/lead-discovery`,
   `GET /api/v1/tasks/{task_id}`,
   `GET /api/v1/campaigns/{campaign_id}/lead-discovery/tasks`, and
   `GET /api/v1/campaigns/{campaign_id}/leads`.
5. Frontend Phase 4 live-backend browser smoke against local PostgreSQL:
   confirmed Campaign discovery start, completed task state, task history,
   three mock candidate leads, duplicate-task conflict handling, and hidden
   start action for draft / archived Campaign details.
6. Frontend Phase 5 build verification: selected Lead validation UI,
   validation task status/history, factual `lead_intelligence` display, and
   invalid / duplicate / insufficient-content / no-intelligence states compile
   against the current TypeScript contracts.

## Frontend Phase Overview

| Frontend phase | Backend alignment | Human Stitch design | Codex frontend implementation | Status | Notes |
|---|---|---|---|---|---|
| Frontend Foundation | Foundation stabilization | Not required / optional. | React + TypeScript + Vite shell, dashboard layout foundation, API client foundation, loading/error/empty-state patterns. | Basic shell present; business workflow UI pending. | Keep user-facing text Chinese. |
| Frontend Phase 1 | Backend Phase 1 / Phase 1B Sources + Knowledge | Company / Source / Knowledge basic pages. | Implement Company, Source, and Knowledge UI according to current API contract. | Planned / pending alignment. | Must show current text/URL source scope only. Do not imply uploaded documents, OCR, crawling, or file parsing support. |
| Frontend Phase 2 | Backend Phase 2 Product Card | Product Card list, detail, manual creation, editing, confirmation, and deletion UI. | Implemented Product Card UI according to finalized backend contract. | Implemented for the supported Product Card UI lifecycle. | Local PostgreSQL live-backend browser smoke passed, including Campaign-linked 409 UI messaging. |
| Frontend Phase 3 | Backend Phase 3 Campaign; minimum backend vertical slice completed. | Campaign create, draft edit/delete, confirm, archive, duplicate as draft, list/detail, archived filter, and criteria review UI. | Implemented for the supported Campaign lifecycle using the backend Campaign contract and Stitch Campaign visual context. | Implemented for the supported Campaign UI lifecycle. | Local PostgreSQL live-backend browser smoke passed for direct route reachability, create, confirm, and filters. Future Campaign UI changes must remain contract-backed and must not introduce Lead Discovery actions inside the Phase 3 Campaign UI. |
| Frontend Phase 4 | Backend Phase 4 Lead Discovery | Lead discovery task initiation and discovery result UI. | Implemented Lead Discovery UI from verified mock-provider-backed backend APIs and Stitch design context. | Implemented; live-backend browser smoke passed. | Depends on backend task and lead APIs, not frontend-only fake data. Must not imply validation, scoring, contacts, outreach, Gmail, real search, or real crawling. |
| Frontend Phase 5 | Backend Phase 5 Lead Validation + Intelligence | Lead validation, intelligence, evidence, and content sufficiency states. | Implemented inside the confirmed Campaign Lead Discovery workspace from corrected Stitch screens and backend Phase 5 APIs. | Implemented; frontend build passed, live-backend browser smoke pending. | Backend first slice is implemented with mock crawler data; UI shows uncertainty and incomplete data honestly and keeps scoring/review/contacts/outreach/Gmail out of scope. |
| Frontend Phase 6 | Backend Phase 6 Lead Scoring | Lead score, recommendation, matching reasons, risk notes, uncertainty, and evidence UI. | Implement scoring UI after AI scoring contract exists. | Future. | AI recommendation must stay separate from human review status. |
| Frontend Phase 7 | Backend Phase 7 Lead Review | Lead review pages and human decision controls. | Implement user review UI after review API contract exists. | Future. | User review remains required before outreach. |
| Frontend Phase 8 | Backend Phase 8 Contacts | Contact records, contact status, selected valid email contact, and manual reference review UI. | Implement contact selection UI after contact contract exists. | Future. | Manual references cannot be draft recipients. |
| Frontend Phase 9 | Backend Phase 9 Outreach Draft + Gmail Draft | Outreach draft review, Gmail Draft status, and draft-creation controls. | Implement outreach draft UI after draft-only Gmail contract exists. | Future. | User manually reviews and sends from Gmail. |
| Frontend Phase 10 | Backend phases 1-9 integrated | End-to-end MVP workflow review across all implemented screens. | Integrate company, source, knowledge, product, campaign, lead, contact, and outreach screens. | Future. | This is the integrated frontend MVP workflow phase. |
| Frontend Phase 11 | Backend Phase 11 Background Jobs + Deployment | Task status, runtime health, and deployment-aware UI states. | Implement job and runtime status UI after worker runtime exists. | Future. | Worker behavior must match actual backend runtime. |
| Frontend Phase 12 | Backend Phase 12 MVP Stabilization | Usability hardening and demo-readiness checks. | Frontend smoke checks, regression fixes, and demo readiness. | Future. | Stabilization should not expand MVP scope. |

## Human Stitch Design Tasks

The user is responsible for manually creating UI designs in Stitch.

Human design tasks include:

- Creating page layout designs.
- Designing user-facing workflow screens.
- Designing important user actions and confirmation dialogs.
- Designing empty, loading, error, and success states when possible.
- Keeping all user-facing text in Chinese.

Stitch design does not define backend business logic.

Stitch design is used as visual and interaction reference only.

API contract, data model, business rules, validation rules, allowed status
transitions, and project documents remain the source of truth for functionality.

## Codex Frontend Implementation Tasks

Codex is responsible for implementing frontend code.

Codex implementation tasks include:

- Reading project rules.
- Reading current phase API contract.
- Reading current phase data model and business rules.
- Reading validation rules and allowed status transitions.
- Reading `docs/UI_REQUIREMENTS.md`.
- Reading Stitch MCP design context when required by the current frontend phase.
- For new Campaign UI work, stopping before implementation when Stitch Campaign
  design context is unavailable.
- Implementing React frontend pages and components.
- Connecting frontend pages to backend APIs.
- Adding loading, error, empty, and success states.
- Ensuring all user-facing text is Chinese.

Codex must not freely redesign UI unless explicitly instructed.

Codex must not implement unsupported frontend features that are not backed by the
current API contract.

## Phase-by-Phase Frontend Plan

### Frontend Foundation

Backend alignment:

- Foundation stabilization.

Human Stitch design scope:

- Not required for the basic shell.
- Optional visual refinement only if the user provides Stitch design context.

Codex implementation scope:

- Maintain React + TypeScript + Vite shell.
- Maintain dashboard layout foundation.
- Keep API client usage centralized or consistent with the frontend structure.
- Keep loading, error, empty, and success patterns consistent.
- Keep all user-facing text Chinese.

Dependencies:

- Project rules.
- `docs/UI_REQUIREMENTS.md`.
- Existing frontend structure.

Status:

- Basic shell present.
- Business workflow UI pending.

### Frontend Phase 1: Company / Sources / Knowledge

Backend alignment:

- Backend Phase 1 / Phase 1B Sources + Knowledge.

Human Stitch design scope:

- Company profile page.
- Source input page for current text and URL scope.
- Knowledge draft and review page.
- Loading, error, empty, and success states when possible.

Codex implementation scope:

- Implement Company, Source, and Knowledge pages based on the current API
  contract.
- Implement API client integration for current supported fields only.
- Implement form validation that matches backend validation.
- Implement loading, error, empty, and success states.
- Keep all user-facing text Chinese.

Dependencies:

- Company, Source, and Knowledge API contract.
- Current text/URL source data model.
- Knowledge review business rules.
- Stitch MCP design context for user-designed workflow screens.

Status:

- Planned / pending alignment.
- Current backend supports text and URL source records only.

### Frontend Phase 2: Product Card

Backend alignment:

- Backend Phase 2 Product Card.

Human Stitch design scope:

- Product Card list page.
- Product Card detail dialog or page.
- Manual Product Card creation UI.
- Product Card editing UI.
- Product Card confirmation UI.
- Product Card deletion confirmation.

Codex implementation scope:

- Product Card UI is implemented based on the finalized backend contract.
- API client integration exists for list, detail, create, patch, confirm, and
  delete behavior.
- Form validation follows backend validation.
- Status-based UI behavior follows the supported backend contract.
- Loading, error, empty, and success states exist for the implemented UI.
- Keep all user-facing text Chinese.

Dependencies:

- Product Card API contract.
- Product Card data model.
- Product Card business rules.
- Stitch MCP design context for user-designed workflow screens.

Status:

- Implemented for the supported Product Card UI lifecycle.
- Backend contract is complete and the frontend UI is implemented.
- Local PostgreSQL live-backend browser smoke has passed for the supported
  Product Card UI lifecycle and Campaign-linked 409 UI messaging.

### Frontend Phase 3: Campaign

Backend alignment:

- Backend Phase 3 Campaign.
- The minimum Campaign backend vertical slice is completed.

Human Stitch design scope:

- Campaign list page.
- Campaign detail page.
- Campaign creation page.
- Campaign edit page.
- Campaign confirmation flow.
- Campaign archive confirmation.
- Campaign duplicate / copy as draft flow.
- Archived Campaign explicit filter entry.
- Campaign criteria review UI.
- Status-based action visibility for draft, confirmed, and archived Campaigns.

Codex implementation scope:

- Campaign pages were implemented after Stitch Campaign design context was
  provided or authorized.
- Campaign pages are based on the API contract and Stitch visual context.
- API client integration exists for the supported Campaign lifecycle.
- Form validation and status-based UI behavior exist for the supported
  Campaign lifecycle.
- Draft Campaign actions are: edit, delete, and confirm.
- Confirmed Campaign actions are: view details, archive, and duplicate as
  draft.
- The Phase 3 Campaign UI must still not show or wire start / use for Lead
  Discovery. Lead Discovery actions belong to Frontend Phase 4 now that the
  backend Phase 4 APIs are smoke-verified, and still require the appropriate UI
  design context or explicit user authorization before implementation.
- Confirmed Campaigns must not show edit, delete, or return-to-draft actions.
- Archived Campaigns are read-only and must not show edit, delete, restore, or
  start Lead Discovery actions.
- Archived Campaigns may appear in the default Campaign list / `全部` view
  alongside draft and confirmed Campaigns. The UI may also provide an explicit
  archived filter.
- Campaign page titles, form labels, buttons, status labels, empty states,
  errors, success messages, and confirmation dialogs must remain Chinese.
- Loading, error, empty, and success states exist for the implemented Campaign
  UI.

Dependencies:

- Campaign API contract.
- Campaign data model.
- Campaign business rules.
- Campaign validation rules and allowed status transitions.
- Product Card confirmed-only rule and Campaign `product_card_snapshot` rule.
- Stitch Campaign design context. This is required for Campaign frontend
  implementation.

Status:

- Implemented for the supported Campaign UI lifecycle.
- Phase 3 is complete for the supported Campaign lifecycle; Phase 4 Lead
  Discovery backend first implementation has passed local PostgreSQL migration
  and API smoke verification.
- Campaign backend/API/data contract work has a completed minimum backend
  vertical slice.
- Campaign frontend UI is implemented for the current supported lifecycle.
- Local PostgreSQL live-backend browser smoke has passed for direct route
  reachability, Campaign create, confirm, and status filters.

### Frontend Phase 4: Lead Discovery

Backend alignment:

- Backend Phase 4 Lead Discovery.
- Verified API surfaces:
  - `POST /api/v1/campaigns/{campaign_id}/lead-discovery`
  - `GET /api/v1/tasks/{task_id}`
  - `GET /api/v1/campaigns/{campaign_id}/lead-discovery/tasks`
  - `GET /api/v1/campaigns/{campaign_id}/leads`
- Verified business rules:
  - Draft Campaigns return HTTP `409` with `campaign_not_confirmed`.
  - Confirmed Campaigns can create a Lead Discovery task.
  - The create response returns a `pending` task reference.
  - The first implementation executes `MockSearchProvider` immediately and the
    task can then be read as `completed`.
  - Completed Lead Discovery stores candidate leads with `provider_name`,
    `search_query`, `discovery_status = discovered`,
    `validation_status = pending`, and `review_status = unreviewed`.
  - A Campaign with an existing `completed` Lead Discovery task returns HTTP
    `409` with `lead_discovery_already_exists`.
  - Campaign status remains `confirmed`; Lead Discovery status is stored in
    `task_runs`, not `campaigns.status`.

Human Stitch design scope:

- Confirmed Campaign entry point for starting Lead Discovery.
- Lead Discovery task status panel.
- Candidate lead result list.
- Empty state for completed searches with zero leads.
- Error states for draft Campaigns, archived Campaigns, duplicate discovery
  tasks, provider failure, and unavailable backend.
- Clear visual distinction between discovered candidates and later-phase
  validation, scoring, review, contact, outreach, and Gmail Draft flows.

Codex implementation scope:

- Add frontend API client methods for the verified endpoints only.
- Add a Frontend Phase 4 UI entry point only for confirmed Campaigns.
- Hide or disable Lead Discovery start for draft and archived Campaigns
  according to backend rules.
- After starting discovery, show the returned task reference as pending and poll
  or refresh `GET /api/v1/tasks/{task_id}` for the actual task status.
- Show candidate leads from `GET /api/v1/campaigns/{campaign_id}/leads`.
- Label Phase 4 leads as discovered, pending validation, and unreviewed.
- Show duplicate-task conflicts from `lead_discovery_already_exists` as an
  honest Chinese error state instead of creating a new frontend-only run.
- Keep all user-facing text Chinese.

Out of scope for Frontend Phase 4:

- Lead Validation UI.
- Website intelligence or crawling UI.
- AI scoring, recommendations, fit scores, reasons, or evidence UI.
- Lead approval / rejection UI.
- Contacts, selected email contact, Outreach Draft, Gmail Draft, auto-send, or
  CRM sequence UI.
- Real search provider controls or any claim that mock provider results are
  real external evidence.

Dependencies:

- Phase 4 API contract and data model.
- Current Campaign lifecycle and confirmed-only Lead Discovery rule.
- `docs/UI_REQUIREMENTS.md`.
- Stitch / user-provided design context for the Lead Discovery UI was read
  before implementation.

Status:

- Implemented inside confirmed Campaign detail.
- Build verification passed with `npm.cmd --prefix frontend run build`.
- Local PostgreSQL live-backend browser smoke passed for confirmed Campaign
  start, completed task status/history, three mock candidate leads,
  duplicate-task conflict handling, and hidden start action for draft /
  archived Campaign details.

### Frontend Phase 5: Lead Validation + Intelligence

Backend alignment:

- Backend Phase 5 Lead Validation + Intelligence.
- Planned API surfaces:
  - `POST /api/v1/leads/{lead_id}/validation`
  - `GET /api/v1/leads/{lead_id}/validation/tasks`
  - `GET /api/v1/leads/{lead_id}/intelligence`
  - `GET /api/v1/tasks/{task_id}`

Human Stitch design scope:

- Lead validation start and task status states.
- Validation result states: valid, invalid, duplicate, and insufficient
  content.
- Website intelligence summary and evidence display.
- Empty, loading, provider-failure, and no-intelligence states.
- Clear separation from scoring, review, contacts, outreach, and Gmail Draft.

Codex implementation scope:

- Implemented inside the confirmed Campaign Lead Discovery workspace after the
  backend Phase 5 contract and implementation existed.
- Uses backend task and intelligence APIs only; does not use frontend-only fake
  validation data.
- Shows Lead Validation task status from `task_runs`.
- Shows `leads.validation_status` as the business validation result.
- Shows `lead_intelligence` factual fields and evidence traceability when the
  backend returns them.
- Keeps all user-facing text Chinese.
- Corrects Stitch sample-only static values during implementation by binding UI
  display to real backend response fields.

Out of scope for Frontend Phase 5:

- AI fit score, recommendations, matching reasons, or risk notes.
- Human lead approval or rejection controls.
- Contact discovery, selected email contact, Outreach Draft, Gmail Draft,
  email sending, auto-send, follow-up sequence, or CRM pipeline actions.
- Any claim that real crawling or extracted website evidence exists when the
  backend uses a mock provider.

Dependencies:

- Phase 5 API contract and data model.
- Phase 5 validation status transitions.
- `docs/UI_REQUIREMENTS.md`.
- Corrected Stitch screens for Lead Validation + Intelligence UI.

Status:

- Backend first slice is implemented with `MockCrawlerProvider`.
- Frontend implementation is complete for the supported Phase 5 UI slice.
- Frontend build verification passed with `npm.cmd --prefix frontend run build`.
- Local PostgreSQL live-backend browser smoke remains pending.

## Handoff Requirements

After completing frontend work, Codex must report:

- Modified files.
- Implementation summary.
- API contract alignment.
- Stitch design alignment when applicable.
- User-facing Chinese text verification.
- Tests or verification performed.
- Missing dependencies.
- Remaining risks.
- Commit and push status.
