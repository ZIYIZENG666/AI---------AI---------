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

The current frontend implementation order is:

1. Implement Frontend Phase 2 Product Card UI against the finalized backend
   Product Card contract.
2. Then continue to Phase 4 Lead Discovery only after the Product Card UI gap is
   closed and the Phase 4 backend contract, data model, business rules,
   validation rules, and provider boundaries are clarified.

Campaign real full-stack verification with live backend and PostgreSQL data
remains useful, but it does not replace the current implementation priority:
Frontend Phase 2 Product Card UI comes before Phase 4 Lead Discovery.

## Frontend Phase Overview

| Frontend phase | Backend alignment | Human Stitch design | Codex frontend implementation | Status | Notes |
|---|---|---|---|---|---|
| Frontend Foundation | Foundation stabilization | Not required / optional. | React + TypeScript + Vite shell, dashboard layout foundation, API client foundation, loading/error/empty-state patterns. | Basic shell present; business workflow UI pending. | Keep user-facing text Chinese. |
| Frontend Phase 1 | Backend Phase 1 / Phase 1B Sources + Knowledge | Company / Source / Knowledge basic pages. | Implement Company, Source, and Knowledge UI according to current API contract. | Planned / pending alignment. | Must show current text/URL source scope only. Do not imply uploaded documents, OCR, crawling, or file parsing support. |
| Frontend Phase 2 | Backend Phase 2 Product Card | Product Card list, detail, manual creation, editing, confirmation, and deletion UI. | Implement Product Card UI according to finalized backend contract. | Planned / pending UI; current next frontend implementation priority. | Must not show unsupported Product Card statuses or unsupported lifecycle actions. Complete this before Phase 4 Lead Discovery. |
| Frontend Phase 3 | Backend Phase 3 Campaign; minimum backend vertical slice completed. | Campaign create, draft edit/delete, confirm, archive, duplicate as draft, list/detail, archived filter, and criteria review UI. | Implemented for the supported Campaign lifecycle using the backend Campaign contract and Stitch Campaign visual context. | Implemented for the supported Campaign UI lifecycle. | Future Campaign UI changes must remain contract-backed and must not introduce Lead Discovery actions before Phase 4 exists. |
| Frontend Phase 4 | Backend Phase 4 Lead Discovery | Lead discovery task initiation and discovery result UI. | Implement lead discovery UI after provider-backed discovery APIs exist. | Future. | Must depend on provider-backed discovery APIs, not frontend-only fake data. |
| Frontend Phase 5 | Backend Phase 5 Lead Validation + Intelligence | Lead validation, intelligence, evidence, and content sufficiency states. | Implement validation and intelligence UI after backend contract exists. | Future. | Must show uncertainty and incomplete data honestly. |
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

- Implement Product Card UI based on the finalized backend contract.
- Implement API client integration for list, detail, create, patch, confirm, and
  delete behavior.
- Implement form validation that matches backend validation.
- Implement status-based UI behavior supported by the backend contract.
- Implement loading, error, empty, and success states.
- Keep all user-facing text Chinese.

Dependencies:

- Product Card API contract.
- Product Card data model.
- Product Card business rules.
- Stitch MCP design context for user-designed workflow screens.

Status:

- Planned / pending UI.
- Backend contract is complete; frontend UI is not implemented yet.
- Current next frontend implementation priority before Phase 4 Lead Discovery.

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
- The UI must still not show or wire start / use for Lead Discovery until the
  backend Lead Discovery API contract exists. Frontend Phase 3 must not start
  Lead Discovery or imply that unsupported discovery work is available.
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
- Current official active phase.
- Campaign backend/API/data contract work has a completed minimum backend
  vertical slice.
- Campaign frontend UI is implemented for the current supported lifecycle.
- Real full-stack browser verification against live backend and PostgreSQL data
  remains pending.

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
