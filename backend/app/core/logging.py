"""Basic logging setup for the backend skeleton."""

import logging


def configure_logging() -> None:
    """Initialize a simple root logger configuration once."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
