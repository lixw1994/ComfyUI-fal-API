from __future__ import annotations

from ..fal_utils import ApiHandler, ImageUtils

class Seedream4TextToImage:
    ENDPOINT = "fal-ai/bytedance/seedream/v4/text-to-image"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "guidance_scale": (
                    "FLOAT",
                    {"default": 3.5, "min": 0.0, "max": 20.0, "step": 0.1},
                ),
                "num_inference_steps": (
                    "INT",
                    {"default": 28, "min": 1, "max": 100},
                ),
            },
            "optional": {
                "negative_prompt": ("STRING", {"default": "", "multiline": True}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2147483647}),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4}),
                "output_format": (["jpeg", "png"], {"default": "jpeg"}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"
    CATEGORY = "FAL/Image"

    def generate_image(
        self,
        prompt,
        guidance_scale,
        num_inference_steps,
        negative_prompt="",
        seed=-1,
        num_images=1,
        output_format="jpeg",
    ):
        arguments = {
            "prompt": prompt,
            "guidance_scale": guidance_scale,
            "num_inference_steps": num_inference_steps,
            "negative_prompt": negative_prompt,
            "num_images": num_images,
            "output_format": output_format,
        }

        if seed != -1:
            arguments["seed"] = seed

        return ApiHandler.run_image_job(
            "Seedream4 Text-to-Image", self.ENDPOINT, arguments
        )


class Seedream4ImageEdit:
    ENDPOINT = "fal-ai/bytedance/seedream/v4/edit"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image": ("IMAGE",),
            },
            "optional": {
                "guidance_scale": (
                    "FLOAT",
                    {"default": 3.5, "min": 0.0, "max": 20.0, "step": 0.1},
                ),
                "num_inference_steps": (
                    "INT",
                    {"default": 28, "min": 1, "max": 100},
                ),
                "image_strength": (
                    "FLOAT",
                    {"default": 0.7, "min": 0.0, "max": 1.0, "step": 0.05},
                ),
                "negative_prompt": ("STRING", {"default": "", "multiline": True}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2147483647}),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4}),
                "output_format": (["jpeg", "png"], {"default": "jpeg"}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"
    CATEGORY = "FAL/Image"

    def generate_image(
        self,
        prompt,
        image,
        guidance_scale=3.5,
        num_inference_steps=28,
        image_strength=0.7,
        negative_prompt="",
        seed=-1,
        num_images=1,
        output_format="jpeg",
    ):
        image_url = ImageUtils.upload_image(image)
        if not image_url:
            return ApiHandler.handle_image_generation_error(
                "Seedream4 Edit", "Failed to upload reference image"
            )

        arguments = {
            "prompt": prompt,
            "image_url": image_url,
            "guidance_scale": guidance_scale,
            "num_inference_steps": num_inference_steps,
            "image_strength": image_strength,
            "negative_prompt": negative_prompt,
            "num_images": num_images,
            "output_format": output_format,
        }

        if seed != -1:
            arguments["seed"] = seed

        return ApiHandler.run_image_job("Seedream4 Edit", self.ENDPOINT, arguments)

NODE_CLASS_MAPPINGS = {
    "Seedream4TextToImage_fal": Seedream4TextToImage,
    "Seedream4Edit_fal": Seedream4ImageEdit,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Seedream4TextToImage_fal": "Seedream4 Text-to-Image (fal)",
    "Seedream4Edit_fal": "Seedream4 Edit (fal)",
}
