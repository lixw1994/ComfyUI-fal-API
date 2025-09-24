from __future__ import annotations

import json
from typing import Dict

from ..fal_utils import ApiHandler, ImageUtils


class _WanBaseNode:
    CATEGORY = "FAL/VideoGeneration"
    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_video"


class WanProImageToVideoNode(_WanBaseNode):
    MODEL_NAME = "wan-pro-image"
    FAL_ENDPOINT = "fal-ai/wan-pro/image-to-video"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image": ("IMAGE",),
            },
            "optional": {
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
            },
        }

    def generate_video(self, prompt, image, enable_safety_checker=True, seed=0):
        image_url = ImageUtils.upload_image(image)
        if not image_url:
            return ApiHandler.handle_video_generation_error(
                self.MODEL_NAME, "Failed to upload reference image"
            )

        arguments = {
            "prompt": prompt,
            "image_url": image_url,
            "enable_safety_checker": enable_safety_checker,
        }

        if seed:
            arguments["seed"] = seed

        return ApiHandler.run_video_job(
            self.MODEL_NAME, self.FAL_ENDPOINT, arguments
        )


class WanProTextToVideoNode(_WanBaseNode):
    MODEL_NAME = "wan-pro-text"
    FAL_ENDPOINT = "fal-ai/wan-pro/text-to-video"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
            },
            "optional": {
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
            },
        }

    def generate_video(self, prompt, enable_safety_checker=True, seed=0):
        arguments = {
            "prompt": prompt,
            "enable_safety_checker": enable_safety_checker,
        }

        if seed:
            arguments["seed"] = seed

        return ApiHandler.run_video_job(
            self.MODEL_NAME, self.FAL_ENDPOINT, arguments
        )


class WanTurboTextToVideoNode(_WanBaseNode):
    MODEL_NAME = "wan-turbo-text"
    FAL_ENDPOINT = "fal-ai/wan/turbo/text-to-video"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
            },
            "optional": {
                "resolution": (["720p", "1080p"], {"default": "1080p"}),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
            },
        }

    def generate_video(self, prompt, resolution="1080p", enable_safety_checker=True, seed=0):
        arguments = {
            "prompt": prompt,
            "resolution": resolution,
            "enable_safety_checker": enable_safety_checker,
        }

        if seed:
            arguments["seed"] = seed

        return ApiHandler.run_video_job(
            self.MODEL_NAME, self.FAL_ENDPOINT, arguments
        )


class WanTurboImageToVideoNode(_WanBaseNode):
    MODEL_NAME = "wan-turbo-image"
    FAL_ENDPOINT = "fal-ai/wan/turbo/image-to-video"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image": ("IMAGE",),
            },
            "optional": {
                "resolution": (["720p", "1080p"], {"default": "1080p"}),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
            },
        }

    def generate_video(self, prompt, image, resolution="1080p", enable_safety_checker=True, seed=0):
        image_url = ImageUtils.upload_image(image)
        if not image_url:
            return ApiHandler.handle_video_generation_error(
                self.MODEL_NAME, "Failed to upload reference image"
            )

        arguments = {
            "prompt": prompt,
            "image_url": image_url,
            "resolution": resolution,
            "enable_safety_checker": enable_safety_checker,
        }

        if seed:
            arguments["seed"] = seed

        return ApiHandler.run_video_job(
            self.MODEL_NAME, self.FAL_ENDPOINT, arguments
        )


def _merge_advanced_arguments(arguments: Dict[str, object], advanced_parameters: str):
    if not advanced_parameters:
        return arguments
    try:
        payload = json.loads(advanced_parameters)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in advanced_parameters: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("advanced_parameters must decode to a JSON object")
    arguments.update(payload)
    return arguments


class WanAnimateMoveNode(_WanBaseNode):
    MODEL_NAME = "wan-animate-move"
    FAL_ENDPOINT = "fal-ai/wan/v2.2-14b/animate/move"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_url": ("STRING", {"default": ""}),
                "prompt": ("STRING", {"default": "Describe the motion you want", "multiline": True}),
            },
            "optional": {
                "negative_prompt": ("STRING", {"default": "", "multiline": True}),
                "mask_prompt": ("STRING", {"default": ""}),
                "strength": ("FLOAT", {"default": 0.6, "min": 0.0, "max": 1.0, "step": 0.05}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
                "advanced_parameters": ("STRING", {"default": ""}),
            },
        }

    def generate_video(
        self,
        video_url,
        prompt,
        negative_prompt="",
        mask_prompt="",
        strength=0.6,
        seed=0,
        advanced_parameters="",
    ):
        video_url = (video_url or "").strip()
        if not video_url:
            return ApiHandler.handle_video_generation_error(
                self.MODEL_NAME, "video_url is required"
            )

        prompt = (prompt or "").strip()
        if not prompt:
            return ApiHandler.handle_video_generation_error(
                self.MODEL_NAME, "prompt is required"
            )

        arguments: Dict[str, object] = {
            "video_url": video_url,
            "prompt": prompt,
        }
        if negative_prompt:
            arguments["negative_prompt"] = negative_prompt
        if mask_prompt:
            arguments["mask_prompt"] = mask_prompt
        if strength is not None:
            arguments["strength"] = float(strength)
        if seed:
            arguments["seed"] = seed

        try:
            arguments = _merge_advanced_arguments(arguments, advanced_parameters)
        except ValueError as exc:
            return ApiHandler.handle_video_generation_error(self.MODEL_NAME, str(exc))

        return ApiHandler.run_video_job(
            self.MODEL_NAME, self.FAL_ENDPOINT, arguments
        )


class WanAnimateReplaceNode(_WanBaseNode):
    MODEL_NAME = "wan-animate-replace"
    FAL_ENDPOINT = "fal-ai/wan/v2.2-14b/animate/replace"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_url": ("STRING", {"default": ""}),
                "image": ("IMAGE",),
            },
            "optional": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "mask_prompt": ("STRING", {"default": ""}),
                "strength": ("FLOAT", {"default": 0.8, "min": 0.0, "max": 1.0, "step": 0.05}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
                "advanced_parameters": ("STRING", {"default": ""}),
            },
        }

    def generate_video(
        self,
        video_url,
        image,
        prompt="",
        mask_prompt="",
        strength=0.8,
        seed=0,
        advanced_parameters="",
    ):
        video_url = (video_url or "").strip()
        if not video_url:
            return ApiHandler.handle_video_generation_error(
                self.MODEL_NAME, "video_url is required"
            )

        image_url = ImageUtils.upload_image(image)
        if not image_url:
            return ApiHandler.handle_video_generation_error(
                self.MODEL_NAME, "Failed to upload replacement image"
            )

        arguments: Dict[str, object] = {
            "video_url": video_url,
            "image_url": image_url,
        }
        if prompt:
            arguments["prompt"] = prompt
        if mask_prompt:
            arguments["mask_prompt"] = mask_prompt
        if strength is not None:
            arguments["strength"] = float(strength)
        if seed:
            arguments["seed"] = seed

        try:
            arguments = _merge_advanced_arguments(arguments, advanced_parameters)
        except ValueError as exc:
            return ApiHandler.handle_video_generation_error(self.MODEL_NAME, str(exc))

        return ApiHandler.run_video_job(
            self.MODEL_NAME, self.FAL_ENDPOINT, arguments
        )


NODE_CLASS_MAPPINGS = {
    "WanProImageToVideo_fal": WanProImageToVideoNode,
    "WanProTextToVideo_fal": WanProTextToVideoNode,
    "WanTurboTextToVideo_fal": WanTurboTextToVideoNode,
    "WanTurboImageToVideo_fal": WanTurboImageToVideoNode,
    "WanAnimateMove_fal": WanAnimateMoveNode,
    "WanAnimateReplace_fal": WanAnimateReplaceNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WanProImageToVideo_fal": "Wan Pro Image-to-Video (fal)",
    "WanProTextToVideo_fal": "Wan Pro Text-to-Video (fal)",
    "WanTurboTextToVideo_fal": "Wan Turbo Text-to-Video (fal)",
    "WanTurboImageToVideo_fal": "Wan Turbo Image-to-Video (fal)",
    "WanAnimateMove_fal": "Wan Animate Move (fal)",
    "WanAnimateReplace_fal": "Wan Animate Replace (fal)",
}
