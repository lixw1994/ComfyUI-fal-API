from __future__ import annotations

from ..fal_utils import ApiHandler, ImageUtils


class _KlingBaseNode:
    MODEL_NAME: str = ""
    ENDPOINT_TEXT: str | None = None
    ENDPOINT_IMAGE: str | None = None

    ASPECT_RATIOS = ("16:9", "9:16", "1:1")
    DURATIONS = ("5", "10")
    SUPPORTS_TAIL_IMAGE = False
    SUPPORTS_NEGATIVE_PROMPT = False
    SUPPORTS_CFG_SCALE = False
    DEFAULT_CFG_SCALE = 0.5

    @classmethod
    def INPUT_TYPES(cls):
        required = {
            "prompt": ("STRING", {"default": "", "multiline": True}),
            "duration": (list(cls.DURATIONS), {"default": cls.DURATIONS[0]}),
            "aspect_ratio": (list(cls.ASPECT_RATIOS), {"default": cls.ASPECT_RATIOS[0]}),
        }

        optional: dict[str, tuple] = {}
        if cls.ENDPOINT_IMAGE:
            optional["image"] = ("IMAGE",)
            if cls.SUPPORTS_TAIL_IMAGE:
                optional["tail_image"] = ("IMAGE",)

        if cls.SUPPORTS_NEGATIVE_PROMPT:
            optional["negative_prompt"] = ("STRING", {"default": "", "multiline": True})

        if cls.SUPPORTS_CFG_SCALE:
            optional["cfg_scale"] = (
                "FLOAT",
                {"default": cls.DEFAULT_CFG_SCALE, "min": 0.0, "max": 3.0, "step": 0.05},
            )

        return {"required": required, "optional": optional}

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/VideoGeneration"

    def generate_video(
        self,
        prompt,
        duration,
        aspect_ratio,
        image=None,
        tail_image=None,
        negative_prompt="",
        cfg_scale=0.5,
    ):
        model_name = getattr(self, "MODEL_NAME", "kling-video")

        try:
            duration_value = int(duration)
        except (TypeError, ValueError):
            duration_value = duration

        arguments = {
            "prompt": prompt,
            "duration": duration_value,
            "aspect_ratio": aspect_ratio,
        }

        if self.SUPPORTS_CFG_SCALE:
            arguments["cfg_scale"] = cfg_scale

        if self.SUPPORTS_NEGATIVE_PROMPT and negative_prompt:
            arguments["negative_prompt"] = negative_prompt

        endpoint: str | None

        if image is not None:
            if not self.ENDPOINT_IMAGE:
                return ApiHandler.handle_video_generation_error(
                    model_name, "Image input is not supported for this node"
                )

            image_url = ImageUtils.upload_image(image)
            if not image_url:
                return ApiHandler.handle_video_generation_error(
                    model_name, "Failed to upload image"
                )
            arguments["image_url"] = image_url

            if self.SUPPORTS_TAIL_IMAGE and tail_image is not None:
                tail_image_url = ImageUtils.upload_image(tail_image)
                if not tail_image_url:
                    return ApiHandler.handle_video_generation_error(
                        model_name, "Failed to upload tail image"
                    )
                arguments["tail_image_url"] = tail_image_url

            endpoint = self.ENDPOINT_IMAGE
        else:
            endpoint = self.ENDPOINT_TEXT

        if not endpoint:
            return ApiHandler.handle_video_generation_error(
                model_name, "Endpoint not configured for this node"
            )

        return ApiHandler.run_video_job(model_name, endpoint, arguments)


class KlingNode(_KlingBaseNode):
    MODEL_NAME = "kling-video/v1/standard"
    ENDPOINT_TEXT = "fal-ai/kling-video/v1/standard/text-to-video"
    ENDPOINT_IMAGE = "fal-ai/kling-video/v1/standard/image-to-video"


class KlingPro10Node(_KlingBaseNode):
    MODEL_NAME = "kling-video/v1/pro"
    ENDPOINT_TEXT = "fal-ai/kling-video/v1/pro/text-to-video"
    ENDPOINT_IMAGE = "fal-ai/kling-video/v1/pro/image-to-video"
    SUPPORTS_TAIL_IMAGE = True


class KlingPro16Node(_KlingBaseNode):
    MODEL_NAME = "kling-video/v1.6/pro"
    ENDPOINT_TEXT = "fal-ai/kling-video/v1.6/pro/text-to-video"
    ENDPOINT_IMAGE = "fal-ai/kling-video/v1.6/pro/image-to-video"
    SUPPORTS_TAIL_IMAGE = True


class KlingMasterNode(_KlingBaseNode):
    MODEL_NAME = "kling-video/v2/master"
    ENDPOINT_TEXT = "fal-ai/kling-video/v2/master/text-to-video"
    ENDPOINT_IMAGE = "fal-ai/kling-video/v2/master/image-to-video"


class KlingMaster21Node(_KlingBaseNode):
    MODEL_NAME = "kling-video/v2.1/master"
    ENDPOINT_TEXT = "fal-ai/kling-video/v2.1/master/text-to-video"
    ENDPOINT_IMAGE = "fal-ai/kling-video/v2.1/master/image-to-video"
    SUPPORTS_NEGATIVE_PROMPT = True
    SUPPORTS_CFG_SCALE = True


class KlingTurbo25ProNode(_KlingBaseNode):
    MODEL_NAME = "kling-video/v2.5-turbo/pro"
    ENDPOINT_TEXT = "fal-ai/kling-video/v2.5-turbo/pro/text-to-video"
    ENDPOINT_IMAGE = "fal-ai/kling-video/v2.5-turbo/pro/image-to-video"
    SUPPORTS_TAIL_IMAGE = True
    SUPPORTS_NEGATIVE_PROMPT = True
    SUPPORTS_CFG_SCALE = True


NODE_CLASS_MAPPINGS = {
    "Kling_fal": KlingNode,
    "KlingPro10_fal": KlingPro10Node,
    "KlingPro16_fal": KlingPro16Node,
    "KlingMaster_fal": KlingMasterNode,
    "KlingMaster21_fal": KlingMaster21Node,
    "KlingTurbo25Pro_fal": KlingTurbo25ProNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Kling_fal": "Kling Video Generation (fal)",
    "KlingPro10_fal": "Kling Pro v1.0 Video Generation (fal)",
    "KlingPro16_fal": "Kling Pro v1.6 Video Generation (fal)",
    "KlingMaster_fal": "Kling Master v2.0 Video Generation (fal)",
    "KlingMaster21_fal": "Kling Master v2.1 Video Generation (fal)",
    "KlingTurbo25Pro_fal": "Kling Turbo v2.5 Pro Video Generation (fal)",
}
