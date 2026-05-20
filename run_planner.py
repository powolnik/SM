import json
import os
import time
import traceback
import sys
from src.utils.logger import debug_log


if __name__ == "__main__":
    debug_log("H0", "run_planner.py:24", "script_start", {"cwd": os.getcwd()})
    
    # Check for test run argument
    is_test = "--test" in sys.argv
    
    try:
        from src.content.content_planner import run_planner as run_content_planner
        from src.content.content_planner import run_executor
        debug_log("H1", "run_planner.py:27", "import_success", {"symbol": "run_planner"})
    except Exception as e:
        debug_log("H1", "run_planner.py:29", "import_failed", {"error": str(e), "traceback": traceback.format_exc()})
        raise

    try:
        if is_test:
            # Usage: python run_planner.py --test [filename]
            # Defaults to test_plan.json if no filename provided
            idx = sys.argv.index("--test")
            filename = sys.argv[idx + 1] if (len(sys.argv) > idx + 1 and not sys.argv[idx + 1].startswith("--")) else "test_plan.json"
            print(f"Test run mode enabled for: {filename}")
            run_executor(filename, dry_run=True)
        else:
            run_content_planner()
        debug_log("H5", "run_planner.py:34", "delegated_run_completed", {"module": "src.content.content_planner"})
    except Exception as e:
        debug_log("H4", "run_planner.py:54", "runtime_failed", {"error": str(e), "traceback": traceback.format_exc()})
        raise
