from TTS.api import TTS
from pathlib import Path
import torch
from diffusers import StableDiffusionXLPipeline


# ---------- AUDIO MODEL CONFIG ----------
MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
DEVICE = "cpu"

# ---------- IMAGE MODEL CONFIG ----------
MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

DEFAULT_NEGATIVE_PROMPT = (
    "low quality, blurry, distorted, bad anatomy, "
    "extra limbs, extra fingers, watermark, text"
)


def load_models():
    # Load TTS model
    global tts
    tts = TTS(MODEL_NAME).to(DEVICE)

    # Load SDXL
    global pipe
    pipe = StableDiffusionXLPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16,
        use_safetensors=True
    ).to(DEVICE)

    pipe.enable_attention_slicing()
    pipe.enable_vae_slicing()

def del_models():
    global tts
    global pipe
    del tts
    del pipe
    torch.cuda.empty_cache()