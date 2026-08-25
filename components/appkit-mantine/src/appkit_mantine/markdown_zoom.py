"""Helper to include Mermaid zoom script for markdown preview."""

import reflex as rx
from reflex.assets import asset
from reflex.components.component import Component


class MermaidZoomScript(Component):
    """React component wrapper that loads the Mermaid zoom script."""

    tag = "MermaidZoomLoader"
    # importable_path omits the ?v= content hash, which Vite would treat as an
    # optimized-dep URL and cache immutably, pinning a stale React instance.
    library = asset(
        path="mermaid_zoom_loader.js",
        shared=True,
    ).importable_path
    is_default = False


def mermaid_zoom_script() -> rx.Component:
    """Include the Mermaid SVG zoom JavaScript.

    Add this component to any page that uses markdown preview or renders images
    that should support click-to-zoom behaviour.
    """

    return MermaidZoomScript.create()
