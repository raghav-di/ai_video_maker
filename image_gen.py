import torch
from diffusers import StableDiffusionXLPipeline
from pathlib import Path
from typing import List, Dict
from PIL import Image

# ---------- CONFIG ----------
IMAGE_DIR = Path("assets/images")
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

DEFAULT_NEGATIVE_PROMPT = (
    "low quality, blurry, distorted, bad anatomy, "
    "extra limbs, extra fingers, watermark, text"
)

# ---------- CORE FUNCTION ----------
def generate_scene_images(
    scenes: List[Dict],
    width: int = 1024,
    height: int = 1024,
    steps: int = 30,
    guidance_scale: float = 7.5
):
    """
    Generates one image per scene using SDXL.
    Images are saved to assets/images/.
    """

    # Load SDXL
    pipe = StableDiffusionXLPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16,
        use_safetensors=True
    ).to(DEVICE)

    pipe.enable_attention_slicing()
    pipe.enable_vae_slicing()

    for scene in scenes:
        scene_id = scene["scene_id"]
        prompt = scene["image_prompt_en"]

        out_path = IMAGE_DIR / f"scene_{scene_id:02d}.png"

        print(f"🎨 Generating image for scene {scene_id}")

        image = pipe(
            prompt=prompt,
            negative_prompt=DEFAULT_NEGATIVE_PROMPT,
            width=width,
            height=height,
            num_inference_steps=steps,
            guidance_scale=guidance_scale
        ).images[0]

        image.save(out_path)

    # Free GPU memory
    del pipe
    torch.cuda.empty_cache()


# ---------- CLI TEST ----------
if __name__ == "__main__":
    import json

    with open("assets/metadata/scenes.json", "r", encoding="utf-8") as f:
        scenes = json.load(f)

    generate_scene_images(scenes)
    print("✅ All images generated successfully")
