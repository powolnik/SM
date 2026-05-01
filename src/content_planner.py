
import json
import os
from openai import OpenAI


def generate_instagram_content_series():
    # Load character data
    char_path = os.path.join(os.path.dirname(__file__), "../../characters/Kai.json")
    with open(char_path, "r", encoding="utf-8") as f:
        character_data = json.load(f)

    # Prepare prompt
    prompt = f"""
Based on the character profile below, create an Instagram content series.

Character profile:
{json.dumps(character_data, indent=2, ensure_ascii=False)}

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

    # Call AI model
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPENROUTER_API_KEY")
    )
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
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


if __name__ == "__main__":
    content_series = generate_instagram_content_series()
    print(content_series)
