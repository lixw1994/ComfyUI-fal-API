from __future__ import annotations

from ..fal_utils import ApiHandler, ImageUtils, ResultProcessor


class QwenImageEdit:
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
                "sync_mode": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "negative_prompt": ("STRING", {"default": "", "multiline": True}),
                "seed": ("INT", {"default": -1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "edit_image"
    CATEGORY = "FAL/Image"

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
        sync_mode,
        negative_prompt="",
        seed=-1,
    ):
        model_name = "Qwen Image Edit"
        image_url = ImageUtils.upload_image(image)
        if not image_url:
            print(f"Error: Failed to upload image for {model_name}")
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
            "sync_mode": sync_mode,
        }

        if image_size == "custom":
            arguments["image_size"] = {"width": width, "height": height}
        else:
            arguments["image_size"] = image_size

        if negative_prompt:
            arguments["negative_prompt"] = negative_prompt

        if seed != -1:
            arguments["seed"] = seed

        return ApiHandler.run_image_job(model_name, "fal-ai/qwen-image-edit", arguments)


NODE_CLASS_MAPPINGS = {
    "QwenImageEdit_fal": QwenImageEdit,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "QwenImageEdit_fal": "Qwen Image Edit (fal)",
}
