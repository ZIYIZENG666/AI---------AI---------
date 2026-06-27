# AI 销售知识库 + AI 客户匹配判断系统

## Project Summary

This project is an AI-powered B2B sales assistant.

The system helps users turn company information into a structured sales knowledge
base, create product cards, define sales campaigns, discover potential leads,
score customer fit, explain matching reasons, and generate Gmail draft outreach
emails for user review.

The first version focuses on a single-user MVP / prototype. It does not include a
full account system, team permission system, CRM, or automatic email sending.

## Core Goal

The goal of this project is to help B2B sales teams answer:

- What does my company offer?
- Which type of customers should I target?
- Which companies are worth contacting?
- Why is this lead a good or bad match?
- What should I write in the first outreach email?

## MVP Scope

The MVP includes:

- Company profile creation
- Company information input
- AI-generated knowledge draft
- User-confirmed knowledge base
- Product card creation
- Campaign creation
- Lead discovery
- Lead website analysis
- AI customer-fit scoring
- Matching reasons and risk notes
- User lead review
- Gmail draft generation

The MVP does not include:

- Full user account system
- Team workspace permission system
- Automatic email sending
- LinkedIn API integration
- Full CRM features
- Advanced reply tracking
- Multi-agent architecture
- Google Sheets workflow

## Tech Stack

Frontend:

- React
- TypeScript
- Vite

Backend:

- FastAPI
- Python

Database:

- PostgreSQL
- Alembic migration

Background Jobs:

- Redis
- RQ

Deployment:

- Docker
- Docker Compose

AI / External Services:

- LLM Provider abstraction
- Search Provider abstraction
- Crawler Provider abstraction
- Gmail Draft Provider abstraction

## Project Rules

Before developing, always read:

1. `AGENTS.md`
2. `docs/README.md`
3. `docs/DEVELOPMENT_PROGRESS.md`
4. The relevant document under `docs/`

Codex must read `docs/DEVELOPMENT_PROGRESS.md` before development to understand
the current completed work, verification status, known limitations, and next
recommended task.

Important project rule documents:

- `docs/PROJECT_OVERVIEW.md`
- `docs/PRODUCT_REQUIREMENTS.md`
- `docs/MVP_SCOPE.md`
- `docs/WORKFLOW.md`
- `docs/SYSTEM_ARCHITECTURE.md`
- `docs/MODULE_BOUNDARIES.md`
- `docs/DATA_MODEL.md`
- `docs/API_CONTRACT.md`
- `docs/AI_RULES.md`
- `docs/CODING_STANDARDS.md`
- `docs/UI_REQUIREMENTS.md`: Defines frontend UI rules, the Stitch-to-Codex
  workflow, dashboard page structure, and Chinese user-facing text requirements.
- `docs/TESTING_STRATEGY.md`
- `docs/DEPLOYMENT_GUIDE.md`
- `docs/DEVELOPMENT_PROGRESS.md`: Records completed phases, changed files,
  verification results, known limitations, and the next recommended development
  step.

## Development Principle

This project must be developed as a maintainable modular monolith.

Code should be easy to modify, test, replace, and deploy.

Do not build unnecessary features outside the MVP scope.
