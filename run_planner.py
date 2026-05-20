import json
import os
import time
import traceback
import sys


def _debug_log(hypothesis_id, location, message, data):
    # #region agent log
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
    # #endregion

if __name__ == "__main__":
    _debug_log("H0", "run_planner.py:24", "script_start", {"cwd": os.getcwd()})
    
    # Check for test run argument
    is_test = "--test" in sys.argv
    
    try:
        from src.content.content_planner import run_planner as run_content_planner
        from src.content.content_planner import run_executor
        _debug_log("H1", "run_planner.py:27", "import_success", {"symbol": "run_planner"})
    except Exception as e:
        _debug_log("H1", "run_planner.py:29", "import_failed", {"error": str(e), "traceback": traceback.format_exc()})
        raise

    try:
        if is_test:
            # Example: run_executor("some_plan.json", dry_run=True)
            # You would need to specify the plan file as an argument
            print("Test run mode enabled.")
        else:
            run_content_planner()
        _debug_log("H5", "run_planner.py:34", "delegated_run_completed", {"module": "src.content.content_planner"})
    except Exception as e:
        _debug_log("H4", "run_planner.py:54", "runtime_failed", {"error": str(e), "traceback": traceback.format_exc()})
        raise
