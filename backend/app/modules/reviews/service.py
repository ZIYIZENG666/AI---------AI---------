"""Service placeholders for the reviews module."""

from app.modules.reviews.repository import ReviewRepository


class ReviewService:
    """Business service placeholder for reviews."""

    def __init__(self, repository: ReviewRepository | None = None) -> None:
        self.repository = repository or ReviewRepository()
