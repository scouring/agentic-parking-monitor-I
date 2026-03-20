import json
from datetime import datetime
import pandas as pd
import streamlit as st
import os

def log_stats(stats):
    # Prepare the new entry
    entry = {
        "timestamp": datetime.now().isoformat(),  # ISO format is safer for JSON
        "occupied": stats["occupied"],
        "available": stats["available"],
        "rate": stats["occupied"] / stats["total"]
    }

    # Initialize session state df if somehow missing
    if "df" not in st.session_state:
        if os.path.exists("data_log.json"):
            st.session_state.df = pd.read_json("data_log.json", lines=True)
        else:
            st.session_state.df = pd.DataFrame(columns=["timestamp", "occupied", "available", "rate"])

    # Append new entry to session state df
    st.session_state.df = pd.concat(
        [st.session_state.df, pd.DataFrame([entry])],
        ignore_index=True
    )

    # Write entry to file (append)
    with open("data_log.json", "a") as f:
        f.write(json.dumps(entry) + "\n")

    return st.session_state.df