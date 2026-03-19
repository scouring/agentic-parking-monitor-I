from dotenv import load_dotenv
import os
from openai import OpenAI
import json

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def run_agent(stats): 
    prompt = f"""
    You are an AI parking operations assistant.

    Parking data:
    {json.dumps(stats)}

    Your job:
    - Analyze occupancy
    - Decide what action to take
    - Provide a short message for users

    Respond in JSON:
    {{
      "decision": "...",
      "message": "...",
      "action": "alert | ok | recommend"
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful parking assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "message": response.choices[0].message.content
    }