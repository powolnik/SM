import json
import time
from openai import OpenAI


def _word_count(text):
    return len(str(text).strip().split())


def _require_keys(obj, required_keys, path):
    if not isinstance(obj, dict):
        raise ValueError(f"{path} must be an object.")
    missing = [key for key in required_keys if key not in obj]
    if missing:
        raise ValueError(f"{path} is missing required keys: {', '.join(missing)}")


def _validate_plan_schema(plan):
    _require_keys(plan, ["series_title", "target_audience", "posts", "execution_status"], "plan")

    if not isinstance(plan["series_title"], str) or not plan["series_title"].strip():
        raise ValueError("plan.series_title must be a non-empty string.")
    if not isinstance(plan["target_audience"], str) or not plan["target_audience"].strip():
        raise ValueError("plan.target_audience must be a non-empty string.")
    if plan["execution_status"] not in ["draft", "confirmed", "in_progress", "completed"]:
        raise ValueError("plan.execution_status must be one of: draft, confirmed, in_progress, completed.")

    posts = plan["posts"]
    if not isinstance(posts, list):
        raise ValueError("plan.posts must be an array.")
    if not (6 <= len(posts) <= 10):
        raise ValueError("plan.posts must contain between 6 and 10 posts.")

    required_post_keys = [
        "post_number",
        "goal",
        "format",
        "hook",
        "caption",
        "on_image_text",
        "hashtags",
        "cta",
        "image_prompt",
    ]
    required_image_prompt_keys = [
        "scene_description",
        "subject",
        "composition",
        "lighting",
        "color_palette",
        "style",
        "mood",
        "background_details",
        "props_details",
        "technical",
    ]
    required_technical_keys = ["aspect_ratio", "lens", "quality", "negative_prompt"]
    allowed_formats = {"single_image", "carousel", "reel_cover"}

    for i, post in enumerate(posts):
        post_path = f"plan.posts[{i}]"
        _require_keys(post, required_post_keys, post_path)

        if isinstance(post["post_number"], bool) or not isinstance(post["post_number"], int):
            raise ValueError(f"{post_path}.post_number must be an integer.")
        if post["format"] not in allowed_formats:
            raise ValueError(f"{post_path}.format must be one of: {', '.join(sorted(allowed_formats))}.")
        if _word_count(post["hook"]) > 12:
            raise ValueError(f"{post_path}.hook must have at most 12 words.")
        if _word_count(post["on_image_text"]) > 8:
            raise ValueError(f"{post_path}.on_image_text must have at most 8 words.")

        caption_words = _word_count(post["caption"])
        if not (120 <= caption_words <= 220):
            raise ValueError(f"{post_path}.caption must have between 120 and 220 words.")

        hashtags = post["hashtags"]
        if not isinstance(hashtags, list) or len(hashtags) != 5:
            raise ValueError(f"{post_path}.hashtags must contain exactly 5 items.")
        if any((not isinstance(tag, str)) or (not tag.startswith("#")) for tag in hashtags):
            raise ValueError(f"{post_path}.hashtags must be strings starting with '#'.")

        for text_key in ["goal", "hook", "caption", "on_image_text", "cta"]:
            if not isinstance(post[text_key], str) or not post[text_key].strip():
                raise ValueError(f"{post_path}.{text_key} must be a non-empty string.")

        image_prompt = post["image_prompt"]
        _require_keys(image_prompt, required_image_prompt_keys, f"{post_path}.image_prompt")
        for key in [
            "scene_description",
            "subject",
            "composition",
            "lighting",
            "style",
            "mood",
            "background_details",
            "props_details",
        ]:
            if not isinstance(image_prompt[key], str) or not image_prompt[key].strip():
                raise ValueError(f"{post_path}.image_prompt.{key} must be a non-empty string.")

        color_palette = image_prompt["color_palette"]
        if not isinstance(color_palette, list) or not color_palette:
            raise ValueError(f"{post_path}.image_prompt.color_palette must be a non-empty array.")
        if any((not isinstance(color, str)) or (not color.strip()) for color in color_palette):
            raise ValueError(f"{post_path}.image_prompt.color_palette must contain non-empty strings.")

        technical = image_prompt["technical"]
        _require_keys(technical, required_technical_keys, f"{post_path}.image_prompt.technical")
        for key in required_technical_keys:
            if not isinstance(technical[key], str) or not technical[key].strip():
                raise ValueError(f"{post_path}.image_prompt.technical.{key} must be a non-empty string.")


def _debug_log(hypothesis_id, location, message, data):
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


class PlanGenerator:
    def __init__(self, api_key, plan_store):
        self.client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
        self.plan_store = plan_store

    def create_new_plan(self, character_profile, existing_plans):
        existing_titles = [p.get("series_title", "Unknown") for p in existing_plans]
        titles_str = ", ".join(existing_titles) if existing_titles else "None"
        plans_context = json.dumps(existing_plans, indent=2) if existing_plans else "None"
        
        prompt = f"""
Based on the character profile below, create an Instagram content series.

Character profile:
{json.dumps(character_profile, indent=2, ensure_ascii=False)}

Existing series history:
{plans_context}

Return ONLY valid JSON with this schema:
{{
  "series_title": "string",
  "target_audience": "string",
  "execution_status": "draft",
  "posts": [...]
}}
"""
        
        response = self.client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You write precise, production-ready Instagram copy and image-generation prompts. Follow the schema exactly and output JSON only."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content
        cleaned_json = content.replace("```json", "").replace("```", "").strip()
        plan = json.loads(cleaned_json)
        
        # Ensure status is set to draft
        plan["execution_status"] = "draft"
        
        _validate_plan_schema(plan)
        return plan
