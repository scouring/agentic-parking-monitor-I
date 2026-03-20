import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import timedelta

def forecast_next_hour():
    df = pd.read_json("data_log.json", lines=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    if len(df) < 3:
        return None  # not enough data

    df["ts_numeric"] = df["timestamp"].astype(np.int64) // 10**9

    X = df["ts_numeric"].values.reshape(-1, 1)
    y = df["occupied"].values

    model = LinearRegression()
    model.fit(X, y)

    last_ts = df["timestamp"].iloc[-1]
    next_ts = last_ts + timedelta(hours=1)

    next_ts_num = np.array([[next_ts.value // 10**9]])
    prediction = model.predict(next_ts_num)[0]

    return max(0, int(prediction)), next_ts