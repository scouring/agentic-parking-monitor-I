def decide_parking_action(stats):

    total = stats["total"]
    occupied = stats["occupied"]

    if total == 0:
        return "No parking spaces detected"
    
    rate = occupied / total

    if rate > 0.9:
        action = "Parking lot FULL alert"

    elif rate > 0.75:
        action = "Parking lot nearly full"

    elif rate > 0.4:
        action = "Parking lot moderately occupied"

    else:
        action = "Parking mostly available"

    return action
    