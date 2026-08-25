"""Guards against versioned asset URLs leaking into component ``library`` values.

``rx.asset()`` returns a content-versioned URL (``...bridge.jsx?v=<hash>``).
Vite's dev server treats *any* module URL carrying a ``?v=`` query as an
optimized dependency and serves it with ``Cache-Control: immutable``, which
permanently pins the rewritten dependency URLs baked into that module and
yields a second React instance (``resolveDispatcher() is null``).

Component ``library`` values must therefore use ``AssetPathStr.importable_path``.
"""

from __future__ import annotations

from appkit_assistant.components.mcp_app_bridge import McpAppBridge


def test_mcp_app_bridge_library_is_unversioned() -> None:
    library = McpAppBridge().library

    assert library is not None
    assert library.startswith("$/public/external/")
    assert "?v=" not in library
    assert "$/public//" not in library
