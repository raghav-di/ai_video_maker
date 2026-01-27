import soundfile as sf
import librosa
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np

from models import tts


# ---------- PATHS ----------
AUDIO_DIR = Path("assets/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# ---------- CORE FUNCTION ----------
def generate_scene_audios(
    scenes: List[Dict],
    language: str,
    speaker_wav: str,
    queue = None
) -> Tuple[str, List[float]]:
    """
    Generates per-scene audio, measures durations,
    concatenates into a full story audio.

    Returns:
        full_audio_path (str)
        scene_durations (List[float])
    """

    scene_audio_paths = []
    scene_durations = []

    for scene in scenes:
        scene_id = scene["scene_id"]
        text = scene["audio_script"]

        out_path = AUDIO_DIR / f"scene_{scene_id:02d}.wav"

        tts.tts_to_file(
            text=text,
            file_path=str(out_path),
            speaker_wav=speaker_wav,
            language=language
        )

        # Measure duration
        duration = librosa.get_duration(path=str(out_path))
        scene_durations.append(round(duration, 2))
        scene_audio_paths.append(out_path)

    # Concatenate all scene audios
    full_audio_path = AUDIO_DIR / "full_story.wav"
    _concatenate_audios(scene_audio_paths, full_audio_path)

    # Free memory
    del tts

    if queue is not None:
        queue.put((full_audio_path, scene_durations))

    return str(full_audio_path), scene_durations


# ---------- HELPER ----------
def _concatenate_audios(audio_paths: List[Path], output_path: Path):
    audios = []
    sample_rate = None

    for path in audio_paths:
        audio, sr = sf.read(path)
        if sample_rate is None:
            sample_rate = sr
        audios.append(audio)

    final_audio = np.concatenate(audios, axis=0)
    sf.write(output_path, final_audio, sample_rate)


# ---------- CLI TEST ----------
if __name__ == "__main__":
    import json

    with open("assets/metadata/scenes.json", "r", encoding="utf-8") as f:
        scenes = json.load(f)

    language = input("Enter the language (option1- Hindi or option2- English): ")

    full_audio, durations = generate_scene_audios(scenes, language, "ai_video_maker/assets/audio/speaker.wav")

    print("Full audio:", full_audio)
    print("Scene durations:", durations)
