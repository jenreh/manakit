import asyncio
import logging
from collections.abc import AsyncGenerator
from typing import Any

from openai import AsyncOpenAI, AsyncStream

from appkit_assistant.backend.models import (
    AIModel,
    Chunk,
    MCPServer,
    Message,
)
from appkit_assistant.backend.processor import Processor
from appkit_commons.processors import (
    convert_messages_to_openai_format,
    create_text_chunk,
    validate_model_support,
)

logger = logging.getLogger(__name__)


class KnowledgeAIProcessor(Processor):
    """Processor that generates Knowledge AI text responses."""

    def __init__(
        self,
        server: str,
        api_key: str,
        models: dict[str, AIModel] | None = None,
        with_projects: bool = False,
    ) -> None:
        """Initialize the Knowledge AI processor."""
        super().__init__()
        self.api_key = api_key
        self.server = server
        self.models = models
        self.with_projects = with_projects

        if with_projects:
            self._initialize_models()

    def _initialize_models(self) -> None:
        """Initialize the models supported by this processor."""
        try:
            from knai_avvia.backend.models import Project  # noqa: PLC0415
            from knai_avvia.backend.project_repository import (  # noqa: PLC0415
                load_projects,  # noqa: E402
            )
        except ImportError as e:
            logger.error("knai_avvia package not available: %s", e)
            self.models = {}
            return

        try:
            projects: list[Project] = asyncio.run(
                load_projects(
                    url=self.server,
                    api_key=self.api_key,
                )
            )

            if self.models is None:
                self.models = {}

            for project in projects:
                project_key = f"{project.id}"
                self.models[project_key] = AIModel(
                    id=project_key,
                    text=project.name,
                    icon="avvia_intelligence",
                )
        except Exception as e:
            logger.error("Failed to load projects from Knowledge AI: %s", e)
            self.models = {}

    async def process(
        self,
        messages: list[Message],
        model_id: str,
        files: list[str] | None = None,  # noqa: ARG002
        mcp_servers: list[MCPServer] | None = None,  # noqa: ARG002
    ) -> AsyncGenerator[Chunk, None]:
        try:
            from knai_avvia.backend.chat_client import chat_completion  # noqa: PLC0415
        except ImportError as e:
            logger.error("knai_avvia package not available: %s", e)
            raise ImportError(
                "knai_avvia package is required for KnowledgeAIProcessor"
            ) from e

        validate_model_support(model_id, self.models, "KnowledgeAI")

        chat_messages = self._convert_messages(messages)

        try:
            result = await chat_completion(
                api_key=self.api_key,
                server=self.server,
                project_id=int(model_id),
                question=messages[-2].text,  # last human message
                history=chat_messages,
                temperature=0.05,
            )

            if result.answer:
                yield create_text_chunk(
                    result.answer,
                    source="knowledgeai",
                    model=model_id,
                    streaming=False,
                    project_id=model_id,
                )
        except Exception as e:
            raise e

    def get_supported_models(self) -> dict[str, AIModel]:
        return self.models if self.api_key else {}

    def _convert_messages(self, messages: list[Message]) -> list[dict[str, str]]:
        # Import needed for message type filtering
        from appkit_assistant.backend.models import MessageType  # noqa: PLC0415

        return [
            {"role": "Human", "message": msg.text}
            if msg.type == MessageType.HUMAN
            else {"role": "AI", "message": msg.text}
            for msg in (messages or [])
            if msg.type in (MessageType.HUMAN, MessageType.ASSISTANT)
        ]


class KnowledgeAIOpenAIProcessor(Processor):
    """Processor that generates Knowledge AI text responses."""

    def __init__(
        self,
        server: str,
        api_key: str,
        models: dict[str, AIModel] | None = None,
        with_projects: bool = False,
    ) -> None:
        """Initialize the Knowledge AI processor."""
        self.api_key = api_key
        self.server = server
        self.models = models
        self.with_projects = with_projects
        self.client = (
            AsyncOpenAI(api_key=self.api_key, base_url=self.server + "/api/openai/v1")
            if self.api_key
            else None
        )

        if self.with_projects:
            self._initialize_models()

    def _initialize_models(self) -> None:
        """Initialize the models supported by this processor."""
        try:
            from knai_avvia.backend.models import Project  # noqa: PLC0415
            from knai_avvia.backend.project_repository import (  # noqa: PLC0415
                load_projects,  # noqa: E402
            )
        except ImportError as e:
            logger.error("knai_avvia package not available: %s", e)
            self.models = {}
            return

        try:
            projects: list[Project] = asyncio.run(
                load_projects(
                    url=self.server,
                    api_key=self.api_key,
                )
            )

            if self.models is None:
                self.models = {}

            for project in projects:
                project_key = f"{project.id}"
                self.models[project_key] = AIModel(
                    id=project_key,
                    project_id=project.id,
                    text=project.name,
                    icon="avvia_intelligence",
                    stream=False,
                )
        except Exception as e:
            logger.error("Failed to load projects from Knowledge AI: %s", e)
            self.models = {}

    async def process(
        self,
        messages: list[Message],
        model_id: str,
        files: list[str] | None = None,  # noqa: ARG002
        mcp_servers: list[MCPServer] | None = None,  # noqa: ARG002
    ) -> AsyncGenerator[Chunk, None]:
        if not self.client:
            raise ValueError("KnowledgeAI OpenAI Client not initialized.")

        validate_model_support(model_id, self.models, "KnowledgeAI OpenAI")
        model = self.models[model_id]

        chat_messages = convert_messages_to_openai_format(messages)

        try:
            session_params: dict[str, Any] = {
                "model": model.model if model.project_id else model.id,
                "messages": chat_messages[:-1],
                "stream": model.stream,
            }
            if model.project_id:
                session_params["user"] = str(model.project_id)

            session = await self.client.chat.completions.create(**session_params)

            if isinstance(session, AsyncStream):
                async for event in session:
                    if event.choices and event.choices[0].delta:
                        content = event.choices[0].delta.content
                        if content:
                            yield create_text_chunk(
                                content,
                                source="knowledgeai_openai",
                                model=model_id,
                                streaming=True,
                            )
            elif session.choices and session.choices[0].message:
                content = session.choices[0].message.content
                if content:
                    logger.debug("Content:\n%s", content)
                    yield create_text_chunk(
                        content,
                        source="knowledgeai_openai",
                        model=model_id,
                        streaming=False,
                    )
        except Exception as e:
            logger.exception("Failed to get response from OpenAI: %s", e)
            raise e

    def get_supported_models(self) -> dict[str, AIModel]:
        return self.models if self.api_key else {}

    def _convert_messages(self, messages: list[Message]) -> list[dict[str, str]]:
        # Import needed for message type filtering
        from appkit_assistant.backend.models import MessageType  # noqa: PLC0415

        return [
            {"role": "Human", "message": msg.text}
            if msg.type == MessageType.HUMAN
            else {"role": "AI", "message": msg.text}
            for msg in (messages or [])
            if msg.type in (MessageType.HUMAN, MessageType.ASSISTANT)
        ]
