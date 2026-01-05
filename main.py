import json
from pathlib import Path

from module.story_parser import parse_story_to_scenes
from module.tts import generate_scene_audios
from module.image_gen import generate_scene_images
from module.video_builder import build_video


# ---------- PATHS ----------
STORY_FILE = Path("story.txt")
SCENES_FILE = Path("assets/metadata/scenes.json")


# ---------- MAIN PIPELINE ----------
def main():
    print("🎬 Story2Video Pipeline Started")

    # 1️⃣ Load story
    if STORY_FILE.exists():
        story_text = STORY_FILE.read_text(encoding="utf-8")
    else:
        story_text = input("Enter Hindi story:\n")

    # 2️⃣ Story → Scenes
    print("🧠 Parsing story into scenes...")
    scenes = parse_story_to_scenes(story_text)

    # 3️⃣ Generate TTS (audio-first)
    print("🎙️ Generating Hindi audio per scene...")
    full_audio_path, scene_durations = generate_scene_audios(scenes)

    # Save durations into metadata (optional but useful)
    for scene, duration in zip(scenes, scene_durations):
        scene["duration"] = duration

    with open(SCENES_FILE, "w", encoding="utf-8") as f:
        json.dump(scenes, f, ensure_ascii=False, indent=2)

    # 4️⃣ Generate images
    print("🎨 Generating images...")
    generate_scene_images(scenes)

    # 5️⃣ Build final video
    print("🎥 Building final video...")
    build_video(scene_durations)

    print("✅ Pipeline completed successfully!")


# ---------- ENTRY ----------
if __name__ == "__main__":
    main()
