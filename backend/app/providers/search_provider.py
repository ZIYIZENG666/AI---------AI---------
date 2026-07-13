"""Search provider contracts and mock implementation."""

from typing import Any


class SearchProvider:
    """Provider contract for prospect and market search operations."""

    provider_name = "search_provider"

    def search(self, query: str, limit: int) -> list[dict[str, Any]]:
        raise NotImplementedError("Search integration is not implemented.")


class MockSearchProvider(SearchProvider):
    """Deterministic provider used for Phase 4 Lead Discovery development."""

    provider_name = "mock_search"

    def __init__(self, results: list[dict[str, Any]] | None = None) -> None:
        self.results = results

    def search(self, query: str, limit: int) -> list[dict[str, Any]]:
        results = self.results
        if results is None:
            results = self._default_results(query)
        return results[:limit]

    @staticmethod
    def _default_results(query: str) -> list[dict[str, Any]]:
        return [
            {
                "company_name": "Acme Quality Systems",
                "website": "https://acme-quality.example.com",
                "source_url": "https://mock-search.example.com/acme-quality",
                "raw_snippet": f"Mock result matched against: {query}",
                "discovery_reason": "Matches the campaign industry and quality workflow keywords.",
                "description": "Manufacturing quality software buyer profile.",
                "country": "Germany",
                "industry": "Manufacturing",
            },
            {
                "company_name": "Northstar Inspection Group",
                "website": "https://northstar-inspection.example.com",
                "source_url": "https://mock-search.example.com/northstar-inspection",
                "raw_snippet": f"Mock result matched against: {query}",
                "discovery_reason": "Mentions inspection operations aligned with the Campaign criteria.",
                "description": "Industrial inspection services and QA operations.",
                "country": "Germany",
                "industry": "Industrial Services",
            },
            {
                "company_name": "Helio Factory Automation",
                "website": "https://helio-factory.example.com",
                "source_url": "https://mock-search.example.com/helio-factory",
                "raw_snippet": f"Mock result matched against: {query}",
                "discovery_reason": "Fits the target factory automation customer profile.",
                "description": "Automation operator with quality control needs.",
                "country": "Austria",
                "industry": "Factory Automation",
            },
        ]
