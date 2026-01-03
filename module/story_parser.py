import json
from pathlib import Path
from typing import List, Dict
# import google.generativeai as genai

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
#    - image_prompt_en (English, cinematic, detailed)
#    - audio_script_hi (Hindi narration for that scene)
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
    """
    Converts Hindi story text into structured scene JSON.
    """
    # response_text = call_llm(
    #     USER_PROMPT_TEMPLATE.format(story=story_text)
    # )

    # try:
    #     scenes = json.loads(response_text)
    # except json.JSONDecodeError as e:
    #     raise ValueError("LLM did not return valid JSON") from e

    scenes = [
  {
    "scene_id": 1,
    "image_prompt_en": "Early morning sunlight in a quiet Indian village street, soft golden light, cinematic, realistic",
    "audio_script_hi": "सुबह की हल्की धूप में एक छोटा लड़का अपने घर से बाहर निकला।"
  },
  {
    "scene_id": 2,
    "image_prompt_en": "Empty peaceful street with birds flying and trees around, calm morning atmosphere, cinematic",
    "audio_script_hi": "सड़क पर शांति थी और पक्षियों की आवाज़ गूंज रही थी।"
  },
  {
    "scene_id": 3,
    "image_prompt_en": "A young boy sitting under a tree looking up at the sky with a gentle smile, serene, cinematic, realistic",
    "audio_script_hi": "थोड़ी दूर चलने के बाद उसने एक पेड़ के नीचे बैठकर आसमान की ओर देखा और मुस्कुराया।"
  }
]

    # Basic validation
    for i, scene in enumerate(scenes, start=1):
        assert "scene_id" in scene
        assert "image_prompt_en" in scene
        assert "audio_script_hi" in scene
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
