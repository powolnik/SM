import os
import json
import pytest
from src.content.plan_store import PlanStore

def test_plan_store_lifecycle(temp_character_dir):
    store = PlanStore(temp_character_dir)
    
    # Create a dummy plan
    plan = {
        "series_title": "Test Series",
        "target_audience": "Test Audience",
        "execution_status": "draft",
        "posts": []
    }
    
    # Test saving
    file_path = store.save_plan(plan)
    assert os.path.exists(file_path)
    
    # Test loading
    filename = os.path.basename(file_path)
    loaded_plan = store.load_plan(filename)
    assert loaded_plan["series_title"] == "Test Series"
    
    # Test status update
    store.update_plan_status(filename, "confirmed")
    updated_plan = store.load_plan(filename)
    assert updated_plan["execution_status"] == "confirmed"
    
    # Test counts
    counts = store.get_plan_counts()
    assert counts["confirmed"] == 1
    assert counts["draft"] == 0
