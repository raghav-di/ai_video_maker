import subprocess
from pathlib import Path
from typing import List

# ---------- CONFIG ----------
IMAGE_DIR = Path("assets/images")
AUDIO_DIR = Path("assets/audio")
RESULT_DIR = Path("result")
RESULT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_VIDEO = RESULT_DIR / "final_video.mp4"
SUBS_PATH = "assets/metadata/subs.srt"

FPS = 12
TRANSITION_DURATION = 0.5


# ---------- CORE FUNCTION ----------
def build_video(
    scene_durations: List[float],
    resolution: str,
    narration_audio: str,
    ambience_audio: str,
    bg_music: str
):

    RESOLUTION = "1080x1920" if resolution == "1" else "1920x1080"
    image_files = sorted(IMAGE_DIR.glob("scene_*.png"))
    assert len(image_files) == len(scene_durations), \
        "Mismatch between images and scene durations"

    inputs = []
    scene_filters = []

    for idx, (img, duration) in enumerate(zip(image_files, scene_durations)):
        inputs.extend([
            "-loop", "1",
            "-t", str(duration),
            "-i", str(img)
        ])
        scene_filters.append(
            f"[{idx}:v]scale={RESOLUTION},format=yuv420p,setsar=1[v{idx}]"
        )

    # Concatenate all scenes sequentially
    concat_inputs = "".join([f"[v{i}]" for i in range(len(scene_durations))])
    scene_concat = f"{concat_inputs}concat=n={len(scene_durations)}:v=1:a=0[vcat]"

    # Audio filters: narration + ambience loop
    audio_filter = (
        f"[{len(image_files)}:0]volume=1.0[narr];"
        f"[{len(image_files)+1}:0]volume={bg_music},aloop=loop=-1:size=2e+09[amb];"
        f"[narr][amb]amix=inputs=2:duration=shortest[aout]"
    )

    # Subtitles filter: attach to final video label
    subtitle_filter = (
        f"[vcat]subtitles={SUBS_PATH}:"
        "force_style='FontName=Arial,FontSize=16,PrimaryColour=&HFFFFFF&,"
        "OutlineColour=&H000000&,BorderStyle=1,Outline=3,Alignment=10'[vout]"
    )

    full_filter = ";".join(scene_filters) + ";" + scene_concat + ";" + audio_filter + ";" + subtitle_filter

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-i", narration_audio,
        "-i", ambience_audio,
        "-filter_complex", full_filter,
        "-map", "[vout]",
        "-map", "[aout]",
        "-r", str(FPS),
        "-pix_fmt", "yuv420p",
        "-shortest",
        str(OUTPUT_VIDEO)
    ]

    print("🎬 Building final video...")
    subprocess.run(cmd, check=True)
    print(f"✅ Video saved to {OUTPUT_VIDEO}")


# ---------- CLI TEST ----------
if __name__ == "__main__":
    import json
    with open("assets/metadata/scenes.json", "r", encoding="utf-8") as f:
        scenes = json.load(f)

    durations = [scene.get("duration", 5) for scene in scenes]

    narration_audio = AUDIO_DIR / "full_story.wav"
    ambience_audio = "ai_video_maker/assets/audio/ambience.wav"
    res = input("Enter the aspect ratio (option1- 16:9 or option2- 9:16): ")
    bg_music = input("Enter background music preference(from 0.0 to 1.0): ")

    build_video(durations, res, str(narration_audio), str(ambience_audio), bg_music)
