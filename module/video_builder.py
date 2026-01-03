import subprocess
from pathlib import Path
from typing import List, Dict


# ---------- PATHS ----------
IMAGE_DIR = Path("assets/images")
AUDIO_DIR = Path("assets/audio")
RESULT_DIR = Path("result")
RESULT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_VIDEO = RESULT_DIR / "final_video.mp4"

NARRATION_AUDIO = AUDIO_DIR / "full_story.wav"
AMBIENCE_AUDIO = AUDIO_DIR / "ambience_forest.wav"

# ---------- VIDEO SETTINGS ----------
FPS = 30
RESOLUTION = "1080x1920"        # YouTube Shorts (9:16)
TRANSITION_DURATION = 0.5

# ---------- TEXT SETTINGS ----------
FONT_SIZE = 56
TEXT_Y_POS = "h*0.7"            # lower-center (non-blocking)
TEXT_BOX = "box=1:boxcolor=black@0.4:boxborderw=18"


# ---------- CORE ----------
def build_video(
    scenes: List[Dict],
    scene_durations: List[float]
):
    image_files = sorted(IMAGE_DIR.glob("scene_*.png"))
    assert len(image_files) == len(scene_durations)

    inputs = []
    filters = []

    # ---------- IMAGE INPUTS ----------
    for i, (img, dur) in enumerate(zip(image_files, scene_durations)):
        inputs += ["-loop", "1", "-t", str(dur), "-i", str(img)]
        filters.append(
            f"[{i}:v]scale={RESOLUTION},format=yuv420p,setsar=1[v{i}]"
        )

    # ---------- XFADE CHAIN ----------
    xfade_out = None
    for i in range(len(scene_durations) - 1):
        offset = sum(scene_durations[:i+1])
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

    video_stream = f"[{xfade_out}]" if xfade_out else "[v0]"

    # ---------- RULE TEXT (only on rules scene) ----------
    # Assumes rules are in scene 4
    rules = [
        "नियम 1: सूर्यास्त के बाद बाहर न निकलें",
        "नियम 2: जंगल की आवाज़ों का जवाब न दें",
        "नियम 3: दरवाज़े और खिड़कियाँ बंद रखें",
        "नियम 4: अकेले जंगल में न जाएँ"
    ]

    rule_start = sum(scene_durations[:3])
    rule_time = scene_durations[3] / len(rules)

    text_filters = []
    for i, rule in enumerate(rules):
        start = rule_start + i * rule_time
        end = start + rule_time
        text_filters.append(
            f"drawtext=text='{rule}':"
            f"fontsize={FONT_SIZE}:fontcolor=white:"
            f"x=(w-text_w)/2:y={TEXT_Y_POS}:{TEXT_BOX}:"
            f"enable='between(t,{start},{end})'"
        )

    video_filter = video_stream + "".join([f",{t}" for t in text_filters])

    # ---------- AUDIO MIX ----------
    audio_filter = (
        "[a0]volume=1.0[aud];"
        "[a1]volume=0.25,aloop=loop=-1:size=2e+09[amb];"
        "[aud][amb]amix=inputs=2:duration=first[aout]"
    )

    filter_complex = ";".join(filters) + ";" + video_filter + ";" + audio_filter

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

    print("🎬 Building YouTube Shorts video...")
    subprocess.run(cmd, check=True)
    print(f"✅ Saved: {OUTPUT_VIDEO}")


# ---------- CLI TEST ----------
if __name__ == "__main__":
    import json

    with open("assets/metadata/scenes.json", "r", encoding="utf-8") as f:
        scenes = json.load(f)

    durations = [s["duration"] for s in scenes]
    build_video(scenes, durations)
