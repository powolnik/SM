import time
import signal
import sys
import os
from src.content.plan_store import PlanStore
from src.content.content_executor import ContentExecutor
from src.content.plan_generator import PlanGenerator
from src.social.instagram_client import InstagramClient

class AgentOrchestrator:
    def __init__(self, character_name):
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
        print("Agent started. Monitoring plans...")
        while self.running:
            # 1. Check if any plan is currently in progress
            in_progress = self.plan_store.get_plans_by_status("in_progress")
            
            if not in_progress:
                # 2. Check for ready plans
                ready_plans = self.plan_store.get_plans_by_status("ready")
                if ready_plans:
                    filename = list(ready_plans.keys())[0]
                    print(f"Executing plan: {filename}")
                    self.executor.execute_plan(filename)
                else:
                    # 3. If no plans ready, check if we need to generate one
                    # (Logic: only generate if no pending/ready/in_progress plans exist)
                    all_plans = self.plan_store.load_all_plans()
                    if not all_plans:
                        print("No plans found. Generating new plan...")
                        # Assuming character profile is loaded from JSON in character_dir
                        # This part would need integration with your specific profile loader
                        # self.generator.create_new_plan(...)
            
            time.sleep(60)

if __name__ == "__main__":
    # Usage: python main.py kai
    char = sys.argv[1] if len(sys.argv) > 1 else "kai"
    orchestrator = AgentOrchestrator(char)
    orchestrator.run()
