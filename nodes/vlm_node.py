from .fal_utils import ApiHandler, ImageUtils


class VLMNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "model": (
                    [
                        "google/gemini-2.0-flash-001",
                        "google/gemini-2.5-flash",
                        "google/gemini-2.5-flash-lite",
                        "google/gemini-2.5-pro",
                        "anthropic/claude-3.7-sonnet",
                        "anthropic/claude-3.5-sonnet",
                        "anthropic/claude-3-5-haiku",
                        "anthropic/claude-3-haiku",
                        "deepseek/deepseek-r1",
                        "openai/gpt-4o",
                        "openai/gpt-4o-mini",
                        "openai/gpt-4.1",
                        "openai/gpt-5-chat",
                        "openai/gpt-5-mini",
                        "openai/gpt-5-nano",
                        "openai/gpt-oss-120b",
                        "openai/o3",
                    ],
                    {"default": "google/gemini-2.0-flash-001"},
                ),
                "system_prompt": ("STRING", {"default": "", "multiline": True}),
                "image": ("IMAGE",),
            },
            "optional": {
                "reasoning": ("BOOLEAN", {"default": False}),
                "priority": (
                    ["throughput", "latency"],
                    {"default": "latency"},
                ),
                "temperature": (
                    "FLOAT",
                    {"default": 0.7, "min": 0.0, "max": 2.0, "step": 0.1},
                ),
                "max_tokens": (
                    "INT",
                    {"default": 1024, "min": 1, "max": 32768, "step": 1},
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_text"
    CATEGORY = "FAL/VLM"

    def generate_text(
        self,
        prompt,
        model,
        system_prompt,
        image,
        reasoning=False,
        priority="latency",
        temperature=0.7,
        max_tokens=1024,
    ):
        try:
            image_url = ImageUtils.upload_image(image)
            if not image_url:
                return ApiHandler.handle_text_generation_error(
                    model, "Failed to upload image"
                )

            arguments = {
                "model": model,
                "prompt": prompt,
                "system_prompt": system_prompt,
                "image_url": image_url,
            }

            if reasoning:
                arguments["reasoning"] = reasoning

            if priority:
                arguments["priority"] = priority

            if temperature is not None:
                arguments["temperature"] = float(temperature)

            if max_tokens is not None and max_tokens > 0:
                arguments["max_tokens"] = int(max_tokens)

            return ApiHandler.run_text_job(
                model, "fal-ai/any-llm/vision", arguments
            )
        except Exception as e:
            return ApiHandler.handle_text_generation_error(model, str(e))


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "VLM_fal": VLMNode,
}

# Node display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
    "VLM_fal": "VLM (fal)",
}
