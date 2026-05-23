🎬 AI Video Generation from JSON Script

📌 Overview
This project transforms structured JSON scripts into complete AI‑generated videos.
Each scene in the JSON defines:
  scene_id → unique identifier
  image_prompt → text prompt for AI image generation
  audio_script → narration or dialogue text
  subtitle_script → subtitle text for display
  
The pipeline automatically generates:
  Images (via diffusion models)
  Narration audio (via TTS)
  Subtitles (synced with audio)
  Final video composition with transitions
Recruiters and collaborators can quickly see how this project combines generative AI, multimedia rendering, and automation into a scalable workflow.

⚙️ Installation
bash
pip install diffusers==0.36.0 transformers==4.57.6 accelerate==1.12.0 safetensors==0.7.0 coqui-tts==0.27.3 librosa==0.11.0 soundfile==0.13.1 ffmpeg-python==0.2.0 moviepy==1.0.3 faster-whisper==1.2.1 numpy==2.0.2 pillow==11.3.0 tqdm==4.67.1 google-generativeai==0.8.6 subtitle==2.3
pip install torch==2.8.0+cu126 torchvision==0.23.0+cu126 torchaudio==2.8.0+cu126 \
--index-url https://download.pytorch.org/whl/cu126

📂 JSON Script Format
Each scene must include the following fields:
json
{
"scene_id": "scene_01",
"image_prompt": "A futuristic city skyline at sunset",
"audio_script": "Welcome to the city of tomorrow.",
"subtitle_script": "Welcome to the city of tomorrow."
}

🚀 Workflow
  Parse JSON → validate required fields
  Generate Images → diffusion models (Stable Diffusion XL)
  Generate Audio → TTS pipeline (Coqui TTS)
  Add Subtitles → synchronized with narration
  Compose Video → FFmpeg + MoviePy for transitions

🛠️ Tech Stack
  Diffusers → AI image generation
  Coqui TTS → speech synthesis
  FFmpeg / MoviePy → video rendering & transitions
  Faster‑Whisper → audio alignment
  Subtitle → subtitle embedding
  Torch (CUDA 12.6) → GPU acceleration

🎥 Example Output
👉 Recruiters: The project outputs AI‑generated explainer videos from structured scripts.
Since GitHub doesn’t allow direct video embedding, you can view a sample here:
[Video Example – [Drive Link Here](https://drive.google.com/drive/folders/10EEZnNk4q4_0JAFDHLpryTwPQQAZrLfk?usp=sharing)]

🌟 Why This Project Stands Out

  Automation‑driven: Converts text scripts into complete videos with minimal manual effort.
  Scalable design: Modular JSON scene graphs allow multi‑scene rendering.
  Recruiter appeal: Demonstrates applied knowledge in generative AI, backend orchestration, and multimedia engineering.
  Real‑world impact: Useful for education, storytelling, marketing, and content automation.
