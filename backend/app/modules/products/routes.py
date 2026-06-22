"""Route placeholders for the products module."""

from fastapi import APIRouter


router = APIRouter(prefix="/products", tags=["products"])
