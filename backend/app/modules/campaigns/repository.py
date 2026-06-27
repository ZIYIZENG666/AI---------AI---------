"""Repository placeholders for the campaigns module."""

from sqlalchemy.orm import Session


class CampaignRepository:
    """Data access entrypoint placeholder for campaigns."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def is_product_card_referenced(self, product_card_id: str) -> bool:
        """Return whether any Campaign references a Product Card.

        The Campaign table is not implemented in the current Phase 2 task. This
        method is the repository boundary the products service will use once
        Campaign persistence exists.
        """

        return False
