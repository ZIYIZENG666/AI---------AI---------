# Development Progress

## Current Project Stage

Foundation stabilization completed for the first backend slice.

The repository is no longer only a pure skeleton, but it is still far from a full MVP. The `company` module is the only honest implemented vertical slice. Most backend modules outside `company` remain placeholders.

## Completed Work

- Fixed truncated rule documents in `docs/API_CONTRACT.md` and `docs/CODING_STANDARDS.md`.
- Added a real Alembic foundation with `alembic.ini`, `env.py`, `script.py.mako`, `versions/`, and an initial baseline migration.
- Reworked backend configuration to load database and Redis settings from environment variables instead of hardcoding connection secrets in Python code.
- Registered the first working business router in `backend/app/main.py`.
- Implemented a minimal `company` vertical slice with ORM model, schemas, repository, service, routes, and tests.
- Added `/health/db` and `/health/redis` checks with honest dependency probing.
- Aligned `AI_RULES.md`, `DATA_MODEL.md`, and `DEPLOYMENT_GUIDE.md` terminology with the current repository state.
- Updated the core planning and rule documents to add a phased long-term MVP plan and explicit LinkedIn boundaries.

## Current Task

The current stabilization pass is complete.

The next active implementation task is `Phase 1: Sources + Knowledge Vertical Slice`.

This phase should implement the next honest vertical slice: `sources` plus the first `knowledge` draft workflow foundation.

## Long-Term Development Plan

### Phase 1: Sources + Knowledge Vertical Slice

Goal:

- Turn raw company inputs into reviewable knowledge drafts tied to real source records.

Scope:

- Implement `sources` persistence and input flows for URL, text, document metadata, and manual source records.
- Implement the first `knowledge` draft workflow with `draft`, `confirmed`, and `rejected` states.
- Add the required models, migrations, schemas, repositories, services, routes, and tests for this slice.

Exit Criteria:

- A company can store source records and generate or save knowledge draft records linked to those sources.
- Knowledge review state transitions are explicit and covered by tests.
- The slice is honest and complete at the module level: model, schema, repository, service, routes, and tests all exist.

### Phase 2: Product Card Module

Goal:

- Turn confirmed company knowledge into structured, reusable product cards.

Scope:

- Implement product card creation, update, confirmation, and archive flows.
- Define how product cards reference confirmed knowledge and evidence sources.
- Add tests for product card draft and confirmation behavior.

Exit Criteria:

- Users can create and confirm product cards based on confirmed company knowledge.
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

- `docs/DEVELOPMENT_PROGRESS.md`
- `docs/MVP_SCOPE.md`
- `docs/AI_RULES.md`
- `docs/DATA_MODEL.md`
- `docs/API_CONTRACT.md`
- `docs/MODULE_BOUNDARIES.md`

## Test Status

- No code changes were made in this task, so no new automated tests were run.
- Backend tests: `python -m pytest -q` -> `9 passed`
- Backend import smoke check: `import app.main` -> passed
- Alembic CLI smoke check: `python -m alembic -c alembic.ini upgrade head` with temporary SQLite settings -> passed
- Additional verification still needed for live PostgreSQL and live Redis instances

## Known Issues

- Most backend modules other than `company` are still placeholders.
- No real provider implementations exist yet for LLM, search, crawler, Gmail, storage, or task queue.
- No RQ worker runtime is implemented yet, even though Redis and the task queue direction are documented.
- Frontend is still a basic shell and has no business workflow pages.
- Automated tests currently focus only on backend foundation and the `company` slice.

## Next Recommended Step

Start `Phase 1: Sources + Knowledge Vertical Slice` on top of the new company foundation, including:

- source model and migrations
- source input routes
- knowledge draft data model
- draft vs confirmed status handling
- tests for the second vertical slice
