import json
import time
from openai import OpenAI


def _debug_log(hypothesis_id, location, message, data):
    # #region agent log
    payload = {
        "sessionId": "95411c",
        "runId": "pre-fix",
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    with open("debug-95411c.log", "a", encoding="utf-8") as _f:
        _f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    # #endregion


class PlanGenerator:
    def __init__(self, api_key):
        self.client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    def create_new_plan(self, character_profile, existing_plans):
        existing_titles = [p.get("series_title", "Unknown") for p in existing_plans]
        titles_str = ", ".join(existing_titles) if existing_titles else "None"
        plans_context = json.dumps(existing_plans, indent=2) if existing_plans else "None"
        _debug_log("H2", "plan_generator.py:28", "generator_inputs_prepared", {"existing_count": len(existing_plans), "titles_preview": titles_str[:200]})
        
        prompt = f"""
Based on the character profile below, create an Instagram content series.

Character profile:
{json.dumps(character_profile, indent=2, ensure_ascii=False)}

Existing series history (do not repeat these themes or specific post ideas):
{plans_context}

CRITICAL: You must choose a NEW, unique theme for this series that is 
distinct from the existing titles, target audiences, and content listed above.

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
        
        response = self.client.chat.completions.create(
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
        _debug_log("H1", "plan_generator.py:102", "response_received", {"has_choices": hasattr(response, "choices"), "choices_count": len(response.choices) if getattr(response, "choices", None) is not None else 0})

        content = response.choices[0].message.content
        _debug_log("H3", "plan_generator.py:105", "content_extracted", {"is_none": content is None, "content_len": len(content) if isinstance(content, str) else -1, "starts_with_fence": bool(isinstance(content, str) and content.strip().startswith("```"))})
        cleaned_json = content.replace("```json", "").replace("```", "").strip()
        _debug_log("H3", "plan_generator.py:107", "json_cleaned", {"cleaned_len": len(cleaned_json), "starts_with_brace": cleaned_json.startswith("{"), "ends_with_brace": cleaned_json.endswith("}")})
        return json.loads(cleaned_json)
