import subprocess
from pathlib import Path
from typing import List
# import random


# ---------- CONFIG ----------
IMAGE_DIR = Path("assets/images")
AUDIO_DIR = Path("assets/audio")
RESULT_DIR = Path("result")
RESULT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_VIDEO = RESULT_DIR / "final_video.mp4"
SUBS_PATH = "assets/metadata/subs.srt"

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
    scene_filters = []
    # Define some sensible focus points for variation
    focus_points = [
        ("iw/4", "ih/4"),       # top-left
        ("iw/2", "ih/2"),       # center
        ("3*iw/4", "ih/2"),     # right-center
        ("iw/2", "3*ih/4"),     # bottom-center
    ]

    # for idx, (img, duration) in enumerate(zip(image_files, scene_durations)):
    #     inputs.extend([
    #         "-loop", "1",
    #         "-t", str(duration),
    #         "-i", str(img)
    #     ])
    #     frames = int(duration * FPS)
    #     x_expr, y_expr = random.choice(focus_points)

    #     scene_filters.append(
    #         f"[{idx}:v]zoompan=z='zoom+0.001':x='{x_expr}':y='{y_expr}':d={frames}:s={RESOLUTION}:fps={FPS},format=yuv420p,setsar=1[v{idx}]"
    #     )
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
        f"[{len(image_files)+1}:0]volume=0.2,aloop=loop=-1:size=2e+09[amb];"
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

    build_video(durations, str(narration_audio), str(ambience_audio))
