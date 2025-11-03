import logging
from collections.abc import AsyncGenerator
from typing import Any

from openai import AsyncStream

from appkit_assistant.backend.models import (
    Chunk,
    MCPServer,
    Message,
)
from appkit_assistant.backend.processors.openai_base import BaseOpenAIProcessor
from appkit_commons.processors import (
    convert_messages_to_openai_format,
    create_text_chunk,
    validate_model_support,
)

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

        validate_model_support(model_id, self.models, "OpenAI Chat Completions")

        if mcp_servers:
            logger.warning(
                "MCP servers provided to ChatCompletionsProcessor but not supported. "
                "Use OpenAIResponsesProcessor for MCP functionality."
            )

        model = self.models[model_id]

        try:
            chat_messages = convert_messages_to_openai_format(messages)
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
                            yield create_text_chunk(
                                content,
                                source="chat_completions",
                                model=model.model,
                                streaming=True,
                            )
            else:
                content = session.choices[0].message.content
                if content:
                    yield create_text_chunk(
                        content,
                        source="chat_completions",
                        model=model.model,
                        streaming=False,
                    )
        except Exception as e:
            raise e
