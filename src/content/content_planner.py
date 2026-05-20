import os
import json
import time
from dotenv import load_dotenv
try:
    from .plan_store import PlanStore
    from .plan_generator import PlanGenerator
    from .content_executor import ContentExecutor
except ImportError:
    from plan_store import PlanStore
    from plan_generator import PlanGenerator
    from content_executor import ContentExecutor

try:
    from src.social.instagram_client import InstagramClient
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from social.instagram_client import InstagramClient


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


def _get_char_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "..", "..", "characters", "kai")


def run_planner():
    load_dotenv(override=True)
    _debug_log("H3", "content_planner.py:25", "dotenv_loaded", {"override": True})
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    _debug_log("H3", "content_planner.py:28", "api_key_validity_checked", {"present": bool(api_key), "prefix_ok": bool(api_key and api_key.startswith("sk-or-"))})
    if not api_key or not api_key.startswith("sk-or-"):
        raise ValueError("Invalid or missing OPENROUTER_API_KEY.")
    
    char_dir = _get_char_dir()
    
    with open(os.path.join(char_dir, "Kai.json"), "r", encoding="utf-8") as f:
        character_profile = json.load(f)
    _debug_log("H5", "content_planner.py:35", "character_profile_loaded", {"char_dir": char_dir, "keys": list(character_profile.keys()) if isinstance(character_profile, dict) else []})

    store = PlanStore(char_dir)
    generator = PlanGenerator(api_key)

    try:
        existing_plans = store.load_all_plans()
        _debug_log("H5", "content_planner.py:42", "existing_plans_loaded", {"count": len(existing_plans)})
        new_plan = generator.create_new_plan(character_profile, existing_plans)
        _debug_log("H4", "content_planner.py:44", "new_plan_created", {"type": type(new_plan).__name__, "keys": list(new_plan.keys()) if isinstance(new_plan, dict) else []})
        path = store.save_plan(new_plan)
        _debug_log("H5", "content_planner.py:46", "new_plan_saved", {"path": path})
        print(f"Content plan saved to: {path}")
    except Exception as e:
        if "401" in str(e) and "User not found" in str(e):
            print("Authentication failed: OPENROUTER_API_KEY is invalid for OpenRouter.")
            print("Set a valid OpenRouter key (starts with 'sk-or-') and run again.")
            raise
        print(f"Error generating content: {e}")
        raise


def run_executor(plan_filename):
    load_dotenv(override=True)

    char_dir = _get_char_dir()
    store = PlanStore(char_dir)
    ig = InstagramClient()
    executor = ContentExecutor(store, ig)
    executor.execute_plan(plan_filename)


if __name__ == "__main__":
    run_planner()
