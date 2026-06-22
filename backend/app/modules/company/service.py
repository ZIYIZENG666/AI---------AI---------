"""Service placeholders for the company module."""

from app.modules.company.repository import CompanyRepository


class CompanyService:
    """Business service placeholder for companies."""

    def __init__(self, repository: CompanyRepository | None = None) -> None:
        self.repository = repository or CompanyRepository()
