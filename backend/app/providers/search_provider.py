"""Placeholder interface for external search integrations."""


class SearchProvider:
    """Provider contract for prospect and market search operations."""

    def search(self, query: str) -> list[dict]:
        raise NotImplementedError("Search integration is not implemented in the skeleton.")
