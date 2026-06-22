"""Service placeholders for the campaigns module."""

from app.modules.campaigns.repository import CampaignRepository


class CampaignService:
    """Business service placeholder for campaigns."""

    def __init__(self, repository: CampaignRepository | None = None) -> None:
        self.repository = repository or CampaignRepository()
