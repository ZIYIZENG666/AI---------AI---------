# System Architecture

## Purpose

This document defines the technical architecture of the project.

The project should be built as a modular monolith that is easy to maintain, test, deploy, and extend.

## Architecture Style

The project uses a modular monolith architecture.

This means:

- One backend application
- One frontend application
- One main database
- Clear internal business modules
- Shared infrastructure
- Provider interfaces for replaceable external services

The MVP should not use microservices.

## Main Components

### Frontend

Recommended stack:

- React
- TypeScript
- Vite

Frontend responsibilities:

- Web dashboard
- Forms
- Review pages
- Lead result pages
- API calls to backend
- Display task status
- Display AI results and explanations

Frontend must not contain backend business logic.

Frontend UI implementation follows a development-time design-to-code workflow.
Stitch is used as the manual UI design source, and Codex uses Stitch MCP context
when available to implement React frontend components. Stitch is not a product
runtime dependency and is not part of the production system architecture.

### Backend

Recommended stack:

- FastAPI
- Python

Backend responsibilities:

- API endpoints
- Business logic
- Workflow orchestration
- Database access
- AI provider calls
- Search and crawler provider calls
- Gmail draft provider calls
- Background task dispatch

### Database

Main database:

- PostgreSQL

Database migration:

- Alembic

The MVP must use PostgreSQL from the beginning.

Do not use SQLite as the main database.

### Background Jobs

Recommended stack:

- Redis
- RQ

Background jobs should be used for longer tasks such as:

- Lead discovery
- Website crawling
- AI scoring
- Gmail draft creation
- Batch processing

Task queue access should be wrapped behind an internal interface so it can be replaced later if needed.

### AI Provider

LLM calls should be accessed through an AI provider interface.

The system should not hardcode one model deeply into business logic.

AI provider responsibilities:

- Knowledge extraction
- Campaign suggestion
- Lead scoring
- Matching explanation
- Outreach draft generation

### Search Provider

Search APIs should be accessed through a search provider interface.

Search provider responsibilities:

- Search candidate companies
- Return search results
- Provide source URLs

### Crawler Provider

Crawler services should be accessed through a crawler provider interface.

Crawler provider responsibilities:

- Fetch website content
- Extract readable text
- Return page metadata
- Handle crawl errors

### Gmail Draft Provider

Gmail Draft creation should be accessed through a provider interface.

The MVP only supports Gmail draft creation.

Use only the minimum OAuth scope needed to create Gmail drafts, such as
`gmail.compose`.

Do not request Gmail send, modify, full mailbox, mailbox read, inbox sync, move,
delete, label, reply tracking, or reply monitoring permissions.

Gmail Draft Provider is not a complete Gmail integration and must not implement
email automation.

## Backend Layering

Each backend module should follow this structure conceptually:

- `routes`
- `schemas`
- `service`
- `repository`
- `models`

### Route Layer

Responsible for:

- HTTP request handling
- Input validation
- Calling service layer
- Returning response

Routes must not contain complex business logic.

### Schema Layer

Responsible for:

- Request schemas
- Response schemas
- Validation models

### Service Layer

Responsible for:

- Business rules
- Use case logic
- Calling repositories
- Calling providers through interfaces
- Coordinating module logic

### Repository Layer

Responsible for:

- Database queries
- Database persistence
- Data retrieval

Repositories must not call AI, crawler, search, or Gmail providers.

### Model Layer

Responsible for:

- SQLAlchemy models
- Database entity definitions

### Provider Layer

Responsible for:

- Third-party service integrations
- LLM SDK calls
- Search SDK calls
- Crawler SDK calls
- Gmail API calls

Business modules should depend on provider interfaces, not concrete SDKs.

## Main Backend Modules

The system may include these modules:

- company
- sources
- knowledge
- products
- campaigns
- discovery
- intelligence
- qualification
- reviews
- contacts
- outreach
- tasks

## Data Flow

Basic data flow:

1. Frontend sends request to backend API.
2. Backend route validates request.
3. Service executes business logic.
4. Repository reads or writes database.
5. Provider calls external service if needed.
6. Background task handles long-running operations.
7. Backend returns task status or result to frontend.

## Deployment Architecture

MVP deployment should include:

- Frontend app
- Backend API
- PostgreSQL
- Redis
- RQ worker
- Docker Compose
- Environment variables
- Health checks
- Alembic migrations

## Architecture Rules

1. Keep the system modular.
2. Do not put business logic in routes.
3. Do not put database queries in frontend.
4. Do not call third-party SDKs directly from services unless wrapped in providers.
5. Do not build microservices in MVP.
6. Do not build multi-agent architecture in MVP.
7. Do not make advanced RAG a hard dependency in MVP.
8. Keep all major external services replaceable.
