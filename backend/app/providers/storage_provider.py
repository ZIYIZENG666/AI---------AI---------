"""Placeholder interface for file or object storage integrations."""


class StorageProvider:
    """Provider contract for persisting documents and generated artifacts."""

    def save(self, key: str, content: bytes) -> str:
        raise NotImplementedError("Storage integration is not implemented in the skeleton.")
