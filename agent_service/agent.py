from dotenv import load_dotenv
import os
from openai import OpenAI
import json
from agent_service.tools import (
    calculate_occupancy_rate,
    pricing_recommendation,
    traffic_recommendation
)


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def run_agent(stats): 
    rate = calculate_occupancy_rate(stats)

    pricing = pricing_recommendation(rate)
    traffic = traffic_recommendation(rate)

    structured_decision = {
        "occupancy_rate": rate,
        "pricing_action": pricing,
        "traffic_action": traffic
    }

    prompt = f"""
    You are an operations AI for parking management.

    Data:
    {structured_decision}

    Explain the reasoning behind these decisions in a concise, business-friendly way.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a business operations assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "decision": structured_decision,
        "message": response.choices[0].message.content
    }