from __future__ import annotations

from ..fal_utils import ApiHandler, ImageUtils


class MiniMaxNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/VideoGeneration"

    def generate_video(self, prompt, image):
        image_url = ImageUtils.upload_image(image)
        if not image_url:
            return ApiHandler.handle_video_generation_error(
                "minimax/video-01-live", "Failed to upload image"
            )

        arguments = {
            "prompt": prompt,
            "image_url": image_url,
        }

        return ApiHandler.run_video_job(
            "minimax/video-01-live",
            "fal-ai/minimax/video-01-live/image-to-video",
            arguments,
        )


class MiniMaxTextToVideoNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/VideoGeneration"

    def generate_video(self, prompt):
        arguments = {
            "prompt": prompt,
        }

        return ApiHandler.run_video_job(
            "minimax-video", "fal-ai/minimax-video", arguments
        )


class MiniMaxSubjectReferenceNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "subject_reference_image": ("IMAGE",),
                "prompt_optimizer": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/VideoGeneration"

    def generate_video(self, prompt, subject_reference_image, prompt_optimizer):
        image_url = ImageUtils.upload_image(subject_reference_image)
        if not image_url:
            return ApiHandler.handle_video_generation_error(
                "minimax/video-01-subject-reference",
                "Failed to upload subject reference image",
            )

        arguments = {
            "prompt": prompt,
            "subject_reference_image_url": image_url,
            "prompt_optimizer": prompt_optimizer,
        }

        return ApiHandler.run_video_job(
            "minimax/video-01-subject-reference",
            "fal-ai/minimax/video-01-subject-reference",
            arguments,
        )


NODE_CLASS_MAPPINGS = {
    "MiniMax_fal": MiniMaxNode,
    "MiniMaxTextToVideo_fal": MiniMaxTextToVideoNode,
    "MiniMaxSubjectReference_fal": MiniMaxSubjectReferenceNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MiniMax_fal": "MiniMax Video Generation (fal)",
    "MiniMaxTextToVideo_fal": "MiniMax Text-to-Video (fal)",
    "MiniMaxSubjectReference_fal": "MiniMax Subject Reference (fal)",
}
