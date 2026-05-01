import json
import os
from dotenv import load_dotenv


try:
    from plan_repository import list_series_titles, get_all_existing_plans
except Exception as e:
    raise
try:
    from openai import OpenAI
except ImportError:
    raise ImportError(
        "The 'openai' package is not installed. Please install it using one of these commands:\n"
        "pip install openai\n\n"
        "If you have multiple Python versions, use:\n"
        "python -m pip install openai\n\n"
        "This ensures the package is installed for the Python interpreter you're using."
    )


def generate_instagram_content_series():
    # Load character data
    # Get the directory of the current script (src/content)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up two levels to the project root and into characters
    char_path = os.path.join(current_dir, "..", "..", "characters", "kai", "Kai.json")
    plans_dir = os.path.join(current_dir, "..", "..", "characters", "kai", "plans")

    with open(char_path, "r", encoding="utf-8") as f:
        character_data = json.load(f)

    # Get existing plans to avoid duplicates
    existing_plans = get_all_existing_plans(plans_dir)
    existing_titles = [p.get("series_title", "Unknown") for p in existing_plans]
    titles_str = ", ".join(existing_titles) if existing_titles else "None"
    plans_context = json.dumps(existing_plans, indent=2) if existing_plans else "None"

    # Prepare prompt
    prompt = f"""
Based on the character profile below, create an Instagram content series.

Character profile:
{json.dumps(character_data, indent=2, ensure_ascii=False)}

Existing series history (do not repeat these themes or specific post ideas):
{plans_context}

CRITICAL: You must choose a NEW, unique theme for this series that is 
distinct from the existing titles and content listed above.

You are a senior Instagram content strategist and image prompt engineer.
Return ONLY valid JSON with this schema:
{{
  "series_title": "string",
  "target_audience": "string",
  "posts": [
    {{
      "post_number": 1,
      "goal": "string",
      "format": "single_image|carousel|reel_cover",
      "hook": "string (max 12 words)",
      "caption": "string (120-220 words, polished, ready to publish)",
      "on_image_text": "string (max 8 words)",
      "hashtags": ["#tag1", "#tag2", "#tag3", "#tag4", "#tag5"],
      "cta": "string",
      "image_prompt": {{
        "scene_description": "highly detailed visual scene",
        "subject": "main subject details",
        "composition": "camera angle, framing, depth",
        "lighting": "time of day, light style, contrast",
        "color_palette": ["color1", "color2", "color3"],
        "style": "visual style keywords",
        "mood": "emotional tone",
        "background_details": "specific environment elements",
        "props_details": "objects/materials/textures",
        "technical": {{
          "aspect_ratio": "4:5",
          "lens": "e.g. 35mm",
          "quality": "ultra-detailed, sharp focus",
          "negative_prompt": "what to avoid"
        }}
      }}
    }}
  ]
}}

Hard constraints:
- Number of posts must be between 6 and 10.
- Captions must be specific, not generic.
- Image prompts must be production-grade and visually concrete.
- Keep continuity across the whole series (story progression).
- No placeholders like [insert...].
- Return JSON only.
"""
    load_dotenv(override=True)
    # Call AI model
    api_key_raw = os.getenv("OPENROUTER_API_KEY")
    api_key = api_key_raw.strip() if isinstance(api_key_raw, str) else api_key_raw
    if not api_key:
        raise ValueError("Missing OPENROUTER_API_KEY environment variable.")
    if not api_key.startswith("sk-or-"):
        raise ValueError(
            "OPENROUTER_API_KEY does not look like a valid OpenRouter key (expected prefix 'sk-or-')."
        )
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )
    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You write precise, production-ready Instagram copy and image-generation prompts. "
                    "Follow the schema exactly and output JSON only."
                ),
            },
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def save_content_plan(content_series_json):
    cleaned_json = content_series_json.replace("```json", "").replace("```", "").strip()
    content_data = json.loads(cleaned_json)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "..", "..", "characters", "kai", "plans")
    os.makedirs(output_dir, exist_ok=True)

    safe_title = "".join(
        c if c.isalnum() else "_" for c in content_data.get("series_title", "content_plan")
    ).strip("_")
    if not safe_title:
        safe_title = "content_plan"

    file_path = os.path.join(output_dir, f"{safe_title}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(content_data, f, indent=2, ensure_ascii=False)

    return file_path


if __name__ == "__main__":
    try:
        content = generate_instagram_content_series()
        saved_path = save_content_plan(content)
        print(f"Content plan saved to: {saved_path}")
    except Exception as e:
        if "401" in str(e) and "User not found" in str(e):
            print("Authentication failed: OPENROUTER_API_KEY is invalid for OpenRouter.")
            print("Set a valid OpenRouter key (starts with 'sk-or-') and run again.")
            raise
        print(f"Error generating content: {e}")


