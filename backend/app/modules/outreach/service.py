"""Service placeholders for the outreach module."""

from app.modules.outreach.repository import OutreachRepository


class OutreachService:
    """Business service placeholder for outreach."""

    def __init__(self, repository: OutreachRepository | None = None) -> None:
        self.repository = repository or OutreachRepository()
