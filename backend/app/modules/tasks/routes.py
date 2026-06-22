"""Route placeholders for the tasks module."""

from fastapi import APIRouter


router = APIRouter(prefix="/tasks", tags=["tasks"])
