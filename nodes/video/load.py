from __future__ import annotations

import os
import tempfile

import cv2
import requests
import torch


class LoadVideoURL:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "url": ("STRING", {"default": "https://example.com/video.mp4"}),
                "force_rate": ("INT", {"default": 0, "min": 0, "max": 60, "step": 1}),
                "force_size": (
                    [
                        "Disabled",
                        "Custom Height",
                        "Custom Width",
                        "Custom",
                        "256x?",
                        "?x256",
                        "256x256",
                        "512x?",
                        "?x512",
                        "512x512",
                    ],
                ),
                "custom_width": (
                    "INT",
                    {"default": 512, "min": 0, "max": 8192, "step": 8},
                ),
                "custom_height": (
                    "INT",
                    {"default": 512, "min": 0, "max": 8192, "step": 8},
                ),
                "frame_load_cap": (
                    "INT",
                    {"default": 0, "min": 0, "max": 1_000_000, "step": 1},
                ),
                "skip_first_frames": (
                    "INT",
                    {"default": 0, "min": 0, "max": 1_000_000, "step": 1},
                ),
                "select_every_nth": (
                    "INT",
                    {"default": 1, "min": 1, "max": 1_000_000, "step": 1},
                ),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "VHS_VIDEOINFO")
    RETURN_NAMES = ("frames", "frame_count", "video_info")
    FUNCTION = "load_video_from_url"
    CATEGORY = "video"

    def load_video_from_url(
        self,
        url,
        force_rate,
        force_size,
        custom_width,
        custom_height,
        frame_load_cap,
        skip_first_frames,
        select_every_nth,
    ):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=8192):
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        cap = cv2.VideoCapture(temp_file_path)

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = total_frames / fps if fps else 0

        if force_size != "Disabled":
            if force_size == "Custom Width":
                new_height = int(height * (custom_width / width))
                new_width = custom_width
            elif force_size == "Custom Height":
                new_width = int(width * (custom_height / height))
                new_height = custom_height
            elif force_size == "Custom":
                new_width, new_height = custom_width, custom_height
            else:
                target_width, target_height = map(
                    int, force_size.replace("?", "0").split("x")
                )
                if target_width == 0:
                    new_width = int(width * (target_height / height))
                    new_height = target_height
                else:
                    new_height = int(height * (target_width / width))
                    new_width = target_width
        else:
            new_width, new_height = width, height

        frames = []
        frame_count = 0

        for i in range(total_frames):
            ret, frame = cap.read()
            if not ret:
                break

            if i < skip_first_frames:
                continue

            if (i - skip_first_frames) % select_every_nth != 0:
                continue

            if force_size != "Disabled":
                frame = cv2.resize(frame, (new_width, new_height))

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = torch.from_numpy(frame).float() / 255.0
            frames.append(frame)

            frame_count += 1

            if frame_load_cap > 0 and frame_count >= frame_load_cap:
                break

        cap.release()
        os.unlink(temp_file_path)

        frames_tensor = torch.stack(frames) if frames else torch.empty(0)

        loaded_fps = fps if force_rate == 0 else force_rate
        video_info = {
            "source_fps": fps,
            "source_frame_count": total_frames,
            "source_duration": duration,
            "source_width": width,
            "source_height": height,
            "loaded_fps": loaded_fps,
            "loaded_frame_count": frame_count,
            "loaded_duration": frame_count / loaded_fps if loaded_fps else 0,
            "loaded_width": new_width,
            "loaded_height": new_height,
        }

        return (frames_tensor, frame_count, video_info)


NODE_CLASS_MAPPINGS = {
    "LoadVideoURL": LoadVideoURL,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadVideoURL": "Load Video from URL",
}
