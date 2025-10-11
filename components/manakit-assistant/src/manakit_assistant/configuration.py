from pydantic import SecretStr

from manakit_commons.configuration import BaseConfig


class AssistantConfig(BaseConfig):
    # Google API configuration
    google_api_key: SecretStr | None = None
    # OpenAI API configuration
    openai_base_url: str | None = None
    openai_api_key: SecretStr | None = None
    # Perplexity API configuration
    perplexity_api_key: SecretStr | None = None
