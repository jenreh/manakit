"""FastAPI endpoints for MCP Apps resource proxying and tool calls.

These endpoints are called by the McpAppBridge frontend component to:
- Fetch HTML resources from MCP servers (proxied through backend)
- Forward tool calls from MCP App iframes to MCP servers
- List UI-enabled tools for a given server

Authentication: every endpoint requires a valid session. The user
identity is resolved server-side from the session cookie by
``require_session``; callers cannot supply their own user id.
"""

import json as _json
import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from appkit_assistant.backend.database.models import MCPServer
from appkit_assistant.backend.database.repositories import mcp_server_repo
from appkit_assistant.backend.services.mcp_apps_service import (
    McpAppsService,
)
from appkit_assistant.backend.services.mcp_auth_service import MCPAuthService
from appkit_assistant.backend.services.mcp_token_service import (
    MCPTokenService,
)
from appkit_commons.database.session import get_asyncdb_session
from appkit_user.authentication.http_guard import RequiredSession

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/mcp-apps", tags=["mcp-apps"])

# Lazily initialized service instances
_mcp_apps_service: McpAppsService | None = None


def _get_mcp_apps_service() -> McpAppsService:
    """Get or create the shared McpAppsService instance.

    Lazily initializes the service with its dependencies
    to avoid import-time instantiation issues.
    """
    global _mcp_apps_service  # noqa: PLW0603
    if _mcp_apps_service is None:
        auth_service = MCPAuthService(redirect_uri="")
        token_service = MCPTokenService(mcp_auth_service=auth_service)
        _mcp_apps_service = McpAppsService(token_service=token_service)
    return _mcp_apps_service


class ToolCallRequest(BaseModel):
    """Request body for proxying a tool call."""

    tool_name: str
    arguments: dict[str, Any] = {}


async def _get_server(server_id: int) -> MCPServer:
    """Retrieve an MCP server by ID or raise 404.

    Args:
        server_id: The MCP server ID

    Returns:
        The MCPServer instance

    Raises:
        HTTPException: If server is not found
    """
    async with get_asyncdb_session() as session:
        server = await mcp_server_repo.find_by_id(session, server_id)
        if not server:
            raise HTTPException(
                status_code=404,
                detail="MCP server not found",
            )
        return server


@router.get("/{server_id}/resource")
async def get_resource(
    server_id: int,
    uri: str,
    user: RequiredSession,
) -> HTMLResponse:
    """Fetch an MCP App resource (HTML content) from a server.

    Returns the HTML content with text/html content type.
    Resource metadata (CSP, prefersBorder) is forwarded as X-MCP-* headers
    so the McpAppBridge frontend can apply security policies and visual
    preferences without parsing the HTML body.
    """
    server = await _get_server(server_id)

    resource = await _get_mcp_apps_service().fetch_resource(server, user.user_id, uri)
    if not resource:
        raise HTTPException(
            status_code=502,
            detail="Failed to fetch resource from MCP server",
        )

    extra_headers: dict[str, str] = {
        "X-MCP-Resource-URI": resource.uri,
    }
    if resource.csp is not None:
        extra_headers["X-MCP-CSP"] = _json.dumps(resource.csp)
    if resource.permissions is not None:
        extra_headers["X-MCP-Permissions"] = _json.dumps(resource.permissions)
    if resource.prefers_border is not None:
        extra_headers["X-MCP-Prefers-Border"] = str(resource.prefers_border).lower()

    return HTMLResponse(
        content=resource.html_content,
        headers=extra_headers,
    )


@router.post("/{server_id}/tools/call")
async def call_tool(
    server_id: int,
    request: ToolCallRequest,
    user: RequiredSession,
) -> dict[str, Any]:
    """Proxy a tool call from an MCP App iframe to the MCP server.

    This is the endpoint that McpAppBridge.jsx calls when the
    iframe requests a tool call.
    """
    logger.debug(
        "Proxying tool call %s on server %d for user %d",
        request.tool_name,
        server_id,
        user.user_id,
    )
    server = await _get_server(server_id)

    return await _get_mcp_apps_service().proxy_tool_call(
        server, user.user_id, request.tool_name, request.arguments
    )


@router.get("/{server_id}/tools")
async def list_ui_tools(
    server_id: int,
    user: RequiredSession,
) -> list[dict[str, Any]]:
    """List UI-enabled tools for an MCP server.

    Returns the list of tools that have MCP App views,
    used by the frontend to know which tools can render iframes.
    """
    server = await _get_server(server_id)

    tools = await _get_mcp_apps_service().discover_ui_tools(server, user.user_id)
    return [tool.model_dump() for tool in tools]
