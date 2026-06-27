# Coding Standards

## Purpose

This document defines repository-level coding standards.

It focuses on code organization, naming, layering, configuration, logging, testing, and forbidden implementation patterns.

## General Principles

1. Keep code simple and readable.
2. Prefer explicit business flow over clever abstractions.
3. Keep modules separated by responsibility.
4. Avoid duplicated business rules.
5. Keep the MVP scope narrow.
6. Write code that is easy to test and replace.

## Backend Coding Rules

Backend standards:

1. Use FastAPI for HTTP APIs.
2. Use SQLAlchemy for ORM and persistence.
3. Use Alembic for schema migration.
4. Keep business logic in services, not routes.
5. Keep database access in repositories.
6. Keep third-party integrations behind provider or adapter interfaces.
7. Keep workflows focused on orchestration, not low-level implementation details.

## Frontend Coding Rules

Frontend standards:

1. Use React + TypeScript + Vite.
2. Keep business rules on the backend unless the rule is strictly presentation-only.
3. Keep API access logic separated from presentational components.
4. Make loading, empty, error, and review states explicit.
5. Do not hardcode backend secrets or provider credentials in frontend code.
6. All user-visible text must be Chinese, including page titles, buttons, form
   labels, dialogs, errors, empty states, status labels, menus, and confirmation
   prompts.
7. Frontend layout and visual implementation should follow Stitch-generated UI
   designs when available.

Product Card UI vocabulary and interaction rules:

- Use `产品卡片`, `产品`, `待确认`, `已确认`, `手动添加产品`, `编辑`, `删除`,
  `确认产品卡片`, `保存修改`, `取消`, and `已被获客任务使用` for the
  corresponding user-visible concepts.
- Draft cards may show `编辑`, `确认产品卡片`, and `删除`; confirmed cards may
  show `编辑` and `删除`, but not `确认产品卡片`.
- A Product Card details dialog owns unsaved field state. Show `取消` and
  `保存修改` after a field changes.
- Cancelling restores the saved values without an API call. Saving calls PATCH
  and must not change Product Card status.
- Do not persist UI-only states such as `editing`, `modified`, or
  `pending_changes` as business or database statuses.

## Module Structure Rules

Each backend business module should follow this structure conceptually:

```text
module/
  routes.py
  schemas.py
  service.py
  repository.py
  models.py
```

Layer responsibilities:

1. `routes.py`: HTTP request and response handling only.
2. `schemas.py`: request and response validation models.
3. `service.py`: business rules and use-case logic.
4. `repository.py`: database persistence and queries.
5. `models.py`: SQLAlchemy ORM definitions.

## Naming Rules

Rules:

1. Use descriptive names over shortened names.
2. Use `snake_case` for Python files, variables, JSON fields, and functions.
3. Use `PascalCase` for Python classes and Pydantic models.
4. Use stable plural resource names for API endpoints.
5. Use consistent domain vocabulary across docs, schemas, models, and tests.
6. For Product Cards, use confirm only for `draft -> confirmed` and delete for
   removal. Do not use reject/rejected as Product Card API or business
   vocabulary.

## Database Constraint Naming Rules

Rules:

1. SQLAlchemy ORM `CheckConstraint` names must match the constraint names
   created by Alembic migrations.
2. Use `ck_<table_name>_<column_name>` for new status, type, and enum-like checks.
3. For example, a Product Card status constraint should use
   `ck_product_cards_status` in both the ORM model and migration.
4. Do not rely on different local names that resolve to different database names
   through naming conventions.
5. Review the final PostgreSQL constraint name when generating or reviewing a migration.
6. A model and migration naming mismatch must be treated as a schema defect
   because it can cause false Alembic diffs and unsafe later enum changes.
7. New modules must verify naming consistency before their migration is accepted.

## Configuration Rules

Rules:

1. Read runtime configuration from environment variables.
2. Keep example values in `.env.example`.
3. Do not hardcode real passwords, API keys, tokens, or OAuth secrets in code.
4. Keep environment-specific behavior explicit through settings.
5. If a setting is required for runtime, document it and fail honestly when missing.

## Logging Rules

Rules:

1. Log enough to debug failures and state transitions.
2. Do not log secrets, OAuth tokens, raw API keys, or full connection strings.
3. Prefer structured and consistent log messages.
4. Log external dependency failures with provider name and high-level context.
5. Keep debug-only logging out of production defaults unless intentionally enabled.

## Testing Rules

Rules:

1. Add or update tests when logic changes.
2. Cover the happy path and the key failure path for each implemented business slice.
3. Use mocks or test doubles for third-party providers.
4. Keep automated tests deterministic and lightweight.
5. Do not claim a module is complete unless working code and basic tests exist where appropriate.

## Error Handling Rules

Rules:

1. Use predictable API error responses.
2. Raise clear application errors for expected business failures.
3. Do not hide failures behind fake success payloads.
4. Validation failures should remain machine-readable.
5. Dependency failures should be reported honestly.

## AI and Provider Usage Rules

Rules:

1. Services may depend on provider interfaces, not concrete SDKs.
2. Repositories must not call LLMs, crawlers, search APIs, email finders, or Gmail APIs.
3. Prompts should stay in centralized prompt locations.
4. AI output must pass schema validation before being trusted.
5. Gmail integration must remain draft-only.

## Forbidden Patterns

Do not:

1. Put business logic directly in route handlers.
2. Put third-party SDK calls directly in services unless wrapped by providers.
3. Put AI calls in repositories.
4. Put database queries in frontend code.
5. Hardcode credentials or real secrets in code.
6. Introduce fake “completed” modules that only expose placeholder endpoints.
7. Reintroduce Google Sheets, LinkedIn API integration, automatic email sending,
   or microservice splitting without explicit direction.
