from __future__ import annotations

from ..fal_utils import ApiHandler, ImageUtils, ResultProcessor


class QwenImageEdit:
    CATEGORY = "FAL/Image"
    MODEL_NAME = "Qwen Image Edit"
    FAL_ENDPOINT = "fal-ai/qwen-image-edit"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image": ("IMAGE",),
                "image_size": (
                    [
                        "square_hd",
                        "square",
                        "portrait_4_3",
                        "portrait_16_9",
                        "landscape_4_3",
                        "landscape_16_9",
                        "custom",
                    ],
                    {"default": "square_hd"},
                ),
                "width": (
                    "INT",
                    {"default": 512, "min": 128, "max": 2048, "step": 8},
                ),
                "height": (
                    "INT",
                    {"default": 512, "min": 128, "max": 2048, "step": 8},
                ),
                "num_inference_steps": ("INT", {"default": 30, "min": 1, "max": 50}),
                "guidance_scale": (
                    "FLOAT",
                    {"default": 4.0, "min": 1.0, "max": 20.0, "step": 0.1},
                ),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4}),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
                "output_format": (["png", "jpeg"], {"default": "png"}),
                "acceleration": (["none", "regular", "high"], {"default": "none"}),
            },
            "optional": {
                "negative_prompt": ("STRING", {"default": "", "multiline": True}),
                "seed": ("INT", {"default": -1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "edit_image"

    def edit_image(
        self,
        prompt,
        image,
        image_size,
        width,
        height,
        num_inference_steps,
        guidance_scale,
        num_images,
        enable_safety_checker,
        output_format,
        acceleration,
        negative_prompt="",
        seed=-1,
    ):
        image_url = ImageUtils.upload_image(image)
        if not image_url:
            print(f"Error: Failed to upload image for {self.MODEL_NAME}")
            return ResultProcessor.create_blank_image()

        arguments = {
            "prompt": prompt,
            "image_url": image_url,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "num_images": num_images,
            "enable_safety_checker": enable_safety_checker,
            "output_format": output_format,
            "acceleration": acceleration,
        }

        if image_size == "custom":
            arguments["image_size"] = {"width": width, "height": height}
        else:
            arguments["image_size"] = image_size

        if negative_prompt:
            arguments["negative_prompt"] = negative_prompt

        if seed != -1:
            arguments["seed"] = seed

        return ApiHandler.run_image_job(
            self.MODEL_NAME, self.FAL_ENDPOINT, arguments
        )


NODE_CLASS_MAPPINGS = {
    "QwenImageEdit_fal": QwenImageEdit,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "QwenImageEdit_fal": "Qwen Image Edit (fal)",
}
