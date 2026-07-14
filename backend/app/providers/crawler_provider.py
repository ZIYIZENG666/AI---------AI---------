"""Crawler provider contracts and mock implementation."""

from typing import Any


class CrawlerProvider:
    """Provider contract for collecting bounded website intelligence."""

    provider_name = "crawler_provider"

    def fetch(self, url: str) -> dict[str, Any]:
        raise NotImplementedError("Crawler integration is not implemented.")


class MockCrawlerProvider(CrawlerProvider):
    """Deterministic provider used for Phase 5 Lead Validation development."""

    provider_name = "mock_crawler"

    def __init__(self, results: dict[str, dict[str, Any]] | None = None) -> None:
        self.results = results or {}

    def fetch(self, url: str) -> dict[str, Any]:
        if url in self.results:
            result = self.results[url]
            if result.get("raise"):
                raise RuntimeError(str(result["raise"]))
            return result

        lowered = url.lower()
        if "provider-failure" in lowered:
            raise RuntimeError("mock crawler failed")
        if "insufficient" in lowered:
            return self._insufficient_result(url)
        return self._valid_result(url)

    @staticmethod
    def _valid_result(url: str) -> dict[str, Any]:
        return {
            "final_url": url,
            "website_summary": "Mock website content describes a B2B company with a clear product and customer profile.",
            "products_or_services": [
                "Mock industrial operations platform",
                "Mock quality workflow service",
            ],
            "target_customers": [
                "Manufacturing quality teams",
                "Industrial operations leaders",
            ],
            "business_model": "B2B software and services",
            "pain_points": [
                "Manual review work",
                "Limited process visibility",
            ],
            "evidence": [
                {
                    "source_url": url,
                    "snippet": "Mock evidence snippet from the company website.",
                }
            ],
            "content_quality": "sufficient",
            "crawl_status": "completed",
        }

    @staticmethod
    def _insufficient_result(url: str) -> dict[str, Any]:
        return {
            "final_url": url,
            "website_summary": None,
            "products_or_services": [],
            "target_customers": [],
            "business_model": None,
            "pain_points": [],
            "evidence": [],
            "content_quality": "insufficient",
            "crawl_status": "insufficient_content",
        }
