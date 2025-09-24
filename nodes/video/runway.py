from __future__ import annotations

from ..fal_utils import ApiHandler, ImageUtils


class RunwayGen3Node:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image": ("IMAGE",),
                "duration": (["5", "10"], {"default": "5"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_video"
    CATEGORY = "FAL/VideoGeneration"

    def generate_video(self, prompt, image, duration):
        try:
            image_url = ImageUtils.upload_image(image)
            if not image_url:
                return ApiHandler.handle_video_generation_error(
                    "runway-gen3", "Failed to upload image"
                )

            arguments = {
                "prompt": prompt,
                "image_url": image_url,
                "duration": duration,
            }

            return ApiHandler.run_video_job(
                "runway-gen3", "fal-ai/runway-gen3/turbo/image-to-video", arguments
            )
        except Exception as e:
            return ApiHandler.handle_video_generation_error("runway-gen3", str(e))


NODE_CLASS_MAPPINGS = {
    "RunwayGen3_fal": RunwayGen3Node,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwayGen3_fal": "Runway Gen3 Image-to-Video (fal)",
}
