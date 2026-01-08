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
    "image_prompt_en": "Government forest office interior, dim lighting, old files on wooden desk, cinematic, eerie shadows, realistic",
    "audio_script_hi": "बधाई हो! आपके पिता फॉरेस्ट गार्ड बन गए हैं।",
    "subtitle_script_hi": "Badhai ho! Aapke pita forest guard ban gaye hain."
  },
  {
    "scene_id": 2,
    "image_prompt_en": "Official appointment letter on desk, flickering tube light, unsettling atmosphere, cinematic horror style",
    "audio_script_hi": "आपकी पोस्टिंग छत्तीसगढ़ के एक घने जंगल में हुई है।",
    "subtitle_script_hi": "Aapki posting Chhattisgarh ke jungle mein hui hai."
  },
  {
    "scene_id": 3,
    "image_prompt_en": "Dense Chhattisgarh forest, tall trees blocking sunlight, thick fog, dark green tones, horror cinematic",
    "audio_script_hi": "लेकिन यह जंगल कोई आम जंगल नहीं है।",
    "subtitle_script_hi": "Lekin yeh jungle koi aam jungle nahi hai."
  },
  {
    "scene_id": 4,
    "image_prompt_en": "Haunted forest with twisted trees, strange mist, eerie silence, dark horror mood, cinematic lighting",
    "audio_script_hi": "लोग इस जंगल को श्रापित मानते हैं।",
    "subtitle_script_hi": "Log is jungle ko shraapit maante hain."
  },
  {
    "scene_id": 5,
    "image_prompt_en": "Deep forest path at dusk, shadows between trees, unsettling presence, cinematic horror realism",
    "audio_script_hi": "कहा जाता है कि यह जंगल लोगों का शिकार करता है।",
    "subtitle_script_hi": "Kaha jaata hai yeh jungle logon ka shikaar karta hai."
  },
  {
    "scene_id": 6,
    "image_prompt_en": "Isolated wooden house in the middle of dark forest, faint yellow light inside, horror atmosphere, cinematic",
    "audio_script_hi": "आपका घर इसी जंगल के लगभग बीच में है।",
    "subtitle_script_hi": "Aapka ghar jungle ke bilkul beech mein hai."
  },
  {
    "scene_id": 7,
    "image_prompt_en": "Forest house interior at night, window shadows, dim lantern light, suspenseful horror style",
    "audio_script_hi": "अब आपकी सुरक्षा कुछ नियमों पर निर्भर करती है।",
    "subtitle_script_hi": "Ab aapki suraksha kuch niyamon par nirbhar karti hai."
  },
  {
    "scene_id": 8,
    "image_prompt_en": "Warning signboard in forest, scratched symbols, red markings, eerie horror cinematic look",
    "audio_script_hi": "पहला नियम: सूर्यास्त के बाद घर से बाहर कभी न निकलें।",
    "subtitle_script_hi": "Pehla niyam: Sooryaast ke baad bahar na niklein."
  },
  {
    "scene_id": 9,
    "image_prompt_en": "Dark forest at night, invisible presence, rustling leaves, unsettling horror atmosphere",
    "audio_script_hi": "दूसरा नियम: अगर जंगल से कोई आवाज़ बुलाए, तो जवाब न दें।",
    "subtitle_script_hi": "Doosra niyam: Jungle ki awaaz ka jawaab na dein."
  },
  {
    "scene_id": 10,
    "image_prompt_en": "House doors and windows tightly shut at night, moonlight outside, tense horror mood",
    "audio_script_hi": "तीसरा नियम: रात में दरवाज़े और खिड़कियाँ बंद रखें।",
    "subtitle_script_hi": "Teesra niyam: Raat mein darwaaze band rakhein."
  },
  {
    "scene_id": 11,
    "image_prompt_en": "Lonely forest trail disappearing into darkness, warning vibe, cinematic horror",
    "audio_script_hi": "चौथा नियम: जंगल में कभी भी अकेले न जाएँ।",
    "subtitle_script_hi": "Chautha niyam: Jungle mein kabhi akele na jaayein."
  },
  {
    "scene_id": 12,
    "image_prompt_en": "Early morning forest with faint sunlight, fog still present, mysterious calm after horror",
    "audio_script_hi": "आशा करते हैं कि आपको इस जंगल में रहना पसंद आएगा।",
    "subtitle_script_hi": "Umeed hai aapko yeh jungle pasand aayega."
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
