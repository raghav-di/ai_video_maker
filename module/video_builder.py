import subprocess
from pathlib import Path
from typing import List


# ---------- CONFIG ----------
IMAGE_DIR = Path("assets/images")
AUDIO_DIR = Path("assets/audio")
RESULT_DIR = Path("result")
RESULT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_VIDEO = RESULT_DIR / "final_video.mp4"

FPS = 30
RESOLUTION = "1280x720"   # change to 1920x1080 later if needed
TRANSITION_DURATION = 0.5  # seconds


# ---------- CORE FUNCTION ----------
def build_video(
    scene_durations: List[float],
    audio_path: str
):
    """
    Builds final video using images, scene durations, and narration audio.
    """

    image_files = sorted(IMAGE_DIR.glob("scene_*.png"))

    assert len(image_files) == len(scene_durations), \
        "Mismatch between images and scene durations"

    # Create FFmpeg input arguments
    inputs = []
    filter_parts = []
    current_time = 0.0

    for idx, (img, duration) in enumerate(zip(image_files, scene_durations)):
        inputs.extend([
            "-loop", "1",
            "-t", str(duration),
            "-i", str(img)
        ])

        # Scale & format
        filter_parts.append(
            f"[{idx}:v]scale={RESOLUTION},format=yuv420p,setsar=1[v{idx}]"
        )

    # Build xfade transitions
    filter_complex = ""
    for i in range(len(scene_durations) - 1):
        offset = sum(scene_durations[:i+1]) - TRANSITION_DURATION

        if i == 0:
            filter_complex += (
                f"[v0][v1]xfade=transition=fade:"
                f"duration={TRANSITION_DURATION}:offset={offset}[v01];"
            )
        else:
            filter_complex += (
                f"[v{i:02d}][v{i+1}]xfade=transition=fade:"
                f"duration={TRANSITION_DURATION}:offset={offset}[v{i+1:02d}];"
            )

    final_video_label = (
        f"[v{len(scene_durations)-1:02d}]"
        if len(scene_durations) > 1 else "[v0]"
    )

    full_filter = ";".join(filter_parts) + ";" + filter_complex.rstrip(";")

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-i", audio_path,
        "-filter_complex", full_filter,
        "-map", final_video_label,
        "-map", f"{len(image_files)}:a",
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

    durations = []
    for scene in scenes:
        durations.append(scene.get("duration", 5))

    audio_path = AUDIO_DIR / "full_story.wav"

    build_video(durations, str(audio_path))
