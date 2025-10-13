"""Repository for MCP server data access operations."""

import logging

import reflex as rx

from manakit_assistant.backend.models import MCPServer

logger = logging.getLogger(__name__)


class MCPServerRepository:
    """Repository class for MCP server database operations."""

    @staticmethod
    async def get_all() -> list[MCPServer]:
        """Retrieve all MCP servers ordered by name."""
        async with rx.asession() as session:
            result = await session.exec(MCPServer.select().order_by(MCPServer.name))
            return result.all()

    @staticmethod
    async def get_by_id(server_id: int) -> MCPServer | None:
        """Retrieve an MCP server by ID."""
        async with rx.asession() as session:
            result = await session.exec(
                MCPServer.select().where(MCPServer.id == server_id)
            )
            return result.first()

    @staticmethod
    @staticmethod
    async def create(
        name: str,
        url: str,
        headers: str,
        description: str | None = None,
    ) -> MCPServer:
        """Create a new MCP server."""
        async with rx.asession() as session:
            server = MCPServer(
                name=name,
                url=url,
                headers=headers,
                description=description,
            )
            session.add(server)
            await session.commit()
            await session.refresh(server)
            logger.debug("Created MCP server: %s", name)
            return server

    @staticmethod
    async def update(
        server_id: int,
        name: str,
        url: str,
        headers: str,
        description: str | None = None,
    ) -> MCPServer | None:
        """Update an existing MCP server."""
        async with rx.asession() as session:
            result = await session.exec(
                MCPServer.select().where(MCPServer.id == server_id)
            )
            server = result.first()
            if server:
                server.name = name
                server.url = url
                server.headers = headers
                server.description = description
                await session.commit()
                await session.refresh(server)
                logger.debug("Updated MCP server: %s", name)
                return server
            logger.warning("MCP server with ID %s not found for update", server_id)
            return None

    @staticmethod
    async def delete(server_id: int) -> bool:
        """Delete an MCP server by ID."""
        async with rx.asession() as session:
            result = await session.exec(
                MCPServer.select().where(MCPServer.id == server_id)
            )
            server = result.first()
            if server:
                await session.delete(server)
                await session.commit()
                logger.debug("Deleted MCP server: %s", server.name)
                return True
            logger.warning("MCP server with ID %s not found for deletion", server_id)
            return False
