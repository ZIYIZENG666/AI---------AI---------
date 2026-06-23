"""Service logic for the product card module."""

from app.core.errors import AppError
from app.modules.company.models import CompanyProfile
from app.modules.company.repository import CompanyRepository
from app.modules.knowledge.models import KnowledgeItem
from app.modules.knowledge.repository import KnowledgeRepository
from app.modules.products.repository import ProductRepository


class DeterministicProductCardGenerator:
    """Map confirmed knowledge into a product card without external AI."""

    def generate(
        self,
        company: CompanyProfile,
        knowledge_items: list[KnowledgeItem],
    ) -> dict:
        values_by_category: dict[str, list[str]] = {}
        for item in knowledge_items:
            category = item.category.strip().lower()
            values_by_category.setdefault(category, []).append(item.content)

        description_values = self._values_for(
            values_by_category,
            "product_description",
            "product",
            "service",
            "source_summary",
        )
        if not description_values:
            description_values = [item.content for item in knowledge_items]

        target_values = self._values_for(
            values_by_category,
            "target_customer",
            "target_customers",
            "ideal_customer",
        )
        value_values = self._values_for(
            values_by_category,
            "value_proposition",
            "benefit",
            "benefits",
        )

        product_name_values = self._values_for(
            values_by_category,
            "product_name",
        )
        name = (
            product_name_values[0][:255]
            if product_name_values
            else f"{company.name} Product Card"[:255]
        )

        return {
            "company_id": company.id,
            "name": name,
            "description": "\n\n".join(description_values),
            "target_customer": self._first_or_default(
                target_values,
                company.target_market,
            ),
            "pain_points": self._values_for(
                values_by_category,
                "pain_point",
                "pain_points",
            ),
            "value_proposition": self._first_or_default(
                value_values,
                company.value_proposition,
            ),
            "use_cases": self._values_for(
                values_by_category,
                "use_case",
                "use_cases",
            ),
            "differentiators": self._values_for(
                values_by_category,
                "differentiator",
                "differentiators",
                "differentiation",
            ),
            "source_knowledge_item_ids": [item.id for item in knowledge_items],
            "status": "draft",
        }

    @staticmethod
    def _values_for(
        values_by_category: dict[str, list[str]],
        *categories: str,
    ) -> list[str]:
        return [
            value
            for category in categories
            for value in values_by_category.get(category, [])
        ]

    @staticmethod
    def _first_or_default(values: list[str], fallback: str | None) -> str:
        if values:
            return values[0]
        return fallback or "Not specified in confirmed knowledge."


class ProductService:
    """Business service for deterministic product cards."""

    def __init__(
        self,
        repository: ProductRepository,
        company_repository: CompanyRepository,
        knowledge_repository: KnowledgeRepository,
        generator: DeterministicProductCardGenerator | None = None,
    ) -> None:
        self.repository = repository
        self.company_repository = company_repository
        self.knowledge_repository = knowledge_repository
        self.generator = generator or DeterministicProductCardGenerator()

    def create_product_card(self, company_id: str):
        company = self._get_company(company_id)
        confirmed_knowledge = self.knowledge_repository.list_confirmed_by_company(
            company_id
        )
        if not confirmed_knowledge:
            raise AppError(
                message="At least one confirmed knowledge item is required.",
                status_code=409,
                code="confirmed_knowledge_required",
            )

        return self.repository.create(
            self.generator.generate(company, confirmed_knowledge)
        )

    def list_product_cards(self, company_id: str, limit: int, offset: int) -> dict:
        self._get_company(company_id)
        items, total = self.repository.list_by_company(
            company_id=company_id,
            limit=limit,
            offset=offset,
        )
        return {
            "items": items,
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    def get_product_card(self, product_card_id: str):
        product_card = self.repository.get_by_id(product_card_id)
        if product_card is None:
            raise AppError(
                message="Product card not found.",
                status_code=404,
                code="product_card_not_found",
            )
        return product_card

    def confirm_product_card(self, product_card_id: str):
        product_card = self.get_product_card(product_card_id)
        self._require_draft(product_card.status)
        return self.repository.update_status(product_card, "confirmed")

    def reject_product_card(self, product_card_id: str):
        product_card = self.get_product_card(product_card_id)
        self._require_draft(product_card.status)
        return self.repository.update_status(product_card, "rejected")

    def _get_company(self, company_id: str):
        company = self.company_repository.get_by_id(company_id)
        if company is None:
            raise AppError(
                message="Company profile not found.",
                status_code=404,
                code="company_not_found",
            )
        return company

    @staticmethod
    def _require_draft(current_status: str) -> None:
        if current_status != "draft":
            raise AppError(
                message="Only draft product cards can be reviewed.",
                status_code=409,
                code="product_card_not_draft",
            )
