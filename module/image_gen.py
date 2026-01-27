from pathlib import Path
from typing import List, Dict

from module.models import pipe, DEFAULT_NEGATIVE_PROMPT

# ---------- CONFIG ----------
IMAGE_DIR = Path("assets/images")
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

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

    for scene in scenes:
        scene_id = scene["scene_id"]
        prompt = scene["image_prompt"]

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


# ---------- CLI TEST ----------
if __name__ == "__main__":
    import json

    with open("assets/metadata/scenes.json", "r", encoding="utf-8") as f:
        scenes = json.load(f)

    generate_scene_images(scenes)
    print("✅ All images generated successfully")
