import json
import logging
from collections.abc import AsyncGenerator
from typing import Any

from manakit_assistant.backend.models import (
    AIModel,
    Chunk,
    ChunkType,
    MCPServer,
    Message,
    MessageType,
)
from manakit_assistant.backend.processors.openai_base import BaseOpenAIProcessor

logger = logging.getLogger(__name__)


class OpenAIResponsesProcessor(BaseOpenAIProcessor):
    """Simplified processor using content accumulator pattern."""

    def __init__(
        self,
        models: dict[str, AIModel],
        api_key: str | None = None,
        base_url: str | None = None,
        is_azure: bool = False,
    ) -> None:
        super().__init__(models, api_key, base_url, is_azure)
        self._current_reasoning_session: str | None = None

    async def process(
        self,
        messages: list[Message],
        model_id: str,
        files: list[str] | None = None,  # noqa: ARG002
        mcp_servers: list[MCPServer] | None = None,
        payload: dict[str, Any] | None = None,
    ) -> AsyncGenerator[Chunk, None]:
        """Process messages using simplified content accumulator pattern."""
        if not self.client:
            raise ValueError("OpenAI Client not initialized.")

        if model_id not in self.models:
            msg = f"Model {model_id} not supported by OpenAI processor"
            raise ValueError(msg)

        model = self.models[model_id]

        try:
            session = await self._create_responses_request(
                messages, model, mcp_servers, payload
            )

            if hasattr(session, "__aiter__"):  # Streaming
                async for event in session:
                    chunk = self._handle_event(event)
                    if chunk:
                        yield chunk
            else:  # Non-streaming
                content = self._extract_responses_content(session)
                if content:
                    yield Chunk(
                        chunk_type=ChunkType.TEXT,
                        content=content,
                        chunk_metadata={
                            "source": "responses_api",
                            "streaming": "false",
                        },
                    )
        except Exception as e:
            raise e

    def _handle_event(self, event: Any) -> Chunk | None:
        """Simplified event handler returning actual event content in chunks."""
        if not hasattr(event, "type"):
            return None

        event_type = event.type
        logger.debug("Event: %s", event)

        # Try different handlers in order
        handlers = [
            self._handle_lifecycle_events,
            lambda et: self._handle_text_events(et, event),
            lambda et: self._handle_item_events(et, event),
            lambda et: self._handle_mcp_events(et, event),
            lambda et: self._handle_content_events(et, event),
            lambda et: self._handle_completion_events(et, event),
            lambda et: self._handle_image_events(et, event),
        ]

        for handler in handlers:
            result = handler(event_type)
            if result:
                return result

        # Log unhandled events for debugging
        logger.debug("Unhandled event type: %s", event_type)
        return None

    def _handle_lifecycle_events(self, event_type: str) -> Chunk | None:
        """Handle lifecycle events."""
        lifecycle_events = {
            "response.created": ("created", {"stage": "created"}),
            "response.in_progress": ("in_progress", {"stage": "in_progress"}),
            "response.done": ("done", {"stage": "done"}),
        }

        if event_type in lifecycle_events:
            content, metadata = lifecycle_events[event_type]
            chunk_type = (
                ChunkType.LIFECYCLE
                if event_type != "response.done"
                else ChunkType.COMPLETION
            )
            return self._create_chunk(chunk_type, content, metadata)
        return None

    def _handle_text_events(self, event_type: str, event: Any) -> Chunk | None:
        """Handle text-related events."""
        if event_type == "response.output_text.delta":
            return self._create_chunk(
                ChunkType.TEXT, event.delta, {"delta": event.delta}
            )

        if event_type == "response.output_text.annotation.added":
            return self._create_chunk(
                ChunkType.ANNOTATION,
                event.annotation,
                {"annotation": event.annotation},
            )

        if (
            event_type == "response.content_part.added"
            and hasattr(event, "part")
            and hasattr(event.part, "text")
        ):
            return self._create_chunk(
                ChunkType.TEXT, event.part.text, {"content_part": "added"}
            )
        return None

    def _handle_item_events(self, event_type: str, event: Any) -> Chunk | None:
        """Handle item added/done events for MCP calls and reasoning."""
        if (
            event_type == "response.output_item.added"
            and hasattr(event, "item")
            and hasattr(event.item, "type")
        ):
            return self._handle_item_added(event.item)

        if (
            event_type == "response.output_item.done"
            and hasattr(event, "item")
            and hasattr(event.item, "type")
        ):
            return self._handle_item_done(event.item)

        return None

    def _handle_item_added(self, item: Any) -> Chunk | None:
        """Handle when an item is added."""
        if item.type == "mcp_call":
            tool_name = getattr(item, "name", "unknown_tool")
            tool_id = getattr(item, "id", "unknown_id")
            server_label = getattr(item, "server_label", "unknown_server")
            return self._create_chunk(
                ChunkType.TOOL_CALL,
                f"Benutze Werkzeug: {server_label}.{tool_name}",
                {
                    "tool_name": tool_name,
                    "tool_id": tool_id,
                    "server_label": server_label,
                    "status": "starting",
                    "reasoning_session": self._current_reasoning_session,
                },
            )

        if item.type == "reasoning":
            reasoning_id = getattr(item, "id", "unknown_id")
            # Track the current reasoning session
            self._current_reasoning_session = reasoning_id
            return self._create_chunk(
                ChunkType.THINKING,
                "Denke nach...",
                {"reasoning_id": reasoning_id, "status": "starting"},
            )
        return None

    def _handle_item_done(self, item: Any) -> Chunk | None:
        """Handle when an item is completed."""
        if item.type == "mcp_call":
            return self._handle_mcp_call_done(item)

        if item.type == "reasoning":
            reasoning_id = getattr(item, "id", "unknown_id")
            summary = getattr(item, "summary", [])
            summary_text = str(summary) if summary else "beendet."
            return self._create_chunk(
                ChunkType.THINKING_RESULT,
                summary_text,
                {"reasoning_id": reasoning_id, "status": "completed"},
            )
        return None

    def _handle_mcp_call_done(self, item: Any) -> Chunk | None:
        """Handle MCP call completion."""
        tool_id = getattr(item, "id", "unknown_id")
        tool_name = getattr(item, "name", "unknown_tool")
        error = getattr(item, "error", None)
        output = getattr(item, "output", None)

        if error:
            error_text = self._extract_error_text(error)
            return self._create_chunk(
                ChunkType.TOOL_RESULT,
                f"Werkzeugfehler: {error_text}",
                {
                    "tool_id": tool_id,
                    "tool_name": tool_name,
                    "status": "error",
                    "error": True,
                    "error_details": str(error),
                    "reasoning_session": self._current_reasoning_session,
                },
            )

        output_text = str(output) if output else "Werkzeug erfolgreich aufgerufen"
        return self._create_chunk(
            ChunkType.TOOL_RESULT,
            output_text,
            {
                "tool_id": tool_id,
                "tool_name": tool_name,
                "status": "completed",
                "reasoning_session": self._current_reasoning_session,
            },
        )

    def _extract_error_text(self, error: Any) -> str:
        """Extract readable error text from error object."""
        if isinstance(error, dict) and "content" in error:
            content = error["content"]
            if isinstance(content, list) and content:
                return content[0].get("text", str(error))
        return "Unknown error"

    def _handle_mcp_events(self, event_type: str, event: Any) -> Chunk | None:
        """Handle MCP-specific events."""
        # if event_type == "response.mcp_call_arguments.delta":
        #     tool_id = getattr(event, "item_id", "unknown_id")
        #     arguments_delta = getattr(event, "delta", "")
        #     return self._create_chunk(
        #         ChunkType.TOOL_CALL,
        #         arguments_delta,
        #         {
        #             "tool_id": tool_id,
        #             "status": "arguments_streaming",
        #             "delta": arguments_delta,
        #             "reasoning_session": self._current_reasoning_session,
        #         },
        #     )

        if event_type == "response.mcp_call_arguments.done":
            tool_id = getattr(event, "item_id", "unknown_id")
            arguments = getattr(event, "arguments", "")
            return self._create_chunk(
                ChunkType.TOOL_CALL,
                f"Parameter: {arguments}",
                {
                    "tool_id": tool_id,
                    "status": "arguments_complete",
                    "arguments": arguments,
                    "reasoning_session": self._current_reasoning_session,
                },
            )

        if event_type == "response.mcp_call.failed":
            tool_id = getattr(event, "item_id", "unknown_id")
            return self._create_chunk(
                ChunkType.TOOL_RESULT,
                f"Werkzeugnutzung abgebrochen: {tool_id}",
                {
                    "tool_id": tool_id,
                    "status": "failed",
                    "error": True,
                    "reasoning_session": self._current_reasoning_session,
                },
            )

        # if event_type == "response.mcp_call.in_progress":
        #     tool_id = getattr(event, "item_id", "unknown_id")
        #     return self._create_chunk(
        #         ChunkType.TOOL_CALL,
        #         "Tool call in progress...",
        #         {"tool_id": tool_id, "status": "in_progress"},
        #     )

        # if event_type == "response.mcp_list_tools.in_progress":
        #     tool_id = getattr(event, "item_id", "unknown_id")
        #     return self._create_chunk(
        #         ChunkType.TOOL_CALL,
        #         "Lade verfügbare Werkzeuge...",
        #         {"tool_id": tool_id, "status": "listing_tools"},
        #     )

        # if event_type == "response.mcp_list_tools.completed":
        #     tool_id = getattr(event, "item_id", "unknown_id")
        #     return self._create_chunk(
        #         ChunkType.TOOL_RESULT,
        #         "Verfügbare Werkzeuge geladen.",
        #         {"tool_id": tool_id, "status": "tools_listed"},
        #     )

        return None

    def _handle_content_events(self, event_type: str, event: Any) -> Chunk | None:  # noqa: ARG002
        """Handle content-related events."""
        if event_type == "response.content_part.added":
            # Content part added - this typically starts text streaming
            return None  # No need to show this as a separate chunk

        if event_type == "response.content_part.done":
            # Content part completed - this typically ends text streaming
            return None  # No need to show this as a separate chunk

        # if event_type == "response.output_text.done":
        #     # Text output completed - this contains the final text
        #     text = getattr(event, "text", "")
        #     if text:  # Only create chunk if there's actual text content
        #         return self._create_chunk(
        #             ChunkType.TEXT,
        #             text,
        #             {"status": "text_complete", "final_text": True},
        #         )
        return None

    def _handle_completion_events(self, event_type: str, event: Any) -> Chunk | None:  # noqa: ARG002
        """Handle completion-related events."""
        if event_type == "response.completed":
            return self._create_chunk(
                ChunkType.COMPLETION,
                "Response generation completed",
                {"status": "response_complete"},
            )
        return None

    def _handle_image_events(self, event_type: str, event: Any) -> Chunk | None:
        """Handle image-related events."""
        if "image" in event_type and (hasattr(event, "url") or hasattr(event, "data")):
            image_data = {
                "url": getattr(event, "url", ""),
                "data": getattr(event, "data", ""),
            }
            image_str = str(image_data)
            return self._create_chunk(ChunkType.IMAGE, image_str, image_data)
        return None

    def _create_chunk(
        self,
        chunk_type: ChunkType,
        content: str,
        extra_metadata: dict[str, str] | None = None,
    ) -> Chunk:
        """Create a Chunk with actual content from the event"""
        metadata = {
            "processor": "openai_responses_simplified",
        }

        if extra_metadata:
            # Ensure all metadata values are strings
            for key, value in extra_metadata.items():
                if value is not None:
                    metadata[key] = str(value)

        return Chunk(
            type=chunk_type,
            text=content,
            chunk_metadata=metadata,
        )

    async def _create_responses_request(
        self,
        messages: list[Message],
        model: AIModel,
        mcp_servers: list[MCPServer] | None = None,
        payload: dict[str, Any] | None = None,
    ) -> Any:
        """Create a simplified responses API request."""
        # Convert messages to responses format
        input_messages = self._convert_messages_to_responses_format(messages)

        # Extract system message if present
        system_message = self._extract_system_message(messages)

        # Configure MCP tools if provided
        tools = self._configure_mcp_tools(mcp_servers) if mcp_servers else []

        params = {
            "model": model.model,
            "input": input_messages,
            "stream": model.stream,
            "temperature": model.temperature,
            "tools": tools,
            "reasoning": {"effort": "medium"},
            **(payload or {}),
        }

        # Add system message if present
        if system_message:
            params["system"] = system_message

        return await self.client.responses.create(**params)

    def _configure_mcp_tools(
        self, mcp_servers: list[MCPServer] | None
    ) -> list[dict[str, Any]]:
        """Configure MCP servers as tools for the responses API."""
        if not mcp_servers:
            return []

        tools = []
        for server in mcp_servers:
            tool_config = {
                "type": "mcp",
                "server_label": server.name,
                "server_url": server.url,
                "require_approval": "never",
            }

            if server.headers and server.headers != "{}":
                tool_config["headers"] = json.loads(server.headers)

            tools.append(tool_config)

        return tools

    def _convert_messages_to_responses_format(
        self, messages: list[Message]
    ) -> list[dict[str, Any]]:
        """Convert messages to the responses API input format."""
        input_messages = []

        for msg in messages:
            if msg.type == MessageType.SYSTEM:
                continue  # System messages are handled differently

            role = "user" if msg.type == MessageType.HUMAN else "assistant"
            content_type = "input_text" if role == "user" else "output_text"
            input_messages.append(
                {"role": role, "content": [{"type": content_type, "text": msg.text}]}
            )

        return input_messages

    def _extract_system_message(self, messages: list[Message]) -> str | None:
        """Extract system message from messages list."""
        for msg in messages:
            if msg.type == MessageType.SYSTEM:
                return msg.text
        return None

    def _extract_responses_content(self, session: Any) -> str | None:
        """Extract content from non-streaming responses."""
        if (
            hasattr(session, "output")
            and session.output
            and isinstance(session.output, list)
            and session.output
        ):
            first_output = session.output[0]
            if hasattr(first_output, "content") and first_output.content:
                if isinstance(first_output.content, list):
                    return first_output.content[0].get("text", "")
                return str(first_output.content)
        return None
