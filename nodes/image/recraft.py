from __future__ import annotations

from ..fal_utils import ApiHandler


class Recraft:
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
                    {"default": 512, "min": 512, "max": 2048, "step": 16},
                ),
                "height": (
                    "INT",
                    {"default": 512, "min": 512, "max": 2048, "step": 16},
                ),
                "style": (
                    [
                        "any",
                        "realistic_image",
                        "digital_illustration",
                        "vector_illustration",
                        "realistic_image/b_and_w",
                        "realistic_image/hard_flash",
                        "realistic_image/hdr",
                        "realistic_image/natural_light",
                        "realistic_image/studio_portrait",
                        "realistic_image/enterprise",
                        "realistic_image/motion_blur",
                        "digital_illustration/pixel_art",
                        "digital_illustration/hand_drawn",
                        "digital_illustration/grain",
                        "digital_illustration/infantile_sketch",
                        "digital_illustration/2d_art_poster",
                        "digital_illustration/handmade_3d",
                        "digital_illustration/hand_drawn_outline",
                        "digital_illustration/engraving_color",
                        "digital_illustration/2d_art_poster_2",
                        "vector_illustration/engraving",
                        "vector_illustration/line_art",
                        "vector_illustration/line_circuit",
                        "vector_illustration/linocut",
                    ],
                    {"default": "realistic_image"},
                ),
            },
            "optional": {
                "style_id": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"
    CATEGORY = "FAL/Image"

    def generate_image(self, prompt, image_size, width, height, style, style_id=""):
        arguments = {
            "prompt": prompt,
            "style": style,
        }

        if image_size == "custom":
            arguments["image_size"] = {"width": width, "height": height}
        else:
            arguments["image_size"] = image_size

        if style_id:
            arguments["style_id"] = style_id

        return ApiHandler.run_image_job("Recraft", "fal-ai/recraft-v3", arguments)


NODE_CLASS_MAPPINGS = {
    "Recraft_fal": Recraft,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Recraft_fal": "Recraft V3 (fal)",
}
