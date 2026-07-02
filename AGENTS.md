# AGENTS.md

## Purpose

This file defines the rules that AI coding assistants such as Codex must follow
when working on this project.

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
9. `docs/UI_REQUIREMENTS.md`
10. `docs/TESTING_STRATEGY.md`
11. User's direct instruction

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
15. Keep only the three most recent Codex task records in
    `docs/DEVELOPMENT_PROGRESS.md`; remove older task records when adding a new
    one.
16. The progress update must include completed work, changed files, test
    results, known issues, and the next recommended step.
17. Do not claim a module is complete unless it has working models, schemas,
    repository and service logic, routes, and tests where appropriate.
18. When implementing frontend UI, Codex must follow `docs/UI_REQUIREMENTS.md`
    and use Stitch-generated design context when available. Codex must not freely
    redesign the UI unless explicitly requested.
19. At the start of each phase, backend work must clarify the current phase API
    contract, data model, business rules, validation rules, and allowed status
    transitions.
20. Frontend implementation must be based on the current backend API contract,
    data model, business rules, validation rules, and allowed status
    transitions.
21. Codex must not implement frontend features that are not supported by the
    current backend API contract, and must not imply unsupported capabilities in
    the UI.
22. Frontend phase numbers must stay synchronized with backend phase numbers.
    For example, Backend Phase 3 means Campaign backend/API/data contract work,
    and Frontend Phase 3 means Campaign frontend UI work.
23. All user-facing frontend text must be Chinese, including buttons, page
    titles, hints, errors, empty states, confirmation dialogs, and form labels.

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

Gmail access must be draft-only:

- Use the minimum OAuth permission needed to create drafts, for example
  `gmail.compose`.
- Do not request full Gmail access.
- Do not read, sync, move, delete, label, or modify the user's existing mailbox
  contents.

Do not implement:

- Auto-send email
- Gmail send permission
- Gmail modify permission
- Bulk email sending
- Reply automation
- Reply tracking or reply monitoring
- Inbox sync or mailbox read features

The user must manually review and send emails.

## External Service Rules

Do not integrate LinkedIn API.

Do not reintroduce Google Sheets workflow.

Do not require paid Google Cloud services for MVP.

Search, crawler, LLM, email finder, and Gmail features must be implemented through
provider interfaces so they can be replaced later.

## Database Rules

The MVP uses PostgreSQL from the beginning.

Use Alembic for database migrations.

Do not use SQLite as the main database.

The first version may be single-user, but the data model should keep future
workspace / owner fields where appropriate.

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
5. Any known limitations or risks
6. Commit / push status
7. Recommended next step

The completion report must clearly include:

- Changed files
- Summary of changes
- Tests added or updated
- How to run or verify
- API contract alignment
- Stitch design alignment when applicable
- User-facing Chinese text verification when frontend is involved
- Known limitations or risks
- Commit/push status
- Recommended next step

Codex must report whether it committed changes. Codex must report whether it
pushed changes to GitHub. If Codex did not commit or did not push, it must state
that clearly. Codex must not imply that changes are on GitHub unless they were
actually committed and pushed.

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
