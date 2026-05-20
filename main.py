import time
import signal
import sys
import os
from src.content.plan_store import PlanStore
from src.content.content_executor import ContentExecutor
from src.content.plan_generator import PlanGenerator
from src.social.instagram_client import InstagramClient

# Set to True to test without actually posting to Instagram
DRY_RUN = True

class AgentOrchestrator:
    def __init__(self, character_name):
        self.character_name = character_name
        self.character_dir = os.path.join("characters", character_name)
        self.plan_store = PlanStore(self.character_dir)
        self.ig_client = InstagramClient()
        self.executor = ContentExecutor(self.plan_store, self.ig_client)
        self.generator = PlanGenerator(os.getenv("OPENAI_API_KEY"), self.plan_store)
        self.running = True
        
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def stop(self, signum, frame):
        print("Stopping agent...")
        self.running = False
        self.ig_client.close()

    def run(self):
        print(f"Agent started for {self.character_name}. Monitoring plans...")
        while self.running:
            # 1. Check if any plan is currently in progress
            in_progress = self.plan_store.get_plans_by_status("in_progress")
            
            if not in_progress:
                # 2. Check for ready plans
                ready_plans = self.plan_store.get_plans_by_status("ready")
                if ready_plans:
                    filename = list(ready_plans.keys())[0]
                    print(f"Executing plan: {filename}")
                    self.executor.execute_plan(filename, dry_run=DRY_RUN)
                else:
                    # 3. If no plans ready, check if we need to generate one
                    all_plans = self.plan_store.load_all_plans()
                    if not all_plans:
                        print("No plans found. Generating new plan...")
                        try:
                            # Load character profile (assuming it exists at this path)
                            profile_path = os.path.join(self.character_dir, f"{self.character_name.capitalize()}.json")
                            with open(profile_path, 'r', encoding='utf-8') as f:
                                profile = json.load(f)
                            
                            new_plan = self.generator.create_new_plan(profile, [])
                            self.plan_store.save_plan(new_plan)
                            print("New plan generated and saved as draft.")
                        except Exception as e:
                            print(f"Error generating plan: {e}")
            
            time.sleep(60)

if __name__ == "__main__":
    import json
    # Usage: python main.py kai
    char = sys.argv[1] if len(sys.argv) > 1 else "kai"
    orchestrator = AgentOrchestrator(char)
    orchestrator.run()
