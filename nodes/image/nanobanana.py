from __future__ import annotations

from ..fal_utils import ApiHandler, ImageUtils, ResultProcessor

class NanoBanana:
    ENDPOINT = "fal-ai/nano-banana"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
            },
            "optional": {
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4}),
                "output_format": (["jpeg", "png"], {"default": "jpeg"}),
                "sync_mode": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"
    CATEGORY = "FAL/Image"

    def generate_image(
        self,
        prompt,
        num_images=1,
        output_format="jpeg",
        sync_mode=False,
    ):
        arguments = {
            "prompt": prompt,
            "num_images": num_images,
            "output_format": output_format,
        }

        if sync_mode:
            arguments["sync_mode"] = sync_mode

        return ApiHandler.run_image_job("Nano Banana", self.ENDPOINT, arguments)


class NanoBananaEdit:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image_1": ("IMAGE",),
            },
            "optional": {
                "image_2": ("IMAGE",),
                "image_3": ("IMAGE",),
                "image_4": ("IMAGE",),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4}),
                "output_format": (["jpeg", "png"], {"default": "jpeg"}),
                "sync_mode": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"
    CATEGORY = "FAL/Image"

    def generate_image(
        self,
        prompt,
        image_1,
        image_2=None,
        image_3=None,
        image_4=None,
        num_images=1,
        output_format="jpeg",
        sync_mode=False,
    ):
        image_urls = []

        for i, img in enumerate([image_1, image_2, image_3, image_4], 1):
            if img is None:
                continue
            url = ImageUtils.upload_image(img)
            if url:
                image_urls.append(url)
            else:
                print(f"Error: Failed to upload image {i} for Nano Banana Edit")
                return ResultProcessor.create_blank_image()

        if not image_urls:
            print("Error: At least one image is required for Nano Banana Edit")
            return ResultProcessor.create_blank_image()

        arguments = {
            "prompt": prompt,
            "num_images": num_images,
            "output_format": output_format,
        }

        arguments["image_urls"] = image_urls

        if sync_mode:
            arguments["sync_mode"] = sync_mode

        return ApiHandler.run_image_job(
            "Nano Banana Edit", "fal-ai/nano-banana/edit", arguments
        )


# Node class mappings

NODE_CLASS_MAPPINGS = {
    "NanoBanana_fal": NanoBanana,
    "NanoBananaEdit_fal": NanoBananaEdit,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "NanoBanana_fal": "Nano Banana (fal)",
    "NanoBananaEdit_fal": "Nano Banana Edit (fal)",
}
