from src.content.content_planner import generate_instagram_content_series
import json
import os

if __name__ == "__main__":
    # This script now acts as the entry point
    content_series_json = generate_instagram_content_series()
    
    cleaned_json = content_series_json.replace("```json", "").replace("```", "").strip()
    content_data = json.loads(cleaned_json)
    
    # Adjust path relative to the root
    output_dir = os.path.join("characters", "kai", "plans")
    os.makedirs(output_dir, exist_ok=True)
    
    safe_title = "".join([c if c.isalnum() else "_" for c in content_data.get("series_title", "content_plan")])
    file_path = os.path.join(output_dir, f"{safe_title}.json")
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(content_data, f, indent=2, ensure_ascii=False)
        
    print(f"Content plan saved to: {file_path}")
