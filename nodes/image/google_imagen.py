from __future__ import annotations

from ..fal_utils import ApiHandler


class Imagen4PreviewNode:
    CATEGORY = "FAL/Image"
    MODEL_NAME = "Imagen4 Preview"
    FAL_ENDPOINT = "fal-ai/imagen4/preview"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"

    def generate_image(self, prompt):
        arguments = {
            "prompt": prompt,
        }

        return ApiHandler.run_image_job(
            self.MODEL_NAME, self.FAL_ENDPOINT, arguments
        )


NODE_CLASS_MAPPINGS = {
    "Imagen4Preview_fal": Imagen4PreviewNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Imagen4Preview_fal": "Imagen4 Preview (fal)",
}
