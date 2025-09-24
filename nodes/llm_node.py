from .fal_utils import ApiHandler


class LLMNode:
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
                        "anthropic/claude-3-5-haiku",
                        "anthropic/claude-3.5-sonnet",
                        "anthropic/claude-3.7-sonnet",
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
    CATEGORY = "FAL/LLM"

    def generate_text(
        self,
        prompt,
        model,
        system_prompt,
        reasoning=False,
        priority="latency",
        temperature=0.7,
        max_tokens=1024,
    ):
        arguments = {
            "model": model,
            "prompt": prompt,
            "system_prompt": system_prompt,
        }

        if reasoning:
            arguments["reasoning"] = reasoning

        if priority:
            arguments["priority"] = priority

        if temperature is not None:
            arguments["temperature"] = float(temperature)

        if max_tokens is not None and max_tokens > 0:
            arguments["max_tokens"] = int(max_tokens)

        return ApiHandler.run_text_job(model, "fal-ai/any-llm", arguments)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "LLM_fal": LLMNode,
}

# Node display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
    "LLM_fal": "LLM (fal)",
}
