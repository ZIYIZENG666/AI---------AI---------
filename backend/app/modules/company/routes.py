"""Route placeholders for the company module."""

from fastapi import APIRouter


router = APIRouter(prefix="/companies", tags=["company"])
