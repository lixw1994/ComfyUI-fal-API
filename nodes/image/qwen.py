from __future__ import annotations

from typing import List

from ..fal_utils import ApiHandler, ImageUtils, ResultProcessor

_IMAGE_SIZE_CHOICES = [
    "square_hd",
    "square",
    "portrait_4_3",
    "portrait_16_9",
    "landscape_4_3",
    "landscape_16_9",
    "custom",
]

_ACCELERATION_CHOICES = ["none", "regular", "high"]
_OUTPUT_FORMAT_CHOICES = ["png", "jpeg"]


def _serialize_image_size(image_size: str, width: int, height: int):
    if image_size == "custom":
        return {"width": width, "height": height}
    return image_size


class QwenImageTextToImage:
    CATEGORY = "FAL/Image"
    MODEL_NAME = "Qwen Image Text-to-Image"
    FAL_ENDPOINT = "fal-ai/qwen-image"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image_size": (_IMAGE_SIZE_CHOICES, {"default": "square_hd"}),
                "width": ("INT", {"default": 1024, "min": 256, "max": 2048, "step": 8}),
                "height": ("INT", {"default": 1024, "min": 256, "max": 2048, "step": 8}),
            },
            "optional": {
                "num_inference_steps": ("INT", {"default": 30, "min": 1, "max": 100}),
                "guidance_scale": ("FLOAT", {"default": 4.0, "min": 0.0, "max": 20.0, "step": 0.1}),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4}),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
                "output_format": (_OUTPUT_FORMAT_CHOICES, {"default": "png"}),
                "acceleration": (_ACCELERATION_CHOICES, {"default": "none"}),
                "negative_prompt": ("STRING", {"default": "", "multiline": True}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**32 - 1}),
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
        num_inference_steps=30,
        guidance_scale=4.0,
        num_images=1,
        enable_safety_checker=True,
        output_format="png",
        acceleration="none",
        negative_prompt="",
        seed=-1,
    ):
        arguments = {
            "prompt": prompt,
            "image_size": _serialize_image_size(image_size, width, height),
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "num_images": num_images,
            "enable_safety_checker": enable_safety_checker,
            "output_format": output_format,
            "acceleration": acceleration,
        }

        if negative_prompt:
            arguments["negative_prompt"] = negative_prompt
        if seed != -1:
            arguments["seed"] = seed

        return ApiHandler.run_image_job(
            self.MODEL_NAME, self.FAL_ENDPOINT, arguments
        )


class QwenImageImageToImage:
    CATEGORY = "FAL/Image"
    MODEL_NAME = "Qwen Image-to-Image"
    FAL_ENDPOINT = "fal-ai/qwen-image/image-to-image"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image": ("IMAGE",),
                "image_size": (_IMAGE_SIZE_CHOICES, {"default": "square_hd"}),
                "width": ("INT", {"default": 1024, "min": 256, "max": 2048, "step": 8}),
                "height": ("INT", {"default": 1024, "min": 256, "max": 2048, "step": 8}),
            },
            "optional": {
                "image_strength": ("FLOAT", {"default": 0.8, "min": 0.0, "max": 1.0, "step": 0.05}),
                "num_inference_steps": ("INT", {"default": 30, "min": 1, "max": 100}),
                "guidance_scale": ("FLOAT", {"default": 4.0, "min": 0.0, "max": 20.0, "step": 0.1}),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4}),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
                "output_format": (_OUTPUT_FORMAT_CHOICES, {"default": "png"}),
                "acceleration": (_ACCELERATION_CHOICES, {"default": "none"}),
                "negative_prompt": ("STRING", {"default": "", "multiline": True}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**32 - 1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"

    def generate_image(
        self,
        prompt,
        image,
        image_size,
        width,
        height,
        image_strength=0.8,
        num_inference_steps=30,
        guidance_scale=4.0,
        num_images=1,
        enable_safety_checker=True,
        output_format="png",
        acceleration="none",
        negative_prompt="",
        seed=-1,
    ):
        image_url = ImageUtils.upload_image(image)
        if not image_url:
            print("Error: Failed to upload reference image for Qwen image-to-image")
            return ResultProcessor.create_blank_image()

        arguments = {
            "prompt": prompt,
            "image_url": image_url,
            "image_size": _serialize_image_size(image_size, width, height),
            "image_strength": image_strength,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "num_images": num_images,
            "enable_safety_checker": enable_safety_checker,
            "output_format": output_format,
            "acceleration": acceleration,
        }

        if negative_prompt:
            arguments["negative_prompt"] = negative_prompt
        if seed != -1:
            arguments["seed"] = seed

        return ApiHandler.run_image_job(
            self.MODEL_NAME, self.FAL_ENDPOINT, arguments
        )


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
                "image_size": (_IMAGE_SIZE_CHOICES, {"default": "square_hd"}),
                "width": ("INT", {"default": 1024, "min": 256, "max": 2048, "step": 8}),
                "height": ("INT", {"default": 1024, "min": 256, "max": 2048, "step": 8}),
            },
            "optional": {
                "num_inference_steps": ("INT", {"default": 30, "min": 1, "max": 100}),
                "guidance_scale": ("FLOAT", {"default": 4.0, "min": 0.0, "max": 20.0, "step": 0.1}),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4}),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
                "output_format": (_OUTPUT_FORMAT_CHOICES, {"default": "png"}),
                "acceleration": (_ACCELERATION_CHOICES, {"default": "none"}),
                "negative_prompt": ("STRING", {"default": "", "multiline": True}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**32 - 1}),
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
        num_inference_steps=30,
        guidance_scale=4.0,
        num_images=1,
        enable_safety_checker=True,
        output_format="png",
        acceleration="none",
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
            "image_size": _serialize_image_size(image_size, width, height),
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "num_images": num_images,
            "enable_safety_checker": enable_safety_checker,
            "output_format": output_format,
            "acceleration": acceleration,
        }

        if negative_prompt:
            arguments["negative_prompt"] = negative_prompt
        if seed != -1:
            arguments["seed"] = seed

        return ApiHandler.run_image_job(
            self.MODEL_NAME, self.FAL_ENDPOINT, arguments
        )


class QwenImageEditInpaint:
    CATEGORY = "FAL/Image"
    MODEL_NAME = "Qwen Image Edit Inpaint"
    FAL_ENDPOINT = "fal-ai/qwen-image-edit/inpaint"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image": ("IMAGE",),
                "mask": ("MASK",),
                "image_size": (_IMAGE_SIZE_CHOICES, {"default": "square_hd"}),
                "width": ("INT", {"default": 1024, "min": 256, "max": 2048, "step": 8}),
                "height": ("INT", {"default": 1024, "min": 256, "max": 2048, "step": 8}),
            },
            "optional": {
                "num_inference_steps": ("INT", {"default": 30, "min": 1, "max": 100}),
                "guidance_scale": ("FLOAT", {"default": 4.0, "min": 0.0, "max": 20.0, "step": 0.1}),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4}),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
                "output_format": (_OUTPUT_FORMAT_CHOICES, {"default": "png"}),
                "acceleration": (_ACCELERATION_CHOICES, {"default": "none"}),
                "negative_prompt": ("STRING", {"default": "", "multiline": True}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**32 - 1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"

    def generate_image(
        self,
        prompt,
        image,
        mask,
        image_size,
        width,
        height,
        num_inference_steps=30,
        guidance_scale=4.0,
        num_images=1,
        enable_safety_checker=True,
        output_format="png",
        acceleration="none",
        negative_prompt="",
        seed=-1,
    ):
        image_url = ImageUtils.upload_image(image)
        if not image_url:
            print(f"Error: Failed to upload image for {self.MODEL_NAME}")
            return ResultProcessor.create_blank_image()

        mask_image = ImageUtils.mask_to_image(mask)
        mask_url = ImageUtils.upload_image(mask_image)
        if not mask_url:
            print(f"Error: Failed to upload mask for {self.MODEL_NAME}")
            return ResultProcessor.create_blank_image()

        arguments = {
            "prompt": prompt,
            "image_url": image_url,
            "mask_image_url": mask_url,
            "image_size": _serialize_image_size(image_size, width, height),
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "num_images": num_images,
            "enable_safety_checker": enable_safety_checker,
            "output_format": output_format,
            "acceleration": acceleration,
        }

        if negative_prompt:
            arguments["negative_prompt"] = negative_prompt
        if seed != -1:
            arguments["seed"] = seed

        return ApiHandler.run_image_job(
            self.MODEL_NAME, self.FAL_ENDPOINT, arguments
        )


class QwenImageEditPlus:
    CATEGORY = "FAL/Image"
    MODEL_NAME = "Qwen Image Edit Plus"
    FAL_ENDPOINT = "fal-ai/qwen-image-edit-plus"

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
                "num_inference_steps": ("INT", {"default": 30, "min": 1, "max": 100}),
                "guidance_scale": ("FLOAT", {"default": 4.0, "min": 0.0, "max": 20.0, "step": 0.1}),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4}),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
                "output_format": (_OUTPUT_FORMAT_CHOICES, {"default": "png"}),
                "acceleration": (_ACCELERATION_CHOICES, {"default": "none"}),
                "negative_prompt": ("STRING", {"default": "", "multiline": True}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**32 - 1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"

    def generate_image(
        self,
        prompt,
        image_1,
        image_2=None,
        image_3=None,
        image_4=None,
        num_inference_steps=30,
        guidance_scale=4.0,
        num_images=1,
        enable_safety_checker=True,
        output_format="png",
        acceleration="none",
        negative_prompt="",
        seed=-1,
    ):
        image_inputs = [image_1, image_2, image_3, image_4]
        image_urls: List[str] = []
        for idx, img in enumerate(image_inputs, 1):
            if img is None:
                continue
            url = ImageUtils.upload_image(img)
            if not url:
                print(f"Error: Failed to upload image {idx} for {self.MODEL_NAME}")
                return ResultProcessor.create_blank_image()
            image_urls.append(url)

        if not image_urls:
            print(f"Error: At least one image is required for {self.MODEL_NAME}")
            return ResultProcessor.create_blank_image()

        arguments = {
            "prompt": prompt,
            "image_urls": image_urls,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "num_images": num_images,
            "enable_safety_checker": enable_safety_checker,
            "output_format": output_format,
            "acceleration": acceleration,
        }

        if negative_prompt:
            arguments["negative_prompt"] = negative_prompt
        if seed != -1:
            arguments["seed"] = seed

        return ApiHandler.run_image_job(
            self.MODEL_NAME, self.FAL_ENDPOINT, arguments
        )


NODE_CLASS_MAPPINGS = {
    "QwenImageTextToImage_fal": QwenImageTextToImage,
    "QwenImageImageToImage_fal": QwenImageImageToImage,
    "QwenImageEdit_fal": QwenImageEdit,
    "QwenImageEditInpaint_fal": QwenImageEditInpaint,
    "QwenImageEditPlus_fal": QwenImageEditPlus,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "QwenImageTextToImage_fal": "Qwen Image Text-to-Image (fal)",
    "QwenImageImageToImage_fal": "Qwen Image-to-Image (fal)",
    "QwenImageEdit_fal": "Qwen Image Edit (fal)",
    "QwenImageEditInpaint_fal": "Qwen Image Edit Inpaint (fal)",
    "QwenImageEditPlus_fal": "Qwen Image Edit Plus (fal)",
}
