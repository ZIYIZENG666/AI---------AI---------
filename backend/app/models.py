"""Import ORM models so shared metadata stays populated."""

from app.modules.campaigns.models import Campaign
from app.modules.company.models import CompanyProfile
from app.modules.discovery.models import Lead
from app.modules.intelligence.models import LeadIntelligence
from app.modules.knowledge.models import KnowledgeItem
from app.modules.products.models import ProductCard
from app.modules.qualification.models import LeadScore
from app.modules.sources.models import CompanySource
from app.modules.tasks.models import TaskRun

__all__ = [
    "Campaign",
    "CompanyProfile",
    "CompanySource",
    "KnowledgeItem",
    "Lead",
    "LeadIntelligence",
    "LeadScore",
    "ProductCard",
    "TaskRun",
]
