"""Common utilities for AI processors.

This module provides shared utilities for AI processor implementations to eliminate
code duplication and ensure consistency across different processor types.

Key utilities:
- Message format conversion (OpenAI format)
- Chunk creation helpers
- Model validation
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

    # Import types only for type checking to avoid circular dependencies
    # Actual imports happen at runtime in functions

logger = logging.getLogger(__name__)


def convert_messages_to_openai_format(
    messages: list[Any],
) -> list[dict[str, str]]:
    """Convert internal messages to OpenAI chat completion format.

    This is a common pattern across multiple processors (OpenAIChatCompletions,
    KnowledgeAIOpenAI) that converts internal Message objects to the format
    expected by OpenAI's API.

    The conversion includes:
    - Mapping MessageType to OpenAI roles (user, assistant, system)
    - Merging consecutive messages with the same role (except system)
    - Filtering out unsupported message types

    Args:
        messages: List of Message objects with type and text attributes

    Returns:
        List of dictionaries with 'role' and 'content' keys suitable for OpenAI API

    Example:
        ```python
        from appkit_assistant.backend.models import Message, MessageType

        messages = [
            Message(type=MessageType.SYSTEM, text="You are a helpful assistant"),
            Message(type=MessageType.HUMAN, text="Hello"),
            Message(type=MessageType.HUMAN, text="How are you?"),
        ]
        formatted = convert_messages_to_openai_format(messages)
        # Result: [
        #     {"role": "system", "content": "You are a helpful assistant"},
        #     {"role": "user", "content": "Hello\n\nHow are you?"}
        # ]
        ```

    Notes:
        - OpenAI Chat Completions requires that after any system messages,
          user/tool messages must alternate with assistant messages.
        - To ensure this, consecutive user or assistant messages are merged
          by concatenating their text with a blank line separator.
        - System messages are never merged.
    """
    # Import at runtime to avoid circular dependencies
    from appkit_assistant.backend.models import MessageType  # noqa: PLC0415

    formatted: list[dict[str, str]] = []
    role_map = {
        MessageType.HUMAN: "user",
        MessageType.SYSTEM: "system",
        MessageType.ASSISTANT: "assistant",
    }

    for msg in messages or []:
        if msg.type not in role_map:
            continue
        role = role_map[msg.type]

        # Merge consecutive messages with same role (except system)
        if formatted and role != "system" and formatted[-1]["role"] == role:
            formatted[-1]["content"] = formatted[-1]["content"] + "\n\n" + msg.text
        else:
            formatted.append({"role": role, "content": msg.text})

    return formatted


def create_text_chunk(
    text: str,
    source: str,
    model: str | None = None,
    streaming: bool = False,
    **extra_metadata: Any,
) -> Any:
    """Create a text chunk with consistent metadata.

    Provides a unified way to create text chunks across different processors,
    ensuring consistent metadata structure.

    Args:
        text: The text content of the chunk
        source: Source identifier (e.g., "chat_completions", "lorem_ipsum")
        model: Optional model identifier
        streaming: Whether this chunk is from a streaming response
        **extra_metadata: Additional metadata to include in the chunk

    Returns:
        Chunk object with TEXT type and standardized metadata

    Example:
        ```python
        chunk = create_text_chunk(
            text="Hello world",
            source="openai",
            model="gpt-4",
            streaming=True,
            session_id="abc123",
        )
        # chunk.chunk_metadata = {
        #     "source": "openai",
        #     "model": "gpt-4",
        #     "streaming": "true",
        #     "session_id": "abc123"
        # }
        ```
    """
    # Import at runtime to avoid circular dependencies
    from appkit_assistant.backend.models import Chunk, ChunkType  # noqa: PLC0415

    metadata = {
        "source": source,
        "streaming": str(streaming),
    }

    if model:
        metadata["model"] = model

    # Add any extra metadata
    metadata.update(extra_metadata)

    return Chunk(
        type=ChunkType.TEXT,
        text=text,
        chunk_metadata=metadata,
    )


def validate_model_support(
    model_id: str,
    supported_models: dict[str, Any],
    processor_name: str,
) -> None:
    """Validate that a model is supported by the processor.

    Common validation pattern used across all processors to check if a
    requested model is available.

    Args:
        model_id: The model ID to validate
        supported_models: Dictionary of supported models
        processor_name: Name of the processor for error messages

    Raises:
        ValueError: If the model is not supported

    Example:
        ```python
        validate_model_support(
            model_id="gpt-4",
            supported_models={"gpt-4": model_obj, "gpt-3.5-turbo": model_obj2},
            processor_name="OpenAI",
        )
        # Raises ValueError if model not found
        ```
    """
    if model_id not in supported_models:
        msg = f"Model {model_id} not supported by {processor_name} processor"
        logger.error(msg)
        raise ValueError(msg)
