import os
import json

class ContentRepository:
    def __init__(self, character_dir):
        self.plans_dir = os.path.join(character_dir, "plans")
        os.makedirs(self.plans_dir, exist_ok=True)

    def get_all_plans(self):
        plans = []
        if not os.path.exists(self.plans_dir):
            return plans
        for filename in os.listdir(self.plans_dir):
            if filename.endswith(".json"):
                try:
                    with open(os.path.join(self.plans_dir, filename), 'r', encoding='utf-8') as f:
                        plans.append(json.load(f))
                except (json.JSONDecodeError, IOError):
                    continue
        return plans

    def save_plan(self, plan_data):
        safe_title = "".join(c if c.isalnum() else "_" for c in plan_data.get("series_title", "plan")).strip("_")
        file_path = os.path.join(self.plans_dir, f"{safe_title or 'plan'}.json")
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(plan_data, f, indent=2, ensure_ascii=False)
        return file_path
