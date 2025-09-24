from __future__ import annotations

from ..fal_utils import ApiHandler, ImageUtils


class Veo2ImageToVideoNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image": ("IMAGE",),
                "aspect_ratio": (
                    ["auto", "auto_prefer_portrait", "16:9", "9:16"],
                    {"default": "auto"},
                ),
                "duration": (["5s", "6s", "7s", "8s"], {"default": "5s"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/VideoGeneration"

    def generate_video(self, prompt, image, aspect_ratio, duration):
        image_url = ImageUtils.upload_image(image)
        if not image_url:
            return ApiHandler.handle_video_generation_error(
                "veo2", "Failed to upload image"
            )

        arguments = {
            "prompt": prompt,
            "image_url": image_url,
            "aspect_ratio": aspect_ratio,
            "duration": duration,
        }

        return ApiHandler.run_video_job(
            "veo2", "fal-ai/veo2/image-to-video", arguments
        )


class _Veo3TextNodeBase:
    MODEL_NAME: str = ""
    ENDPOINT: str = ""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "aspect_ratio": (
                    ["16:9", "9:16", "1:1"],
                    {"default": "16:9"},
                ),
                "duration": (
                    ["4s", "6s", "8s"],
                    {"default": "8s"},
                ),
            },
            "optional": {
                "negative_prompt": ("STRING", {"default": "", "multiline": True}),
                "enhance_prompt": ("BOOLEAN", {"default": True}),
                "auto_fix": ("BOOLEAN", {"default": True}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2147483647}),
                "resolution": (["720p", "1080p"], {"default": "720p"}),
                "generate_audio": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/VideoGeneration"

    def generate_video(
        self,
        prompt,
        aspect_ratio,
        duration,
        negative_prompt="",
        enhance_prompt=True,
        auto_fix=True,
        seed=-1,
        resolution="720p",
        generate_audio=True,
    ):
        arguments = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "duration": duration,
            "negative_prompt": negative_prompt,
            "enhance_prompt": enhance_prompt,
            "auto_fix": auto_fix,
            "resolution": resolution,
            "generate_audio": generate_audio,
        }

        if seed != -1:
            arguments["seed"] = seed

        return ApiHandler.run_video_job(
            self.MODEL_NAME, self.ENDPOINT, arguments
        )


class Veo3Node(_Veo3TextNodeBase):
    MODEL_NAME = "veo3"
    ENDPOINT = "fal-ai/veo3"


class Veo3FastNode(_Veo3TextNodeBase):
    MODEL_NAME = "veo3_fast"
    ENDPOINT = "fal-ai/veo3/fast"


class _Veo3ImageToVideoBase:
    MODEL_NAME: str = ""
    ENDPOINT: str = ""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image": ("IMAGE",),
                "aspect_ratio": (
                    ["auto", "16:9", "9:16"],
                    {"default": "auto"},
                ),
                "duration": (["8s"], {"default": "8s"}),
            },
            "optional": {
                "generate_audio": ("BOOLEAN", {"default": True}),
                "resolution": (["720p", "1080p"], {"default": "720p"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/VideoGeneration"

    def generate_video(
        self,
        prompt,
        image,
        aspect_ratio,
        duration,
        generate_audio=True,
        resolution="720p",
    ):
        image_url = ImageUtils.upload_image(image)
        if not image_url:
            return ApiHandler.handle_video_generation_error(
                self.MODEL_NAME, "Failed to upload image"
            )

        arguments = {
            "prompt": prompt,
            "image_url": image_url,
            "aspect_ratio": aspect_ratio,
            "duration": duration,
            "generate_audio": generate_audio,
            "resolution": resolution,
        }

        return ApiHandler.run_video_job(
            self.MODEL_NAME, self.ENDPOINT, arguments
        )


class Veo3ImageToVideoNode(_Veo3ImageToVideoBase):
    MODEL_NAME = "veo3_image_to_video"
    ENDPOINT = "fal-ai/veo3/image-to-video"


class Veo3FastImageToVideoNode(_Veo3ImageToVideoBase):
    MODEL_NAME = "veo3_fast_image_to_video"
    ENDPOINT = "fal-ai/veo3/fast/image-to-video"


NODE_CLASS_MAPPINGS = {
    "Veo2ImageToVideo_fal": Veo2ImageToVideoNode,
    "Veo3_fal": Veo3Node,
    "Veo3Fast_fal": Veo3FastNode,
    "Veo3ImageToVideo_fal": Veo3ImageToVideoNode,
    "Veo3FastImageToVideo_fal": Veo3FastImageToVideoNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Veo2ImageToVideo_fal": "Google Veo2 Image-to-Video (fal)",
    "Veo3_fal": "Veo3 Video Generation (fal)",
    "Veo3Fast_fal": "Veo3 Fast Video Generation (fal)",
    "Veo3ImageToVideo_fal": "Veo3 Image-to-Video (fal)",
    "Veo3FastImageToVideo_fal": "Veo3 Fast Image-to-Video (fal)",
}
