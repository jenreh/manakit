"""
Base processor interface for AI processing services.
"""

import abc
import logging
from collections.abc import AsyncGenerator

from appkit_assistant.backend.models import AIModel, Chunk, MCPServer, Message

logger = logging.getLogger(__name__)


class Processor(abc.ABC):
    """Base processor interface for AI processing services."""

    @abc.abstractmethod
    async def process(
        self,
        messages: list[Message],
        model_id: str,
        files: list[str] | None = None,
        mcp_servers: list[MCPServer] | None = None,
    ) -> AsyncGenerator[Chunk, None]:
        """
        Process the thread using an AI model.

        Args:
            messages: The list of messages to process.
            model_id: The ID of the model to use.
            files: Optional list of file paths that were uploaded.
            mcp_servers: Optional list of MCP servers to use as tools.

        Returns:
            An async generator that yields Chunk objects containing different content
            types.
        """

    @abc.abstractmethod
    def get_supported_models(self) -> dict[str, AIModel]:
        """
        Get a dictionary of models supported by this processor.

        Returns:
            Dictionary mapping model IDs to AIModel objects.
        """
