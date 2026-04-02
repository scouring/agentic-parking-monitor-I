import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("data_log.jsonl")

def log_stats(stats):

    entry = {
        "timestamp": datetime.now().isoformat(),
        "total": stats["total"],
        "occupied": stats["occupied"],
        "empty": stats["empty"],
        "rate": stats["occupied"] / stats["total"]
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry)+"\n")