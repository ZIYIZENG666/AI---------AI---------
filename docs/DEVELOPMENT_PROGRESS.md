# Development Progress

## Current Project Stage

Foundation stabilization, Phase 1B, and the Phase 2 Product Card backend slice are complete.

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
- Added product card create, list, get, confirm, and reject APIs with explicit review-state rules.
- Added the `product_cards` table through Alembic revision `20260623_0003`.
- Added Product Card API tests covering confirmed-knowledge eligibility, draft/rejected exclusion, company isolation, reads, transitions, and error responses.

## Current Task

`Phase 2: Product Card Module` is complete.

The next active implementation task is `Phase 3: Campaign Module`.

The completed Product Card slice uses deterministic category mapping and company-profile fallbacks. It does not call an LLM or external API, and draft or rejected knowledge is never used.

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

Status: Completed for the deterministic confirmed-knowledge backend slice.

Goal:

- Turn confirmed company knowledge into structured, reusable product cards.

Scope:

- Implement product card creation, listing, retrieval, confirmation, and rejection flows.
- Define how product cards reference confirmed knowledge and evidence sources.
- Add tests for confirmed-knowledge gating, product card review behavior, and invalid IDs.

Exit Criteria:

- Users can create, confirm, and reject product cards based on confirmed company knowledge.
- Product card state and evidence references are persisted and validated.
- Product cards become usable downstream inputs for campaign creation.

### Phase 3: Campaign Module

Goal:

- Create confirmed campaigns that define who to target and how to position outreach.

Scope:

- Implement campaign create, edit, confirm, and archive flows.
- Store targeting criteria, search keywords, exclusion rules, scoring focus, and outreach angle.
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
- Add tests or smoke checks for task execution boundaries where practical.

Exit Criteria:

- Long-running workflows can run through background jobs with explicit task states.
- Deployment docs and runtime configuration match the code that actually exists.
- PostgreSQL, Redis, API, and worker responsibilities are clearly verified.

### Phase 12: MVP Stabilization

Goal:

- Prepare the MVP for consistent demo, testing, and controlled real use.

Scope:

- Close contract gaps, improve validation and error handling, expand automated tests, and fix workflow regressions.
- Review documentation accuracy across architecture, API, data model, AI rules, and deployment.
- Tighten observability, failure handling, and manual review safeguards.

Exit Criteria:

- Core MVP workflows are covered by reliable automated tests and smoke checks.
- Documentation, implementation, and runtime behavior are aligned.
- The team can demo the end-to-end MVP without relying on placeholder behavior in critical paths.

## Recently Changed Files

- `backend/alembic/versions/20260623_0003_create_product_cards.py`
- `backend/app/main.py`
- `backend/app/models.py`
- `backend/app/modules/knowledge/repository.py`
- `backend/app/modules/products/__init__.py`
- `backend/app/modules/products/models.py`
- `backend/app/modules/products/schemas.py`
- `backend/app/modules/products/repository.py`
- `backend/app/modules/products/service.py`
- `backend/app/modules/products/routes.py`
- `backend/tests/test_products.py`
- `backend/README.md`
- `docs/DEVELOPMENT_PROGRESS.md`
- `docs/DATA_MODEL.md`
- `docs/API_CONTRACT.md`

## Test Status

- Focused Phase 2 tests: `python -m pytest -q tests/test_products.py` -> `9 passed, 1 warning`
- Full backend tests: `python -m pytest -q` -> `31 passed, 1 warning`
- Python compile smoke check: `python -m compileall -q app tests` -> passed
- Backend import, OpenAPI generation, and Phase 2 route/method smoke check -> passed
- Alembic upgrade/downgrade/upgrade cycle with an isolated SQLite database -> passed and preserved the Phase 1A/1B tables when revision `20260623_0003` was downgraded
- PostgreSQL offline Alembic SQL generation through revision `20260623_0003` -> passed
- The warning is a Starlette deprecation warning for its current `httpx` TestClient integration; it does not fail the tests.
- Live PostgreSQL and live Redis verification remains pending.

## Known Issues

- Most backend modules other than `company`, `sources`, `knowledge`, and `products` are still placeholders.
- Knowledge draft generation is deterministic and only copies supplied content or creates a manual-review URL note; it does not perform AI extraction.
- Product Card generation is deterministic; fields without matching confirmed-knowledge categories remain empty lists or explicit `Not specified` values.
- Product cards do not yet support manual editing; Phase 2 provides generation, reads, confirmation, and rejection only.
- Source support is limited to text and URL. Document parsing, Word/PDF handling, image OCR, storage, and crawling are not implemented.
- No real provider implementations exist yet for LLM, search, crawler, Gmail, storage, or task queue.
- No RQ worker runtime is implemented yet, even though Redis and the task queue direction are documented.
- Frontend is still a basic shell and has no business workflow pages.
- Live PostgreSQL and Redis services were not exercised in this task.

## Next Recommended Step

Start `Phase 3: Campaign Module` as the next small backend vertical slice, including:

- a `campaigns` SQLAlchemy model and Alembic migration
- creation from confirmed product cards only
- explicit campaign targeting, search criteria, qualification criteria, outreach angle, and lifecycle status fields
- schemas, repository, service, routes, and tests following the existing vertical-slice pattern
- no lead discovery, crawler, search provider, or background worker implementation in the initial campaign slice
