"""Import ORM models so shared metadata stays populated."""

from app.modules.company.models import CompanyProfile

__all__ = ["CompanyProfile"]
