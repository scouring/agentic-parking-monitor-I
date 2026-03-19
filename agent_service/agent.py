from agent_service.decision_engine import decide_parking_action

def run_agent(stats):
    if stats["total"] == 0:
        return {
            "occupancy_rate": 0,
            "decision": "no parking spaces detected"
        }

    decision = decide_parking_action(stats)

    return {
        "occupancy_rate": stats["occupied"] / stats["total"],
        "decision": decision
    }