"""Service placeholders for the discovery module."""

from app.modules.discovery.repository import DiscoveryRepository


class DiscoveryService:
    """Business service placeholder for discovery."""

    def __init__(self, repository: DiscoveryRepository | None = None) -> None:
        self.repository = repository or DiscoveryRepository()
