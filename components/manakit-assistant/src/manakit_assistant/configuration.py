from pydantic import SecretStr

from manakit_commons.configuration import BaseConfig


class AssistantConfig(BaseConfig):
    perplexity_api_key: SecretStr | None = None
    openai_base_url: str | None = None
    openai_api_key: SecretStr | None = None
    google_api_key: SecretStr | None = None
