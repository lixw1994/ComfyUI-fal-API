from __future__ import annotations

from ..fal_utils import ApiHandler, ImageUtils


class LumaDreamMachineNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "mode": (
                    ["text-to-video", "image-to-video"],
                    {"default": "text-to-video"},
                ),
                "aspect_ratio": (
                    ["16:9", "9:16", "4:3", "3:4", "21:9", "9:21"],
                    {"default": "16:9"},
                ),
            },
            "optional": {
                "image": ("IMAGE",),
                "end_image": ("IMAGE",),
                "loop": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/VideoGeneration"

    def generate_video(
        self, prompt, mode, aspect_ratio, image=None, end_image=None, loop=False
    ):
        arguments = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "loop": loop,
        }

        model_name = "luma-dream-machine"

        if mode == "image-to-video":
            if image is None:
                return ApiHandler.handle_video_generation_error(
                    model_name, "Image is required for image-to-video mode"
                )
            image_url = ImageUtils.upload_image(image)
            if not image_url:
                return ApiHandler.handle_video_generation_error(
                    model_name, "Failed to upload image"
                )
            arguments["image_url"] = image_url

            if end_image is not None:
                end_image_url = ImageUtils.upload_image(end_image)
                if not end_image_url:
                    return ApiHandler.handle_video_generation_error(
                        model_name, "Failed to upload end image"
                    )
                arguments["end_image_url"] = end_image_url

            endpoint = "fal-ai/luma-dream-machine/ray-2/image-to-video"
        else:
            endpoint = "fal-ai/luma-dream-machine/ray-2"

        return ApiHandler.run_video_job(model_name, endpoint, arguments)


NODE_CLASS_MAPPINGS = {
    "LumaDreamMachine_fal": LumaDreamMachineNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LumaDreamMachine_fal": "Luma Dream Machine (fal)",
}
