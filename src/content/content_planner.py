import os
import json
import time
from dotenv import load_dotenv
try:
    from .plan_store import PlanStore
    from .plan_generator import PlanGenerator
except ImportError:
    from plan_store import PlanStore
    from plan_generator import PlanGenerator


class ContentPlannerService:
    def __init__(self):
        load_dotenv(override=True)
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.char_dir = os.path.join(current_dir, "..", "..", "characters", "kai")
        
        self.store = PlanStore(self.char_dir)
        self.generator = PlanGenerator(self.api_key)
        
        self._log("H3", "content_planner.py:init", "service_initialized", {"char_dir": self.char_dir})

    def _log(self, hypothesis_id, location, message, data):
        payload = {
            "sessionId": "0a5624",
            "runId": "pre-fix",
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data,
            "timestamp": int(time.time() * 1000),
        }
        with open("debug-0a5624.log", "a", encoding="utf-8") as _f:
            _f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def run_planner(self):
        self._log("H3", "content_planner.py:28", "api_key_validity_checked", {"present": bool(self.api_key), "prefix_ok": bool(self.api_key and self.api_key.startswith("sk-or-"))})
        if not self.api_key or not self.api_key.startswith("sk-or-"):
            raise ValueError("Invalid or missing OPENROUTER_API_KEY.")
        
        with open(os.path.join(self.char_dir, "Kai.json"), "r", encoding="utf-8") as f:
            character_profile = json.load(f)
        self._log("H5", "content_planner.py:35", "character_profile_loaded", {"keys": list(character_profile.keys())})

        try:
            existing_plans = self.store.load_all_plans()
            self._log("H5", "content_planner.py:42", "existing_plans_loaded", {"count": len(existing_plans)})
            new_plan = self.generator.create_new_plan(character_profile, existing_plans)
            self._log("H4", "content_planner.py:44", "new_plan_created", {"type": type(new_plan).__name__})
            path = self.store.save_plan(new_plan)
            self._log("H5", "content_planner.py:46", "new_plan_saved", {"path": path})
            return path
        except Exception as e:
            self._log("H4", "content_planner.py:error", "generation_failed", {"error": str(e)})
            raise

if __name__ == "__main__":
    service = ContentPlannerService()
    try:
        path = service.run_planner()
        print(f"Content plan saved to: {path}")
    except Exception as e:
        print(f"Error generating content: {e}")
