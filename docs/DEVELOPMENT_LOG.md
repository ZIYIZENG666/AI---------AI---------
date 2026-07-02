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

This summary is based on the previous contents of
`docs/DEVELOPMENT_PROGRESS.md` before the 2026-06-30 phase-tracking update.

| Area | Status | Summary |
|---|---|---|
| Foundation stabilization | Completed | Project scaffold, environment-driven backend config, Alembic foundation, health checks, company router, and rule-doc stabilization were completed. |
| Phase 1B | Completed | The minimum source and knowledge slice supports text/URL source records and deterministic source-to-knowledge draft creation. |
| Phase 1: Sources + Knowledge | Completed | Source persistence, knowledge draft creation, review transitions, filtering, migrations, routes, services, repositories, schemas, and tests exist for the MVP text/URL slice. |
| Phase 2: Product Card backend contract | Completed | Product Card backend supports AI-generated and manual cards, `draft` and `confirmed` lifecycle, edit, confirm, delete, `source_type`, and tests under the finalized contract. |
| Phase 3: Campaign | Active / current | Campaign is the current active phase but is not implemented yet. The current API contract documents planned endpoints and fields only. |
| Frontend business workflow | Planned / pending | The frontend remains a basic shell. Product Card UI and later business workflow screens are not implemented yet. |

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

### Phase 3 Readiness Items

Planned or pending work summarized from the prior progress file:

- Extend Product Card route-level scoping when API context supports company or
  future workspace ownership.
- Audit non-Product-Card ORM and Alembic check constraints for consistent
  `ck_<table_name>_<column_name>` naming.
- Run the current migration chain against a live isolated PostgreSQL test
  database.
- Begin Campaign backend implementation as the next vertical slice.

## Dated Task Entries

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
