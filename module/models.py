from TTS.api import TTS
from pathlib import Path


# ---------- AUDIO MODEL CONFIG ----------

MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
DEVICE = "cpu"

# Load TTS model
def load_model():
    return TTS(MODEL_NAME).to(DEVICE)

tts = load_model()