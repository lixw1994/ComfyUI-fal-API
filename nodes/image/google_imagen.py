from __future__ import annotations

from ..fal_utils import ApiHandler


class Imagen4PreviewNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"
    CATEGORY = "FAL/Image"

    def generate_image(self, prompt):
        arguments = {
            "prompt": prompt,
        }

        return ApiHandler.run_image_job(
            "Imagen4 Preview", "fal-ai/imagen4/preview", arguments
        )


NODE_CLASS_MAPPINGS = {
    "Imagen4Preview_fal": Imagen4PreviewNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Imagen4Preview_fal": "Imagen4 Preview (fal)",
}
