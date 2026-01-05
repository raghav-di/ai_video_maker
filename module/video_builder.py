import subprocess
from pathlib import Path
from typing import List


# ---------- PATHS ----------
IMAGE_DIR = Path("assets/images")
AUDIO_DIR = Path("assets/audio")
RESULT_DIR = Path("result")
RESULT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_VIDEO = RESULT_DIR / "final_video.mp4"

NARRATION_AUDIO = AUDIO_DIR / "full_story.wav"
AMBIENCE_AUDIO = "ai_video_maker/assets/audio/ambience_forest.wav"


# ---------- VIDEO SETTINGS ----------
FPS = 30
RESOLUTION = "1080x1920"        # YouTube Shorts (9:16)
TRANSITION_DURATION = 0.5


# ---------- CORE ----------
def build_video(scene_durations: List[float]):

    image_files = sorted(IMAGE_DIR.glob("scene_*.png"))
    assert len(image_files) == len(scene_durations), \
        "Number of images and scene durations must match"

    inputs = []
    filters = []

    # ---------- IMAGE INPUTS ----------
    for i, (img, dur) in enumerate(zip(image_files, scene_durations)):
        inputs += [
            "-loop", "1",
            "-t", str(dur),
            "-i", str(img)
        ]

        filters.append(
            f"[{i}:v]scale={RESOLUTION},format=yuv420p,setsar=1[v{i}]"
        )

    # ---------- XFADE CHAIN (FIXED – LAST SCENE INCLUDED) ----------
    xfade_out = None

    for i in range(len(scene_durations) - 1):
        offset = sum(scene_durations[:i + 1])

        if i == 0:
            filters.append(
                f"[v0][v1]xfade=transition=fade:"
                f"duration={TRANSITION_DURATION}:offset={offset}[vx1]"
            )
            xfade_out = "vx1"
        else:
            filters.append(
                f"[{xfade_out}][v{i+1}]xfade=transition=fade:"
                f"duration={TRANSITION_DURATION}:offset={offset}[vx{i+1}]"
            )
            xfade_out = f"vx{i+1}"

    final_video_stream = f"[{xfade_out}]" if xfade_out else "[v0]"

    # ---------- AUDIO MIX (Narration + Looping Ambience) ----------
    audio_filter = (
        "[5:a]volume=1.0[narr];"
        "[6:a]volume=0.2,aloop=loop=-1:size=2e+09[amb];"
        "[narr][amb]amix=inputs=2:duration=first[aout]"
    )

    filter_complex = (
        ";".join(filters)
        + f";{final_video_stream}[v]"
        + f";{audio_filter}"
    )

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-i", str(NARRATION_AUDIO),
        "-i", str(AMBIENCE_AUDIO),
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "[aout]",
        "-r", str(FPS),
        "-pix_fmt", "yuv420p",
        str(OUTPUT_VIDEO)
    ]

    print("🎬 Building final video (no subtitles, with ambience)...")
    subprocess.run(cmd, check=True)
    print(f"✅ Video saved to {OUTPUT_VIDEO}")


# ---------- CLI TEST ----------
if __name__ == "__main__":
    import json

    with open("assets/metadata/scenes.json", "r", encoding="utf-8") as f:
        scenes = json.load(f)

    durations = [scene["duration"] for scene in scenes]
    build_video(durations)
