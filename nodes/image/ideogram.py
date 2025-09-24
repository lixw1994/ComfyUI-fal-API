from __future__ import annotations

from ..fal_utils import ApiHandler


class Ideogramv3:
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
                    {"default": "landscape_4_3"},
                ),
                "width": (
                    "INT",
                    {"default": 1024, "min": 512, "max": 1440, "step": 32},
                ),
                "height": (
                    "INT",
                    {"default": 768, "min": 512, "max": 1440, "step": 32},
                ),
                "num_inference_steps": ("INT", {"default": 28, "min": 1, "max": 100}),
                "guidance_scale": ("FLOAT", {"default": 3.5, "min": 0.0, "max": 20.0}),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 10}),
                "safety_tolerance": (["1", "2", "3", "4", "5", "6"], {"default": "2"}),
            },
            "optional": {
                "seed": ("INT", {"default": -1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"
    CATEGORY = "FAL/Image"

    def generate_image(
        self,
        prompt,
        image_size,
        width,
        height,
        num_inference_steps,
        guidance_scale,
        num_images,
        safety_tolerance,
        seed=-1,
    ):
        arguments = {
            "prompt": prompt,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "num_images": num_images,
            "safety_tolerance": safety_tolerance,
        }
        if image_size == "custom":
            arguments["image_size"] = {"width": width, "height": height}
        else:
            arguments["image_size"] = image_size
        if seed != -1:
            arguments["seed"] = seed

        return ApiHandler.run_image_job("Ideogramv3", "fal-ai/ideogram/v3", arguments)


NODE_CLASS_MAPPINGS = {
    "Ideogramv3_fal": Ideogramv3,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Ideogramv3_fal": "Ideogramv3 (fal)",
}
