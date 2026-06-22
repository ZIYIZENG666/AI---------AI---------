"""Placeholder interface for Gmail draft creation."""


class GmailProvider:
    """Provider contract for draft-oriented email actions only."""

    def create_draft(self, subject: str, body: str) -> str:
        raise NotImplementedError("Gmail integration is not implemented in the skeleton.")
