"""Placeholder interface for web crawling or scraping integrations."""


class CrawlerProvider:
    """Provider contract for collecting external web content."""

    def fetch(self, url: str) -> str:
        raise NotImplementedError("Crawler integration is not implemented in the skeleton.")
