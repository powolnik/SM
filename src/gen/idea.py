
import json
import os
from openai import OpenAI

def generate_instagram_ideas():
    # Load character data
    char_path = os.path.join(os.path.dirname(__file__), '../../characters/Kai.json')
    with open(char_path, 'r') as f:
        character_data = json.load(f)

    # Prepare prompt
    prompt = f"Based on the following character profile, generate a series of Instagram post ideas:\n{json.dumps(character_data, indent=2)}"

    # Call AI model
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a creative Instagram content strategist."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    ideas = generate_instagram_ideas()
    print(ideas)
