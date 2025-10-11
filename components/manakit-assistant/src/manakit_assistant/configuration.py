from pydantic import SecretStr

from manakit_commons.configuration import BaseConfig


class AssistantConfig(BaseConfig):
    google_api_key: SecretStr | None = None
    """API key for Google services."""
    openai_base_url: str | None = None
    """Base URL for OpenAI API compatible services, e.g. Azure."""
    openai_api_key: SecretStr | None = None
    """API key for OpenAI services."""
    perplexity_api_key: SecretStr | None = None
    """API key for Perplexity services."""
