import os
import json
import time


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


class PlanStore:
    def __init__(self, character_dir):
        self.plans_dir = os.path.join(character_dir, "plans")
        os.makedirs(self.plans_dir, exist_ok=True)

    def load_all_plans(self):
        plans = {}
        if not os.path.exists(self.plans_dir):
            return plans
        for filename in os.listdir(self.plans_dir):
            if filename.endswith(".json"):
                try:
                    with open(os.path.join(self.plans_dir, filename), 'r', encoding='utf-8') as f:
                        plans[filename] = json.load(f)
                except (json.JSONDecodeError, IOError):
                    continue
        return plans

    def get_plans_by_status(self, status):
        all_plans = self.load_all_plans()
        return {
            filename: plan for filename, plan in all_plans.items() 
            if plan.get("execution_status") == status
        }

    def load_plan(self, filename):
        path = os.path.join(self.plans_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_plan(self, plan):
        safe_title = "".join(c if c.isalnum() else "_" for c in plan.get("series_title", "plan")).strip("_")
        file_path = os.path.join(self.plans_dir, f"{safe_title or 'plan'}.json")
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        return file_path

    def get_plan_counts(self):
        counts = {"pending": 0, "in_progress": 0, "completed": 0, "draft": 0, "ready": 0}
        for filename in os.listdir(self.plans_dir):
            if filename.endswith(".json"):
                plan = self.load_plan(filename)
                status = plan.get("execution_status", "pending")
                counts[status] = counts.get(status, 0) + 1
        return counts

    def update_plan_status(self, filename, status):
        path = os.path.join(self.plans_dir, filename)
        plan = self.load_plan(filename)
        plan["execution_status"] = status
        with open(path, "w", encoding='utf-8') as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
