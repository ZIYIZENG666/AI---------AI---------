# Development Progress

## Purpose

This file is the current high-level phase tracker for backend and frontend work.

Detailed historical task logs belong in `docs/DEVELOPMENT_LOG.md`. This file
should stay focused on the active phase, phase status, current known limits, and
the latest Codex task record required by `AGENTS.md`.

## Current Active Phase

Phase 3: Campaign is the current active phase.

- Backend Phase 3 = Campaign backend/API/data contract work.
- Frontend Phase 3 = Campaign frontend UI work.
- Frontend Phase 3 and Backend Phase 3 use the same phase number and should be
  tracked together.
- Some frontend Phase 3 work depends on manual Google Stitch UI design before
  Codex implementation.

## Required Status Alignment

- Foundation stabilization: Completed.
- Phase 1B: Completed.
- Phase 1 Sources + Knowledge: Completed.
- Phase 2 Product Card backend contract: Completed.
- Phase 3 Campaign: Active / current active phase.

## Unified Phase Tracking

| Phase number | Backend scope | Backend status | Frontend scope | Frontend status | Notes / current next step |
|---|---|---|---|---|---|
| Foundation stabilization | Project scaffold, environment-driven config, Alembic baseline, health checks, company router, and rule-doc stabilization. | Completed | React + TypeScript + Vite shell and dashboard foundation. | Basic shell present; business workflow UI pending. | Foundation is complete, but this is not a full MVP. |
| Phase 1B | Minimum text/URL source records plus deterministic knowledge draft and review behavior. | Completed | Feeds Frontend Phase 1 company/source/knowledge screens. | Planned. | UI must not imply uploaded documents, crawling, or OCR support. |
| Phase 1: Sources + Knowledge | Source persistence, knowledge drafts, knowledge review transitions, models, schemas, repositories, services, routes, migrations, and tests for the MVP text/URL slice. | Completed | Frontend Phase 1: Company / Source / Knowledge basic UI alignment. | Planned. | Frontend should follow the current text/URL backend contract only. |
| Phase 2: Product Card | Product Card backend contract for AI-generated and manual cards, draft/confirmed lifecycle, edit, confirm, delete, source type, company ownership, and tests. | Completed for backend contract. | Frontend Phase 2: Product Card UI. | Planned / pending. | Product Card frontend must use the finalized backend contract and Chinese user-facing text. |
| Phase 3: Campaign | Campaign model, migration, schemas, repository, service, routes, API contract, lifecycle, confirmed Product Card linkage, and tests. | Active / current phase; not complete. | Frontend Phase 3: Campaign UI synchronized with Backend Phase 3 Campaign. | Active planning; implementation should follow Stitch design context when available. | Next implementation step is the minimal Campaign backend vertical slice. |
| Phase 4: Lead Discovery | Provider-driven candidate lead discovery from confirmed Campaign criteria. | Planned / future. | Lead discovery task/result UI. | Planned / future. | Must use provider boundaries and store traceable source URLs. |
| Phase 5: Lead Validation + Intelligence | Lead normalization, duplicate handling, website availability checks, intelligence capture, evidence storage, and content sufficiency. | Planned / future. | Lead validation and lead intelligence UI states. | Planned / future. | Must not pretend validation or crawling has completed before implementation exists. |
| Phase 6: Lead Scoring | Evidence-based customer-fit scoring, recommendations, risk notes, uncertainty, and provider-mocked tests. | Planned / future. | Lead score, evidence, risk, and recommendation UI. | Planned / future. | AI recommendation remains separate from human review status. |
| Phase 7: Lead Review | User approval, rejection, and manual-review workflow. | Planned / future. | Lead review pages and decision controls. | Planned / future. | AI must not approve leads for the user. |
| Phase 8: Contacts | Contact records, contact type/status, manual LinkedIn reference storage, and selected valid email contact boundary. | Planned / future. | Contact selection and contact validation UI. | Planned / future. | Gmail Draft eligibility requires a selected valid email contact. |
| Phase 9: Outreach Draft + Gmail Draft | Outreach draft records, Gmail Draft provider boundary, duplicate prevention, and draft-only Gmail behavior. | Planned / future. | Outreach draft status and Gmail Draft review UI. | Planned / future. | Gmail behavior must remain draft-only and user-reviewed. |
| Phase 10: Frontend MVP Workflow | Backend phases 1-9 should provide the APIs that the frontend workflow consumes. | Planned / future integration. | End-to-end frontend workflow across company, source, knowledge, product, campaign, lead, contact, and outreach screens. | Planned / future. | Frontend must follow `docs/UI_REQUIREMENTS.md`, `docs/API_CONTRACT.md`, and Stitch design context when available. |
| Phase 11: Background Jobs + Deployment | Background workers, task execution, deployment alignment, and real PostgreSQL migration smoke verification. | Planned / future. | Task progress, runtime health, and deployment-aware frontend states. | Planned / future. | Worker runtime is not implemented yet. |
| Phase 12: MVP Stabilization | Contract gaps, validation, error handling, test coverage, docs accuracy, and production-readiness checks. | Planned / future. | Frontend stabilization, smoke checks, and demo readiness. | Planned / future. | Real PostgreSQL schema validation remains an exit gate. |

## Frontend / Backend Phase Alignment

- Frontend phase numbering follows backend phase numbering where possible.
- Frontend Phase 3 corresponds to Backend Phase 3 Campaign.
- A backend phase being completed does not automatically mean the matching
  frontend phase is implemented.
- Frontend implementation must follow backend API contracts and must not invent
  unsupported backend behavior.
- Stitch is a design reference for layout and visual direction. `AGENTS.md`,
  `docs/API_CONTRACT.md`, `docs/DATA_MODEL.md`, and `docs/UI_REQUIREMENTS.md`
  remain authoritative for project rules and behavior.

## Current Known Limits

- Backend implementation is real through `company`, `sources`, `knowledge`, and
  `products`; most later modules remain placeholders.
- Campaign persistence and Campaign APIs are not implemented yet.
- Product Card frontend UI has not been implemented for the finalized backend
  contract.
- Frontend remains a basic shell and does not yet provide the business workflow
  screens.
- Stitch UI screens and Stitch MCP design context have not yet been provided in
  this repository.
- Source support is limited to text and URL records. Uploaded documents,
  document parsing, OCR, file storage, and crawling are not implemented.
- No real provider implementations exist yet for LLM, search, crawler, Gmail,
  storage, or task queue behavior.
- No RQ worker runtime is implemented yet.
- The migration chain has not been executed against a live isolated PostgreSQL
  test database.
- Route-level Product Card company/workspace authorization remains planned
  hardening; repository/service company-scoped helpers exist but do not
  implement account or workspace authorization.

## Latest Codex Task Records

This section keeps compact records for the latest Codex tasks. Detailed task
history should be moved to `docs/DEVELOPMENT_LOG.md`.

### 2026-06-30 - Unified Phase Tracking and Frontend Plan Documentation

Completed: Documentation-only update to separate detailed historical logging
from high-level phase tracking and to align frontend/backend phase numbering.

What changed:

- Added `docs/DEVELOPMENT_LOG.md` for detailed historical development entries.
- Added `docs/FRONTEND_DEVELOPMENT_PLAN.md` for frontend phase planning and
  backend/frontend phase synchronization.
- Reworked this file into a unified backend/frontend phase tracking table.
- Marked Phase 3 Campaign as the current active phase.
- Added the new documentation files to the project documentation indexes.

Files modified:

- `README.md`
- `docs/README.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Files added:

- `docs/DEVELOPMENT_LOG.md`
- `docs/FRONTEND_DEVELOPMENT_PLAN.md`

Verification commands:

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `rg -n "DEVELOPMENT_LOG|FRONTEND_DEVELOPMENT_PLAN" README.md docs/README.md docs/DEVELOPMENT_PROGRESS.md docs/DEVELOPMENT_LOG.md docs/FRONTEND_DEVELOPMENT_PLAN.md`
- `rg` search for rejected legacy terminology across the new phase-tracking
  docs.

Test status:

- Documentation-only task; backend tests, frontend tests, migrations, compile
  checks, package checks, and runtime checks were not run.
- `git status --short` listed modified tracked docs and the two new untracked
  docs.
- `git diff --name-only` listed the tracked Markdown files changed in this task.
- `git diff --check` passed; Git printed LF-to-CRLF working-copy warnings only.
- New-document reference search found `DEVELOPMENT_LOG` and
  `FRONTEND_DEVELOPMENT_PLAN` references in the project indexes and progress
  docs.
- Rejected legacy wording search returned no matches in the new phase-tracking
  docs.
- Trailing-whitespace search returned no matches in the new/updated progress
  docs.

Known limitations:

- This task does not implement Campaign backend behavior.
- This task does not implement frontend pages.
- This task does not provide Stitch design context.

Next recommended step:

- Begin Phase 3 Campaign as the next backend vertical slice, starting with the
  minimal Campaign model, migration, schemas, repository, service, routes, and
  tests. Campaign must select only confirmed Product Cards from the same
  company.

### 2026-06-29 - Development Progress Retention Cleanup

Completed: Documentation-only cleanup that kept `docs/DEVELOPMENT_PROGRESS.md`
to the latest recent task records and clarified progress-log retention.

Detailed history moved forward through `docs/DEVELOPMENT_LOG.md`.

### 2026-06-29 - Gmail Draft Only Scope Wording Repair

Completed: Documentation-only wording repair for Gmail Draft-only scope and
selected valid email contact eligibility.

Detailed history moved forward through `docs/DEVELOPMENT_LOG.md`.
