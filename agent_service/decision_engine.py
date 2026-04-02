def make_conclusion(stats, forecast=None):
    rate = stats["occupied"] / stats["total"]

    forecast_rate = None

    if forecast:
        forecast_rate = forecast / stats["total"]

    conclusion = {
        "occupancy_rate": rate,
        "pricing": "maintain",
        "traffic": "normal",
        "alert": None
    }

    if rate > 0.9:
        conclusion["pricing"] = "increase_15%"
        conclusion["traffic"] = "redirect"
        conclusion["alert"] = "Lot nearly full"

    elif rate < 0.5:
        conclusion["pricing"] = "decrease_10%"

    if forecast_rate and forecast_rate > 0.95:
        conclusion["alert"] = "High demand expected next hour"
        conclusion["pricing"] = "increase_15%"

    return conclusion