import os
import json
from dotenv import load_dotenv
from repository import ContentRepository
from generator import ContentGenerator

def run_planner():
    load_dotenv(override=True)
    
    # Validate API key
    api_key_raw = os.getenv("OPENROUTER_API_KEY")
    api_key = api_key_raw.strip() if isinstance(api_key_raw, str) else api_key_raw
    if not api_key:
        raise ValueError("Missing OPENROUTER_API_KEY environment variable.")
    if not api_key.startswith("sk-or-"):
        raise ValueError(
            "OPENROUTER_API_KEY does not look like a valid OpenRouter key (expected prefix 'sk-or-')."
        )
    
    # Setup paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    char_dir = os.path.join(current_dir, "..", "..", "characters", "kai")
    char_path = os.path.join(char_dir, "Kai.json")
    
    # Load character data
    with open(char_path, "r", encoding="utf-8") as f:
        char_data = json.load(f)

    # Initialize components
    repo = ContentRepository(char_dir)
    gen = ContentGenerator(api_key)

    try:
        # Generate and save content
        plans = repo.get_all_plans()
        new_plan = gen.generate_series(char_data, plans)
        path = repo.save_plan(new_plan)
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


