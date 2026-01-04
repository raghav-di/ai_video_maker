from module.video_builder import AMBIENCE_AUDIO
import torch
import soundfile as sf
import librosa
from pathlib import Path
from typing import List, Dict, Tuple
from TTS.api import TTS

# ---------- CONFIG ----------
AUDIO_DIR = Path("assets/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# ---------- CORE FUNCTION ----------
def generate_scene_audios(
    scenes: List[Dict],
    speaker_wav: str = None,
    language: str = "hi"
) -> Tuple[str, List[float]]:
    """
    Generates per-scene audio, measures durations,
    concatenates into a full story audio.

    Returns:
        full_audio_path (str)
        scene_durations (List[float])
    """

    # Load TTS model
    tts = TTS(MODEL_NAME).to(DEVICE)

    scene_audio_paths = []
    scene_durations = []

    for scene in scenes:
        scene_id = scene["scene_id"]
        text = scene["audio_script_hi"]

        out_path = AUDIO_DIR / f"scene_{scene_id:02d}.wav"

        tts.tts_to_file(
            text=text,
            file_path=str(out_path),
            speaker_wav="ai_video_maker/assets/audio/speaker.wav",
            language='hi'
        )

        # Measure duration
        duration = librosa.get_duration(path=str(out_path))
        scene_durations.append(round(duration, 2))
        scene_audio_paths.append(out_path)

    # Concatenate all scene audios
    full_audio_path = AUDIO_DIR / "full_story.wav"
    _concatenate_audios(scene_audio_paths, full_audio_path)

    # Free GPU memory
    del tts
    torch.cuda.empty_cache()

    return str(full_audio_path), scene_durations


# ---------- HELPER ----------
def _concatenate_audios(audio_paths: List[Path], output_path: Path):
    combined_audio = []
    sample_rate = None

    for path in audio_paths:
        audio, sr = sf.read(path)
        if sample_rate is None:
            sample_rate = sr
        combined_audio.append(audio)

    final_audio = sum(combined_audio[1:], combined_audio[0])
    sf.write(output_path, final_audio, sample_rate)


# ---------- CLI TEST ----------
if __name__ == "__main__":
    import json

    with open("assets/metadata/scenes.json", "r", encoding="utf-8") as f:
        scenes = json.load(f)

    full_audio, durations = generate_scene_audios(scenes)

    print("Full audio:", full_audio)
    print("Scene durations:", durations)
