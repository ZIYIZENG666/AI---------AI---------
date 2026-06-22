"""Service placeholders for the contacts module."""

from app.modules.contacts.repository import ContactRepository


class ContactService:
    """Business service placeholder for contacts."""

    def __init__(self, repository: ContactRepository | None = None) -> None:
        self.repository = repository or ContactRepository()
