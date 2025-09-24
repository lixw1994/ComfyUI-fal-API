from __future__ import annotations

from ..fal_utils import ApiHandler


class Sana:
    CATEGORY = "FAL/Image"
    MODEL_NAME = "Sana"
    FAL_ENDPOINT = "fal-ai/sana"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
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
                    {"default": 3840, "min": 512, "max": 4096, "step": 16},
                ),
                "height": (
                    "INT",
                    {"default": 2160, "min": 512, "max": 4096, "step": 16},
                ),
                "num_inference_steps": ("INT", {"default": 18, "min": 1, "max": 50}),
                "guidance_scale": (
                    "FLOAT",
                    {"default": 5.0, "min": 1.0, "max": 20.0, "step": 0.1},
                ),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4}),
            },
            "optional": {
                "negative_prompt": ("STRING", {"default": "", "multiline": True}),
                "seed": ("INT", {"default": -1}),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
                "output_format": (["png", "jpeg"], {"default": "png"}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"

    def generate_image(
        self,
        prompt,
        image_size,
        width,
        height,
        num_inference_steps,
        guidance_scale,
        num_images,
        negative_prompt="",
        seed=-1,
        enable_safety_checker=True,
        output_format="png",
    ):
        arguments = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "num_images": num_images,
            "enable_safety_checker": enable_safety_checker,
            "output_format": output_format,
        }

        if image_size == "custom":
            arguments["image_size"] = {"width": width, "height": height}
        else:
            arguments["image_size"] = image_size

        if seed != -1:
            arguments["seed"] = seed

        return ApiHandler.run_image_job(
            self.MODEL_NAME, self.FAL_ENDPOINT, arguments
        )


NODE_CLASS_MAPPINGS = {
    "Sana_fal": Sana,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Sana_fal": "Sana (fal)",
}
