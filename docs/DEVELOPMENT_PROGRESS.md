# Development Progress

## Current Project Stage

Foundation stabilization and Phase 1B are complete. The finalized Phase 2
Product Card backend contract is now implemented for the modular monolith
backend.

Project rule documents and progress-log retention rules have also been refreshed
through local documentation work on 2026-06-29. Those rule updates clarify Phase
3 Campaign planning, Product Card AI output mapping, lead recommendation versus
human review status, selected-contact Gmail Draft eligibility, Gmail Draft-only
OAuth / mailbox-access boundaries, and retention of only the three most recent
Codex task records.

The repository is no longer only a pure skeleton, but it is still far from a
full MVP. The honest implemented backend slices are now `company`, `sources`,
`knowledge`, and `products`. Most other backend modules remain placeholders.

## Completed Work

- Fixed truncated rule documents in `docs/API_CONTRACT.md` and `docs/CODING_STANDARDS.md`.
- Added a real Alembic foundation with `alembic.ini`, `env.py`,
  `script.py.mako`, `versions/`, and an initial baseline migration.
- Reworked backend configuration to load database and Redis settings from
  environment variables instead of hardcoding connection secrets in Python code.
- Registered the first working business router in `backend/app/main.py`.
- Implemented a minimal `company` vertical slice with ORM model, schemas, repository, service, routes, and tests.
- Added `/health/db` and `/health/redis` checks with honest dependency probing.
- Aligned `AI_RULES.md`, `DATA_MODEL.md`, and `DEPLOYMENT_GUIDE.md` terminology with the current repository state.
- Updated the core planning and rule documents to add a phased long-term MVP plan and explicit LinkedIn boundaries.
- Implemented company-owned text and URL source records with create, list, and get APIs.
- Implemented deterministic source-to-knowledge draft creation without a crawler or LLM dependency.
- Implemented knowledge review transitions for `draft`, `confirmed`, and `rejected`, including status-filtered company lists.
- Added the `company_sources` and `knowledge_items` tables through a new Alembic migration.
- Added focused API tests for source ownership, source listing, draft
  generation, review transitions, status separation, invalid IDs, and invalid
  repeat review.
- Implemented deterministic Product Card generation from confirmed company knowledge only.
- Initially added a legacy Product Card API that included reject/rejected
  behavior; that lifecycle has since been removed by the finalized Phase 2
  contract and must not be treated as current behavior.
- Added the `product_cards` table through Alembic revision `20260623_0003`.
- Added Product Card API tests covering confirmed-knowledge eligibility,
  exclusion of draft/rejected knowledge from AI-generated cards, company
  isolation, reads, transitions, and error responses.
- Documented the Product Card company/workspace scope plan, ORM/migration
  constraint naming standard, and required PostgreSQL migration smoke-test
  boundary.
- Finalized Product Card Phase 2 questions 3 and 5 across the project rule
  documents without changing backend, frontend, migrations, or tests.
- Formalized the Stitch-to-Codex frontend workflow, Chinese user-facing text
  requirement, dashboard page expectations, and UI design handoff rules in
  project documentation only.
- Implemented the finalized Product Card Phase 2 backend contract:
  - Product Card statuses are limited to `draft` and `confirmed`.
  - Product Card `reject` / `rejected` behavior was removed from the API and schemas.
  - Added `source_type` with `ai_generated` and `manual`.
  - AI-generated Product Cards still use
    `POST /api/v1/companies/{company_id}/product-cards`, use confirmed
    knowledge only, store exact confirmed knowledge IDs, and start as `draft`.
  - Manual Product Card creation is available through
    `POST /api/v1/product-cards`, requires `company_id`, starts as `draft`, uses
    `source_type = manual`, and defaults `source_knowledge_item_ids` to an empty
    list.
  - Added `GET /api/v1/product-cards`,
    `PATCH /api/v1/product-cards/{product_card_id}`, and
    `DELETE /api/v1/product-cards/{product_card_id}`.
  - Product Card confirmation is idempotent for already confirmed cards.
  - Product Card deletion physically removes draft cards and confirmed cards when the Campaign reference boundary reports no references.
  - Product Card repository/service methods now include company-scoped lookup
    helpers for future use without claiming workspace authorization.
- Added a minimal Campaign repository reference-check boundary used by the
  Product service; this does not implement the Campaign module.
- Added Alembic revision `20260627_0004` to add `source_type`, remove legacy
  `rejected` Product Cards, replace the status check constraint with
  `ck_product_cards_status`, and add `ck_product_cards_source_type`.
- Rewrote Product Card API tests for the finalized backend contract.
- Set `docs/DEVELOPMENT_PROGRESS.md` task-record retention to the three most
  recent Codex development tasks.

## Recent Task Records

This section keeps only the three most recent Codex development task records.
When a new task record is added, remove older task records beyond the latest
three while keeping the project-stage summary, completed-work summary, long-term
plan, current known issues, and next recommended step up to date.

### 2026-06-29 - Development Progress Retention Cleanup

Completed: Documentation-only cleanup to keep this progress log to the latest
three Codex task records.

What changed:

- Added project rule wording that `docs/DEVELOPMENT_PROGRESS.md` should retain
  only the three most recent Codex task records.
- Updated `README.md` and `docs/README.md` descriptions to match the
  three-record retention policy.
- Removed older task records beyond the latest three from this file.
- Kept the current project stage, completed-work summary, long-term development
  plan, known issues, and next recommended step sections.

Files modified:

- `AGENTS.md`
- `README.md`
- `docs/README.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification commands:

- `git status --short`
- `rg -n "^### [0-9]{4}-[0-9]{2}-[0-9]{2} -" docs/DEVELOPMENT_PROGRESS.md`
- `git diff --check`
- `rg -n "three most recent|latest three|three task records" AGENTS.md README.md docs/README.md docs/DEVELOPMENT_PROGRESS.md`

Test status:

- Documentation-only task; backend tests, frontend tests, migrations, compile
  checks, package checks, and runtime checks were not run.
- Task-record heading search confirmed `docs/DEVELOPMENT_PROGRESS.md` keeps
  exactly three recent task records after this update.
- Retention wording search confirmed the three-record rule appears in
  `AGENTS.md`, `README.md`, `docs/README.md`, and this file.
- `git diff --check` passed with no whitespace errors.

Known limitations:

- This task intentionally removes older task-level detail from
  `docs/DEVELOPMENT_PROGRESS.md`; Git history remains the source for older
  detailed records.
- This task did not change backend code, frontend code, tests, migrations,
  package files, runtime configuration, or API behavior.

Next recommended step:

- Commit this documentation-only retention cleanup if accepted.
- After the cleanup is committed, begin `Phase 3: Campaign Module` as the next
  backend vertical slice.

### 2026-06-29 - Gmail Draft Only Scope Wording Repair

Completed: Documentation-only wording repair for Gmail Draft-only scope and
selected valid email contact eligibility.

What changed:

- Clarified that Gmail Draft creation is not full email automation and not a
  complete Gmail integration.
- Added explicit minimum OAuth scope wording with `gmail.compose` as the example
  draft-creation permission.
- Explicitly prohibited `gmail.send`, `gmail.modify`, full Gmail access,
  mailbox read, inbox sync, move, delete, label, reply tracking, and reply
  monitoring permissions or behavior.
- Replaced ambiguous reply-tracking out-of-scope wording such as "advanced" or
  "complex" reply tracking with broader out-of-scope wording.
- Expanded selected valid email contact wording in product, workflow, module
  boundary, and testing docs:
  - the frontend passes `contact_id`;
  - the backend verifies that `contact_id` belongs to the approved lead;
  - `outreach_drafts.contact_id` stores the selected contact after validation.
- Kept all changes documentation-only. No backend code, frontend code, tests,
  migrations, dependencies, or runtime configuration were changed.

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

Verification commands:

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `rg -n "gmail\.compose|gmail\.send|gmail\.modify|mailbox read|inbox sync|reply tracking|reply monitoring|full Gmail access|complete Gmail integration|email automation" AGENTS.md README.md docs`
- `rg` search for the old ambiguous reply-tracking out-of-scope wording in
  `README.md` and `docs`.
- `rg -n "contact_id|outreach_drafts\.contact_id|selected valid email contact|lead-level public email|public_email" docs/AI_RULES.md docs/API_CONTRACT.md docs/DATA_MODEL.md docs/MODULE_BOUNDARIES.md docs/PRODUCT_REQUIREMENTS.md docs/TESTING_STRATEGY.md docs/WORKFLOW.md docs/DEVELOPMENT_PROGRESS.md`

Test status:

- Documentation-only task; backend tests, frontend tests, migrations, compile
  checks, and package checks were not run.
- `git diff --name-only` confirmed that only Markdown documentation files were
  changed.
- `git diff --check` passed with no whitespace errors.
- Gmail scope search confirmed `gmail.compose` is now documented as the example
  minimum draft-creation scope, while `gmail.send` and `gmail.modify` appear
  only in prohibition wording.
- Reply-tracking search confirmed the old ambiguous reply-tracking wording is no
  longer present.
- Eligibility search confirmed `contact_id`, backend ownership verification,
  `outreach_drafts.contact_id`, selected valid email contact wording, and
  denial-only lead-level email wording remain documented.

Known limitations:

- This task did not change implementation behavior.
- No OAuth implementation exists yet; this task only tightened project rules for
  later Gmail Draft provider work.

Next recommended step:

- Commit this documentation-only wording repair if accepted.
- After that, begin `Phase 3: Campaign Module` as the next backend vertical
  slice.

### 2026-06-29 - Rule Document Self-Check and Progress Catch-Up

Completed: Project rule document self-check and progress-log catch-up.

What changed:

- Verified that the rule document entry points exist and remain discoverable
  from `README.md`, `docs/README.md`, and `AGENTS.md`.
- Confirmed that `README.md` tells Codex to read
  `docs/DEVELOPMENT_PROGRESS.md` before development.
- Confirmed that `docs/README.md` indexes `docs/UI_REQUIREMENTS.md` and
  `docs/DEVELOPMENT_PROGRESS.md`.
- Found that the latest local HEAD commit dated 2026-06-29 updated
  `docs/AI_RULES.md`, `docs/API_CONTRACT.md`, and `docs/DATA_MODEL.md`, but did
  not update `docs/DEVELOPMENT_PROGRESS.md`.
- Updated this progress log so it reflects the latest rule-document state.
- Recorded the latest rule-document clarifications:
  - Product Card AI output mapping is not the same as database persistence.
  - Manual Product Cards must include `company_id`; Product Cards must not exist
    without a company.
  - Planned Phase 3 Campaign endpoints and fields are documented as future
    contract boundaries, not current implementation.
  - AI lead recommendation and human `review_status` are separate concepts.
  - Gmail Draft eligibility uses a user-selected `contact_id` verified by the
    backend; it must not add or rely on a `contacts.selected` boolean.

Files modified:

- `docs/DEVELOPMENT_PROGRESS.md`

Rule documents checked:

- `AGENTS.md`
- `README.md`
- `docs/README.md`
- `docs/AI_RULES.md`
- `docs/API_CONTRACT.md`
- `docs/DATA_MODEL.md`
- `docs/DEVELOPMENT_PROGRESS.md`

Verification commands:

- `git status --short`
- `git log -5 --date=short --pretty=format:"%h %ad %s"`
- `git show --stat --name-only --pretty=format:"commit %H%nDate: %ad%nSubject: %s" --date=iso-strict HEAD`
- `git show --unified=2 -- docs/AI_RULES.md docs/API_CONTRACT.md docs/DATA_MODEL.md`
- `rg -n -C 4 "DEVELOPMENT_PROGRESS|UI_REQUIREMENTS|Document Reading Order|Project Documents|Codex" README.md docs\README.md`
- `rg -n "public[_]email|public[ ]email|Public[ ]email|selected valid email|lead-level email|email-like" -g "*.md" .`
- `rg -n "LinkedIn API|LinkedIn|Google Sheets|LangGraph|multi-agent|auto-send|automatic email|Gmail send|Gmail modify|browser automation|profile extraction|contact downloading" AGENTS.md README.md docs`
- `rg` search for common malformed `DEVELOPMENT_PROGRESS` references in
  Markdown files.

Test status:

- Documentation-only self-check and progress update; backend tests, frontend
  tests, migrations, compile checks, and package checks were not run.
- Git history confirmed latest local HEAD is commit
  `6b0d2e518336a5143960c48a252be1671d789ebf` from 2026-06-29 with subject
  `规则文档更新`.
- Latest local HEAD changed only `docs/AI_RULES.md`, `docs/API_CONTRACT.md`,
  and `docs/DATA_MODEL.md`.
- Before this progress catch-up, `docs/DEVELOPMENT_PROGRESS.md` still listed
  the latest current task as 2026-06-27.
- Rule-entry search confirmed `docs/DEVELOPMENT_PROGRESS.md` is referenced from
  both `README.md` and `docs/README.md`.
- Email eligibility search confirmed remaining lead-level public-email wording
  is denial wording, while selected valid email contact wording is present.
- LinkedIn / Google Sheets / Gmail send boundary search confirmed the
  prohibition language is still present across the main rule documents.
- Typo search found no malformed `DEVELOPMENT_PROGRESS` references in Markdown
  files.

Known limitations:

- This task did not change backend code, frontend code, tests, migrations,
  package files, runtime configuration, or API behavior.
- This self-check verified local repository state only; it did not prove whether
  the latest commit has been pushed to GitHub.
- The progress catch-up is a local working-tree change until it is committed and
  pushed.

Next recommended step:

- Commit this `docs/DEVELOPMENT_PROGRESS.md` catch-up if the self-check result is
  accepted.
- After the progress log is committed, begin `Phase 3: Campaign Module` as the
  next backend vertical slice.

## Phase 3 Readiness Hardening

These are planned constraints or pending verification, not completed implementation:

1. Extend Product Card route-level scoping when the API accepts company or future
   workspace context for get, patch, confirm, and delete. Repository/service
   helpers for `product_card_id + company_id` now exist, but full authorization
   is not implemented.
2. Audit non-Product-Card ORM and Alembic check constraints so status/type
   constraint names use the same `ck_<table_name>_<column_name>` name.
3. Run the current migration chain against a real isolated PostgreSQL test
   database; SQLite migration cycling and PostgreSQL offline SQL generation are
   not sufficient proof.

Resolved Product Card contract decisions:

- Product Card lists include `draft` and `confirmed` only; rejected visibility is not a supported concept.
- Confirm is idempotent for already confirmed cards, and removal uses delete with Campaign-reference protection.

## Long-Term Development Plan

### Phase 1: Sources + Knowledge Vertical Slice

Status: Completed for the MVP text/URL minimum slice.

Goal:

- Turn raw company inputs into reviewable knowledge drafts tied to real source records.

Scope:

- Implement `sources` persistence and input flows for simple URL and text source records.
- Implement the first `knowledge` draft workflow with `draft`, `confirmed`, and `rejected` states.
- Add the required models, migrations, schemas, repositories, services, routes, and tests for this slice.

Exit Criteria:

- A company can store source records and generate or save knowledge draft records linked to those sources.
- Knowledge review state transitions are explicit and covered by tests.
- The slice is honest and complete at the module level: model, schema, repository, service, routes, and tests all exist.

### Phase 2: Product Card Module

Status: Finalized backend contract is implemented. Product Card frontend work remains pending.

Goal:

- Turn confirmed company knowledge into structured, reusable product cards.

Scope:

- Implement AI-generated and manual product card creation, listing, retrieval, editing, confirmation, and deletion flows.
- Define how product cards reference confirmed knowledge and evidence sources.
- Add tests for confirmed-knowledge gating, product card review behavior, and invalid IDs.

Exit Criteria:

- Backend users can generate or manually create, edit, confirm, and delete product cards under the finalized lifecycle rules.
- Product card state and evidence references are persisted and validated.
- Product cards become usable downstream inputs for campaign creation after Campaign is implemented.

### Phase 3: Campaign Module

Goal:

- Create confirmed campaigns that define who to target and how to position outreach.

Scope:

- Implement campaign create, edit, confirm, and archive flows.
- Store targeting criteria, search keywords, exclusion rules, scoring focus, and
  outreach angle.
- Enforce that Campaign uses a Product Card from the same company; preserve a
  future workspace-scope path without claiming workspace authorization already
  exists.
- Add tests for campaign lifecycle and product-card linkage.

Exit Criteria:

- Users can create campaigns linked to confirmed product cards.
- Campaign confirmation is explicit and required before downstream lead work starts.
- Campaign routes, validation, business logic, and tests are in place.

### Phase 4: Lead Discovery

Goal:

- Discover candidate leads from campaign criteria through provider-driven search workflows.

Scope:

- Implement discovery task initiation, search query generation, provider boundary integration, and initial lead storage.
- Persist discovery source URLs, company names, websites, and discovery status.
- Add tests for discovery orchestration and lead creation boundaries.

Exit Criteria:

- A confirmed campaign can create candidate lead records with traceable discovery sources.
- Discovery logic stays behind service and provider boundaries.
- Discovery results are stored without pretending validation or scoring already happened.

### Phase 5: Lead Validation + Intelligence

Goal:

- Clean discovered leads and collect usable website intelligence before scoring.

Scope:

- Implement normalization, duplicate handling, website availability checks, and invalid-lead filtering.
- Implement website intelligence capture, extracted evidence storage, and content sufficiency checks.
- Add tests for validation decisions and intelligence persistence.

Exit Criteria:

- Leads move through explicit validation states such as `valid`, `invalid`, `duplicate`, and `insufficient_content`.
- Website intelligence and evidence are stored separately from raw lead discovery data.
- Only validated leads move forward to scoring.

### Phase 6: Lead Scoring

Goal:

- Produce evidence-based customer-fit judgments for validated leads.

Scope:

- Implement scoring workflow inputs from campaign, product card, confirmed knowledge, and lead intelligence.
- Store fit score, recommendation, matching reasons, risk notes, evidence, and uncertainty.
- Add tests for scoring persistence, output validation, and provider mocking.

Exit Criteria:

- Validated leads can receive structured scoring results with evidence and risk notes.
- Scoring never bypasses evidence requirements or provider abstraction boundaries.
- Tests cover the scoring workflow with mocked external dependencies.

### Phase 7: Lead Review

Goal:

- Keep final approval decisions in user hands before any contact or outreach work happens.

Scope:

- Implement review states, approve/reject actions, and optional manual review notes.
- Separate user review logic from scoring logic and persistence.
- Add tests for approval rules and review transitions.

Exit Criteria:

- Leads can be explicitly approved, rejected, or flagged for manual review.
- Only approved leads become eligible for downstream contact and outreach flows.
- Review decisions are auditable and tested.

### Phase 8: Contacts

Goal:

- Store usable lead contact options with clear type, source, and validation status.

Scope:

- Implement contact persistence for email, contact form, phone, manual, and LinkedIn reference records.
- Enforce validation status handling and manual-reference semantics for LinkedIn URLs.
- Add tests for contact creation, status rules, and Gmail Draft eligibility boundaries.

Exit Criteria:

- Leads can have structured contact records with explicit `contact_type` and `status`.
- LinkedIn references remain manual references only and do not count as Gmail Draft recipients.
- A selected valid email contact becomes a reliable prerequisite for outreach drafting.

### Phase 9: Outreach Draft + Gmail Draft

Goal:

- Generate reviewable outreach drafts and create Gmail drafts for approved leads with valid email contacts.

Scope:

- Implement outreach draft generation, storage, duplicate prevention, and Gmail Draft provider integration.
- Enforce eligibility rules based on lead review status and selected contact status.
- Add tests for draft generation rules, duplicate prevention, and Gmail Draft creation with mocks.

Exit Criteria:

- Approved leads with selected valid email contacts can produce outreach drafts and Gmail drafts.
- The system creates Gmail drafts only and never sends or modifies live emails automatically.
- Outreach state transitions and provider failures are tested and explicit.

### Phase 10: Frontend MVP Workflow

Goal:

- Expose the MVP backend flow through a usable end-to-end frontend workflow.

Scope:

- Build the minimum pages and flows for company, sources, knowledge review,
  product cards, campaigns, leads, review, contacts, and outreach drafts.
- Surface task status, validation errors, evidence, and manual review points.
- Add frontend smoke or integration coverage where practical.

Exit Criteria:

- A user can move through the MVP flow from company setup to Gmail Draft review in the frontend.
- Frontend screens rely on documented API contracts instead of placeholder assumptions.
- Key manual review checkpoints are visible and usable.

### Phase 11: Background Jobs + Deployment

Goal:

- Make async workflows and runtime packaging viable for real MVP operation.

Scope:

- Implement background job execution for discovery, intelligence, scoring, and
  draft-generation workflows.
- Add worker runtime, task status updates, operational docs, and deployment
  alignment for PostgreSQL and Redis.
- Add required real-PostgreSQL migration smoke verification for the accumulated
  migration chain.
- Add tests or smoke checks for task execution boundaries where practical.

Exit Criteria:

- Long-running workflows can run through background jobs with explicit task states.
- Deployment docs and runtime configuration match the code that actually exists.
- PostgreSQL, Redis, API, and worker responsibilities are clearly verified.
- The migration chain passes `upgrade head` on an isolated real PostgreSQL database.

### Phase 12: MVP Stabilization

Goal:

- Prepare the MVP for consistent demo, testing, and controlled real use.

Scope:

- Close contract gaps, improve validation and error handling, expand automated
  tests, and fix workflow regressions.
- Review documentation accuracy across architecture, API, data model, AI rules, and deployment.
- Tighten observability, failure handling, and manual review safeguards.
- Re-run real-PostgreSQL migration smoke checks as a required stabilization gate.

Exit Criteria:

- Core MVP workflows are covered by reliable automated tests and smoke checks.
- Documentation, implementation, and runtime behavior are aligned.
- The team can demo the end-to-end MVP without relying on placeholder behavior
  in critical paths.
- Real PostgreSQL schema validation confirms JSON/JSONB, foreign keys, indexes,
  check constraints, names, and migration order.

## Recently Changed Files

- `AGENTS.md`
- `README.md`
- `docs/README.md`
- `docs/DEVELOPMENT_PROGRESS.md`

## Test Status

- Documentation-only retention cleanup; backend tests, frontend tests, compile
  checks, migrations, package checks, and runtime checks were not run because no
  code, tests, migrations, dependencies, package files, or runtime configuration
  files were changed.
- `git diff --name-only` confirmed that only Markdown documentation files were changed.
- Task-record heading search confirmed `docs/DEVELOPMENT_PROGRESS.md` now keeps
  exactly three recent task records.
- Retention wording search confirmed the three-record rule appears in
  `AGENTS.md`, `README.md`, `docs/README.md`, and
  `docs/DEVELOPMENT_PROGRESS.md`.
- `git diff --check` passed with no whitespace errors.

## Known Issues

- Most backend modules other than `company`, `sources`, `knowledge`, and `products` are still placeholders.
- Knowledge draft generation is deterministic and only copies supplied content or
  creates a manual-review URL note; it does not perform AI extraction.
- Product Card generation is deterministic; fields without matching
  confirmed-knowledge categories remain empty lists or explicit `Not specified`
  values.
- Product Card frontend UI has not been implemented or updated for the finalized backend contract.
- Product Card get, patch, confirm, and delete routes remain single-user ID paths
  per the current API contract. Repository/service company-scoped helpers now
  exist, but route-level company/workspace authorization is not implemented.
- Campaign reference protection is wired through a repository boundary and
  tested with a fake reference repository, but real Campaign persistence is not
  implemented yet.
- Non-Product-Card ORM/migration check constraint names still require a code-and-migration audit against the new naming standard.
- The migration chain has not been executed against a live isolated PostgreSQL test database.
- Source support is limited to text and URL. Uploaded document handling,
  document parsing, Word/PDF handling, image OCR, file storage, and crawling are
  not implemented.
- No real provider implementations exist yet for LLM, search, crawler, Gmail, storage, or task queue.
- No RQ worker runtime is implemented yet, even though Redis and the task queue direction are documented.
- Frontend is still a basic shell and has no business workflow pages.
- Stitch UI screens and Stitch MCP design context have not yet been provided;
  this task defines the future frontend handoff workflow only.
- Live PostgreSQL and Redis services were not exercised in this task.

## Next Recommended Step

Commit this documentation-only retention cleanup if accepted, then begin
`Phase 3: Campaign Module` as a backend vertical slice, starting with the
minimal Campaign model, migration, schemas, repository, service, routes, and
tests. Campaign must select only confirmed Product Cards from the same company.

Before or during Phase 3, if an isolated live PostgreSQL database becomes available:

- run `alembic upgrade head`
- run `alembic downgrade -1`
- run `alembic upgrade head`

Additional recommended hardening:

- tighten route-level Product Card scoping when the API accepts company or future workspace context, without adding a full account system
- audit and normalize remaining non-Product-Card ORM/migration check constraint names
- implement the Product Card frontend UI from Stitch context when frontend work resumes
