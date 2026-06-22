"""Service placeholders for the knowledge module."""

from app.modules.knowledge.repository import KnowledgeRepository


class KnowledgeService:
    """Business service placeholder for knowledge."""

    def __init__(self, repository: KnowledgeRepository | None = None) -> None:
        self.repository = repository or KnowledgeRepository()
