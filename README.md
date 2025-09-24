# ComfyUI-fal-API

Custom nodes for using Flux models with  fal API in ComfyUI with only one API Key for all.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Available Nodes](#available-nodes)
  - [Image Generation](#image-generation)
  - [Video Generation](#video-generation)
  - [Language Models (LLMs)](#language-models-llms)
  - [Vision Language Models (VLMs)](#vision-language-models-vlms)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Installation

1. Navigate to your ComfyUI custom nodes directory:
   ```
   cd custom_nodes
   ```

2. Clone this repository:
   ```
   git clone https://github.com/gokayfem/ComfyUI-fal-API.git
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Get your fal API key from [fal.ai](https://fal.ai/dashboard/keys)

2. Open the `config.ini` file inside `custom_nodes/ComfyUI-fal-API`

3. Replace `<your_fal_api_key_here>` with your actual fal API key:
   ```ini
   [API]
   FAL_KEY = your_actual_api_key
   ```

4. Alternatively, you can set the FAL_KEY environment variable:
   ```bash
   export FAL_KEY=your_actual_api_key
   ```

## Usage

After installation and configuration, restart ComfyUI. The new nodes will be available in the node browser under the "FAL" category.

## Available Nodes

### Image Generation

- **Flux Pro (fal)**: Generate high-quality images using the Flux Pro model
- **Flux Dev (fal)**: Use the development version of Flux for image generation
- **Flux Schnell (fal)**: Fast image generation with Flux Schnell
- **Flux Pro 1.1 (fal)**: Latest version of Flux Pro for image generation
- **Flux Ultra (fal)**: Ultra-high quality image generation with advanced controls
- **Flux General (fal)**: ControlNets, Ipadapters, Loras for Flux Dev
- **Flux LoRA (fal)**: Flux with dual LoRA support for custom styles
- **Flux Pro Kontext (fal)**: Context-aware single image-to-image generation with max_quality toggle
- **Flux Pro Kontext Multi (fal)**: Multi-image composition (2-4 images) with context awareness and max_quality toggle
- **Flux Pro Kontext Text-to-Image (fal)**: Text-to-image with aspect ratio controls and max_quality toggle
- **Recraft V3 (fal)**: Professional design generation with multiple style options
- **Sana (fal)**: High-quality image synthesis with ultra-high resolution support
- **HiDream Full (fal)**: Advanced image generation with comprehensive parameter control
- **Ideogram v3 (fal)**: Advanced text-to-image generation with typography support
- **Nano Banana (fal)**: Google diffusion model for prompt-only image generation
- **Nano Banana Edit (fal)**: Multi-image guided editing variant of Nano Banana
- **Seedream4 Text-to-Image (fal)**: Seedream v4 prompt-to-image generation with guidance controls
- **Seedream4 Edit (fal)**: Seedream v4 image editing with adjustable strength

### Video Generation

- **Kling Video Generation (fal)**: Generate videos using the Kling model
- **Kling Pro v1.0 Video Generation (fal)**: Original version of Kling Pro for video generation
- **Kling Pro v1.6 Video Generation (fal)**: Latest version of Kling Pro with improved quality
- **Kling Master v2.0 Video Generation (fal)**: Advanced video generation with Kling Master
- **Runway Gen3 Image-to-Video (fal)**: Convert images to videos using Runway Gen3
- **Luma Dream Machine (fal)**: Create videos with Luma Dream Machine
- **MiniMax Video Generation (fal)**: Generate videos using MiniMax model
- **MiniMax Text-to-Video (fal)**: Create videos from text prompts using MiniMax
- **MiniMax Subject Reference (fal)**: Generate videos with subject reference using MiniMax
- **Google Veo2 Image-to-Video (fal)**: Convert images to videos using Google's Veo2 model
- **Wan Pro Image-to-Video (fal)**: High-quality video generation with Wan Pro model
- **Video Upscaler (fal)**: Upscale video quality using AI
- **Combined Video Generation (fal)**: Generate videos using multiple services simultaneously
  - Supports Kling Pro v1.6, Kling Master v2.0, MiniMax, Luma, Veo2, and Wan Pro
  - Each service can be individually enabled/disabled
  - Wan Pro runs with safety checker enabled and automatic seed selection
- **Google Veo3 (fal)**: Next-generation video synthesis with optional audio track
- **Google Veo3 Fast (fal)**: Low-latency Veo3 generation with auto-fix and audio controls
- **Google Veo3 Image-to-Video (fal)**: Animate reference frames with Veo3
- **Google Veo3 Fast Image-to-Video (fal)**: Rapid Veo3 animation variant tuned for speed
- **Kling Master v2.1 Video Generation (fal)**: Enhanced Master tier with CFG and negative prompt support
- **Kling Turbo v2.5 Pro Video Generation (fal)**: Latest Kling fast Pro pipeline with tail image support
- **Load Video from URL**: Load and process videos from a given URL

### Example Workflows

- `example_workflows/Flux-Kontext-Workflow.json`: Flux Pro Kontext image-to-image setup
- `example_workflows/Video-Workflow-Veo2.json`: Google Veo2 image-to-video pipeline

### Language Models (LLMs)

- **LLM (fal)**: Large Language Model for text generation and processing
  - Supports explicit `reasoning`, `priority`, `temperature`, and `max_tokens` controls
  - Available models (excerpt):
    - google/gemini-2.5-flash, google/gemini-2.5-pro, google/gemini-2.0-flash-001
    - anthropic/claude-3.5-sonnet, anthropic/claude-3-5-haiku, anthropic/claude-3.7-sonnet
    - deepseek/deepseek-r1, meta-llama/llama-4-maverick, meta-llama/llama-3.2-90b-vision-instruct
    - openai/gpt-5-chat, openai/gpt-4.1, openai/gpt-4o, openai/o3, openai/gpt-oss-120b

### Vision Language Models (VLMs)

- **VLM (fal)**: Vision Language Model for image understanding and text generation
  - Supports `reasoning`, `priority`, `temperature`, and `max_tokens`, plus image upload
  - Available models (excerpt):
    - google/gemini-2.5-flash / flash-lite / pro, google/gemini-2.0-flash-001
    - anthropic/claude-3.7-sonnet, anthropic/claude-3.5-sonnet, anthropic/claude-3-5-haiku
    - meta-llama/llama-3.2-90b-vision-instruct, meta-llama/llama-4-maverick, meta-llama/llama-4-scout
    - openai/gpt-4o, openai/gpt-4o-mini, openai/gpt-4.1, openai/gpt-5-chat, openai/o3
  - Ideal for captioning, VQA, reasoning over visual context, and multimodal prompt chaining

## Troubleshooting

If you encounter any errors during installation or usage, try the following:

1. Ensure you have the latest version of ComfyUI installed
2. Update this custom node package:
   ```
   cd custom_nodes/ComfyUI-fal-API
   git pull
   pip install -r requirements.txt
   ```
3. If you're using ComfyUI Windows Portable, you may need to install fal-client manually:
   ```
   ComfyUI_windows_portable>.\python_embeded\python.exe -m pip install fal-client
   ```

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please open an issue on the [GitHub repository](https://github.com/gokayfem/ComfyUI-fal-API/issues).
