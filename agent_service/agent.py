from dotenv import load_dotenv
import os
from openai import OpenAI
import json
from agent_service.tools import (
    calculate_occupancy_rate,
    pricing_recommendation,
    traffic_recommendation
)
from agent_service.decision_engine import make_conclusion
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def run_agent(stats, forecast=None): 
    rate = calculate_occupancy_rate(stats)
    pricing = pricing_recommendation(rate)
    traffic = traffic_recommendation(rate)
    conclusion = make_conclusion(stats, forecast)

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
    Explain this parking decision clearly for a manager:

    {conclusion}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a business operations assistant."},
            {"role": "system", "content": "You are an operations assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "conclusion": conclusion,
        "decision": structured_decision,
        "message": response.choices[0].message.content
    }