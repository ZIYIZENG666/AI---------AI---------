# Development Progress

## Current Project Stage

Foundation stabilization and Phase 1B are complete. The finalized Phase 2 Product Card backend contract is now implemented for the modular monolith backend.

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
- Initially added a legacy Product Card API that included reject/rejected behavior; that lifecycle has since been removed by the finalized Phase 2 contract and must not be treated as current behavior.
- Added the `product_cards` table through Alembic revision `20260623_0003`.
- Added Product Card API tests covering confirmed-knowledge eligibility, exclusion of draft/rejected knowledge from AI-generated cards, company isolation, reads, transitions, and error responses.
- Documented the Product Card company/workspace scope plan, ORM/migration constraint naming standard, and required PostgreSQL migration smoke-test boundary.
- Finalized Product Card Phase 2 questions 3 and 5 across the project rule documents without changing backend, frontend, migrations, or tests.
- Formalized the Stitch-to-Codex frontend workflow, Chinese user-facing text requirement, dashboard page expectations, and UI design handoff rules in project documentation only.
- Implemented the finalized Product Card Phase 2 backend contract:
  - Product Card statuses are limited to `draft` and `confirmed`.
  - Product Card `reject` / `rejected` behavior was removed from the API and schemas.
  - Added `source_type` with `ai_generated` and `manual`.
  - AI-generated Product Cards still use `POST /api/v1/companies/{company_id}/product-cards`, use confirmed knowledge only, store exact confirmed knowledge IDs, and start as `draft`.
  - Manual Product Card creation is available through `POST /api/v1/product-cards`, requires `company_id`, starts as `draft`, uses `source_type = manual`, and defaults `source_knowledge_item_ids` to an empty list.
  - Added `GET /api/v1/product-cards`, `PATCH /api/v1/product-cards/{product_card_id}`, and `DELETE /api/v1/product-cards/{product_card_id}`.
  - Product Card confirmation is idempotent for already confirmed cards.
  - Product Card deletion physically removes draft cards and confirmed cards when the Campaign reference boundary reports no references.
  - Product Card repository/service methods now include company-scoped lookup helpers for future use without claiming workspace authorization.
- Added a minimal Campaign repository reference-check boundary used by the Product service; this does not implement the Campaign module.
- Added Alembic revision `20260627_0004` to add `source_type`, remove legacy `rejected` Product Cards, replace the status check constraint with `ck_product_cards_status`, and add `ck_product_cards_source_type`.
- Rewrote Product Card API tests for the finalized backend contract.

## Current Task

Completed: Documentation consistency repair for the finalized Product Card, LinkedIn, Gmail Draft eligibility, and Codex handoff rules.

What changed:

- Updated backend-facing documentation so the current implemented backend slices are `company`, `sources`, `knowledge`, and `products`.
- Clarified that Campaign, Lead Discovery, Contacts, Outreach, and frontend workflow pages are still not implemented.
- Updated the Product Card API contract to include both list entry points: `GET /api/v1/product-cards` and `GET /api/v1/companies/{company_id}/product-cards`.
- Kept the Product Card lifecycle aligned to create/list/get/patch/confirm/delete with `draft` and `confirmed` only, no `rejected`, and no reject endpoint.
- Clarified that Product Card PATCH must not change status, source type, source knowledge, or company ownership.
- Updated the Codex completion report format to require commit/push status and truthful reporting when no commit or push happened.
- Replaced the old direct email-field Gmail Draft eligibility wording with selected valid email contact rules.
- Reconfirmed that LinkedIn references are manual references only and cannot be Gmail Draft recipients or Gmail Draft eligibility.
- Added `docs/DEVELOPMENT_PROGRESS.md` to the documentation indexes.

Not changed in this task:

- No backend or frontend business code was changed.
- No tests were changed.
- No migrations were changed.
- No Campaign, Lead Discovery, Contacts, Outreach, Gmail Provider, or frontend workflow implementation was added.
- No LinkedIn automation, Google Sheets workflow, automatic email sending, multi-agent system, or LangGraph workflow was introduced.

## Phase 3 Readiness Hardening

These are planned constraints or pending verification, not completed implementation:

1. Extend Product Card route-level scoping when the API accepts company or future workspace context for get, patch, confirm, and delete. Repository/service helpers for `product_card_id + company_id` now exist, but full authorization is not implemented.
2. Audit non-Product-Card ORM and Alembic check constraints so status/type constraint names use the same `ck_<table_name>_<column_name>` name.
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
- `README.md`
- `backend/README.md`
- `docs/API_CONTRACT.md`
- `docs/DEVELOPMENT_PROGRESS.md`
- `docs/README.md`
- `docs/TESTING_STRATEGY.md`

## Test Status

- Documentation-only task; backend tests, frontend tests, compile checks, and migrations were not run because no business code, tests, or migration files were changed.
- `rg` verification confirmed the target docs no longer use the old direct email-field wording for Gmail Draft eligibility.
- `rg` verification confirmed the Product Card company-scoped list endpoint, selected valid email contact wording, Gmail send / modify / delete prohibition, `DEVELOPMENT_PROGRESS.md` index entry, and commit/push status reporting text are present.
- `git diff --name-only` confirmed the changed files are Markdown documentation files only.
- `git diff --check` passed with no whitespace errors; Git emitted line-ending normalization warnings for the touched Markdown files.

## Known Issues

- Most backend modules other than `company`, `sources`, `knowledge`, and `products` are still placeholders.
- Knowledge draft generation is deterministic and only copies supplied content or creates a manual-review URL note; it does not perform AI extraction.
- Product Card generation is deterministic; fields without matching confirmed-knowledge categories remain empty lists or explicit `Not specified` values.
- Product Card frontend UI has not been implemented or updated for the finalized backend contract.
- Product Card get, patch, confirm, and delete routes remain single-user ID paths per the current API contract. Repository/service company-scoped helpers now exist, but route-level company/workspace authorization is not implemented.
- Campaign reference protection is wired through a repository boundary and tested with a fake reference repository, but real Campaign persistence is not implemented yet.
- Non-Product-Card ORM/migration check constraint names still require a code-and-migration audit against the new naming standard.
- The migration chain has not been executed against a live isolated PostgreSQL test database.
- Source support is limited to text and URL. Document parsing, Word/PDF handling, image OCR, storage, and crawling are not implemented.
- No real provider implementations exist yet for LLM, search, crawler, Gmail, storage, or task queue.
- No RQ worker runtime is implemented yet, even though Redis and the task queue direction are documented.
- Frontend is still a basic shell and has no business workflow pages.
- Stitch UI screens and Stitch MCP design context have not yet been provided; this task defines the future frontend handoff workflow only.
- Live PostgreSQL and Redis services were not exercised in this task.

## Next Recommended Step

Begin `Phase 3: Campaign Module` as a backend vertical slice, starting with the minimal Campaign model, migration, schemas, repository, service, routes, and tests. Campaign must select only confirmed Product Cards from the same company.

Before or during Phase 3, if an isolated live PostgreSQL database becomes available:

- run `alembic upgrade head`
- run `alembic downgrade -1`
- run `alembic upgrade head`

Additional recommended hardening:

- tighten route-level Product Card scoping when the API accepts company or future workspace context, without adding a full account system
- audit and normalize remaining non-Product-Card ORM/migration check constraint names
- implement the Product Card frontend UI from Stitch context when frontend work resumes
