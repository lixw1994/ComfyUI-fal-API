from __future__ import annotations

import asyncio

from fal_client import AsyncClient

from ..fal_utils import FalConfig, ImageUtils

fal_config = FalConfig()


class CombinedVideoGenerationNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image": ("IMAGE",),
                "kling_duration": (["5", "10"], {"default": "5"}),
                "kling_luma_aspect_ratio": (
                    ["16:9", "9:16", "1:1"],
                    {"default": "16:9"},
                ),
                "luma_loop": ("BOOLEAN", {"default": False}),
                "veo2_aspect_ratio": (
                    ["auto", "auto_prefer_portrait", "16:9", "9:16"],
                    {"default": "auto"},
                ),
                "veo2_duration": (["5s", "6s", "7s", "8s"], {"default": "5s"}),
                "enable_klingpro": ("BOOLEAN", {"default": True}),
                "enable_klingmaster": ("BOOLEAN", {"default": True}),
                "enable_minimax": ("BOOLEAN", {"default": True}),
                "enable_luma": ("BOOLEAN", {"default": True}),
                "enable_veo2": ("BOOLEAN", {"default": True}),
                "enable_wanpro": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = (
        "klingpro_v1.6_video",
        "klingmaster_v2.0_video",
        "minimax_video",
        "luma_video",
        "veo2_video",
        "wanpro_video",
    )
    FUNCTION = "generate_videos"
    CATEGORY = "FAL/VideoGeneration"

    async def generate_klingpro_video(
        self, client, prompt, image_url, kling_duration, kling_luma_aspect_ratio
    ):
        try:
            arguments = {
                "prompt": prompt,
                "image_url": image_url,
                "duration": kling_duration,
                "aspect_ratio": kling_luma_aspect_ratio,
            }
            handler = await client.submit(
                "fal-ai/kling-video/v1.6/pro/image-to-video", arguments=arguments
            )
            while True:
                result = await handler.get()
                if "video" in result and "url" in result["video"]:
                    return result["video"]["url"]
                if result.get("status") == "FAILED":
                    raise RuntimeError("Video generation failed")
                await asyncio.sleep(1)
        except Exception as e:
            print(f"Error generating KlingPro video: {str(e)}")
            return "Error: Unable to generate KlingPro video."

    async def generate_klingmaster_video(
        self, client, prompt, image_url, kling_duration, kling_luma_aspect_ratio
    ):
        try:
            arguments = {
                "prompt": prompt,
                "image_url": image_url,
                "duration": kling_duration,
                "aspect_ratio": kling_luma_aspect_ratio,
            }
            handler = await client.submit(
                "fal-ai/kling-video/v2/master/image-to-video", arguments=arguments
            )
            while True:
                result = await handler.get()
                if "video" in result and "url" in result["video"]:
                    return result["video"]["url"]
                if result.get("status") == "FAILED":
                    raise RuntimeError("Video generation failed")
                await asyncio.sleep(1)
        except Exception as e:
            print(f"Error generating KlingMaster video: {str(e)}")
            return "Error: Unable to generate KlingMaster video."

    async def generate_minimax_video(self, client, prompt, image_url):
        try:
            arguments = {
                "prompt": prompt,
                "image_url": image_url,
            }
            handler = await client.submit(
                "fal-ai/minimax/video-01-live/image-to-video", arguments=arguments
            )
            while True:
                result = await handler.get()
                if "video" in result and "url" in result["video"]:
                    return result["video"]["url"]
                if result.get("status") == "FAILED":
                    raise RuntimeError("Video generation failed")
                await asyncio.sleep(1)
        except Exception as e:
            print(f"Error generating MiniMax video: {str(e)}")
            return "Error: Unable to generate MiniMax video."

    async def generate_luma_video(
        self, client, prompt, image_url, kling_luma_aspect_ratio, luma_loop
    ):
        try:
            arguments = {
                "prompt": prompt,
                "image_url": image_url,
                "aspect_ratio": kling_luma_aspect_ratio,
                "loop": luma_loop,
            }
            handler = await client.submit(
                "fal-ai/luma-dream-machine/ray-2/image-to-video", arguments=arguments
            )
            while True:
                result = await handler.get()
                if "video" in result and "url" in result["video"]:
                    return result["video"]["url"]
                if result.get("status") == "FAILED":
                    raise RuntimeError("Video generation failed")
                await asyncio.sleep(1)
        except Exception as e:
            print(f"Error generating Luma video: {str(e)}")
            return "Error: Unable to generate Luma video."

    async def generate_veo2_video(
        self, client, prompt, image_url, aspect_ratio, duration
    ):
        try:
            arguments = {
                "prompt": prompt,
                "image_url": image_url,
                "aspect_ratio": aspect_ratio,
                "duration": duration,
            }
            handler = await client.submit(
                "fal-ai/veo2/image-to-video", arguments=arguments
            )
            while True:
                result = await handler.get()
                if "video" in result and "url" in result["video"]:
                    return result["video"]["url"]
                if result.get("status") == "FAILED":
                    raise RuntimeError("Video generation failed")
                await asyncio.sleep(1)
        except Exception as e:
            print(f"Error generating Veo2 video: {str(e)}")
            return "Error: Unable to generate Veo2 video."

    async def generate_wanpro_video(self, client, prompt, image_url):
        try:
            arguments = {
                "prompt": prompt,
                "image_url": image_url,
                "enable_safety_checker": True,
                "seed": None,
            }

            handler = await client.submit(
                "fal-ai/wan-pro/image-to-video", arguments=arguments
            )
            while True:
                result = await handler.get()
                if "video" in result and "url" in result["video"]:
                    return result["video"]["url"]
                if result.get("status") == "FAILED":
                    raise RuntimeError("Video generation failed")
                await asyncio.sleep(1)
        except Exception as e:
            print(f"Error generating Wan Pro video: {str(e)}")
            return "Error: Unable to generate Wan Pro video."

    async def generate_all_videos(
        self,
        prompt,
        image_url,
        kling_duration,
        kling_luma_aspect_ratio,
        luma_loop,
        veo2_aspect_ratio,
        veo2_duration,
        enable_klingpro,
        enable_klingmaster,
        enable_minimax,
        enable_luma,
        enable_veo2,
        enable_wanpro,
    ):
        try:
            tasks = []
            results = [None] * 6

            client = AsyncClient(key=fal_config.get_key())

            if enable_klingpro:
                tasks.append(
                    self.generate_klingpro_video(
                        client, prompt, image_url, kling_duration, kling_luma_aspect_ratio
                    )
                )
            else:
                tasks.append(None)

            if enable_klingmaster:
                tasks.append(
                    self.generate_klingmaster_video(
                        client, prompt, image_url, kling_duration, kling_luma_aspect_ratio
                    )
                )
            else:
                tasks.append(None)

            if enable_minimax:
                tasks.append(self.generate_minimax_video(client, prompt, image_url))
            else:
                tasks.append(None)

            if enable_luma:
                tasks.append(
                    self.generate_luma_video(
                        client, prompt, image_url, kling_luma_aspect_ratio, luma_loop
                    )
                )
            else:
                tasks.append(None)

            if enable_veo2:
                tasks.append(
                    self.generate_veo2_video(
                        client, prompt, image_url, veo2_aspect_ratio, veo2_duration
                    )
                )
            else:
                tasks.append(None)

            if enable_wanpro:
                tasks.append(self.generate_wanpro_video(client, prompt, image_url))
            else:
                tasks.append(None)

            valid_tasks = [task for task in tasks if task is not None]
            if valid_tasks:
                completed_results = await asyncio.gather(*valid_tasks)

                idx = 0
                for i, task in enumerate(tasks):
                    if task is not None:
                        results[i] = completed_results[idx]
                        idx += 1
                    else:
                        results[i] = "Service disabled"

            return results
        except Exception as e:
            print(f"Error in generate_all_videos: {str(e)}")
            return ["Error: Unable to generate videos."] * 6

    def generate_videos(
        self,
        prompt,
        image,
        kling_duration,
        kling_luma_aspect_ratio,
        luma_loop,
        veo2_aspect_ratio,
        veo2_duration,
        enable_klingpro,
        enable_klingmaster,
        enable_minimax,
        enable_luma,
        enable_veo2,
        enable_wanpro,
    ):
        try:
            image_url = ImageUtils.upload_image(image)
            if not image_url:
                return ("Error: Unable to upload image.",) * 6

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(
                self.generate_all_videos(
                    prompt,
                    image_url,
                    kling_duration,
                    kling_luma_aspect_ratio,
                    luma_loop,
                    veo2_aspect_ratio,
                    veo2_duration,
                    enable_klingpro,
                    enable_klingmaster,
                    enable_minimax,
                    enable_luma,
                    enable_veo2,
                    enable_wanpro,
                )
            )
            loop.close()

            return tuple(results)
        except Exception as e:
            print(f"Error in combined video generation: {str(e)}")
            return ("Error: Unable to generate videos.",) * 6


NODE_CLASS_MAPPINGS = {
    "CombinedVideoGeneration_fal": CombinedVideoGenerationNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CombinedVideoGeneration_fal": "Combined Video Generation (fal)",
}
