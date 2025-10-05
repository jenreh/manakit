"""Mantine RichTextEditor (Tiptap) component wrapper for Reflex.

Provides a WYSIWYG rich text editor based on Tiptap with Mantine UI.
Uses external JavaScript wrapper file for React hook management.

Documentation: https://mantine.dev/x/tiptap/
"""

from __future__ import annotations

from typing import Literal

import reflex as rx
from reflex.assets import asset
from reflex.components.component import NoSSRComponent
from reflex.event import EventHandler
from reflex.vars.base import Var


class RichTextEditor(NoSSRComponent):
    """Mantine RichTextEditor - WYSIWYG editor with automatic hook management.

    Based on: https://mantine.dev/x/tiptap/

    This component uses a custom JavaScript wrapper that handles the useEditor
    React hook internally. The wrapper is located in assets/external/mantine/tiptap/

    Props:
        content: HTML content for the editor
        on_update: Callback when content changes (receives HTML string)
        editable: Whether the editor is editable (default: True)
        placeholder: Placeholder text when editor is empty
        variant: Visual style - "default" or "subtle"
        with_typography_styles: Apply typography styles (default: True)
        labels: Localization labels
    """

    tag = "RichTextEditorWrapper"

    # Point to our custom wrapper component (same directory as this module)
    library = "$/public/" + asset(
        path="tiptap_wrapper.js",
        shared=True,
    )
    is_default = False

    lib_dependencies: list[str] = [
        "@mantine/tiptap@8.2.5",
        "@mantine/core@8.2.5",
        "@tiptap/react@^2.10.4",
        "@tiptap/pm@^2.10.4",
        "@tiptap/extension-link@^2.10.4",
        "@tiptap/starter-kit@^2.10.4",
        "@tiptap/extension-highlight@^2.10.4",
        "@tiptap/extension-text-align@^2.10.4",
        "@tiptap/extension-subscript@^2.10.4",
        "@tiptap/extension-superscript@^2.10.4",
        "@tiptap/extension-color@^2.10.4",
        "@tiptap/extension-text-style@^2.10.4",
        "@tiptap/extension-placeholder@^2.10.4",
    ]

    # Content management
    content: Var[str] = None
    """HTML content for the editor."""

    on_update: EventHandler[lambda html: [html]] = None
    """Callback when content changes (receives HTML string)."""

    # Editor state
    editable: Var[bool] = None
    """Whether the editor is editable. Default: True."""

    placeholder: Var[str] = None
    """Placeholder text when editor is empty."""

    # Visual props
    variant: Var[Literal["default", "subtle"]] = None
    """Visual style: default (with borders) or subtle (borderless)."""

    with_typography_styles: Var[bool] = None
    """Apply typography styles to content. Default: True."""

    # Localization
    labels: Var[dict] = None
    """Localization labels for controls."""


# Namespace
class RichTextEditorNamespace(rx.ComponentNamespace):
    """Namespace for RichTextEditor component."""

    __call__ = staticmethod(RichTextEditor.create)


rich_text_editor = RichTextEditorNamespace()
