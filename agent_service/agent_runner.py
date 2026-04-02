from dotenv import load_dotenv
import os
from openai import OpenAI

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

    forecast_rate = None
    if forecast:
        forecast_rate = forecast / stats["total"]
    pricing = pricing_recommendation(rate, forecast_rate)
    traffic = traffic_recommendation(rate)
    conclusion = make_conclusion(stats, forecast)

    structured_decision = {
        "occupancy_rate": rate,
        "forecast_occupancy": forecast,
        "pricing_action": pricing,
        "traffic_action": traffic
    }

    prompt = f"""
    You are an AI parking operations assistant.

    Parking data:
    {structured_decision}

    Explain the operational reasoning behind these decisions
    in simple language for a parking manager.

    Decision:
    {conclusion}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You manage parking operations."},
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "conclusion": conclusion,
        "decision": structured_decision,
        "message": response.choices[0].message.content
    }