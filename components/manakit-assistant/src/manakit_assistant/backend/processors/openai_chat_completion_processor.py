import logging
from collections.abc import AsyncGenerator
from typing import Any

from openai import AsyncStream
from openai.types.chat import ChatCompletionMessageParam

from manakit_assistant.backend.models import (
    Chunk,
    ChunkType,
    MCPServer,
    Message,
    MessageType,
)
from manakit_assistant.backend.processors.openai_base import BaseOpenAIProcessor

logger = logging.getLogger(__name__)


class OpenAIChatCompletionsProcessor(BaseOpenAIProcessor):
    """Processor that generates responses using OpenAI's Chat Completions API."""

    async def process(
        self,
        messages: list[Message],
        model_id: str,
        files: list[str] | None = None,  # noqa: ARG002
        mcp_servers: list[MCPServer] | None = None,
        payload: dict[str, Any] | None = None,
    ) -> AsyncGenerator[Chunk, None]:
        """Process messages using the Chat Completions API.

        Args:
            messages: List of messages to process
            model_id: ID of the model to use
            files: File attachments (not used in chat completions)
            mcp_servers: MCP servers (will log warning if provided)
            payload: Additional payload parameters
        """
        if not self.client:
            raise ValueError("OpenAI Client not initialized.")

        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not supported by OpenAI processor")

        if mcp_servers:
            logger.warning(
                "MCP servers provided to ChatCompletionsProcessor but not supported. "
                "Use OpenAIResponsesProcessor for MCP functionality."
            )

        model = self.models[model_id]

        try:
            chat_messages = self._convert_messages_to_openai_format(messages)
            session = await self.client.chat.completions.create(
                model=model.model,
                messages=chat_messages[:-1],
                stream=model.stream,
                temperature=model.temperature,
                extra_body=payload,
            )

            if isinstance(session, AsyncStream):
                async for event in session:
                    if event.choices and event.choices[0].delta:
                        content = event.choices[0].delta.content
                        if content:
                            yield self._create_chunk(content, model.model, stream=True)
            else:
                content = session.choices[0].message.content
                if content:
                    yield self._create_chunk(content, model.model)
        except Exception as e:
            raise e

    def _create_chunk(self, content: str, model: str, stream: bool = False) -> Chunk:
        return Chunk(
            type=ChunkType.TEXT,
            text=content,
            chunk_metadata={
                "source": "chat_completions",
                "streaming": stream,
                "model": model,
            },
        )

    def _convert_messages_to_openai_format(
        self, messages: list[Message]
    ) -> list[ChatCompletionMessageParam]:
        """Convert internal messages to OpenAI chat completion format."""
        return [
            {"role": "user", "content": msg.text}
            if msg.type == MessageType.HUMAN
            else {"role": "developer", "content": msg.text}
            if msg.type == MessageType.SYSTEM
            else {"role": "assistant", "content": msg.text}
            for msg in (messages or [])
            if msg.type
            in (MessageType.HUMAN, MessageType.ASSISTANT, MessageType.SYSTEM)
        ]
