def count_occupancy(detections):

    occupied = 0
    empty = 0

    for d in detections:

        if d["class"] == 1:
            occupied += 1
        else:
            empty += 1

    return {
        "occupied": occupied,
        "empty": empty,
        "total": occupied + empty
    }