# Development Progress

## Current Project Stage

Foundation stabilization completed for the first backend slice.

The repository is no longer only a pure skeleton, but it is still far from a full MVP. Most backend modules outside `company` remain placeholders.

## Completed Work

- Fixed truncated rule documents in `docs/API_CONTRACT.md` and `docs/CODING_STANDARDS.md`.
- Added a real Alembic foundation with `alembic.ini`, `env.py`, `script.py.mako`, `versions/`, and an initial baseline migration.
- Reworked backend configuration to load database and Redis settings from environment variables instead of hardcoding connection secrets in Python code.
- Registered the first working business router in `backend/app/main.py`.
- Implemented a minimal `company` vertical slice with ORM model, schemas, repository, service, routes, and tests.
- Added `/health/db` and `/health/redis` checks with honest dependency probing.
- Aligned `AI_RULES.md`, `DATA_MODEL.md`, and `DEPLOYMENT_GUIDE.md` terminology with the current repository state.

## Current Task

The current stabilization pass is complete.

The next active task should be to implement the next honest vertical slice, likely `sources` plus the first `knowledge` draft workflow foundation.

## Recently Changed Files

- `AGENTS.md`
- `.env.example`
- `docker-compose.yml`
- `docs/API_CONTRACT.md`
- `docs/CODING_STANDARDS.md`
- `docs/AI_RULES.md`
- `docs/DATA_MODEL.md`
- `docs/DEPLOYMENT_GUIDE.md`
- `docs/DEVELOPMENT_PROGRESS.md`
- `backend/app/core/config.py`
- `backend/app/core/database.py`
- `backend/app/core/errors.py`
- `backend/app/main.py`
- `backend/app/models.py`
- `backend/app/modules/company/models.py`
- `backend/app/modules/company/schemas.py`
- `backend/app/modules/company/repository.py`
- `backend/app/modules/company/service.py`
- `backend/app/modules/company/routes.py`
- `backend/alembic.ini`
- `backend/alembic/env.py`
- `backend/alembic/script.py.mako`
- `backend/alembic/versions/20260622_0001_create_company_profiles.py`
- `backend/tests/conftest.py`
- `backend/tests/test_health.py`
- `backend/tests/test_companies.py`
- `backend/tests/test_config.py`
- `backend/tests/test_database.py`
- `backend/README.md`
- `backend/alembic/README.md`

## Test Status

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

Implement the `sources` module and the first `knowledge` draft flow on top of the new company foundation, including:

- source model and migrations
- source input routes
- knowledge draft data model
- draft vs confirmed status handling
- tests for the second vertical slice
