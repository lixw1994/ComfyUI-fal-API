from __future__ import annotations

from . import (
    combined,
    kling,
    load,
    luma,
    minimax,
    runway,
    seedance,
    upscaler,
    veo,
    wan,
)

_MODULES = [
    minimax,
    kling,
    runway,
    luma,
    veo,
    wan,
    upscaler,
    load,
    seedance,
    combined,
]

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

for module in _MODULES:
    NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
