"""Route placeholders for the discovery module."""

from fastapi import APIRouter


router = APIRouter(prefix="/discovery", tags=["discovery"])
