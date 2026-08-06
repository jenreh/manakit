"""Guards against versioned asset URLs leaking into component ``library`` values.

``rx.asset()`` returns a content-versioned URL (``...wrapper.js?v=<hash>``).
Vite's dev server treats *any* module URL carrying a ``?v=`` query as an
optimized dependency and serves it with ``Cache-Control: immutable``, which
permanently pins the rewritten dependency URLs baked into that module. The
result is a second React instance (``resolveDispatcher() is null``) and dead
``/node_modules/.vite/deps/*.js?v=<stale>`` imports.

Component ``library`` values must therefore use ``AssetPathStr.importable_path``,
which is the same asset prefixed with ``$/public`` and without the version query.
"""

from __future__ import annotations

import pytest
from reflex.components.component import Component

from appkit_mantine.alert_dialog import AlertDialogRoot
from appkit_mantine.maps import Map
from appkit_mantine.markdown_preview import MarkdownPreview
from appkit_mantine.markdown_zoom import MermaidZoomScript
from appkit_mantine.rich_select import RichSelect, RichSelectItem
from appkit_mantine.tiptap import RichTextEditor
from appkit_mantine.tree import Tree

_LOCAL_ASSET_COMPONENTS = [
    AlertDialogRoot,
    Map,
    MarkdownPreview,
    MermaidZoomScript,
    RichSelect,
    RichSelectItem,
    RichTextEditor,
    Tree,
]


@pytest.mark.parametrize(
    "component",
    _LOCAL_ASSET_COMPONENTS,
    ids=lambda component: component.__name__,
)
def test_local_asset_library_is_unversioned(component: type[Component]) -> None:
    library = component().library

    assert library is not None
    assert library.startswith("$/public/external/")
    assert "?v=" not in library
    assert "$/public//" not in library
