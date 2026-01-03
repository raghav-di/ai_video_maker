import json
from pathlib import Path
from typing import List, Dict

# ---------- CONFIG ----------
OUTPUT_DIR = Path("assets/metadata")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------- PROMPT TEMPLATE ----------
SYSTEM_PROMPT = """
You are a story-to-scene parser.

Rules:
1. Input is a Hindi story.
2. Break the story into logical visual scenes.
3. For EACH scene return:
   - scene_id (starting from 1)
   - image_prompt_en (English, cinematic, detailed)
   - audio_script_hi (Hindi narration for that scene)
4. DO NOT estimate time.
5. Return ONLY valid JSON array.
6. No explanations, no markdown.
"""

USER_PROMPT_TEMPLATE = """
Hindi Story:
{story}
"""

# ---------- LLM CALL (PLACEHOLDER) ----------
def call_llm(system_prompt: str, user_prompt: str) -> str:
    """
    Replace this function with:
    - OpenAI API
    - HuggingFace inference
    - Local LLaMA/Mistral

    For now, this is a placeholder.
    """
    raise NotImplementedError("LLM call not implemented yet")

# ---------- MAIN FUNCTION ----------
def parse_story_to_scenes(story_text: str) -> List[Dict]:
    """
    Converts Hindi story text into structured scene JSON.
    """
    response_text = call_llm(
        SYSTEM_PROMPT,
        USER_PROMPT_TEMPLATE.format(story=story_text)
    )

    try:
        scenes = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError("LLM did not return valid JSON") from e

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
