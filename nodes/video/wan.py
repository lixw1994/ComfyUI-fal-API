from __future__ import annotations

import json
from typing import Any, Dict

from ..fal_utils import ApiHandler, ImageUtils, VideoUtils


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


def _merge_advanced_arguments(arguments: Dict[str, Any], advanced_parameters: str):
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


class WanV22TextToVideoNode(_WanBaseNode):
    MODEL_NAME = "wan-v2.2-text"
    FAL_ENDPOINT = "fal-ai/wan/v2.2-14b/text-to-video"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
            },
            "optional": {
                "negative_prompt": ("STRING", {"default": "", "multiline": True}),
                "num_frames": ("INT", {"default": 81, "min": 17, "max": 161}),
                "frames_per_second": ("INT", {"default": 24, "min": 4, "max": 60}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
                "resolution": (["580p", "720p"], {"default": "720p"}),
                "aspect_ratio": (["16:9", "9:16", "1:1"], {"default": "16:9"}),
                "num_inference_steps": ("INT", {"default": 40, "min": 1, "max": 200}),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
                "enable_prompt_expansion": ("BOOLEAN", {"default": True}),
                "guidance_scale": ("FLOAT", {"default": 3.5, "min": 0.0, "max": 20.0, "step": 0.1}),
                "guidance_scale_2": ("FLOAT", {"default": 3.5, "min": 0.0, "max": 20.0, "step": 0.1}),
                "shift": ("FLOAT", {"default": 5.0, "min": 1.0, "max": 10.0, "step": 0.1}),
                "interpolator_model": (["none", "film", "rife"], {"default": "film"}),
                "num_interpolated_frames": ("INT", {"default": 0, "min": 0, "max": 4}),
                "adjust_fps_for_interpolation": ("BOOLEAN", {"default": True}),
                "video_quality": (["low", "medium", "high", "maximum"], {"default": "high"}),
                "video_write_mode": (["fast", "balanced", "small"], {"default": "balanced"}),
                "advanced_parameters": ("STRING", {"default": ""}),
            },
        }

    def generate_video(
        self,
        prompt,
        negative_prompt="",
        num_frames=81,
        frames_per_second=24,
        seed=0,
        resolution="720p",
        aspect_ratio="16:9",
        num_inference_steps=40,
        enable_safety_checker=True,
        enable_prompt_expansion=True,
        guidance_scale=3.5,
        guidance_scale_2=3.5,
        shift=5.0,
        interpolator_model="none",
        num_interpolated_frames=0,
        adjust_fps_for_interpolation=True,
        video_quality="high",
        video_write_mode="balanced",
        advanced_parameters="",
    ):
        prompt = (prompt or "").strip()
        if not prompt:
            return ApiHandler.handle_video_generation_error(
                self.MODEL_NAME, "prompt is required"
            )

        arguments: Dict[str, Any] = {
            "prompt": prompt,
            "num_frames": int(num_frames),
            "frames_per_second": int(frames_per_second),
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
            "num_inference_steps": int(num_inference_steps),
            "enable_safety_checker": bool(enable_safety_checker),
            "enable_prompt_expansion": bool(enable_prompt_expansion),
            "guidance_scale": float(guidance_scale),
            "guidance_scale_2": float(guidance_scale_2),
            "shift": float(shift),
            "interpolator_model": interpolator_model,
            "num_interpolated_frames": int(num_interpolated_frames),
            "adjust_fps_for_interpolation": bool(adjust_fps_for_interpolation),
            "video_quality": video_quality,
            "video_write_mode": video_write_mode,
        }
        if negative_prompt:
            arguments["negative_prompt"] = negative_prompt
        if seed:
            arguments["seed"] = seed

        try:
            arguments = _merge_advanced_arguments(arguments, advanced_parameters)
        except ValueError as exc:
            return ApiHandler.handle_video_generation_error(self.MODEL_NAME, str(exc))

        return ApiHandler.run_video_job(
            self.MODEL_NAME, self.FAL_ENDPOINT, arguments
        )


class WanV22ImageToVideoNode(_WanBaseNode):
    MODEL_NAME = "wan-v2.2-image"
    FAL_ENDPOINT = "fal-ai/wan/v2.2-14b/image-to-video"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image": ("IMAGE",),
            },
            "optional": {
                "end_image": ("IMAGE",),
                "end_image_url": ("STRING", {"default": ""}),
                "negative_prompt": ("STRING", {"default": "", "multiline": True}),
                "num_frames": ("INT", {"default": 81, "min": 17, "max": 161}),
                "frames_per_second": ("INT", {"default": 16, "min": 4, "max": 60}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
                "resolution": (["480p", "580p", "720p"], {"default": "720p"}),
                "aspect_ratio": (["auto", "16:9", "9:16", "1:1"], {"default": "auto"}),
                "num_inference_steps": ("INT", {"default": 27, "min": 1, "max": 200}),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
                "enable_prompt_expansion": ("BOOLEAN", {"default": True}),
                "acceleration": (["regular", "none"], {"default": "regular"}),
                "guidance_scale": ("FLOAT", {"default": 3.5, "min": 0.0, "max": 20.0, "step": 0.1}),
                "guidance_scale_2": ("FLOAT", {"default": 3.5, "min": 0.0, "max": 20.0, "step": 0.1}),
                "shift": ("FLOAT", {"default": 5.0, "min": 1.0, "max": 10.0, "step": 0.1}),
                "interpolator_model": (["none", "film", "rife"], {"default": "film"}),
                "num_interpolated_frames": ("INT", {"default": 1, "min": 0, "max": 4}),
                "adjust_fps_for_interpolation": ("BOOLEAN", {"default": True}),
                "video_quality": (["low", "medium", "high", "maximum"], {"default": "high"}),
                "video_write_mode": (["fast", "balanced", "small"], {"default": "balanced"}),
                "advanced_parameters": ("STRING", {"default": ""}),
            },
        }

    def generate_video(
        self,
        prompt,
        image,
        end_image=None,
        end_image_url="",
        negative_prompt="",
        num_frames=81,
        frames_per_second=16,
        seed=0,
        resolution="720p",
        aspect_ratio="auto",
        num_inference_steps=27,
        enable_safety_checker=True,
        enable_prompt_expansion=True,
        acceleration="regular",
        guidance_scale=3.5,
        guidance_scale_2=3.5,
        shift=5.0,
        interpolator_model="film",
        num_interpolated_frames=1,
        adjust_fps_for_interpolation=True,
        video_quality="high",
        video_write_mode="balanced",
        advanced_parameters="",
    ):
        prompt = (prompt or "").strip()
        if not prompt:
            return ApiHandler.handle_video_generation_error(
                self.MODEL_NAME, "prompt is required"
            )

        image_url = ImageUtils.upload_image(image)
        if not image_url:
            return ApiHandler.handle_video_generation_error(
                self.MODEL_NAME, "Failed to upload reference image"
            )

        resolved_end_image_url = (end_image_url or "").strip()
        if not resolved_end_image_url and end_image is not None:
            resolved_end_image_url = ImageUtils.upload_image(end_image)
            if not resolved_end_image_url:
                return ApiHandler.handle_video_generation_error(
                    self.MODEL_NAME, "Failed to upload end image"
                )

        arguments: Dict[str, Any] = {
            "prompt": prompt,
            "image_url": image_url,
            "num_frames": int(num_frames),
            "frames_per_second": int(frames_per_second),
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
            "num_inference_steps": int(num_inference_steps),
            "enable_safety_checker": bool(enable_safety_checker),
            "enable_prompt_expansion": bool(enable_prompt_expansion),
            "acceleration": acceleration,
            "guidance_scale": float(guidance_scale),
            "guidance_scale_2": float(guidance_scale_2),
            "shift": float(shift),
            "interpolator_model": interpolator_model,
            "num_interpolated_frames": int(num_interpolated_frames),
            "adjust_fps_for_interpolation": bool(adjust_fps_for_interpolation),
            "video_quality": video_quality,
            "video_write_mode": video_write_mode,
        }
        if resolved_end_image_url:
            arguments["end_image_url"] = resolved_end_image_url
        if negative_prompt:
            arguments["negative_prompt"] = negative_prompt
        if seed:
            arguments["seed"] = seed

        try:
            arguments = _merge_advanced_arguments(arguments, advanced_parameters)
        except ValueError as exc:
            return ApiHandler.handle_video_generation_error(self.MODEL_NAME, str(exc))

        return ApiHandler.run_video_job(
            self.MODEL_NAME, self.FAL_ENDPOINT, arguments
        )


class WanAnimateMoveNode(_WanBaseNode):
    MODEL_NAME = "wan-v2.2-animate-move"
    FAL_ENDPOINT = "fal-ai/wan/v2.2-14b/animate/move"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            },
            "optional": {
                "video_url": ("STRING", {"default": ""}),
                "video": ("IMAGE",),
                "video_info": ("VHS_VIDEOINFO",),
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "negative_prompt": ("STRING", {"default": "", "multiline": True}),
                "strength": ("FLOAT", {"default": 0.6, "min": 0.01, "max": 1.0, "step": 0.01}),
                "resolution": (["432p", "480p", "540p"], {"default": "432p"}),
                "num_inference_steps": ("INT", {"default": 20, "min": 1, "max": 200}),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
                "shift": ("FLOAT", {"default": 5.0, "min": 1.0, "max": 10.0, "step": 0.1}),
                "video_quality": (["low", "medium", "high", "maximum"], {"default": "high"}),
                "video_write_mode": (["fast", "balanced", "small"], {"default": "balanced"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
                "advanced_parameters": ("STRING", {"default": ""}),
            },
        }

    def generate_video(
        self,
        image,
        video_url="",
        video=None,
        video_info=None,
        prompt="",
        negative_prompt="",
        strength=0.6,
        resolution="432p",
        num_inference_steps=20,
        enable_safety_checker=True,
        shift=5.0,
        video_quality="high",
        video_write_mode="balanced",
        seed=0,
        advanced_parameters="",
    ):
        video_url = (video_url or "").strip()
        if not video_url and video is not None:
            video_url = VideoUtils.upload_video(video, video_info)
            if not video_url:
                return ApiHandler.handle_video_generation_error(
                    self.MODEL_NAME, "Failed to upload provided video"
                )
        if not video_url:
            return ApiHandler.handle_video_generation_error(
                self.MODEL_NAME, "video_url is required"
            )

        image_url = ImageUtils.upload_image(image)
        if not image_url:
            return ApiHandler.handle_video_generation_error(
                self.MODEL_NAME, "Failed to upload control image"
            )

        arguments: Dict[str, Any] = {
            "video_url": video_url,
            "image_url": image_url,
            "strength": float(strength),
            "resolution": resolution,
            "num_inference_steps": int(num_inference_steps),
            "enable_safety_checker": bool(enable_safety_checker),
            "shift": float(shift),
            "video_quality": video_quality,
            "video_write_mode": video_write_mode,
        }
        if prompt:
            arguments["prompt"] = prompt
        if negative_prompt:
            arguments["negative_prompt"] = negative_prompt
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
    MODEL_NAME = "wan-v2.2-animate-replace"
    FAL_ENDPOINT = "fal-ai/wan/v2.2-14b/animate/replace"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            },
            "optional": {
                "video_url": ("STRING", {"default": ""}),
                "video": ("IMAGE",),
                "video_info": ("VHS_VIDEOINFO",),
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "strength": ("FLOAT", {"default": 0.8, "min": 0.01, "max": 1.0, "step": 0.01}),
                "resolution": (["480p", "580p", "720p"], {"default": "480p"}),
                "num_inference_steps": ("INT", {"default": 20, "min": 1, "max": 200}),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
                "shift": ("FLOAT", {"default": 5.0, "min": 1.0, "max": 10.0, "step": 0.1}),
                "video_quality": (["low", "medium", "high", "maximum"], {"default": "high"}),
                "video_write_mode": (["fast", "balanced", "small"], {"default": "balanced"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
                "advanced_parameters": ("STRING", {"default": ""}),
            },
        }

    def generate_video(
        self,
        image,
        video_url="",
        video=None,
        video_info=None,
        prompt="",
        strength=0.8,
        resolution="480p",
        num_inference_steps=20,
        enable_safety_checker=True,
        shift=5.0,
        video_quality="high",
        video_write_mode="balanced",
        seed=0,
        advanced_parameters="",
    ):
        video_url = (video_url or "").strip()
        if not video_url and video is not None:
            video_url = VideoUtils.upload_video(video, video_info)
            if not video_url:
                return ApiHandler.handle_video_generation_error(
                    self.MODEL_NAME, "Failed to upload provided video"
                )
        if not video_url:
            return ApiHandler.handle_video_generation_error(
                self.MODEL_NAME, "video_url is required"
            )

        image_url = ImageUtils.upload_image(image)
        if not image_url:
            return ApiHandler.handle_video_generation_error(
                self.MODEL_NAME, "Failed to upload replacement image"
            )

        arguments: Dict[str, Any] = {
            "video_url": video_url,
            "image_url": image_url,
            "strength": float(strength),
            "resolution": resolution,
            "num_inference_steps": int(num_inference_steps),
            "enable_safety_checker": bool(enable_safety_checker),
            "shift": float(shift),
            "video_quality": video_quality,
            "video_write_mode": video_write_mode,
        }
        if prompt:
            arguments["prompt"] = prompt
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
    "WanV22TextToVideo_fal": WanV22TextToVideoNode,
    "WanV22ImageToVideo_fal": WanV22ImageToVideoNode,
    "WanAnimateMove_fal": WanAnimateMoveNode,
    "WanAnimateReplace_fal": WanAnimateReplaceNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WanProImageToVideo_fal": "Wan Pro Image-to-Video (fal)",
    "WanProTextToVideo_fal": "Wan Pro Text-to-Video (fal)",
    "WanTurboTextToVideo_fal": "Wan Turbo Text-to-Video (fal)",
    "WanTurboImageToVideo_fal": "Wan Turbo Image-to-Video (fal)",
    "WanV22TextToVideo_fal": "Wan v2.2 Text-to-Video (fal)",
    "WanV22ImageToVideo_fal": "Wan v2.2 Image-to-Video (fal)",
    "WanAnimateMove_fal": "Wan v2.2 Animate Move (fal)",
    "WanAnimateReplace_fal": "Wan v2.2 Animate Replace (fal)",
}
