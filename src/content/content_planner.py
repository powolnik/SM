import os
import json
from dotenv import load_dotenv
from plan_store import PlanStore
from plan_generator import PlanGenerator

def run_planner():
    load_dotenv(override=True)
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key or not api_key.startswith("sk-or-"):
        raise ValueError("Invalid or missing OPENROUTER_API_KEY.")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    char_dir = os.path.join(current_dir, "..", "..", "characters", "kai")
    
    with open(os.path.join(char_dir, "Kai.json"), "r", encoding="utf-8") as f:
        character_profile = json.load(f)

    store = PlanStore(char_dir)
    generator = PlanGenerator(api_key)

    try:
        existing_plans = store.load_all_plans()
        new_plan = generator.create_new_plan(character_profile, existing_plans)
        path = store.save_plan(new_plan)
        print(f"Content plan saved to: {path}")
    except Exception as e:
        if "401" in str(e) and "User not found" in str(e):
            print("Authentication failed: OPENROUTER_API_KEY is invalid for OpenRouter.")
            print("Set a valid OpenRouter key (starts with 'sk-or-') and run again.")
            raise
        print(f"Error generating content: {e}")
        raise

if __name__ == "__main__":
    run_planner()


