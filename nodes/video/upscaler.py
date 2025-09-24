from __future__ import annotations

from ..fal_utils import ApiHandler


class VideoUpscalerNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_url": ("STRING", {"default": ""}),
                "scale": (
                    "FLOAT",
                    {"default": 2.0, "min": 1.0, "max": 4.0, "step": 0.5},
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "upscale_video"
    CATEGORY = "FAL/VideoGeneration"

    def upscale_video(self, video_url, scale):
        arguments = {"video_url": video_url, "scale": scale}

        return ApiHandler.run_video_job(
            "video-upscaler", "fal-ai/video-upscaler", arguments
        )


NODE_CLASS_MAPPINGS = {
    "VideoUpscaler_fal": VideoUpscalerNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoUpscaler_fal": "Video Upscaler (fal)",
}
