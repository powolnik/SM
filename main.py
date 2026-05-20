import sys
from src.orchestration.orchestrator import AgentOrchestrator

if __name__ == "__main__":
    char = sys.argv[1] if len(sys.argv) > 1 else "kai"
    orchestrator = AgentOrchestrator(char, dry_run=True)
    orchestrator.run()
