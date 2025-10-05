"""Mantine sub-package."""

from reflex.utils import lazy_loader

_MAPPING = {
    "mantine.date": ["date_input"],
    "mantine.inputs": ["form_input"],
    "mantine.masked_input": ["MaskedInput", "masked_input"],
    "mantine.nprogress": ["navigation_progress"],
    "mantine.number_input": ["number_input"],
    "mantine.password_input": ["password_input"],
    "mantine.textarea": ["textarea"],
    "mantine.tiptap": [
        "rich_text_editor",
        "EditorToolbarConfig",
        "ToolbarControlGroup",
    ],
}

_SUBMODULES = set()
_SUBMOD_ATTRS = {"".join(k.split("mantine.")[-1]): v for k, v in _MAPPING.items()}

_SUBMOD_ATTRS.update(
    {
        "base": ["base", "provider"],
    }
)

__getattr__, __dir__, __all__ = lazy_loader.attach(
    __name__,
    submodules=_SUBMODULES,
    submod_attrs=_SUBMOD_ATTRS,
)
