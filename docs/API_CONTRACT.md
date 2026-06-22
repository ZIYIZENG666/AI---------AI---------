# API Contract

## Purpose

This document defines API design rules between frontend and backend.

The backend should provide clear, predictable, and stable APIs for the frontend.

## General Rules

1. Use REST-style APIs for MVP.
2. Use JSON for request and response bodies.
3. Use clear resource names.
4. Use consistent error format.
5. Use pagination for list endpoints where needed.
6. Do not expose internal database details unnecessarily.
7. Do not return secrets or raw credentials.
8. Long-running operations should return a task ID.

## Base Response Style

Successful response example:

```json
{
  "data": {},
  "message": "Success"
}