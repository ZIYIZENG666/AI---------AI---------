"""Service placeholders for the intelligence module."""

from app.modules.intelligence.repository import IntelligenceRepository


class IntelligenceService:
    """Business service placeholder for intelligence."""

    def __init__(self, repository: IntelligenceRepository | None = None) -> None:
        self.repository = repository or IntelligenceRepository()
