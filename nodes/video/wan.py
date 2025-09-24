from __future__ import annotations

from ..fal_utils import ApiHandler, ImageUtils


class WanProNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image": ("IMAGE",),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 2147483647}),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/VideoGeneration"

    def generate_video(self, prompt, image, seed=0, enable_safety_checker=True):
        image_url = ImageUtils.upload_image(image)
        if not image_url:
            return ApiHandler.handle_video_generation_error(
                "wan-pro", "Failed to upload image"
            )

        arguments = {
            "prompt": prompt,
            "image_url": image_url,
            "enable_safety_checker": enable_safety_checker,
        }

        if seed != 0:
            arguments["seed"] = seed

        return ApiHandler.run_video_job(
            "wan-pro", "fal-ai/wan-pro/image-to-video", arguments
        )


NODE_CLASS_MAPPINGS = {
    "WanPro_fal": WanProNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WanPro_fal": "Wan Pro Image-to-Video (fal)",
}
