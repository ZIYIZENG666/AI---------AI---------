"""Repository logic for the product card module."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.products.models import ProductCard


class ProductRepository:
    """Database access for product cards."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, data: dict) -> ProductCard:
        product_card = ProductCard(**data)
        self.session.add(product_card)
        self.session.commit()
        self.session.refresh(product_card)
        return product_card

    def list_by_company(
        self,
        company_id: str,
        limit: int,
        offset: int,
    ) -> tuple[list[ProductCard], int]:
        filters = (ProductCard.company_id == company_id,)
        total = self.session.scalar(
            select(func.count()).select_from(ProductCard).where(*filters)
        ) or 0
        items = list(
            self.session.scalars(
                select(ProductCard)
                .where(*filters)
                .order_by(ProductCard.created_at.desc(), ProductCard.id.desc())
                .limit(limit)
                .offset(offset)
            )
        )
        return items, total

    def get_by_id(self, product_card_id: str) -> ProductCard | None:
        return self.session.get(ProductCard, product_card_id)

    def update_status(
        self,
        product_card: ProductCard,
        new_status: str,
    ) -> ProductCard:
        product_card.status = new_status
        self.session.add(product_card)
        self.session.commit()
        self.session.refresh(product_card)
        return product_card
