"""
OpenAI processor for generating AI responses using OpenAI's API.
"""

import logging
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import Any

from openai import AsyncAzureOpenAI, AsyncOpenAI

from appkit_assistant.backend.models import (
    AIModel,
    Chunk,
    MCPServer,
    Message,
)
from appkit_assistant.backend.processor import Processor

logger = logging.getLogger(__name__)


class BaseOpenAIProcessor(Processor, ABC):
    """Base class for OpenAI processors with common initialization and utilities."""

    def __init__(
        self,
        models: dict[str, AIModel],
        api_key: str | None = None,
        base_url: str | None = None,
        is_azure: bool = False,
    ) -> None:
        """Initialize the base OpenAI processor.

        Args:
            models: Dictionary of supported AI models
            api_key: API key for OpenAI/Azure OpenAI
            base_url: Base URL for the API
            is_azure: Whether to use Azure OpenAI client
        """
        self.api_key = api_key
        self.base_url = base_url
        self.models = models
        self.is_azure = is_azure
        self.client = None

        if self.api_key and self.base_url and is_azure:
            self.client = AsyncAzureOpenAI(
                api_key=self.api_key,
                azure_endpoint=self.base_url,
                api_version="2025-04-01-preview",
            )
        elif self.api_key and self.base_url:
            self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        elif self.api_key:
            self.client = AsyncOpenAI(api_key=self.api_key)
        else:
            logger.warning("No API key found. Processor will not work.")

    @abstractmethod
    async def process(
        self,
        messages: list[Message],
        model_id: str,
        files: list[str] | None = None,
        mcp_servers: list[MCPServer] | None = None,
        payload: dict[str, Any] | None = None,
    ) -> AsyncGenerator[Chunk, None]:
        """Process messages and generate AI response chunks."""

    def get_supported_models(self) -> dict[str, AIModel]:
        """Return supported models if API key is available."""
        return self.models if self.api_key else {}
