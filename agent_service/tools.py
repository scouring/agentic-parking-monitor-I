def calculate_occupancy_rate(stats):
    return stats["occupied"] / stats["total"]


def pricing_recommendation(rate, forecast_rate=None):

    if forecast_rate is None:
        forecast_rate = rate

    if rate > 0.9 or forecast_rate > 0.95:
        return {"action": "increase_price", "amount": 0.15}
    
    elif rate < 0.5 and forecast_rate < 0.6:
        return {"action": "decrease_price", "amount": 0.10}
    
    else:
        return {"action": "maintain_price", "amount": 0.0}


def traffic_recommendation(rate):

    if rate > 0.9:
        return "Redirect drivers to nearby lots"
    
    return "No redirection needed"