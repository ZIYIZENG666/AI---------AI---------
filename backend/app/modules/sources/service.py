"""Service placeholders for the sources module."""

from app.modules.sources.repository import SourceRepository


class SourceService:
    """Business service placeholder for sources."""

    def __init__(self, repository: SourceRepository | None = None) -> None:
        self.repository = repository or SourceRepository()
