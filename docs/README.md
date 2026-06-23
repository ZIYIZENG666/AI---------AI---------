# Documentation Index

This folder contains the project rule documents for the AI Sales Knowledge Base + AI Customer Matching Judgment System.

Codex and future developers should use this folder as the main reference for project direction, scope, architecture, data model, API rules, AI behavior, coding standards, testing, and deployment.

## Documents

### `PROJECT_OVERVIEW.md`

Explains the project positioning, target users, core value, and product direction.

Read this first when you need to understand what the project is.

### `PRODUCT_REQUIREMENTS.md`

Defines the main product requirements and user-facing functions.

Use this when deciding what features the system should provide.

### `MVP_SCOPE.md`

Defines what must be included in the first version and what must not be included.

Use this to prevent scope creep.

### `WORKFLOW.md`

Defines the end-to-end business workflow.

Use this when implementing or modifying the main user journey.

### `SYSTEM_ARCHITECTURE.md`

Defines the technical architecture, major components, and infrastructure direction.

Use this when making backend, frontend, database, task queue, provider, or deployment decisions.

### `MODULE_BOUNDARIES.md`

Defines what each module is responsible for and what it must not do.

Use this when deciding where code should be placed.

### `DATA_MODEL.md`

Defines the main database entities and their relationships.

Use this when creating models, migrations, repositories, or database-related features.

### `API_CONTRACT.md`

Defines API design rules and expected frontend-backend communication patterns.

Use this when creating or changing API endpoints.

### `AI_RULES.md`

Defines how AI should behave in this system.

Use this when implementing prompts, scoring, matching, draft generation, or AI explanations.

### `CODING_STANDARDS.md`

Defines code organization, naming, layering, error handling, and configuration rules.

Use this when writing or reviewing code.

### `UI_REQUIREMENTS.md`

Defines the frontend UI rules, Stitch-to-Codex workflow, dashboard page structure, and Chinese user-facing text requirements.

### `TESTING_STRATEGY.md`

Defines what should be tested and how tests should be structured.

Use this when adding or modifying business logic.

### `DEPLOYMENT_GUIDE.md`

Defines deployment requirements and production-readiness expectations.

Use this when working on Docker, environment variables, database migration, server deployment, and health checks.

## Rule

Before making changes, always check the most relevant document.

If a change affects architecture, workflow, data model, API behavior, AI behavior, or deployment, update the related document.
