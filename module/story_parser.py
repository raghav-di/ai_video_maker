import json
from pathlib import Path
from typing import List, Dict
# import google.generativeai as genai
# from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
# import torch, json

# MODEL_NAME = "meta-llama/Llama-3-8b-instruct"  # choose any instruct-capable model you have access to

# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForCausalLM.from_pretrained(
#     MODEL_NAME,
#     torch_dtype=torch.float16,
#     device_map="auto"
# )

# SYSTEM_RULES = """You are a precise JSON generator.

# Rules:
# 1. Input is a Hindi story.
# 2. Break the story into logical visual scenes.
# 3. For EACH scene return:
#    - scene_id (starting from 1)
#    - image_prompt (English, cinematic, detailed)
#    - audio_script (Hindi narration for that scene)
#    - subtitle_script (Hinglish subtitles for that scene)
# 4. DO NOT estimate time.
# 5. Return ONLY valid JSON array.
# 6. No explanations, no markdown.
# """

# def build_prompt(hindi_story: str) -> str:
#     return f"{SYSTEM_RULES}\n\nHindi story:\n{hindi_story}\n\nOutput:"

# import re

# def extract_last_json_array(text: str) -> str:
#     # Find the last [...] block to guard against preface/epilogue
#     matches = list(re.finditer(r"\[\s*(?:.|\n)*\]", text))
#     if not matches:
#         raise ValueError("No JSON array found in model output.")
#     return matches[-1].group(0)

# def validate_scenes(scenes: list):
#     if not isinstance(scenes, list) or not scenes:
#         raise ValueError("Output must be a non-empty JSON array.")

#     for i, scene in enumerate(scenes, start=1):
#         if not isinstance(scene, dict):
#             raise ValueError(f"Scene {i} must be an object.")
#         required = {"scene_id", "image_prompt", "audio_script", "subtitle_script"}
#         missing = required - set(scene.keys())
#         if missing:
#             raise ValueError(f"Scene {i} missing fields: {missing}")

#         if scene["scene_id"] != i:
#             raise ValueError(f"scene_id must start at 1 and increment; got {scene['scene_id']} at position {i}.")

#         # Basic type checks
#         for k in ["image_prompt", "audio_script", "subtitle_script"]:
#             if not isinstance(scene[k], str) or not scene[k].strip():
#                 raise ValueError(f"Scene {i} field '{k}' must be a non-empty string.")

# def generate_json_scenes(hindi_story: str, max_new_tokens: int = 1024) -> list:
#     prompt = build_prompt(hindi_story)
#     inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

#     output_ids = model.generate(
#         **inputs,
#         max_new_tokens=max_new_tokens,
#         do_sample=True,
#         temperature=0.7,
#         top_p=0.9,
#         eos_token_id=tokenizer.eos_token_id
#     )
#     text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

#     # Extract last JSON array (robust to any stray text)
#     json_text = extract_last_json_array(text)
#     scenes = json.loads(json_text)  # raises if invalid
#     validate_scenes(scenes)         # raises if schema mismatch
#     return scenes


# genai.configure(api_key="gemini_api_key")

# ---------- CONFIG ----------
OUTPUT_DIR = Path("assets/metadata")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------- PROMPT TEMPLATE ----------
# SYSTEM_PROMPT = """
# You are a story-to-scene parser.

# Rules:
# 1. Input is a Hindi story.
# 2. Break the story into logical visual scenes.
# 3. For EACH scene return:
#    - scene_id (starting from 1)
#    - image_prompt (English, cinematic, detailed)
#    - audio_script (Hindi narration for that scene)
#    - subtitle_script (Hinglish subtitles for that scene)
# 4. DO NOT estimate time.
# 5. Return ONLY valid JSON array.
# 6. No explanations, no markdown.
# """

# model = genai.GenerativeModel("gemini-2.0-flash", system_prompt=SYSTEM_PROMPT)

# USER_PROMPT_TEMPLATE = """
# Hindi Story:
# {story}
# """

# # ---------- LLM CALL (PLACEHOLDER) ----------
# def call_llm(user_prompt: str) -> str:
#     response = model.generate_content(user_prompt)
#     response_text = response.text.strip()
#     if response_text.startswith("```json"):
#         response_text = response_text[7:]
#     if response_text.startswith("```"):
#         response_text = response_text[3:]
#     if response_text.endswith("```"):
#         response_text = response_text[:-3]
    
#     response_text = response_text.strip()
    
#     try:
#         return response_text
#     except json.JSONDecodeError as e:
#         print(f"Failed to parse JSON: {e}")
#         print(f"Raw response was: {response_text}")
#         return {"error": "Failed to parse response", "raw_response": response_text}

# ---------- MAIN FUNCTION ----------
def parse_story_to_scenes(story_text: str) -> List[Dict]:

    scenes = json.loads(story_text)

    # Basic validation
    for i, scene in enumerate(scenes, start=1):
        assert "scene_id" in scene
        assert "image_prompt" in scene
        assert "audio_script" in scene
        assert "subtitle_script" in scene
        scene["scene_id"] = i  # enforce ordering

    # Save to file
    output_path = OUTPUT_DIR / "scenes.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(scenes, f, ensure_ascii=False, indent=2)

    return scenes

# ---------- CLI TEST ----------
if __name__ == "__main__":
    story = input("Enter Hindi story:\n")
    scenes = parse_story_to_scenes(story)
    print(f"Saved {len(scenes)} scenes to assets/metadata/scenes.json")

[
  {
    "scene_id": 1,
    "image_prompt": "Severe blizzard hitting a quiet residential neighborhood at night, heavy snowfall, strong winds, cinematic, realistic",
    "audio_script": "It starts quietly. Snow falls. Wind howls. And then suddenly, the power goes out.",
    "subtitle_script": "The blizzard begins. The power goes out."
  },
  {
    "scene_id": 2,
    "image_prompt": "Dark house interior with lights turning off, cold blue moonlight entering through windows, cinematic",
    "audio_script": "No lights. No heating. Just darkness and the sound of a blizzard outside your home.",
    "subtitle_script": "No lights. No heat. Only cold."
  },
  {
    "scene_id": 3,
    "image_prompt": "Person standing near a window watching heavy snowfall, worried expression, dramatic lighting",
    "audio_script": "If you think you can manage the cold easily, congratulations. You are about to become a human popsicle before sunrise.",
    "subtitle_script": "Cold is not your friend."
  },
  {
    "scene_id": 4,
    "image_prompt": "Smartphone showing no signal and low battery in a dark room, realistic survival mood",
    "audio_script": "First rule of survival. Stop checking your phone every five seconds. It will not magically bring the power back.",
    "subtitle_script": "Stop checking your phone."
  },
  {
    "scene_id": 5,
    "image_prompt": "Person putting phone on airplane mode, candle lighting the room, survival atmosphere",
    "audio_script": "Switch your phone to low power mode or airplane mode. Your battery is now more valuable than gold.",
    "subtitle_script": "Save your phone battery."
  }
]