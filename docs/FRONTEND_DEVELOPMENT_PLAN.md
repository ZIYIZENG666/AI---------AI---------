# Frontend Development Plan

## Purpose

This document defines how frontend development should be planned and tracked for
the AI Sales Knowledge Base + AI Customer Matching Judgment System.

Frontend development must stay aligned with backend phase numbers, backend API
contracts, `docs/UI_REQUIREMENTS.md`, and the project rule documents.

## Phase Numbering Rule

Frontend work follows the same phase numbering as backend work where possible.

- Frontend Phase 1 aligns with the Company / Source / Knowledge backend slice.
- Frontend Phase 2 aligns with Product Card backend behavior.
- Frontend Phase 3 corresponds to Backend Phase 3 Campaign.
- Frontend Phase 3 and Backend Phase 3 should be tracked together in
  `docs/DEVELOPMENT_PROGRESS.md`.
- Later frontend phases should remain planned / future until the matching
  backend behavior exists or is explicitly documented as a frontend-only shell.

## Frontend Work Sources

Frontend work may include two parts:

1. Manual UI design using Google Stitch.
2. Codex implementation based on Stitch-generated design context and the
   project rule documents.

Stitch defines visual direction, layout, spacing, screen composition, and user
experience intent. Stitch does not override backend behavior, data model rules,
API contracts, or MVP scope.

Codex must not freely redesign the UI unless explicitly requested.

## Required Frontend Rules

- Frontend implementation must follow `docs/UI_REQUIREMENTS.md`.
- Frontend API usage must follow `docs/API_CONTRACT.md`.
- Frontend user-facing text must be Chinese.
- Frontend must not invent unsupported backend behavior.
- Frontend must not imply that a workflow is implemented before the backend API
  exists.
- Frontend must keep business rules on the backend unless a rule is strictly
  presentation-only.
- Frontend must not add auto-send email behavior.
- Frontend must not add LinkedIn automation.
- Frontend must not add a Google Sheets-based workflow.
- Frontend must preserve the Gmail Draft-only review model.

## Planned Frontend Phases

| Frontend phase | Backend alignment | Frontend scope | Status | Notes |
|---|---|---|---|---|
| Frontend Foundation | Foundation stabilization | React + TypeScript + Vite shell, dashboard layout foundation, API client foundation, loading/error/empty-state patterns. | Basic shell present; business workflow UI pending. | Keep user-facing text Chinese. |
| Frontend Phase 1 | Backend Phase 1 / Phase 1B Sources + Knowledge | Company / Source / Knowledge basic UI alignment. | Planned. | Must show current text/URL source scope only. Do not imply upload, OCR, crawling, or file parsing support. |
| Frontend Phase 2 | Backend Phase 2 Product Card | Product Card UI for list, details, manual creation, editing, confirmation, and deletion under the finalized backend contract. | Planned / pending. | Must not show unsupported Product Card statuses or unsupported lifecycle actions. |
| Frontend Phase 3 | Backend Phase 3 Campaign | Campaign UI for creating, editing, confirming, archiving, and reviewing campaign criteria after backend contract implementation. | Active planning / synchronized with Backend Phase 3. | Manual Stitch design may come first. Codex implementation should wait for backend contract and Stitch context when available. |
| Frontend Phase 4 | Backend Phase 4 Lead Discovery | Lead discovery task initiation and discovery result UI. | Future. | Must depend on provider-backed discovery APIs, not frontend-only fake data. |
| Frontend Phase 5 | Backend Phase 5 Lead Validation + Intelligence | Lead validation state UI, lead website intelligence, evidence, and content sufficiency displays. | Future. | Must show uncertainty and incomplete data honestly. |
| Frontend Phase 6 | Backend Phase 6 Lead Scoring | Lead score, recommendation, matching reasons, risk notes, uncertainty, and evidence UI. | Future. | AI recommendation must stay separate from human review status. |
| Frontend Phase 7 | Backend Phase 7 Lead Review | Approve, reject, and manual-review lead decision UI. | Future. | User review remains required before outreach. |
| Frontend Phase 8 | Backend Phase 8 Contacts | Contact records, contact status, and selected valid email contact UI. | Future. | LinkedIn references are manual review references only and cannot be draft recipients. |
| Frontend Phase 9 | Backend Phase 9 Outreach Draft + Gmail Draft | Outreach draft review, Gmail Draft status, and draft-creation controls. | Future. | User manually reviews and sends from Gmail. |
| Frontend Phase 10 | Backend phases 1-9 integrated | End-to-end MVP workflow UI across company setup through Gmail Draft review. | Future. | This is the integrated frontend MVP workflow phase. |
| Frontend Phase 11 | Backend Phase 11 Background Jobs + Deployment | Task status, runtime health, and deployment-aware UI states. | Future. | Worker behavior must match actual backend runtime. |
| Frontend Phase 12 | Backend Phase 12 MVP Stabilization | Frontend smoke checks, regression fixes, usability hardening, and demo readiness. | Future. | Stabilization should not expand MVP scope. |

## Phase 3 Alignment

Backend Phase 3 and Frontend Phase 3 both mean Campaign.

Backend Phase 3 should provide:

- Campaign data model and migration.
- Campaign schemas.
- Campaign repository and service logic.
- Campaign routes.
- Tests for lifecycle and confirmed Product Card linkage.

Frontend Phase 3 should provide:

- Campaign creation and edit UI.
- Campaign criteria form.
- Confirm/archive controls when supported by the backend contract.
- Status, error, loading, and empty states.
- Chinese user-facing text.

Frontend Phase 3 must wait for or follow the backend Campaign API contract. It
must not create frontend-only behavior that the backend does not support.

## Stitch To Codex Handoff Rule

When Stitch design context is available:

1. Use Stitch for visual structure and interaction intent.
2. Compare the Stitch design against `docs/API_CONTRACT.md`,
   `docs/DATA_MODEL.md`, `docs/MVP_SCOPE.md`, and `docs/UI_REQUIREMENTS.md`.
3. Implement only behavior supported by the current backend contract.
4. Keep all user-facing text Chinese.
5. Report any mismatch between Stitch and project rules before implementing the
   conflicting behavior.

When Stitch design context is not available:

- Codex may implement only conservative UI aligned with existing project docs
  and API contracts.
- Codex must not invent a new product direction or unsupported workflow.
- Large visual redesign work should wait for explicit user direction or Stitch
  context.

## Current Frontend Status

- The frontend stack is React + TypeScript + Vite.
- The frontend remains a basic shell.
- Business workflow pages are not complete.
- Product Card frontend UI has not yet been implemented for the finalized
  backend contract.
- Campaign frontend UI is aligned to Phase 3 planning and should be implemented
  together with or after the backend Campaign contract.
