import pandas as pd
from pathlib import Path

LOG_FILE = Path("data_log.jsonl")

def forecast_next_hour():

    if not LOG_FILE.exists():
        return 0
    
    df = pd.read_json(LOG_FILE, lines=True)

    if len(df) < 10:
        return int(df["occupied"].iloc[-1])
    
    return int(df["occupied"].tail(10).mean())