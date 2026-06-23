# AGENTS.md

## Purpose

This file defines the rules that AI coding assistants such as Codex must follow when working on this project.

The project is an AI Sales Knowledge Base + AI Customer Matching Judgment System.

All AI coding work must follow the project documents in this repository.

## Priority Order

When making development decisions, follow this priority order:

1. `AGENTS.md`
2. `docs/MVP_SCOPE.md`
3. `docs/SYSTEM_ARCHITECTURE.md`
4. `docs/MODULE_BOUNDARIES.md`
5. `docs/DATA_MODEL.md`
6. `docs/API_CONTRACT.md`
7. `docs/AI_RULES.md`
8. `docs/CODING_STANDARDS.md`
9. `docs/TESTING_STRATEGY.md`
10. User's direct instruction

If documents conflict, stop and report the conflict before changing code.

## Project Direction

This project is a modular monolith.

Do not convert it into:

- Microservices
- Multi-agent system
- LangGraph-based system
- Full CRM
- Full email automation platform
- Google Sheets workflow
- LinkedIn API-based system

The MVP must remain focused on:

- Company knowledge base
- Product card
- Campaign
- Lead discovery
- Customer matching score
- Evidence-based recommendation
- Gmail draft generation

## Development Rules

When modifying code:

1. Keep changes small and focused.
2. Do not rewrite unrelated files.
3. Do not introduce new frameworks unless explicitly requested.
4. Do not add features outside MVP scope.
5. Do not remove existing abstractions unless explicitly requested.
6. Do not hardcode API keys, tokens, credentials, or secrets.
7. Use environment variables for configuration.
8. Keep business logic out of route handlers.
9. Keep database access inside repositories.
10. Keep third-party SDK calls inside provider / adapter classes.
11. Keep AI prompts and AI behavior centralized.
12. Add or update tests when logic changes.
13. Update documentation if architecture, API, workflow, or data model changes.
14. Update `docs/DEVELOPMENT_PROGRESS.md` after every Codex development task.
15. The progress update must include completed work, changed files, test results, known issues, and the next recommended step.
16. Do not claim a module is complete unless it has working models, schemas, repository and service logic, routes, and tests where appropriate.

## Architecture Rules

The backend must follow this structure conceptually:

- Route: HTTP layer only
- Schema: request / response validation
- Service: business logic
- Repository: database access
- Model: database model
- Provider / Adapter: third-party service integration
- Workflow: orchestration across modules

Routes must not directly call:

- Database sessions for business logic
- Third-party SDKs
- LLM APIs
- Crawler APIs
- Search APIs
- Gmail APIs

Services must not directly depend on third-party SDKs. Use providers.

Repositories must not call AI, crawler, search, or email services.

## AI Rules

AI features must follow `docs/AI_RULES.md`.

Important rules:

- AI can generate drafts, suggestions, scores, and explanations.
- AI must not automatically send emails.
- AI must not make final business decisions without user review.
- AI scoring must include reasons and evidence.
- AI must identify uncertainty and risk.
- AI must not invent website evidence.
- AI-generated outreach emails must be saved as drafts only.

## Email Rules

The MVP only supports Gmail Draft creation.

Do not implement:

- Auto-send email
- Gmail send permission
- Gmail modify permission
- Bulk email sending
- Reply automation

The user must manually review and send emails.

## External Service Rules

Do not integrate LinkedIn API.

Do not reintroduce Google Sheets workflow.

Do not require paid Google Cloud services for MVP.

Search, crawler, LLM, email finder, and Gmail features must be implemented through provider interfaces so they can be replaced later.

## Database Rules

The MVP uses PostgreSQL from the beginning.

Use Alembic for database migrations.

Do not use SQLite as the main database.

The first version may be single-user, but the data model should keep future workspace / owner fields where appropriate.

## Testing Rules

When adding or changing logic, add tests where reasonable.

Use mocks for:

- LLM calls
- Search APIs
- Crawlers
- Gmail APIs
- Email finder APIs

Do not make real external API calls in automated tests.

## Completion Report Format

After each development task, reply with:

1. What was changed
2. Files modified
3. Tests added or updated
4. How to run or verify
5. Any known limitations
6. Recommended next step

## Do Not Do

Do not:

- Create unnecessary documents
- Add ADR folder unless explicitly requested
- Add account system in MVP unless explicitly requested
- Add automatic email sending
- Add LinkedIn API
- Add Google Sheets
- Mix frontend and backend logic
- Ignore existing project documents
