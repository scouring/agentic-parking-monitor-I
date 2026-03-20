import json
from datetime import datetime

def log_stats(stats):
    with open("data_log.json", "a") as f:
        entry = {
            "timestamp": str(datetime.now()),
            **stats
        }
        f.write(json.dumps(entry) + "\n")