import time
import signal
import sys
import os
import json
from apscheduler.schedulers.background import BackgroundScheduler
from src.content.plan_store import PlanStore
from src.content.content_executor import ContentExecutor
from src.content.plan_generator import PlanGenerator
from src.social.instagram_client import InstagramClient
from src.social.mock_client import MockClient

# Set to True to test without actually posting to Instagram
DRY_RUN = True

class AgentOrchestrator:
    def __init__(self, character_name):
        self.character_name = character_name
        self.character_dir = os.path.join("characters", character_name)
        self.plan_store = PlanStore(self.character_dir)
        
        # Initialize client registry
        self.clients = {
            "instagram": InstagramClient(),
            "mock": MockClient()
        }
        
        self.executor = ContentExecutor(self.plan_store, self.clients)
        self.generator = PlanGenerator(os.getenv("OPENAI_API_KEY"), self.plan_store)
        self.running = True
        
        # Setup Scheduler
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.check_and_execute, 'interval', minutes=1)
        self.scheduler.start()
        
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def check_and_execute(self):
        due_plans = self.plan_store.get_due_plans()
        for filename in due_plans:
            print(f"Executing due plan: {filename}")
            self.executor.execute_plan(filename, dry_run=DRY_RUN)

    def stop(self, signum, frame):
        print("Stopping agent...")
        self.running = False
        self.scheduler.shutdown()
        for client in self.clients.values():
            client.close()

    def run(self):
        print(f"Agent started for {self.character_name}. Monitoring plans...")
        while self.running:
            time.sleep(1)

if __name__ == "__main__":
    char = sys.argv[1] if len(sys.argv) > 1 else "kai"
    orchestrator = AgentOrchestrator(char)
    orchestrator.run()
