from pathlib import Path
import json


# ---------- CONFIG ----------
SCENES_JSON = Path("assets/metadata/scenes.json")
OUTPUT_SRT = Path("assets/metadata/subs.srt")

MAX_CHARS_PER_LINE = 16
MAX_LINES = 1
MIN_DURATION = 1.0  # seconds


# ---------- HELPERS ----------
def split_text_to_lines(text, max_chars=40):
    words = text.split()
    lines = []
    current = ""

    for w in words:
        if len(current) + len(w) + 1 <= max_chars:
            current += (" " if current else "") + w
        else:
            lines.append(current)
            current = w

    if current:
        lines.append(current)

    return lines


def chunk_lines(lines, max_lines=3):
    return [
        lines[i:i + max_lines]
        for i in range(0, len(lines), max_lines)
    ]


def sec_to_srt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:06.3f}".replace(".", ",")


# ---------- CORE ----------
def generate_srt():
    with open(SCENES_JSON, "r", encoding="utf-8") as f:
        scenes = json.load(f)

    srt_lines = []
    index = 1
    current_time = 0.0

    for scene in scenes:
        text = scene["subtitle_script_hi"]
        duration = scene["duration"]

        lines = split_text_to_lines(text, MAX_CHARS_PER_LINE)
        chunks = chunk_lines(lines, MAX_LINES)

        chunk_duration = max(duration / len(chunks), MIN_DURATION)

        for chunk in chunks:
            start = current_time
            end = start + chunk_duration

            srt_lines.append(str(index))
            srt_lines.append(
                f"{sec_to_srt_time(start)} --> {sec_to_srt_time(end)}"
            )
            srt_lines.extend(chunk)
            srt_lines.append("")

            index += 1
            current_time = end

    OUTPUT_SRT.write_text("\n".join(srt_lines), encoding="utf-8")
    print(f"✅ Subtitles written to {OUTPUT_SRT}")


# ---------- RUN ----------
if __name__ == "__main__":
    generate_srt()
