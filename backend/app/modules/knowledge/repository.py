"""Repository logic for the knowledge module."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.knowledge.models import KnowledgeItem


class KnowledgeRepository:
    """Database access for company knowledge items."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, data: dict) -> KnowledgeItem:
        knowledge = KnowledgeItem(**data)
        self.session.add(knowledge)
        self.session.commit()
        self.session.refresh(knowledge)
        return knowledge

    def list_by_company(
        self,
        company_id: str,
        status_filter: str | None,
        limit: int,
        offset: int,
    ) -> tuple[list[KnowledgeItem], int]:
        filters = [KnowledgeItem.company_id == company_id]
        if status_filter is not None:
            filters.append(KnowledgeItem.status == status_filter)

        total = self.session.scalar(
            select(func.count()).select_from(KnowledgeItem).where(*filters)
        ) or 0
        items = list(
            self.session.scalars(
                select(KnowledgeItem)
                .where(*filters)
                .order_by(KnowledgeItem.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
        )
        return items, total

    def get_by_id(self, knowledge_id: str) -> KnowledgeItem | None:
        return self.session.get(KnowledgeItem, knowledge_id)

    def list_confirmed_by_company(self, company_id: str) -> list[KnowledgeItem]:
        return list(
            self.session.scalars(
                select(KnowledgeItem)
                .where(
                    KnowledgeItem.company_id == company_id,
                    KnowledgeItem.status == "confirmed",
                )
                .order_by(KnowledgeItem.created_at.asc(), KnowledgeItem.id.asc())
            )
        )

    def update_status(self, knowledge: KnowledgeItem, new_status: str) -> KnowledgeItem:
        knowledge.status = new_status
        self.session.add(knowledge)
        self.session.commit()
        self.session.refresh(knowledge)
        return knowledge
