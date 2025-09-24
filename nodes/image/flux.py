from __future__ import annotations

from ..fal_utils import ApiHandler, ImageUtils, ResultProcessor


class FluxPro:
    CATEGORY = "FAL/Image"
    MODEL_NAME = "FluxPro"
    FAL_ENDPOINT = "fal-ai/flux-pro"

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

        return ApiHandler.run_image_job(
            self.MODEL_NAME, self.FAL_ENDPOINT, arguments
        )


class FluxDev:
    CATEGORY = "FAL/Image"
    MODEL_NAME = "FluxDev"
    FAL_ENDPOINT = "fal-ai/flux/dev"

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
                    {"default": 1024, "min": 512, "max": 1536, "step": 16},
                ),
                "height": (
                    "INT",
                    {"default": 768, "min": 512, "max": 1536, "step": 16},
                ),
                "num_inference_steps": ("INT", {"default": 28, "min": 1, "max": 100}),
                "guidance_scale": ("FLOAT", {"default": 3.5, "min": 0.0, "max": 20.0}),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 10}),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "seed": ("INT", {"default": -1}),
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
        enable_safety_checker,
        seed=-1,
    ):
        arguments = {
            "prompt": prompt,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "num_images": num_images,
            "enable_safety_checker": enable_safety_checker,
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


class FluxSchnell:
    CATEGORY = "FAL/Image"
    MODEL_NAME = "FluxSchnell"
    FAL_ENDPOINT = "fal-ai/flux/schnell"

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
                    {"default": 1024, "min": 512, "max": 1536, "step": 32},
                ),
                "height": (
                    "INT",
                    {"default": 768, "min": 512, "max": 1536, "step": 32},
                ),
                "num_inference_steps": ("INT", {"default": 4, "min": 1, "max": 100}),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 10}),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "seed": ("INT", {"default": -1}),
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
        num_images,
        enable_safety_checker,
        seed=-1,
    ):
        arguments = {
            "prompt": prompt,
            "num_inference_steps": num_inference_steps,
            "num_images": num_images,
            "enable_safety_checker": enable_safety_checker,
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


class FluxPro11:
    CATEGORY = "FAL/Image"
    MODEL_NAME = "FluxPro 1.1"
    FAL_ENDPOINT = "fal-ai/flux-pro/v1.1"

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
                "num_images": ("INT", {"default": 1, "min": 1, "max": 10}),
                "safety_tolerance": (["1", "2", "3", "4", "5", "6"], {"default": "2"}),
            },
            "optional": {
                "seed": ("INT", {"default": -1}),
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
        num_images,
        safety_tolerance,
        seed=-1,
    ):
        arguments = {
            "prompt": prompt,
            "num_images": num_images,
            "safety_tolerance": safety_tolerance,
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


class FluxUltra:
    CATEGORY = "FAL/Image"
    MODEL_NAME = "FluxUltra"
    FAL_ENDPOINT = "fal-ai/flux-pro/v1.1-ultra"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "aspect_ratio": (
                    ["21:9", "16:9", "4:3", "1:1", "3:4", "9:16", "9:21"],
                    {"default": "16:9"},
                ),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 1}),
                "safety_tolerance": (["1", "2", "3", "4", "5", "6"], {"default": "2"}),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
                "raw": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "seed": ("INT", {"default": -1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"

    def generate_image(
        self,
        prompt,
        aspect_ratio,
        num_images,
        safety_tolerance,
        enable_safety_checker,
        raw,
        seed=-1,
    ):
        arguments = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "num_images": num_images,
            "safety_tolerance": safety_tolerance,
            "enable_safety_checker": enable_safety_checker,
            "raw": raw,
        }
        if seed != -1:
            arguments["seed"] = seed

        return ApiHandler.run_image_job(
            self.MODEL_NAME, self.FAL_ENDPOINT, arguments
        )


class FluxLora:
    CATEGORY = "FAL/Image"
    MODEL_NAME = "FluxLora"
    FAL_ENDPOINT = "fal-ai/flux-lora"

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
                    {"default": 1024, "min": 512, "max": 1536, "step": 16},
                ),
                "height": (
                    "INT",
                    {"default": 768, "min": 512, "max": 1536, "step": 16},
                ),
                "num_inference_steps": ("INT", {"default": 28, "min": 1, "max": 50}),
                "guidance_scale": (
                    "FLOAT",
                    {"default": 3.0, "min": 0.0, "max": 20.0, "step": 0.1},
                ),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4}),
                "enable_safety_checker": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "seed": ("INT", {"default": -1}),
                "lora_path_1": ("STRING", {"default": ""}),
                "lora_scale_1": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.05},
                ),
                "lora_path_2": ("STRING", {"default": ""}),
                "lora_scale_2": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.05},
                ),
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
        enable_safety_checker,
        seed=-1,
        lora_path_1="",
        lora_scale_1=1.0,
        lora_path_2="",
        lora_scale_2=1.0,
    ):
        arguments = {
            "prompt": prompt,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "num_images": num_images,
            "enable_safety_checker": enable_safety_checker,
        }
        if image_size == "custom":
            arguments["image_size"] = {"width": width, "height": height}
        else:
            arguments["image_size"] = image_size
        if seed != -1:
            arguments["seed"] = seed

        # Add LoRAs
        loras = []
        if lora_path_1:
            loras.append({"path": lora_path_1, "scale": lora_scale_1})
        if lora_path_2:
            loras.append({"path": lora_path_2, "scale": lora_scale_2})
        if loras:
            arguments["loras"] = loras

        return ApiHandler.run_image_job(
            self.MODEL_NAME, self.FAL_ENDPOINT, arguments
        )


class FluxGeneral:
    CATEGORY = "FAL/Image"
    MODEL_NAME = "FluxGeneral"
    FAL_ENDPOINT = "fal-ai/flux-general"

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
                    {"default": 1024, "min": 512, "max": 1536, "step": 16},
                ),
                "height": (
                    "INT",
                    {"default": 768, "min": 512, "max": 1536, "step": 16},
                ),
                "num_inference_steps": ("INT", {"default": 28, "min": 1, "max": 50}),
                "guidance_scale": (
                    "FLOAT",
                    {"default": 3.0, "min": 0.0, "max": 20.0, "step": 0.1},
                ),
                "real_cfg_scale": (
                    "FLOAT",
                    {"default": 3.3, "min": 0.0, "max": 5.0, "step": 0.1},
                ),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4}),
                "enable_safety_checker": ("BOOLEAN", {"default": False}),
                "use_real_cfg": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "seed": ("INT", {"default": -1}),
                "ip_adapter_scale": (
                    "FLOAT",
                    {"default": 0.6, "min": 0.0, "max": 1.0, "step": 0.1},
                ),
                "controlnet_conditioning_scale": (
                    "FLOAT",
                    {"default": 0.6, "min": 0.0, "max": 1.0, "step": 0.1},
                ),
                "ip_adapters": (
                    ["None", "XLabs-AI/flux-ip-adapter"],
                    {"default": "None"},
                ),
                "controlnets": (
                    [
                        "None",
                        "XLabs-AI/flux-controlnet-depth-v3",
                        "Shakker-Labs/FLUX.1-dev-ControlNet-Depth",
                        "jasperai/Flux.1-dev-Controlnet-Depth",
                        "jasperai/Flux.1-dev-Controlnet-Surface-Normals",
                        "XLabs-AI/flux-controlnet-canny-v3",
                        "InstantX/FLUX.1-dev-Controlnet-Canny",
                        "jasperai/Flux.1-dev-Controlnet-Upscaler",
                        "promeai/FLUX.1-controlnet-lineart-promeai",
                    ],
                    {"default": "None"},
                ),
                "controlnet_unions": (
                    [
                        "None",
                        "Shakker-Labs/FLUX.1-dev-ControlNet-Union-Pro",
                        "InstantX/FLUX.1-dev-Controlnet-Union",
                    ],
                    {"default": "None"},
                ),
                "controlnet_union_control_mode": (
                    ["canny", "tile", "depth", "blur", "pose", "gray", "low_quality"],
                    {"default": "canny"},
                ),
                "control_image": ("IMAGE",),
                "control_mask": ("MASK",),
                "ip_adapter_image": ("IMAGE",),
                "ip_adapter_mask": ("MASK",),
                "lora_path_1": ("STRING", {"default": ""}),
                "lora_scale_1": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.05},
                ),
                "lora_path_2": ("STRING", {"default": ""}),
                "lora_scale_2": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.05},
                ),
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
        real_cfg_scale,
        num_images,
        enable_safety_checker,
        use_real_cfg,
        seed=-1,
        lora_path_1="",
        lora_scale_1=1.0,
        lora_path_2="",
        lora_scale_2=1.0,
        ip_adapter_scale=0.6,
        controlnet_conditioning_scale=0.6,
        controlnet_union_control_mode="canny",
        ip_adapters="None",
        controlnets="None",
        controlnet_unions="None",
        control_image=None,
        control_mask=None,
        ip_adapter_image=None,
        ip_adapter_mask=None,
    ):
        arguments = {
            "prompt": prompt,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "real_cfg_scale": real_cfg_scale,
            "num_images": num_images,
            "enable_safety_checker": enable_safety_checker,
            "use_real_cfg": use_real_cfg,
        }
        if image_size == "custom":
            arguments["image_size"] = {"width": width, "height": height}
        else:
            arguments["image_size"] = image_size
        if seed != -1:
            arguments["seed"] = seed

        # Add ip_adapters if selected
        if ip_adapters != "None":
            arguments["ip_adapters"] = [
                {
                    "path": ip_adapters,
                    "image_encoder_path": "openai/clip-vit-large-patch14",
                    "scale": ip_adapter_scale,
                }
            ]

        # Controlnet mapping
        controlnet_mapping = {
            "XLabs-AI/flux-controlnet-depth-v3": "https://huggingface.co/XLabs-AI/flux-controlnet-depth-v3/resolve/main/flux-depth-controlnet-v3.safetensors",
            "Shakker-Labs/FLUX.1-dev-ControlNet-Depth": "https://huggingface.co/Shakker-Labs/FLUX.1-dev-ControlNet-Depth/resolve/main/diffusion_pytorch_model.safetensors",
            "jasperai/Flux.1-dev-Controlnet-Depth": "https://huggingface.co/jasperai/Flux.1-dev-Controlnet-Depth/resolve/main/diffusion_pytorch_model.safetensors",
            "jasperai/Flux.1-dev-Controlnet-Surface-Normals": "https://huggingface.co/jasperai/Flux.1-dev-Controlnet-Surface-Normals/resolve/main/diffusion_pytorch_model.safetensors",
            "XLabs-AI/flux-controlnet-canny-v3": "https://huggingface.co/XLabs-AI/flux-controlnet-canny-v3/resolve/main/flux-canny-controlnet-v3.safetensors",
            "InstantX/FLUX.1-dev-Controlnet-Canny": "https://huggingface.co/InstantX/FLUX.1-dev-Controlnet-Canny/resolve/main/diffusion_pytorch_model.safetensors",
            "jasperai/Flux.1-dev-Controlnet-Upscaler": "https://huggingface.co/jasperai/Flux.1-dev-Controlnet-Upscaler/resolve/main/diffusion_pytorch_model.safetensors",
            "promeai/FLUX.1-controlnet-lineart-promeai": "https://huggingface.co/promeai/FLUX.1-controlnet-lineart-promeai/resolve/main/diffusion_pytorch_model.safetensors",
        }

        # Add controlnets if selected
        if controlnets != "None":
            controlnet_path = controlnet_mapping.get(controlnets, controlnets)
            arguments["controlnets"] = [
                {
                    "path": controlnet_path,
                    "conditioning_scale": controlnet_conditioning_scale,
                }
            ]

        # Add controlnet_unions if selected
        if controlnet_unions != "None":
            arguments["controlnet_unions"] = [
                {
                    "path": controlnet_unions,
                    "controls": [
                        {
                            "control_mode": controlnet_union_control_mode,
                        }
                    ],
                }
            ]

        # Handle controlnets
        if controlnets != "None" and control_image is not None:
            control_image_url = ImageUtils.upload_image(control_image)
            if control_image_url:
                controlnet_path = controlnet_mapping.get(controlnets, controlnets)
                arguments["controlnets"] = [
                    {
                        "path": controlnet_path,
                        "conditioning_scale": controlnet_conditioning_scale,
                        "control_image_url": control_image_url,
                    }
                ]
                if control_mask is not None:
                    mask_image = ImageUtils.mask_to_image(control_mask)
                    mask_image_url = ImageUtils.upload_image(mask_image)
                    if mask_image_url:
                        arguments["controlnets"][0]["mask_image_url"] = mask_image_url

        # Handle controlnet_unions
        if controlnet_unions != "None" and control_image is not None:
            control_image_url = ImageUtils.upload_image(control_image)
            if control_image_url:
                arguments["controlnet_unions"] = [
                    {
                        "path": controlnet_unions,
                        "controls": [
                            {
                                "control_mode": controlnet_union_control_mode,
                                "control_image_url": control_image_url,
                            }
                        ],
                    }
                ]
                if control_mask is not None:
                    mask_image = ImageUtils.mask_to_image(control_mask)
                    mask_image_url = ImageUtils.upload_image(mask_image)
                    if mask_image_url:
                        arguments["controlnet_unions"][0]["controls"][0][
                            "mask_image_url"
                        ] = mask_image_url

        # Handle ip_adapters
        if ip_adapters != "None" and ip_adapter_image is not None:
            ip_adapter_image_url = ImageUtils.upload_image(ip_adapter_image)
            if ip_adapter_image_url:
                ip_adapter_path = (
                    "https://huggingface.co/XLabs-AI/flux-ip-adapter/resolve/main/flux-ip-adapter.safetensors?download=true"
                    if ip_adapters == "XLabs-AI/flux-ip-adapter"
                    else ip_adapters
                )
                arguments["ip_adapters"] = [
                    {
                        "path": ip_adapter_path,
                        "image_encoder_path": "openai/clip-vit-large-patch14",
                        "image_url": ip_adapter_image_url,
                        "scale": ip_adapter_scale,
                    }
                ]
                if ip_adapter_mask is not None:
                    mask_image = ImageUtils.mask_to_image(ip_adapter_mask)
                    mask_image_url = ImageUtils.upload_image(mask_image)
                    if mask_image_url:
                        arguments["ip_adapters"][0]["mask_image_url"] = mask_image_url

        # Add LoRAs if provided
        loras = []
        if lora_path_1:
            loras.append({"path": lora_path_1, "scale": lora_scale_1})
        if lora_path_2:
            loras.append({"path": lora_path_2, "scale": lora_scale_2})
        if loras:
            arguments["loras"] = loras

        return ApiHandler.run_image_job(
            self.MODEL_NAME, self.FAL_ENDPOINT, arguments
        )


class FluxProKontext:
    CATEGORY = "FAL/Image"
    MODEL_NAME = "Flux Pro Kontext"
    MODEL_NAME_MAX = "Flux Pro Kontext Max"
    FAL_ENDPOINT = "fal-ai/flux-pro/kontext"
    FAL_MAX_ENDPOINT = "fal-ai/flux-pro/kontext/max"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image": ("IMAGE",),
            },
            "optional": {
                "aspect_ratio": (
                    [
                        None,
                        "21:9",
                        "16:9",
                        "4:3",
                        "3:2",
                        "1:1",
                        "2:3",
                        "3:4",
                        "9:16",
                        "9:21",
                    ],
                    {"default": None},
                ),
                "max_quality": ("BOOLEAN", {"default": False}),
                "guidance_scale": (
                    "FLOAT",
                    {"default": 3.5, "min": 1.0, "max": 20.0, "step": 0.1},
                ),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4}),
                "safety_tolerance": (["1", "2", "3", "4", "5", "6"], {"default": "2"}),
                "output_format": (["jpeg", "png"], {"default": "png"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"

    def generate_image(
        self,
        prompt,
        image,
        aspect_ratio="1:1",
        max_quality=False,
        guidance_scale=3.5,
        num_images=1,
        safety_tolerance="2",
        output_format="png",
        seed=0,
    ):
        model_name = self.MODEL_NAME_MAX if max_quality else self.MODEL_NAME

        # Upload the input image to get URL
        image_url = ImageUtils.upload_image(image)
        if not image_url:
            print(f"Error: Failed to upload image for {model_name}")
            return ResultProcessor.create_blank_image()

        # Dynamic endpoint selection based on max_quality toggle
        endpoint = self.FAL_MAX_ENDPOINT if max_quality else self.FAL_ENDPOINT

        arguments = {
            "prompt": prompt,
            "image_url": image_url,
            "aspect_ratio": aspect_ratio,
            "guidance_scale": guidance_scale,
            "num_images": num_images,
            "safety_tolerance": safety_tolerance,
            "output_format": output_format,
        }

        if seed > 0:
            arguments["seed"] = seed

        return ApiHandler.run_image_job(model_name, endpoint, arguments)


class FluxProKontextMulti:
    CATEGORY = "FAL/Image"
    MODEL_NAME = "Flux Pro Kontext Multi"
    MODEL_NAME_MAX = "Flux Pro Kontext Max Multi"
    FAL_ENDPOINT = "fal-ai/flux-pro/kontext/multi"
    FAL_MAX_ENDPOINT = "fal-ai/flux-pro/kontext/max/multi"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image_1": ("IMAGE",),
                "image_2": ("IMAGE",),
            },
            "optional": {
                "image_3": ("IMAGE",),
                "image_4": ("IMAGE",),
                "aspect_ratio": (
                    [
                        None,
                        "21:9",
                        "16:9",
                        "4:3",
                        "3:2",
                        "1:1",
                        "2:3",
                        "3:4",
                        "9:16",
                        "9:21",
                    ],
                    {"default": None},
                ),
                "max_quality": ("BOOLEAN", {"default": False}),
                "guidance_scale": (
                    "FLOAT",
                    {"default": 3.5, "min": 1.0, "max": 20.0, "step": 0.1},
                ),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4}),
                "safety_tolerance": (["1", "2", "3", "4", "5", "6"], {"default": "2"}),
                "output_format": (["jpeg", "png"], {"default": "png"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"

    def generate_image(
        self,
        prompt,
        image_1,
        image_2,
        image_3=None,
        image_4=None,
        aspect_ratio="1:1",
        max_quality=False,
        guidance_scale=3.5,
        num_images=1,
        safety_tolerance="2",
        output_format="png",
        seed=0,
    ):
        model_name = self.MODEL_NAME_MAX if max_quality else self.MODEL_NAME

        # Upload all provided images
        image_urls = []

        for i, img in enumerate([image_1, image_2, image_3, image_4], 1):
            if img is not None:
                url = ImageUtils.upload_image(img)
                if url:
                    image_urls.append(url)
                else:
                    print(f"Error: Failed to upload image {i} for {model_name}")
                    return ResultProcessor.create_blank_image()

        if len(image_urls) < 2:
            print(f"Error: At least 2 images required for {model_name}")
            return ResultProcessor.create_blank_image()

        # Dynamic endpoint selection based on max_quality toggle
        endpoint = self.FAL_MAX_ENDPOINT if max_quality else self.FAL_ENDPOINT

        arguments = {
            "prompt": prompt,
            "image_urls": image_urls,
            "aspect_ratio": aspect_ratio,
            "guidance_scale": guidance_scale,
            "num_images": num_images,
            "safety_tolerance": safety_tolerance,
            "output_format": output_format,
        }

        if seed > 0:
            arguments["seed"] = seed

        return ApiHandler.run_image_job(model_name, endpoint, arguments)


class FluxProKontextTextToImage:
    CATEGORY = "FAL/Image"
    MODEL_NAME = "Flux Pro Kontext Text-to-Image"
    MODEL_NAME_MAX = "Flux Pro Kontext Max Text-to-Image"
    FAL_ENDPOINT = "fal-ai/flux-pro/kontext/text-to-image"
    FAL_MAX_ENDPOINT = "fal-ai/flux-pro/kontext/max/text-to-image"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
            },
            "optional": {
                "aspect_ratio": (
                    ["21:9", "16:9", "4:3", "3:2", "1:1", "2:3", "3:4", "9:16", "9:21"],
                    {"default": "1:1"},
                ),
                "max_quality": ("BOOLEAN", {"default": False}),
                "guidance_scale": (
                    "FLOAT",
                    {"default": 3.5, "min": 1.0, "max": 20.0, "step": 0.1},
                ),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4}),
                "safety_tolerance": (["1", "2", "3", "4", "5", "6"], {"default": "2"}),
                "output_format": (["jpeg", "png"], {"default": "png"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"

    def generate_image(
        self,
        prompt,
        aspect_ratio="1:1",
        max_quality=False,
        guidance_scale=3.5,
        num_images=1,
        safety_tolerance="2",
        output_format="png",
        seed=0,
    ):
        model_name = self.MODEL_NAME_MAX if max_quality else self.MODEL_NAME

        # Dynamic endpoint selection based on max_quality toggle
        endpoint = self.FAL_MAX_ENDPOINT if max_quality else self.FAL_ENDPOINT

        arguments = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "guidance_scale": guidance_scale,
            "num_images": num_images,
            "safety_tolerance": safety_tolerance,
            "output_format": output_format,
        }

        if seed > 0:
            arguments["seed"] = seed

        return ApiHandler.run_image_job(model_name, endpoint, arguments)

NODE_CLASS_MAPPINGS = {
    "FluxPro_fal": FluxPro,
    "FluxDev_fal": FluxDev,
    "FluxSchnell_fal": FluxSchnell,
    "FluxPro11_fal": FluxPro11,
    "FluxUltra_fal": FluxUltra,
    "FluxLora_fal": FluxLora,
    "FluxGeneral_fal": FluxGeneral,
    "FluxProKontext_fal": FluxProKontext,
    "FluxProKontextMulti_fal": FluxProKontextMulti,
    "FluxProKontextTextToImage_fal": FluxProKontextTextToImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FluxPro_fal": "Flux Pro (fal)",
    "FluxDev_fal": "Flux Dev (fal)",
    "FluxSchnell_fal": "Flux Schnell (fal)",
    "FluxPro11_fal": "Flux Pro 1.1 (fal)",
    "FluxUltra_fal": "Flux Ultra (fal)",
    "FluxLora_fal": "Flux LoRA (fal)",
    "FluxGeneral_fal": "Flux General (fal)",
    "FluxProKontext_fal": "Flux Pro Kontext (fal)",
    "FluxProKontextMulti_fal": "Flux Pro Kontext Multi (fal)",
    "FluxProKontextTextToImage_fal": "Flux Pro Kontext Text-to-Image (fal)",
}
