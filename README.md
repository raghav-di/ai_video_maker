  # 🎬 OpenStoryAI
> **Transform Stories into Cinematic Videos with Generative AI.**
OpenStoryAI is an open-source framework that converts stories into fully generated cinematic videos using modern Generative AI models.
From a single story, OpenStoryAI automatically generates:
* 📝 Structured scene data
* 🎨 AI-generated images
* 🎙️ AI narration
* 💬 Automatic subtitles
* 🎵 Background ambience
* 🎥 Final rendered video

The goal of this project is to build a modular, community-driven framework where developers can contribute new AI models, rendering techniques, transitions, animation modules, and storytelling capabilities.

---

# ✨ Features

## Currently Supported
* ✅ Story parsing into structured JSON scenes
* ✅ Stable Diffusion XL image generation
* ✅ XTTS v2 multilingual narration
* ✅ Automatic subtitle generation from scene JSON
* ✅ FFmpeg-based video rendering
* ✅ Background ambience mixing
* ✅ Runtime AI model downloading
* ✅ Automatic temporary asset generation
* ✅ Automatic output video generation

---

# 🚧 Planned Features
* 🎞️ Advanced scene transitions
* 🎥 Ken Burns camera movement
* 🎭 Character consistency
* 🧠 Better prompt engineering
* 🎵 Sound effect generation
* 🌎 Multiple language support
* 🖼️ FLUX support
* 🎙️ Multiple TTS engine support
* 🖥️ Web UI
* 🔌 Plugin architecture
* ☁️ Cloud rendering support

---

# 🏗 Workflow
```
Story
   │
   ▼
Story Parser
   │
   ▼
Structured Scene JSON
   │
   ├──────────────┐
   │              │
   ▼              ▼
Image Gen      XTTS Narration
   │              │
   └──────┬───────┘
          │
          ▼
 Subtitle Generator
          │
          ▼
 Background Ambience
          │
          ▼
 FFmpeg Video Builder
          │
          ▼
 Final Cinematic Video
```

---

# 📂 Project Structure
```text
OpenStoryAI/
├── assets/
│   └── audio/
│       ├── ambience.wav
│       └── speaker.wav
├── module/
│   ├── image_gen.py
│   ├── models.py
│   ├── story_parser.py
│   ├── subtitle.py
│   ├── tts.py
│   └── video_builder.py
├── main.py
├── story.txt
├── pyproject.toml
├── uv.lock
├── LICENSE
└── README.md
```
📂 JSON Script Format
Each scene must include the following fields:
json
[{
"scene_id": "scene_01",
"image_prompt": "A futuristic city skyline at sunset",
"audio_script": "Welcome to the city of tomorrow.",
"subtitle_script": "Welcome to the city of tomorrow."
}]

During execution the framework automatically creates:
```text
assets/
    images/
    audio/
    metadata/

result/
    final_video.mp4
```

Temporary assets are generated automatically and can safely be deleted after rendering.

---

# 🧠 AI Models

| Component        | Model                        |
| ---------------- | ---------------------------- |
| Image Generation | Stable Diffusion XL Base 1.0 |
| Text-to-Speech   | XTTS v2                      |
| Rendering        | FFmpeg                       |

---

# ⚙️ Installation

## Clone the repository

```bash
git clone https://github.com/raghav-di/OpenStoryAI.git

cd OpenStoryAI
```

## Install dependencies

OpenStoryAI uses **Astral UV**.

```bash
uv sync
```
or if you are using colab
```bash
pip install -r requirements.txt
```

---

# 🚀 Quick Start
Create your story inside
```text
story.txt
```

Run the framework
```bash
uv run main.py
```
or if you are using it in colab
then run exact command to install packages
```bash
!pip install diffusers==0.36.0 transformers==4.57.6 accelerate==1.12.0 safetensors==0.7.0 coqui-tts==0.27.3 librosa==0.11.0 soundfile==0.13.1 ffmpeg-python==0.2.0 moviepy==1.0.3 faster-whisper==1.2.1 numpy==2.0.2 pillow==11.3.0 tqdm==4.67.1 google-generativeai==0.8.6 subtitle==2.3 torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0
```
then
```bash
python main.py
```

On the **first run**, OpenStoryAI automatically downloads the required AI models.
Depending on your internet connection this may take several minutes.

🎥 Example Output
👉 Recruiters: The project outputs AI‑generated explainer videos from structured scripts.
you can view a sample here:
[Video Example – (https://drive.google.com/drive/folders/10EEZnNk4q4_0JAFDHLpryTwPQQAZrLfk?usp=sharing)]

---

# 📜 Story Pipeline

```
Story.txt

↓

Story Parser

↓

Scenes.json

↓

Image Generation

↓

Voice Generation

↓

Subtitle Generation

↓

Background Audio

↓

Video Assembly

↓

Final Video
```

---

# 🎥 Output
After rendering you'll find
```
result/
└── final_video.mp4
```

---

# 🎯 Project Vision
OpenStoryAI is not intended to be just another AI video generator.
The long-term goal is to become a modular open-source framework for AI-powered cinematic storytelling where contributors can experiment with:
* new diffusion models
* new TTS engines
* scene effects
* animation
* transitions
* plugins
* storytelling pipelines

---

# 🤝 Contributing

Contributions of every size are welcome.
You can help by:
* Fixing bugs
* Improving documentation
* Adding transitions
* Supporting new AI models
* Improving prompt engineering
* Creating plugins
* Optimizing rendering
* Improving subtitle generation
* Suggesting new features

If you're new to open source, look for issues labeled:
```
good first issue
```
Please open an Issue before submitting large feature requests.

---

# 🗺 Roadmap

* [x] Story Parsing
* [x] SDXL Integration
* [x] XTTS Integration
* [x] Subtitle Generator
* [x] Background Ambience
* [x] Video Rendering
* [ ] Scene Transitions
* [ ] Camera Motion
* [ ] Character Consistency
* [ ] Multiple Image Models
* [ ] Multiple TTS Models
* [ ] Plugin System
* [ ] Web Interface
* [ ] Cloud Rendering

---

# ❤️ Support OpenStoryAI
If OpenStoryAI helps you build videos or saves you development time, consider supporting the project.

You can support by:
* ⭐ Starring the repository
* 🍴 Forking the project
* 🐛 Reporting bugs
* 💡 Suggesting new features
* 🤝 Contributing code
* ☕ Supporting development through donations

### Donation Options
* GitHub Sponsors *(when available)*
* Razorpay Payment Link *(coming soon)*
* UPI *(coming soon)*
Your support helps fund development, testing, documentation, and new features.

---

# 📜 License
This project is licensed under the **Apache License 2.0**.
See the LICENSE file for details.

---

# 🙏 Acknowledgements
OpenStoryAI is built using the amazing work of the open-source community.

Special thanks to the developers behind:
* Stable Diffusion XL
* XTTS
* FFmpeg
* Astral UV
* Python
Without these projects, OpenStoryAI would not be possible.

---

# ⭐ If you like this project...
Give the repository a **Star** and help OpenStoryAI grow into an open-source framework for AI-powered cinematic storytelling.
