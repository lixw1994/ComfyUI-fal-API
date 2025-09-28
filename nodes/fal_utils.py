import configparser
import io
import os
import tempfile
import threading
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

import numpy as np
import requests
from requests import HTTPError
import torch
from fal_client.client import Completed, SyncClient
from PIL import Image
import cv2

# Default timeouts/polling can be tuned via env vars when integrating in different environments
_HTTP_TIMEOUT_SECONDS = float(os.getenv("FAL_HTTP_TIMEOUT", "30"))
_JOB_TIMEOUT_SECONDS = float(os.getenv("FAL_JOB_TIMEOUT", "600"))
_JOB_POLL_INTERVAL_SECONDS = float(os.getenv("FAL_JOB_POLL_INTERVAL", "0.25"))

# Reuse a global session for media downloads to amortize TCP setup cost
_HTTP_SESSION = requests.Session()


class FalConfig:
    """Manage access to the fal.ai API client and credentials."""

    _instance: Optional["FalConfig"] = None
    _instance_lock = threading.Lock()

    def __new__(cls) -> "FalConfig":
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        config_path = os.path.join(parent_dir, "config.ini")

        config = configparser.ConfigParser()
        config.read(config_path)

        env_key = os.environ.get("FAL_KEY", "").strip()
        file_key = config.get("API", "FAL_KEY", fallback="").strip()

        self._key: Optional[str] = env_key or file_key or None
        self._client: Optional[SyncClient] = None
        self._client_lock = threading.Lock()

        if not self._key:
            print("Warning: FAL_KEY missing from environment and config.ini")
        elif self._key == "<your_fal_api_key_here>":
            print("Warning: FAL_KEY is still set to the placeholder value from config.ini")

    def refresh_key(self, key: str) -> None:
        """Allow consumers to hot-swap API keys (invalidates the cached client)."""

        with self._client_lock:
            self._key = key.strip() if key else None
            self._client = None

    def get_client(self) -> SyncClient:
        """Get or create a SyncClient using the configured API key."""

        if not self._key:
            raise RuntimeError(
                "FAL_KEY is not configured. Set the FAL_KEY environment variable or update config.ini."
            )

        with self._client_lock:
            if self._client is None:
                self._client = SyncClient(key=self._key)
            return self._client

    def get_key(self) -> Optional[str]:
        return self._key


class ImageUtils:
    """Utility functions for image processing and uploads."""

    @staticmethod
    def tensor_to_pil(image):
        """Convert image tensor to PIL Image."""
        try:
            # Convert the image tensor to a numpy array
            if isinstance(image, torch.Tensor):
                image_np = image.cpu().numpy()
            else:
                image_np = np.array(image)

            # Ensure the image is in the correct format (H, W, C)
            if image_np.ndim == 4:
                image_np = image_np.squeeze(0)  # Remove batch dimension if present
            if image_np.ndim == 2:
                image_np = np.stack([image_np] * 3, axis=-1)  # Convert grayscale to RGB
            elif image_np.shape[0] == 3:
                image_np = np.transpose(
                    image_np, (1, 2, 0)
                )  # Change from (C, H, W) to (H, W, C)

            # Normalize the image data to 0-255 range
            if image_np.dtype == np.float32 or image_np.dtype == np.float64:
                image_np = (image_np * 255).astype(np.uint8)

            # Convert to PIL Image
            return Image.fromarray(image_np)
        except Exception as e:
            print(f"Error converting tensor to PIL: {str(e)}")
            return None

    @staticmethod
    def upload_image(image):
        """Upload image tensor to FAL and return URL."""
        try:
            pil_image = ImageUtils.tensor_to_pil(image)
            if not pil_image:
                return None

            buffered = io.BytesIO()
            pil_image.save(buffered, format="PNG")
            buffered.seek(0)

            client = FalConfig().get_client()
            try:
                return client.upload_image(pil_image, format="png")
            except Exception:
                # Fallback to raw bytes upload for older fal-client versions
                return client.upload(
                    buffered.getvalue(), content_type="image/png", file_name="upload.png"
                )
        except Exception as e:
            print(f"Error uploading image: {str(e)}")
            return None

    @staticmethod
    def mask_to_image(mask):
        """Convert mask tensor to image tensor."""
        result = (
            mask.reshape((-1, 1, mask.shape[-2], mask.shape[-1]))
            .movedim(1, -1)
            .expand(-1, -1, -1, 3)
        )
        return result


class VideoUtils:
    """Utility helpers for turning diverse video inputs into fal.ai-uploadable URLs."""

    _DEFAULT_FPS = 24.0
    _CONTENT_TYPE = "video/mp4"
    _DEFAULT_FILENAME = "upload.mp4"

    @staticmethod
    def _tensor_to_uint8_frames(video) -> np.ndarray:
        if video is None:
            raise ValueError("Video input is required for upload")

        if isinstance(video, torch.Tensor):
            data = video.detach().cpu()
            if data.ndim != 4:
                raise ValueError("Expected a 4D tensor for video frames")
            if data.shape[-1] == 3:
                frames = data.numpy()
            elif data.shape[1] == 3:
                frames = data.permute(0, 2, 3, 1).numpy()
            else:
                raise ValueError("Video tensor must have three color channels")
        else:
            array = np.asarray(video)
            if array.ndim != 4 or array.shape[-1] not in (1, 3):
                raise ValueError("Unsupported video array shape")
            frames = array
            if frames.shape[-1] == 1:
                frames = np.repeat(frames, 3, axis=-1)

        if frames.dtype.kind == "f":
            frames = np.clip(frames, 0.0, 1.0)
            frames = (frames * 255.0).round().astype(np.uint8)
        elif frames.dtype != np.uint8:
            frames = frames.astype(np.uint8)

        if frames.size == 0:
            raise ValueError("Video tensor did not contain any frames")

        return frames

    @staticmethod
    def _resolve_fps(video_info: Optional[Dict[str, Any]]) -> float:
        if isinstance(video_info, dict):
            candidates = [
                video_info.get("loaded_fps"),
                video_info.get("source_fps"),
            ]
            for candidate in candidates:
                if isinstance(candidate, (int, float)) and candidate > 0:
                    return float(candidate)
        return VideoUtils._DEFAULT_FPS

    @staticmethod
    def _frames_to_mp4_bytes(frames: np.ndarray, fps: float) -> bytes:
        height, width = frames.shape[1], frames.shape[2]
        temp_path: Optional[str] = None
        writer = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
                temp_path = temp_file.name

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            writer = cv2.VideoWriter(temp_path, fourcc, fps, (width, height))
            if not writer.isOpened():
                raise RuntimeError("Failed to initialize video writer")

            for frame in frames:
                if frame.shape[0] != height or frame.shape[1] != width:
                    raise ValueError("All video frames must share the same dimensions")
                bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                writer.write(bgr_frame)

            writer.release()
            writer = None

            with open(temp_path, "rb") as handle:
                data = handle.read()
            if not data:
                raise RuntimeError("Encoded video was empty")
            return data
        finally:
            if writer is not None:
                writer.release()
            if temp_path and os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except OSError:
                    pass

    @staticmethod
    def _upload_bytes(client: SyncClient, data: bytes, file_name: str) -> str:
        if not data:
            raise ValueError("Cannot upload empty video data")
        return client.upload(
            data,
            content_type=VideoUtils._CONTENT_TYPE,
            file_name=file_name,
        )

    @staticmethod
    def upload_video(video, video_info: Optional[Dict[str, Any]] = None) -> Optional[str]:
        try:
            if video is None:
                raise ValueError("Video input is required for upload")

            if isinstance(video, (list, tuple)) and len(video) == 1:
                video = video[0]

            client = FalConfig().get_client()

            if isinstance(video, (str, os.PathLike)):
                path = Path(video)
                if not path.is_file():
                    raise ValueError(f"Video file not found: {path}")
                upload_file = getattr(client, "upload_file", None)
                if callable(upload_file):
                    return upload_file(os.fspath(path))
                data = path.read_bytes()
                return VideoUtils._upload_bytes(client, data, path.name)

            if isinstance(video, (bytes, bytearray)):
                return VideoUtils._upload_bytes(client, bytes(video), VideoUtils._DEFAULT_FILENAME)

            if hasattr(video, "read"):
                try:
                    if hasattr(video, "seek"):
                        video.seek(0)
                except Exception:
                    pass
                data = video.read()
                file_name = os.path.basename(getattr(video, "name", VideoUtils._DEFAULT_FILENAME)) or VideoUtils._DEFAULT_FILENAME
                return VideoUtils._upload_bytes(client, data, file_name)

            frames = VideoUtils._tensor_to_uint8_frames(video)
            fps = VideoUtils._resolve_fps(video_info)
            data = VideoUtils._frames_to_mp4_bytes(frames, fps)
            return VideoUtils._upload_bytes(client, data, VideoUtils._DEFAULT_FILENAME)
        except Exception as exc:
            print(f"Error uploading video: {str(exc)}")
            return None


class ResultProcessor:
    """Utility functions for processing API results."""

    @staticmethod
    def _extract_image_urls(result: Any) -> List[str]:
        urls: List[str] = []

        if isinstance(result, dict):
            candidates: Sequence[Any] = result.get("images") or []
            if isinstance(candidates, dict):
                candidates = [candidates]
            if isinstance(candidates, list):
                for item in candidates:
                    if isinstance(item, dict) and "url" in item:
                        urls.append(item["url"])
                    elif isinstance(item, str):
                        urls.append(item)

            if not urls and "image" in result:
                item = result["image"]
                if isinstance(item, dict) and "url" in item:
                    urls.append(item["url"])
                elif isinstance(item, str):
                    urls.append(item)

            if not urls and "output" in result:
                output = result["output"]
                if isinstance(output, dict) and "url" in output:
                    urls.append(output["url"])
                elif isinstance(output, list):
                    for item in output:
                        if isinstance(item, dict) and "url" in item:
                            urls.append(item["url"])
                        elif isinstance(item, str):
                            urls.append(item)
                elif isinstance(output, str):
                    urls.append(output)

        # Deduplicate while preserving order
        seen = set()
        unique_urls: List[str] = []
        for url in urls:
            if isinstance(url, str) and url and url not in seen:
                unique_urls.append(url)
                seen.add(url)
        return unique_urls

    @staticmethod
    def _download_image(url: str) -> Image.Image:
        response = _HTTP_SESSION.get(url, timeout=_HTTP_TIMEOUT_SECONDS)
        response.raise_for_status()
        return Image.open(io.BytesIO(response.content))

    @staticmethod
    def _images_to_tensor(images: Iterable[Image.Image]) -> torch.Tensor:
        arrays: List[np.ndarray] = []
        for img in images:
            arrays.append(np.array(img).astype(np.float32) / 255.0)
        stacked_images = np.stack(arrays, axis=0)
        return torch.from_numpy(stacked_images)

    @staticmethod
    def process_image_result(result: Any):
        """Process image generation result and return tensor."""
        try:
            urls = ResultProcessor._extract_image_urls(result)
            if not urls:
                raise ValueError("FAL response did not include any image URLs")

            images = [ResultProcessor._download_image(url).convert("RGB") for url in urls]
            tensor = ResultProcessor._images_to_tensor(images)
            return (tensor,)
        except Exception as e:
            print(f"Error processing image result: {str(e)}")
            return ResultProcessor.create_blank_image()

    @staticmethod
    def process_single_image_result(result: Any):
        """Process single image result and return tensor."""
        return ResultProcessor.process_image_result(result)

    @staticmethod
    def create_blank_image():
        """Create a blank black image tensor."""
        blank_img = Image.new("RGB", (512, 512), color="black")
        img_array = np.array(blank_img).astype(np.float32) / 255.0
        img_tensor = torch.from_numpy(img_array)[None,]
        return (img_tensor,)


class FalAPIError(RuntimeError):
    """Wrap fal.ai API failures with context for the calling node."""

    def __init__(self, endpoint: str, message: str):
        super().__init__(f"{endpoint}: {message}")
        self.endpoint = endpoint
        self.message = message


class ApiHandler:
    """Utility functions for API interactions."""

    @staticmethod
    def _format_http_error(error: HTTPError) -> str:
        status_code = getattr(error.response, "status_code", "?")
        reason = getattr(error.response, "reason", "")
        try:
            payload = error.response.json()
            detail = payload.get("error") or payload
        except Exception:
            detail = getattr(error.response, "text", str(error))
        return f"HTTP {status_code} {reason}: {detail}"

    @staticmethod
    def _extract_result_error(result: Any) -> Optional[str]:
        if isinstance(result, dict):
            if result.get("error"):
                return str(result.get("error"))
            status = result.get("status")
            if status in {"FAILED", "ERROR"}:
                return str(result.get("message") or result)
        return None

    @staticmethod
    def submit_and_get_result(endpoint: str, arguments: Dict[str, Any]):
        """Submit job to FAL API and get result with robust error handling."""

        client = FalConfig().get_client()
        handler = client.submit(endpoint, arguments=arguments)

        start = time.monotonic()
        try:
            for status in handler.iter_events(interval=_JOB_POLL_INTERVAL_SECONDS):
                if isinstance(status, Completed):
                    break
                if time.monotonic() - start > _JOB_TIMEOUT_SECONDS:
                    handler.cancel()
                    raise FalAPIError(endpoint, "Request timed out while waiting for completion")

            result = handler.get()
        except HTTPError as http_error:
            raise FalAPIError(endpoint, ApiHandler._format_http_error(http_error)) from http_error
        except Exception as exc:
            raise FalAPIError(endpoint, str(exc)) from exc

        error_detail = ApiHandler._extract_result_error(result)
        if error_detail:
            raise FalAPIError(endpoint, error_detail)

        return result

    @staticmethod
    def run_image_job(model_name: str, endpoint: str, arguments: Dict[str, Any]):
        try:
            result = ApiHandler.submit_and_get_result(endpoint, arguments)
        except Exception as exc:  # Already wrapped by FalAPIError when appropriate
            return ApiHandler.handle_image_generation_error(model_name, exc)

        try:
            return ResultProcessor.process_image_result(result)
        except Exception as exc:
            return ApiHandler.handle_image_generation_error(model_name, exc)

    @staticmethod
    def run_single_image_job(model_name: str, endpoint: str, arguments: Dict[str, Any]):
        try:
            result = ApiHandler.submit_and_get_result(endpoint, arguments)
        except Exception as exc:
            return ApiHandler.handle_image_generation_error(model_name, exc)

        try:
            return ResultProcessor.process_single_image_result(result)
        except Exception as exc:
            return ApiHandler.handle_image_generation_error(model_name, exc)

    @staticmethod
    def _extract_video_url(result: Any) -> str:
        if isinstance(result, dict):
            video = result.get("video")
            if isinstance(video, dict) and "url" in video:
                return str(video["url"])
            if isinstance(video, list) and video:
                first = video[0]
                if isinstance(first, dict) and "url" in first:
                    return str(first["url"])
                if isinstance(first, str):
                    return first
            if "output" in result:
                output = result["output"]
                if isinstance(output, dict) and "url" in output:
                    return str(output["url"])
                if isinstance(output, list):
                    for item in output:
                        if isinstance(item, dict) and "url" in item:
                            return str(item["url"])
                        if isinstance(item, str):
                            return item
            if "url" in result and isinstance(result["url"], str):
                return str(result["url"])
        raise ValueError("FAL response did not include a video url")

    @staticmethod
    def run_video_job(model_name: str, endpoint: str, arguments: Dict[str, Any]):
        try:
            result = ApiHandler.submit_and_get_result(endpoint, arguments)
        except Exception as exc:
            return ApiHandler.handle_video_generation_error(model_name, exc)

        try:
            video_url = ApiHandler._extract_video_url(result)
            return (video_url,)
        except Exception as exc:
            return ApiHandler.handle_video_generation_error(model_name, exc)

    @staticmethod
    def run_text_job(model_name: str, endpoint: str, arguments: Dict[str, Any]):
        try:
            result = ApiHandler.submit_and_get_result(endpoint, arguments)
        except Exception as exc:
            return ApiHandler.handle_text_generation_error(model_name, exc)

        output = result.get("output") if isinstance(result, dict) else None
        if isinstance(output, str):
            return (output,)
        if isinstance(output, list):
            joined = "\n".join(str(item) for item in output)
            return (joined.strip(),)
        return ApiHandler.handle_text_generation_error(
            model_name, "FAL response did not include textual output"
        )

    @staticmethod
    def handle_video_generation_error(model_name, error):
        """Handle video generation errors consistently."""
        message = error.message if isinstance(error, FalAPIError) else str(error)
        print(f"Error generating video with {model_name}: {message}")
        return (f"Error: Unable to generate video. Details: {message}",)

    @staticmethod
    def handle_image_generation_error(model_name, error):
        """Handle image generation errors consistently."""
        message = error.message if isinstance(error, FalAPIError) else str(error)
        print(f"Error generating image with {model_name}: {message}")
        return ResultProcessor.create_blank_image()

    @staticmethod
    def handle_text_generation_error(model_name, error):
        """Handle text generation errors consistently."""
        message = error.message if isinstance(error, FalAPIError) else str(error)
        print(f"Error generating text with {model_name}: {message}")
        return (f"Error: Unable to generate text. Details: {message}",)
