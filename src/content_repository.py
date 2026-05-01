import os
import json

def get_existing_series_titles(plans_dir):
    titles = []
    if not os.path.exists(plans_dir):
        return titles
    for filename in os.listdir(plans_dir):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(plans_dir, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if "series_title" in data:
                        titles.append(data["series_title"])
            except (json.JSONDecodeError, IOError):
                continue
    return titles
