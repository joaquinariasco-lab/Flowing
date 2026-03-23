import streamlit as st
import json
import time
from datetime import datetime
from random import choice, randint

st.title("Flowing Agent Activity")

# Autorefresh (optional)
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=2000, key="flowing_refresh")
except Exception:
    st.warning("streamlit_autorefresh not installed — auto-refresh disabled")

# Load events
events = []

try:
    with open("trace_log.json") as f:
        for line in f:
            events.append(json.loads(line))
except FileNotFoundError:
    st.info("No trace_log.json found — showing demo events")
    agents = ["Agent_A", "Agent_B"]
    steps = ["Step 1", "Step 2", "Step 3"]
    for i in range(10):
        events.append({
            "agent": choice(agents),
            "step": choice(steps),
            "details": f"Demo output {i+1}",
            "timestamp": time.time() - randint(0, 600)
        })
except Exception as e:
    st.error(f"Error loading events: {e}")

# Display events in a table
if events:
    for e in events:
        st.write(
            e.get("agent", "?"),
            e.get("step", "?"),
            e.get("details", "?"),
            datetime.fromtimestamp(e.get("timestamp", time.time())).strftime("%Y-%m-%d %H:%M:%S")
        )
else:
    st.warning("No events to display")
