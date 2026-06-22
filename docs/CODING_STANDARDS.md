# Coding Standards

## Purpose

This document defines coding standards for the project.

The goal is to keep the codebase clean, consistent, maintainable, and easy for AI coding assistants to work with.

## General Principles

1. Keep code simple.
2. Keep modules separated.
3. Avoid unnecessary abstractions.
4. Do not duplicate business logic.
5. Do not hardcode secrets.
6. Write code that is easy to test.
7. Prefer clear names over clever names.
8. Keep MVP scope in mind.

## Backend Standards

Backend stack:

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Redis
- RQ

## Backend Layering

Each business module should follow this structure conceptually:

```text
module/
  routes.py
  schemas.py
  service.py
  repository.py
  models.py