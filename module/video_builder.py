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
RESOLUTION = "1080x1920"   # change to 1920x1080 later if needed
TRANSITION_DURATION = 0.5  # seconds


# ---------- CORE FUNCTION ----------
def build_video(
    scene_durations: List[float],
    narration_audio: str,
    ambience_audio: str
):
    image_files = sorted(IMAGE_DIR.glob("scene_*.png"))
    assert len(image_files) == len(scene_durations), \
        "Mismatch between images and scene durations"

    inputs = []
    filter_parts = []

    for idx, (img, duration) in enumerate(zip(image_files, scene_durations)):
        inputs.extend([
            "-loop", "1",
            "-t", str(duration),
            "-i", str(img)
        ])
        filter_parts.append(
            f"[{idx}:v]scale={RESOLUTION},format=yuv420p,setsar=1[v{idx}]"
        )

    # Build xfade transitions
    filter_complex = ""
    for i in range(len(scene_durations) - 1):
        offset = sum(scene_durations[:i+1])
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

    # Audio filters: narration + ambience loop
    audio_filter = (
        f"[{len(image_files)}:a]volume=1.0[narr];"
        f"[{len(image_files)+1}:a]volume=0.2,aloop=loop=-1:size=2e+09[amb];"
        f"[narr][amb]amix=inputs=2:duration=shortest[aout]"
    )

    full_filter = ";".join(filter_parts) + ";" + filter_complex.rstrip(";") + ";" + audio_filter

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-i", narration_audio,
        "-i", ambience_audio,
        "-filter_complex", full_filter,
        "-map", final_video_label,
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
    ambience_audio = "ai_video_maker/assets/audio/ambience_forest.wav"

    build_video(durations, str(narration_audio), str(ambience_audio))
