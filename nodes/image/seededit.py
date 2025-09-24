from __future__ import annotations

from ..fal_utils import ApiHandler, ImageUtils, ResultProcessor


class SeedEditV3:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image": ("IMAGE",),
            },
            "optional": {
                "guidance_scale": (
                    "FLOAT",
                    {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.1},
                ),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**32 - 1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"
    CATEGORY = "FAL/Image"

    def generate_image(
        self,
        prompt,
        image,
        guidance_scale=0.5,
        seed=-1,
    ):
        model_name = "SeedEdit 3.0"
        image_url = ImageUtils.upload_image(image)
        if not image_url:
            print(f"Error: Failed to upload image for {model_name}")
            return ResultProcessor.create_blank_image()

        endpoint = "fal-ai/bytedance/seededit/v3/edit-image"
        arguments = {
            "prompt": prompt,
            "image_url": image_url,
            "guidance_scale": guidance_scale,
        }
        if seed != -1:
            arguments["seed"] = seed

        return ApiHandler.run_single_image_job(model_name, endpoint, arguments)


NODE_CLASS_MAPPINGS = {
    "SeedEditV3_fal": SeedEditV3,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SeedEditV3_fal": "SeedEdit 3.0 (fal)",
}
