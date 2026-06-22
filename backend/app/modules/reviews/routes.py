"""Route placeholders for the reviews module."""

from fastapi import APIRouter


router = APIRouter(prefix="/reviews", tags=["reviews"])
