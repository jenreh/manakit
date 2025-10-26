import json
import logging
import uuid
from collections.abc import AsyncGenerator
from enum import StrEnum
from typing import Any

import reflex as rx
from pydantic import BaseModel

from manakit_assistant.backend.model_manager import ModelManager
from manakit_assistant.backend.models import (
    AIModel,
    Chunk,
    ChunkType,
    MCPServer,
    Message,
    MessageType,
    Suggestion,
    ThreadModel,
    ThreadStatus,
)
from manakit_assistant.backend.repositories import MCPServerRepository

logger = logging.getLogger(__name__)


class ThinkingType(StrEnum):
    REASONING = "reasoning"
    TOOL_CALL = "tool_call"


class ThinkingStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ERROR = "error"


class Thinking(BaseModel):
    type: ThinkingType
    id: str  # reasoning_session_id or tool_id
    text: str
    status: ThinkingStatus = ThinkingStatus.IN_PROGRESS
    tool_name: str | None = None
    parameters: str | None = None
    result: str | None = None
    error: str | None = None


class ThreadState(rx.State):
    _thread: ThreadModel = ThreadModel(thread_id=str(uuid.uuid4()))
    ai_models: list[AIModel] = []
    selected_model: str = ""
    processing: bool = False
    messages: list[Message] = []
    prompt: str = ""
    suggestions: list[Suggestion] = []

    # Chunk processing state
    current_chunks: list[Chunk] = []
    thinking_items: list[Thinking] = []  # Consolidated reasoning and tool calls
    image_chunks: list[Chunk] = []
    show_thinking: bool = False
    thinking_expanded: bool = False
    current_activity: str = ""
    current_reasoning_session: str = ""  # Track current reasoning session

    # MCP Server tool support state
    selected_mcp_servers: list[MCPServer] = []
    show_tools_modal: bool = False
    available_mcp_servers: list[MCPServer] = []
    temp_selected_mcp_servers: list[int] = []
    server_selection_state: dict[int, bool] = {}

    # Thread list integration
    with_thread_list: bool = False

    def initialize(self) -> None:
        """Initialize the state."""
        model_manager = ModelManager()
        self.ai_models = model_manager.get_all_models()
        self.selected_model = model_manager.get_default_model()

        self._thread = ThreadModel(
            thread_id=str(uuid.uuid4()),
            title="Neuer Chat",
            messages=[],
            state=ThreadStatus.NEW,
            ai_model=self.selected_model,
            active=True,
        )
        self.messages = []
        logger.debug("Initialized thread state: %s", self._thread)

    def set_thread(self, thread: ThreadModel) -> None:
        """Set the current thread model."""
        self._thread = thread
        self.messages = thread.messages
        self.selected_model = thread.ai_model
        logger.debug("Set current thread: %s", thread.thread_id)

    @rx.var
    def has_ai_models(self) -> bool:
        """Check if there are any chat models."""
        return len(self.ai_models) > 0

    @rx.var
    def has_suggestions(self) -> bool:
        """Check if there are any suggestions."""
        return self.suggestions is not None and len(self.suggestions) > 0

    @rx.var
    def get_ai_model(self) -> str | None:
        """Get the selected chat model."""
        return self.selected_model

    @rx.var
    def current_model_supports_tools(self) -> bool:
        """Check if the currently selected model supports tools."""
        if not self.selected_model:
            return False
        model = ModelManager().get_model(self.selected_model)
        return model.supports_tools if model else False

    @rx.var
    def unique_reasoning_sessions(self) -> list[str]:
        """Get unique reasoning session IDs."""
        return [
            item.id
            for item in self.thinking_items
            if item.type == ThinkingType.REASONING
        ]

    @rx.var
    def unique_tool_calls(self) -> list[str]:
        """Get unique tool call IDs."""
        return [
            item.id
            for item in self.thinking_items
            if item.type == ThinkingType.TOOL_CALL
        ]

    @rx.var
    def last_assistant_message_text(self) -> str:
        """Get the text of the last assistant message in the conversation."""
        for i in range(len(self.messages) - 1, -1, -1):
            if self.messages[i].type == MessageType.ASSISTANT:
                return self.messages[i].text
        return ""

    @rx.var
    def has_thinking_content(self) -> bool:
        """Check if there are any thinking items to display."""
        return len(self.thinking_items) > 0

    @rx.event
    def update_prompt(self, value: str) -> None:
        self.prompt = value

    @rx.event
    def clear(self) -> None:
        self._thread.messages = []
        self._thread.state = ThreadStatus.NEW
        self._thread.ai_model = ModelManager().get_default_model()
        self._thread.active = True
        self._thread.prompt = ""
        self.prompt = ""
        self.messages = []
        self.selected_mcp_servers = []
        self.current_chunks = []
        self.thinking_items = []  # Clear thinking items only on explicit clear
        self.image_chunks = []
        self.show_thinking = False

    @rx.event(background=True)
    async def process_message(self) -> None:
        logger.debug("Sending message: %s", self.prompt)

        async with self:
            # Check if already processing
            if self.processing:
                return

            self.processing = True
            self._clear_chunks()
            # Clear thinking items for new user question
            self.thinking_items = []

            current_prompt = self.prompt.strip()
            if not current_prompt:
                self.processing = False
                return

            self.prompt = ""

            # Add user message and empty assistant message
            self.messages.extend(
                [
                    Message(text=current_prompt, type=MessageType.HUMAN),
                    Message(text="", type=MessageType.ASSISTANT),
                ]
            )

            # Validate model and get processor
            if not self.get_ai_model:
                self._add_error_message("Kein Chat-Modell ausgewählt")
                self.processing = False
                return

        # Get processor outside context to avoid blocking
        processor = ModelManager().get_processor_for_model(self.get_ai_model)
        if not processor:
            async with self:
                self._add_error_message(
                    f"Keinen Adapter für das Modell gefunden: {self.get_ai_model}"
                )
                self.processing = False
            return

        try:
            # Process chunks
            async for chunk in processor.process(
                self.messages,
                self.get_ai_model,
                mcp_servers=self.selected_mcp_servers,
            ):
                async with self:
                    self._handle_chunk(chunk)

            async with self:
                self.show_thinking = False

                # Update thread if using thread list
                if self.with_thread_list:
                    await self._update_thread_list()

        except Exception as ex:
            async with self:
                self.messages.pop()  # Remove empty assistant message
                self.messages.append(Message(text=str(ex), type=MessageType.ERROR))
        finally:
            async with self:
                self.processing = False

    @rx.event
    async def submit_message(self) -> AsyncGenerator[Any, Any]:
        """Submit a message and reset the textarea."""
        yield ThreadState.process_message

    def _clear_chunks(self) -> None:
        """Clear all chunk categorization lists except thinking_items for display."""
        self.current_chunks = []
        # Don't clear thinking_items to preserve thinking display for previous messages
        # self.thinking_items = []
        self.image_chunks = []
        self.current_reasoning_session = ""  # Reset reasoning session for new message

    def _handle_chunk(self, chunk: Chunk) -> None:
        """Handle incoming chunk based on its type."""
        self.current_chunks.append(chunk)

        if chunk.type == ChunkType.TEXT:
            self.messages[-1].text += chunk.text
        elif chunk.type in (ChunkType.THINKING, ChunkType.THINKING_RESULT):
            self._handle_reasoning_chunk(chunk)
        elif chunk.type in (
            ChunkType.TOOL_CALL,
            ChunkType.TOOL_RESULT,
            ChunkType.ACTION,
        ):
            self._handle_tool_chunk(chunk)
        elif chunk.type in (ChunkType.IMAGE, ChunkType.IMAGE_PARTIAL):
            self.image_chunks.append(chunk)
        elif chunk.type == ChunkType.COMPLETION:
            self.show_thinking = False
            logger.debug("Response generation completed")
        elif chunk.type == ChunkType.ERROR:
            self.messages.append(Message(text=chunk.text, type=MessageType.ERROR))
            logger.error("Chunk error: %s", chunk.text)
        else:
            logger.warning("Unhandled chunk type: %s - %s", chunk.type, chunk.text)

    def _handle_reasoning_chunk(self, chunk: Chunk) -> None:
        """Handle reasoning chunks by consolidating them into thinking items."""
        if chunk.type == ChunkType.THINKING:
            self.show_thinking = True
            logger.debug("Thinking: %s", chunk.text)

        reasoning_session = self._get_or_create_reasoning_session(chunk)
        existing_item = self._find_existing_reasoning_item(reasoning_session)

        if existing_item:
            self._update_existing_reasoning_item(existing_item, chunk)
        else:
            self._create_new_reasoning_item(reasoning_session, chunk)

    def _get_or_create_reasoning_session(self, chunk: Chunk) -> str:
        """Get reasoning session ID from metadata or create new one."""
        reasoning_session = chunk.chunk_metadata.get("reasoning_session")
        if reasoning_session:
            return reasoning_session

        # If no session ID in metadata, create separate sessions based on context
        last_item = self.thinking_items[-1] if self.thinking_items else None

        # Create new session if needed
        should_create_new_session = (
            not self.current_reasoning_session
            or (last_item and last_item.type == ThinkingType.TOOL_CALL)
            or (
                last_item
                and last_item.type == ThinkingType.REASONING
                and last_item.status == ThinkingStatus.COMPLETED
            )
        )

        if should_create_new_session:
            self.current_reasoning_session = f"reasoning_{uuid.uuid4().hex[:8]}"

        return self.current_reasoning_session

    def _find_existing_reasoning_item(self, reasoning_session: str) -> Thinking | None:
        """Find existing reasoning item by session ID."""
        for item in self.thinking_items:
            if item.type == ThinkingType.REASONING and item.id == reasoning_session:
                return item
        return None

    def _update_existing_reasoning_item(
        self, existing_item: Thinking, chunk: Chunk
    ) -> None:
        """Update existing reasoning item with new chunk data."""
        if chunk.type == ChunkType.THINKING:
            if existing_item.text:
                existing_item.text += f"\n{chunk.text}"
            else:
                existing_item.text = chunk.text
        elif chunk.type == ChunkType.THINKING_RESULT:
            existing_item.status = ThinkingStatus.COMPLETED
            if chunk.text:
                existing_item.text += f" {chunk.text}"
        # Trigger Reflex reactivity by reassigning the list
        self.thinking_items = self.thinking_items.copy()

    def _create_new_reasoning_item(self, reasoning_session: str, chunk: Chunk) -> None:
        """Create new reasoning item."""
        status = (
            ThinkingStatus.COMPLETED
            if chunk.type == ChunkType.THINKING_RESULT
            else ThinkingStatus.IN_PROGRESS
        )
        new_item = Thinking(
            type=ThinkingType.REASONING,
            id=reasoning_session,
            text=chunk.text,
            status=status,
        )
        self.thinking_items = [*self.thinking_items, new_item]

    def _handle_tool_chunk(self, chunk: Chunk) -> None:
        """Handle tool chunks by consolidating them into thinking items."""
        tool_id = chunk.chunk_metadata.get("tool_id")
        if not tool_id:
            # Generate a tool ID if not provided
            tool_count = len(
                [i for i in self.thinking_items if i.type == ThinkingType.TOOL_CALL]
            )
            tool_id = f"tool_{tool_count}"

        # Find existing tool item or create new one
        existing_item = self._find_existing_tool_item(tool_id)

        if existing_item:
            self._update_existing_tool_item(existing_item, chunk)
        else:
            self._create_new_tool_item(tool_id, chunk)

        logger.debug("Tool event: %s - %s", chunk.type, chunk.text)

    def _find_existing_tool_item(self, tool_id: str) -> Thinking | None:
        """Find existing tool item by ID."""
        for item in self.thinking_items:
            if item.type == ThinkingType.TOOL_CALL and item.id == tool_id:
                return item
        return None

    def _update_existing_tool_item(self, existing_item: Thinking, chunk: Chunk) -> None:
        """Update existing tool item with new chunk data."""
        if chunk.type == ChunkType.TOOL_CALL:
            # Store parameters separately from text
            existing_item.parameters = chunk.chunk_metadata.get(
                "parameters", chunk.text
            )
            existing_item.text = chunk.chunk_metadata.get("description", "")
            # Only set tool_name if it's not already present
            if not existing_item.tool_name:
                existing_item.tool_name = chunk.chunk_metadata.get(
                    "tool_name", "Unknown"
                )
            existing_item.status = ThinkingStatus.IN_PROGRESS
        elif chunk.type == ChunkType.TOOL_RESULT:
            self._handle_tool_result(existing_item, chunk)
        elif chunk.type == ChunkType.ACTION:
            existing_item.text += f"\n---\nAktion: {chunk.text}"
        # Trigger Reflex reactivity by reassigning the list
        self.thinking_items = self.thinking_items.copy()

    def _handle_tool_result(self, existing_item: Thinking, chunk: Chunk) -> None:
        """Handle tool result chunk."""
        # Check if this is an error result
        is_error = (
            "error" in chunk.text.lower()
            or "failed" in chunk.text.lower()
            or chunk.chunk_metadata.get("error")
        )
        existing_item.status = (
            ThinkingStatus.ERROR if is_error else ThinkingStatus.COMPLETED
        )
        # Store result separately from text
        existing_item.result = chunk.text
        if is_error:
            existing_item.error = chunk.text

    def _create_new_tool_item(self, tool_id: str, chunk: Chunk) -> None:
        """Create new tool item."""
        tool_name = chunk.chunk_metadata.get("tool_name", "Unknown")
        status = ThinkingStatus.IN_PROGRESS
        text = ""
        parameters = None
        result = None

        if chunk.type == ChunkType.TOOL_CALL:
            # Store parameters separately from text
            parameters = chunk.chunk_metadata.get("parameters", chunk.text)
            text = chunk.chunk_metadata.get("description", "")
        elif chunk.type == ChunkType.TOOL_RESULT:
            is_error = "error" in chunk.text.lower() or "failed" in chunk.text.lower()
            status = ThinkingStatus.ERROR if is_error else ThinkingStatus.COMPLETED
            result = chunk.text
        else:
            text = chunk.text

        new_item = Thinking(
            type=ThinkingType.TOOL_CALL,
            id=tool_id,
            text=text,
            status=status,
            tool_name=tool_name,
            parameters=parameters,
            result=result,
            error=chunk.text if status == ThinkingStatus.ERROR else None,
        )
        self.thinking_items = [*self.thinking_items, new_item]

    def _add_error_message(self, error_msg: str) -> None:
        """Add an error message to the conversation."""
        logger.error(error_msg)
        self.messages.append(Message(text=error_msg, type=MessageType.ERROR))

    async def _update_thread_list(self) -> None:
        """Update the thread list with current messages."""
        threadlist_state: ThreadListState = await self.get_state(ThreadListState)
        if self._thread.title in {"", "Neuer Chat"}:
            self._thread.title = (
                self.messages[0].text if self.messages else "Neuer Chat"
            )

        self._thread.messages = self.messages
        self._thread.ai_model = self.selected_model
        await threadlist_state.update_thread(self._thread)

    def toggle_thinking_expanded(self) -> None:
        """Toggle the expanded state of the thinking section."""
        self.thinking_expanded = not self.thinking_expanded

    # MCP Server tool support event handlers
    @rx.event
    async def load_available_mcp_servers(self) -> None:
        """Load available MCP servers from the database."""
        self.available_mcp_servers = await MCPServerRepository.get_all()

    @rx.event
    def open_tools_modal(self) -> None:
        """Open the tools modal."""
        self.temp_selected_mcp_servers = [
            server.id for server in self.selected_mcp_servers if server.id
        ]
        self.server_selection_state = {
            server.id: server.id in self.temp_selected_mcp_servers
            for server in self.available_mcp_servers
            if server.id
        }
        self.show_tools_modal = True

    @rx.event
    def set_show_tools_modal(self, show: bool) -> None:
        """Set the visibility of the tools modal."""
        self.show_tools_modal = show

    @rx.event
    def toggle_mcp_server_selection(self, server_id: int, selected: bool) -> None:
        """Toggle MCP server selection in the modal."""
        self.server_selection_state[server_id] = selected
        if selected and server_id not in self.temp_selected_mcp_servers:
            self.temp_selected_mcp_servers.append(server_id)
        elif not selected and server_id in self.temp_selected_mcp_servers:
            self.temp_selected_mcp_servers.remove(server_id)

    @rx.event
    def apply_mcp_server_selection(self) -> None:
        """Apply the temporary MCP server selection."""
        self.selected_mcp_servers = [
            server
            for server in self.available_mcp_servers
            if server.id in self.temp_selected_mcp_servers
        ]
        self.show_tools_modal = False

    def is_mcp_server_selected(self, server_id: int) -> bool:
        """Check if an MCP server is selected."""
        return server_id in self.temp_selected_mcp_servers

    def set_selected_model(self, model_id: str) -> None:
        """Set the selected model."""
        self.selected_model = model_id
        self._thread.ai_model = model_id


class ThreadListState(rx.State):
    """State for the thread list component."""

    thread_store: str = rx.LocalStorage("{}", name="asui-threads", sync=True)
    threads: list[ThreadModel] = []
    active_thread_id: str = ""
    autosave: bool = False

    @rx.var
    def has_threads(self) -> bool:
        """Check if there are any threads."""
        return len(self.threads) > 0

    async def initialize(self, autosave: bool = False) -> None:
        """Initialize the thread list state."""
        self.autosave = autosave
        await self.load_threads()
        logger.debug("Initialized thread list state")

    async def load_threads(self) -> None:
        """Load threads from browser local storage."""
        try:
            thread_data = json.loads(self.thread_store)
            if thread_data and "threads" in thread_data:
                self.threads = [
                    ThreadModel(**thread) for thread in thread_data["threads"]
                ]
                self.active_thread_id = thread_data.get("active_thread_id", "")
                if self.active_thread_id:
                    await self.select_thread(self.active_thread_id)
        except Exception as e:
            logger.error("Error loading threads from local storage: %s", e)
            self.threads = []
            self.active_thread_id = ""

    async def save_threads(self) -> None:
        """Save threads to browser local storage."""
        try:
            thread_list = []
            for thread in self.threads:
                thread_dict = thread.dict()
                if thread.messages:
                    thread_dict["messages"] = [msg.dict() for msg in thread.messages]
                thread_list.append(thread_dict)

            thread_data = {
                "threads": thread_list,
                "active_thread_id": self.active_thread_id,
            }
            self.thread_store = json.dumps(thread_data)
            logger.debug("Saved threads to local storage")
        except Exception as e:
            logger.error("Error saving threads to local storage: %s", e)

    async def reset_thread_store(self) -> None:
        self.thread_store = "{}"

    async def get_thread(self, thread_id: str) -> ThreadModel | None:
        """Get a thread by its ID."""
        for thread in self.threads:
            if thread.thread_id == thread_id:
                return thread
        return None

    async def create_thread(self) -> None:
        """Create a new thread."""
        new_thread = ThreadModel(
            thread_id=str(uuid.uuid4()),
            title="Neuer Chat",
            messages=[],
            state=ThreadStatus.NEW,
            ai_model=ModelManager().get_default_model(),
            active=True,
        )
        self.threads.insert(0, new_thread)
        await self.select_thread(new_thread.thread_id)

        logger.debug("Created new thread: %s", new_thread)

    async def update_thread(self, thread: ThreadModel) -> None:
        """Update a thread."""
        existing_thread = await self.get_thread(thread.thread_id)
        if existing_thread:
            existing_thread.title = thread.title
            existing_thread.messages = thread.messages
            existing_thread.state = thread.state
            existing_thread.active = thread.active
            existing_thread.ai_model = thread.ai_model

        if self.autosave:
            await self.save_threads()
        logger.debug("Updated thread: %s", thread.thread_id)

    async def delete_thread(self, thread_id: str) -> AsyncGenerator[Any, Any]:
        """Delete a thread if not active."""
        if thread_id == self.active_thread_id:
            yield rx.toast.error(
                "Aktiver Chat kann nicht gelöscht werden.",
                position="top-right",
                close_button=True,
            )
            return

        thread = await self.get_thread(thread_id)
        if not thread:
            yield rx.toast.error(
                "Chat nicht gefunden.", position="top-right", close_button=True
            )
            logger.warning("Thread with ID %s not found.", thread_id)
            return

        self.threads.remove(thread)
        await self.save_threads()
        yield rx.toast.info(
            f"Chat '{thread.title}' erfolgreich gelöscht.",
            position="top-right",
            close_button=True,
        )
        await self.select_thread(self.active_thread_id)

    async def select_thread(self, thread_id: str) -> None:
        """Select a thread."""
        for thread in self.threads:
            thread.active = thread.thread_id == thread_id
        self.active_thread_id = thread_id
        active_thread = await self.get_thread(thread_id)

        if active_thread:
            thread_state: ThreadState = await self.get_state(ThreadState)
            thread_state.set_thread(active_thread)
            thread_state.messages = active_thread.messages
            thread_state.selected_model = active_thread.ai_model
            thread_state.with_thread_list = True
