# Development Progress

## Current Project Stage

Foundation stabilization and Phase 1B are complete. A deterministic Phase 2 Product Card backend slice exists, but it still requires implementation updates to match the finalized Product Card contract below.

The repository is no longer only a pure skeleton, but it is still far from a full MVP. The honest implemented backend slices are now `company`, `sources`, `knowledge`, and `products`. Most other backend modules remain placeholders.

## Completed Work

- Fixed truncated rule documents in `docs/API_CONTRACT.md` and `docs/CODING_STANDARDS.md`.
- Added a real Alembic foundation with `alembic.ini`, `env.py`, `script.py.mako`, `versions/`, and an initial baseline migration.
- Reworked backend configuration to load database and Redis settings from environment variables instead of hardcoding connection secrets in Python code.
- Registered the first working business router in `backend/app/main.py`.
- Implemented a minimal `company` vertical slice with ORM model, schemas, repository, service, routes, and tests.
- Added `/health/db` and `/health/redis` checks with honest dependency probing.
- Aligned `AI_RULES.md`, `DATA_MODEL.md`, and `DEPLOYMENT_GUIDE.md` terminology with the current repository state.
- Updated the core planning and rule documents to add a phased long-term MVP plan and explicit LinkedIn boundaries.
- Implemented company-owned text and URL source records with create, list, and get APIs.
- Implemented deterministic source-to-knowledge draft creation without a crawler or LLM dependency.
- Implemented knowledge review transitions for `draft`, `confirmed`, and `rejected`, including status-filtered company lists.
- Added the `company_sources` and `knowledge_items` tables through a new Alembic migration.
- Added focused API tests for source ownership, source listing, draft generation, review transitions, status separation, invalid IDs, and invalid repeat review.
- Implemented deterministic Product Card generation from confirmed company knowledge only.
- Added the legacy product card create, list, get, confirm, and reject APIs that predate the finalized Phase 2 contract.
- Added the `product_cards` table through Alembic revision `20260623_0003`.
- Added Product Card API tests covering confirmed-knowledge eligibility, draft/rejected exclusion, company isolation, reads, transitions, and error responses.
- Documented the Product Card company/workspace scope plan, ORM/migration constraint naming standard, and required PostgreSQL migration smoke-test boundary.
- Finalized Product Card Phase 2 questions 3 and 5 across the project rule documents without changing backend, frontend, migrations, or tests.
- Formalized the Stitch-to-Codex frontend workflow, Chinese user-facing text requirement, dashboard page expectations, and UI design handoff rules in project documentation only.

## Current Task

Product Card Phase 2 question 3 is finalized:

- Product Cards use only `draft` and `confirmed`; lists never return a Product Card `rejected` state and `status=rejected` is unsupported.
- Product Card reject/rejected behavior is replaced by delete.
- Product Cards support both AI-generated (`ai_generated`) and user-created (`manual`) sources, and both start in `draft`.

Product Card Phase 2 question 5 is finalized:

- Draft cards may be edited, confirmed, or deleted; confirmed cards may be edited, used by Campaign, or deleted when unreferenced.
- Confirmed cards do not show a confirmation button, while repeated confirm API calls return HTTP `200` and keep the card confirmed.
- Editing happens in a details dialog; cancel discards unsaved changes, while save calls PATCH without changing status.
- Deleting a confirmed Product Card already referenced by a Campaign returns HTTP `409`.

This task updates rule documents only. The backend, frontend, migration, and test changes required to implement the finalized contract remain pending.

## Phase 3 Readiness Hardening

These are planned constraints or pending verification, not completed implementation:

1. Implement the finalized Product Card create/list/patch/confirm/delete contract and tighten repository/service lookups to `product_card_id + company_id`, then extend to `workspace_id` when multi-tenant support exists.
2. Audit ORM and Alembic check constraints so status/type constraint names use the same `ck_<table_name>_<column_name>` name.
3. Run the current migration chain against a real isolated PostgreSQL test database; SQLite migration cycling and PostgreSQL offline SQL generation are not sufficient proof.

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

Status: Legacy deterministic backend slice exists; finalized contract implementation is pending.

Goal:

- Turn confirmed company knowledge into structured, reusable product cards.

Scope:

- Implement AI-generated and manual product card creation, listing, retrieval, editing, confirmation, and deletion flows.
- Define how product cards reference confirmed knowledge and evidence sources.
- Add tests for confirmed-knowledge gating, product card review behavior, and invalid IDs.

Exit Criteria:

- Users can generate or manually create, edit, confirm, and delete product cards under the finalized lifecycle rules.
- Product card state and evidence references are persisted and validated.
- Product cards become usable downstream inputs for campaign creation.

### Phase 3: Campaign Module

Goal:

- Create confirmed campaigns that define who to target and how to position outreach.

Scope:

- Implement campaign create, edit, confirm, and archive flows.
- Store targeting criteria, search keywords, exclusion rules, scoring focus, and outreach angle.
- Enforce that Campaign uses a Product Card from the same company; preserve a future workspace-scope path without claiming workspace authorization already exists.
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

- Build the minimum pages and flows for company, sources, knowledge review, product cards, campaigns, leads, review, contacts, and outreach drafts.
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

- Implement background job execution for discovery, intelligence, scoring, and draft-generation workflows.
- Add worker runtime, task status updates, operational docs, and deployment alignment for PostgreSQL and Redis.
- Add required real-PostgreSQL migration smoke verification for the accumulated migration chain.
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

- Close contract gaps, improve validation and error handling, expand automated tests, and fix workflow regressions.
- Review documentation accuracy across architecture, API, data model, AI rules, and deployment.
- Tighten observability, failure handling, and manual review safeguards.
- Re-run real-PostgreSQL migration smoke checks as a required stabilization gate.

Exit Criteria:

- Core MVP workflows are covered by reliable automated tests and smoke checks.
- Documentation, implementation, and runtime behavior are aligned.
- The team can demo the end-to-end MVP without relying on placeholder behavior in critical paths.
- Real PostgreSQL schema validation confirms JSON/JSONB, foreign keys, indexes, check constraints, names, and migration order.

## Recently Changed Files

- `AGENTS.md`
- `docs/README.md`
- `docs/UI_REQUIREMENTS.md`
- `docs/WORKFLOW.md`
- `docs/MVP_SCOPE.md`
- `docs/MODULE_BOUNDARIES.md`
- `docs/API_CONTRACT.md`
- `docs/DATA_MODEL.md`
- `docs/AI_RULES.md`
- `docs/CODING_STANDARDS.md`
- `docs/DEVELOPMENT_PROGRESS.md`

## Test Status

- This task changes documentation only, so backend/frontend automated tests were not rerun.
- Last verified Phase 2 focused tests: `9 passed, 1 warning`.
- Last verified full backend suite: `31 passed, 1 warning`.
- Last verified compile and OpenAPI smoke checks: passed.
- SQLite Alembic upgrade/downgrade/upgrade previously passed, but this is not PostgreSQL schema validation.
- PostgreSQL offline Alembic SQL generation previously passed, but no live PostgreSQL migration smoke test has been completed.
- Live PostgreSQL and live Redis verification remains pending.

## Known Issues

- Most backend modules other than `company`, `sources`, `knowledge`, and `products` are still placeholders.
- Knowledge draft generation is deterministic and only copies supplied content or creates a manual-review URL note; it does not perform AI extraction.
- Product Card generation is deterministic; fields without matching confirmed-knowledge categories remain empty lists or explicit `Not specified` values.
- The current Product Card code still implements the legacy reject/rejected lifecycle and does not yet provide manual creation, PATCH editing, delete semantics, or `source_type`.
- Current Product Card get, confirm, and reject operations use ID-only lookup; the finalized get, patch, confirm, and delete contract still needs company-scoped and later workspace-scoped hardening.
- ORM/migration check constraint names still require a code-and-migration audit against the new naming standard.
- The migration chain has not been executed against a live isolated PostgreSQL test database.
- Source support is limited to text and URL. Document parsing, Word/PDF handling, image OCR, storage, and crawling are not implemented.
- No real provider implementations exist yet for LLM, search, crawler, Gmail, storage, or task queue.
- No RQ worker runtime is implemented yet, even though Redis and the task queue direction are documented.
- Frontend is still a basic shell and has no business workflow pages.
- Stitch UI screens and Stitch MCP design context have not yet been provided; this task defines the future frontend handoff workflow only.
- Live PostgreSQL and Redis services were not exercised in this task.

## Next Recommended Step

Implement the finalized Product Card backend/frontend contract before starting `Phase 3: Campaign Module`:

- replace Product Card reject/rejected behavior with delete and restrict status to `draft` / `confirmed`
- add manual creation, `source_type`, PATCH editing, idempotent confirmation, and Campaign-protected deletion
- update the Product Card UI with Chinese labels, details-dialog editing, and the permanent manual-add entry
- before implementing major frontend pages, generate or provide the relevant Stitch UI design and let Codex implement the UI according to `docs/UI_REQUIREMENTS.md`
- update the migration and automated tests to match the finalized contract, then verify against PostgreSQL
- tighten Product Card get, patch, confirm, and delete lookups to company scope, without adding a full account system
- audit and normalize ORM/migration check constraint names
- after hardening, implement the minimal Campaign model, migration, schemas, repository, service, routes, and tests using confirmed same-company Product Cards only
