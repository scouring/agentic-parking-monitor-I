def make_conclusion(stats, forecast=None):
    rate = stats["occupied"] / stats["total"]

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

    if forecast and forecast > stats["total"] * 0.95:
        conclusion["alert"] = "High demand expected next hour"

    return conclusion