from __future__ import annotations

from . import (
    flux,
    google_imagen,
    hidream,
    ideogram,
    nanobanana,
    qwen,
    sana,
    seededit,
    seedream,
    recraft,
)

_MODULES = [
    sana,
    recraft,
    hidream,
    ideogram,
    google_imagen,
    qwen,
    seededit,
    flux,
    seedream,
    nanobanana,
]

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

for module in _MODULES:
    NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
