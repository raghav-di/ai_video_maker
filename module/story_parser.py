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
    "image_prompt_en": "A government forest office with congratulatory atmosphere, official papers on desk, cinematic lighting, realistic",
    "audio_script_hi": "बधाई हो! आपके पिता फॉरेस्ट गार्ड बन गए हैं और आपकी पोस्टिंग छत्तीसगढ़ के एक घने जंगल में हुई है।"
  },
  {
    "scene_id": 2,
    "image_prompt_en": "Dense dark jungle in Chhattisgarh, thick fog, twisted trees, eerie atmosphere, cinematic, realistic",
    "audio_script_hi": "लेकिन यह जंगल कोई आम जंगल नहीं है। लोग इसे श्रापित मानते हैं और कहा जाता है कि यह जंगल लोगों का शिकार करता है।"
  },
  {
    "scene_id": 3,
    "image_prompt_en": "A small isolated house in the middle of a haunted jungle, night time, dim lights inside the house, cinematic horror mood",
    "audio_script_hi": "आपका घर इस जंगल के लगभग बीच में है, और अब आपकी सुरक्षा केवल कुछ नियमों पर निर्भर करती है।"
  },
  {
    "scene_id": 4,
    "image_prompt_en": "A warning board in a dark forest with mysterious symbols, cinematic horror style",
    "audio_script_hi": "पहला नियम: सूर्यास्त के बाद घर से बाहर कभी न निकलें। दूसरा नियम: अगर जंगल से कोई आवाज़ बुलाए, तो जवाब न दें। तीसरा नियम: रात में खिड़कियों और दरवाज़ों को बंद रखें। चौथा नियम: जंगल में कभी भी अकेले न जाएँ।"
  },
  {
    "scene_id": 5,
    "image_prompt_en": "Morning light entering a forest clearing, slightly hopeful yet mysterious atmosphere, cinematic",
    "audio_script_hi": "आशा करते हैं कि आपको इस जंगल में रहना पसंद आएगा।"
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
