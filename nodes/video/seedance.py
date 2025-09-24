from __future__ import annotations

from ..fal_utils import ApiHandler, ImageUtils


class SeedanceImageToVideoNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image": ("IMAGE",),
                "resolution": (["480p", "720p"], {"default": "720p"}),
                "duration": (["5", "10"], {"default": "5"}),
                "camera_fixed": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "seed": ("INT", {"default": -1, "min": -1, "max": 2147483647}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/VideoGeneration"

    def generate_video(self, prompt, image, resolution, duration, camera_fixed, seed=-1):
        image_url = ImageUtils.upload_image(image)
        if not image_url:
            return ApiHandler.handle_video_generation_error(
                "Seedance Image-to-Video", "Failed to upload image"
            )

        arguments = {
            "prompt": prompt,
            "image_url": image_url,
            "resolution": resolution,
            "duration": duration,
            "camera_fixed": camera_fixed,
        }

        if seed != -1:
            arguments["seed"] = seed

        return ApiHandler.run_video_job(
            "Seedance Image-to-Video",
            "fal-ai/bytedance/seedance/v1/lite/image-to-video",
            arguments,
        )


class SeedanceTextToVideoNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "aspect_ratio": (["16:9", "4:3", "1:1", "9:21"], {"default": "16:9"}),
                "resolution": (["480p", "720p"], {"default": "720p"}),
                "duration": (["5", "10"], {"default": "5"}),
                "camera_fixed": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "seed": ("INT", {"default": -1, "min": -1, "max": 2147483647}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/VideoGeneration"

    def generate_video(self, prompt, aspect_ratio, resolution, duration, camera_fixed, seed=-1):
        arguments = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "duration": duration,
            "camera_fixed": camera_fixed,
        }

        if seed != -1:
            arguments["seed"] = seed

        return ApiHandler.run_video_job(
            "Seedance Text-to-Video",
            "fal-ai/bytedance/seedance/v1/lite/text-to-video",
            arguments,
        )


NODE_CLASS_MAPPINGS = {
    "SeedanceImageToVideo_fal": SeedanceImageToVideoNode,
    "SeedanceTextToVideo_fal": SeedanceTextToVideoNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SeedanceImageToVideo_fal": "Seedance Image-to-Video (fal)",
    "SeedanceTextToVideo_fal": "Seedance Text-to-Video (fal)",
}
