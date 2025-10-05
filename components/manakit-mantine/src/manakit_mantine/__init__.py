"""Mantine sub-package."""

from reflex.utils import lazy_loader

_MAPPING = {
    "manakit_mantine.date": ["date_input"],
    "manakit_mantine.inputs": ["form_input", "input"],
    "manakit_mantine.masked_input": ["MaskedInput", "masked_input"],
    "manakit_mantine.nprogress": ["navigation_progress"],
    "manakit_mantine.number_input": ["number_input"],
    "manakit_mantine.password_input": ["password_input"],
    "manakit_mantine.textarea": ["textarea"],
    "manakit_mantine.tiptap": [
        "rich_text_editor",
        "EditorToolbarConfig",
        "ToolbarControlGroup",
    ],
    "manakit_mantine.select": ["select"],
    "manakit_mantine.autocomplete": ["autocomplete"],
    "manakit_mantine.combobox": ["combobox"],
}

_SUBMODULES = set()
_SUBMOD_ATTRS = {
    "".join(k.split("manakit_mantine.")[-1]): v for k, v in _MAPPING.items()
}

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
