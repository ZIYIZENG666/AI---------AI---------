"""Service placeholders for the products module."""

from app.modules.products.repository import ProductRepository


class ProductService:
    """Business service placeholder for products."""

    def __init__(self, repository: ProductRepository | None = None) -> None:
        self.repository = repository or ProductRepository()
