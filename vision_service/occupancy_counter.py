def count_occupancy(detections):

    occupied = 0
    available= 0

    for d in detections:

        if d["class"] == 1:
            occupied += 1
        else:
            available+= 1

    return {
        "occupied": occupied,
        "available": available,
        "total": occupied + available
    }