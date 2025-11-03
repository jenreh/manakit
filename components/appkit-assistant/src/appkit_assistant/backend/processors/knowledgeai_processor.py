import asyncio
import logging
from collections.abc import AsyncGenerator
from typing import Any

from openai import AsyncOpenAI, AsyncStream
from openai.types.chat import ChatCompletionMessageParam

from appkit_assistant.backend.models import (
    AIModel,
    Chunk,
    ChunkType,
    MCPServer,
    Message,
    MessageType,
)
from appkit_assistant.backend.processor import Processor

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

        if model_id not in self.models:
            logger.error("Model %s not supported by OpenAI processor", model_id)
            raise ValueError(f"Model {model_id} not supported by OpenAI processor")

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
                yield Chunk(
                    type=ChunkType.TEXT,
                    text=result.answer,
                    chunk_metadata={
                        "source": "knowledgeai",
                        "project_id": model_id,
                        "streaming": str(False),
                    },
                )
        except Exception as e:
            raise e

    def get_supported_models(self) -> dict[str, AIModel]:
        return self.models if self.api_key else {}

    def _convert_messages(self, messages: list[Message]) -> list[dict[str, str]]:
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

        model = self.models.get(model_id)
        if not model:
            raise ValueError(
                "Model %s not supported by KnowledgeAI processor", model_id
            )

        chat_messages = self._convert_messages_to_openai_format(messages)

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
                            yield Chunk(
                                type=ChunkType.TEXT,
                                text=content,
                                chunk_metadata={
                                    "source": "knowledgeai_openai",
                                    "streaming": str(True),
                                    "model_id": model_id,
                                },
                            )
            elif session.choices and session.choices[0].message:
                content = session.choices[0].message.content
                if content:
                    logger.debug("Content:\n%s", content)
                    yield Chunk(
                        type=ChunkType.TEXT,
                        text=content,
                        chunk_metadata={
                            "source": "knowledgeai_openai",
                            "streaming": str(False),
                            "model_id": model_id,
                        },
                    )
        except Exception as e:
            logger.exception("Failed to get response from OpenAI: %s", e)
            raise e

    def get_supported_models(self) -> dict[str, AIModel]:
        return self.models if self.api_key else {}

    def _convert_messages_to_openai_format(
        self, messages: list[Message]
    ) -> list[ChatCompletionMessageParam]:
        formatted: list[ChatCompletionMessageParam] = []
        role_map = {
            MessageType.HUMAN: "user",
            MessageType.SYSTEM: "system",
            MessageType.ASSISTANT: "assistant",
        }

        for msg in messages or []:
            if msg.type not in role_map:
                continue
            role = role_map[msg.type]
            if formatted and role != "system" and formatted[-1]["role"] == role:
                formatted[-1]["content"] = formatted[-1]["content"] + "\n\n" + msg.text
            else:
                formatted.append({"role": role, "content": msg.text})

        return formatted
