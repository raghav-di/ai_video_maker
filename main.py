import json
from pathlib import Path
import shutil

from module.story_parser import parse_story_to_scenes
from module.tts import generate_scene_audios
from module.image_gen import generate_scene_images
from module.video_builder import build_video
from module.subtitle import generate_srt
# from module.models import load_models, del_models


# ---------- PATHS ----------
STORY_FILE = Path("ai_video_maker/story.txt")
SCENES_FILE = Path("assets/metadata/scenes.json")
# ---------- MAIN PIPELINE ----------
def main():

    print("🎬 Story2Video Pipeline Started")

    res = input("Enter the aspect ratio (option1- 16:9 or option2- 9:16): ")
    lang = input("Enter the language (option1- Hindi or option2- English): ")
    bg_music = input("Enter background music preference(from 0.0 to 1.0): ")

    # Load story
    if STORY_FILE.exists():
        story_text = STORY_FILE.read_text(encoding="utf-8")
    else:
        story_text = input("Enter Hindi story: ")

    # Story → Scenes
    print("🧠 Parsing story into scenes...")
    scenes = parse_story_to_scenes(story_text)

    # Generate TTS
    print("🎙️ Generating Hindi audio per scene...")
    full_audio_path, scene_durations = generate_scene_audios(scenes, lang, "ai_video_maker/assets/audio/speaker.wav")

    for scene, duration in zip(scenes, scene_durations):
        scene["duration"] = duration

    with open(SCENES_FILE, "w", encoding="utf-8") as f:
        json.dump(scenes, f, ensure_ascii=False, indent=2)

    # Generate images
    print("🎨 Generating images...")
    generate_scene_images(scenes)

    # Generate subtitles
    print("💬 Generating subtitles...")
    generate_srt()

    # Build final video
    print("🎥 Building final video...")
    build_video(scene_durations, res, full_audio_path, "ai_video_maker/assets/audio/ambience.wav", bg_music)

    print("✅ Pipeline completed successfully!")


# ---------- ENTRY ----------
if __name__ == "__main__":
    run = True
    while run:

        if Path("assets").exists():
            shutil.rmtree('assets')
        if input("Do you want to create a new video? (y/n): ").lower() == 'y':
            Path("assets").mkdir()
            Path("assets/metadata").mkdir()
            SCENES_FILE
            main()