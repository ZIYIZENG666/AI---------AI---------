"""Service placeholders for the qualification module."""

from app.modules.qualification.repository import QualificationRepository


class QualificationService:
    """Business service placeholder for qualification."""

    def __init__(self, repository: QualificationRepository | None = None) -> None:
        self.repository = repository or QualificationRepository()
