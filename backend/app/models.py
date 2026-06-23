"""Import ORM models so shared metadata stays populated."""

from app.modules.company.models import CompanyProfile
from app.modules.knowledge.models import KnowledgeItem
from app.modules.products.models import ProductCard
from app.modules.sources.models import CompanySource

__all__ = ["CompanyProfile", "CompanySource", "KnowledgeItem", "ProductCard"]
