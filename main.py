import json
import multiprocessing
from pathlib import Path
from multiprocessing import Process, Manager

from module.story_parser import parse_story_to_scenes
from module.tts import generate_scene_audios
from module.image_gen import generate_scene_images
from module.video_builder import build_video
from module.subtitle import generate_srt
from module.models import load_model


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

    # Generate images
    print("🎨 Generating images...")
    p1 = Process(target=generate_scene_images, args=(scenes,))
    p1.start()

    # Generate TTS (audio-first)
    print("🎙️ Generating Hindi audio per scene...")
    load_model()
    with Manager() as manager:
        return_dict = manager.dict()
        p2 = Process(target=generate_scene_audios,
                    args=(scenes, lang, "ai_video_maker/assets/audio/speaker.wav", return_dict))
        p2.start()
        p1.join()
        p2.join()
        full_audio_path, scene_durations = return_dict["result"]

        # Save durations into metadata (optional but useful)
        for scene, duration in zip(scenes, scene_durations):
            scene["duration"] = duration

        with open(SCENES_FILE, "w", encoding="utf-8") as f:
            json.dump(scenes, f, ensure_ascii=False, indent=2)

    # Generate subtitles
    print("💬 Generating subtitles...")
    generate_srt()

    # Build final video
    print("🎥 Building final video...")
    build_video(scene_durations, res, full_audio_path, "ai_video_maker/assets/audio/ambience.wav", bg_music)

    print("✅ Pipeline completed successfully!")


# ---------- ENTRY ----------
if __name__ == "__main__":
    multiprocessing.set_start_method("spawn", force=True)
    main()