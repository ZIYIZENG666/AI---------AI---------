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

    def list_product_cards(
        self,
        limit: int,
        offset: int,
        status_filter: str | None = None,
        company_id: str | None = None,
    ) -> tuple[list[ProductCard], int]:
        filters = [ProductCard.status.in_(("draft", "confirmed"))]
        if status_filter is not None:
            filters.append(ProductCard.status == status_filter)
        if company_id is not None:
            filters.append(ProductCard.company_id == company_id)

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

    def list_by_company(
        self,
        company_id: str,
        limit: int,
        offset: int,
        status_filter: str | None = None,
    ) -> tuple[list[ProductCard], int]:
        return self.list_product_cards(
            company_id=company_id,
            limit=limit,
            offset=offset,
            status_filter=status_filter,
        )

    def get_by_id(self, product_card_id: str) -> ProductCard | None:
        return self.session.scalar(
            select(ProductCard).where(
                ProductCard.id == product_card_id,
                ProductCard.status.in_(("draft", "confirmed")),
            )
        )

    def get_by_id_and_company(
        self,
        product_card_id: str,
        company_id: str,
    ) -> ProductCard | None:
        return self.session.scalar(
            select(ProductCard).where(
                ProductCard.id == product_card_id,
                ProductCard.company_id == company_id,
                ProductCard.status.in_(("draft", "confirmed")),
            )
        )

    def update(self, product_card: ProductCard, data: dict) -> ProductCard:
        for field_name, value in data.items():
            setattr(product_card, field_name, value)

        self.session.add(product_card)
        self.session.commit()
        self.session.refresh(product_card)
        return product_card

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

    def delete(self, product_card: ProductCard) -> None:
        self.session.delete(product_card)
        self.session.commit()
