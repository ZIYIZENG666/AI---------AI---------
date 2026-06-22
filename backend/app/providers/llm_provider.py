"""Placeholder interface for future large language model integrations."""


class LLMProvider:
    """Abstract-ish provider surface for text generation capabilities."""

    def generate_text(self, prompt: str) -> str:
        raise NotImplementedError("LLM integration is not implemented in the skeleton.")
