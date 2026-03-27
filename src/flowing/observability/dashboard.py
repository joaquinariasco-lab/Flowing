import streamlit as st
import json
import time
from datetime import datetime
from random import choice, randint

st.set_page_config(layout="wide")
st.title("Flowing Agent Activity")

# --- AUTO REFRESH ---
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=2000, key="flowing_refresh")
except Exception:
    st.warning("streamlit_autorefresh not installed — auto-refresh disabled")

# --- LOAD EVENTS ---
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
            "trace_id": "demo_trace",
            "span_id": str(i),
            "parent_span_id": str(i-1) if i > 0 else None,
            "agent": choice(agents),
            "type": choice(steps),
            "details": f"Demo output {i+1}",
            "timestamp": time.time() - randint(0, 600)
        })
except Exception as e:
    st.error(f"Error loading events: {e}")

# --- IF EMPTY ---
if not events:
    st.warning("No events to display")
    st.stop()

# --- GROUP BY TRACE ---
traces = {}
for e in events:
    trace_id = e.get("trace_id", "default_trace")
    traces.setdefault(trace_id, []).append(e)

# --- SELECT TRACE ---
trace_ids = list(traces.keys())
selected_trace = st.sidebar.selectbox("Select Trace", trace_ids)

trace_events = traces[selected_trace]

# --- BUILD TREE ---
spans = {
    e["span_id"]: {**e, "children": []}
    for e in trace_events if "span_id" in e
}

root_nodes = []

for span in spans.values():
    parent_id = span.get("parent_span_id")
    if parent_id and parent_id in spans:
        spans[parent_id]["children"].append(span)
    else:
        root_nodes.append(span)

# --- RENDER TREE ---
st.subheader(f"Trace: {selected_trace}")

def render_span(span, level=0):
    indent = "  " * level

    label = f"{indent}▶ {span.get('agent')} | {span.get('type')}"

    expanded = st.checkbox(label, key=span["span_id"])

    if expanded:
        st.json({
            "details": span.get("details"),
            "timestamp": datetime.fromtimestamp(
                span.get("timestamp", time.time())
            ).strftime("%Y-%m-%d %H:%M:%S"),
        })

    for child in span.get("children", []):
        render_span(child, level + 1)

for root in root_nodes:
    render_span(root)

# --- METRICS ---
st.sidebar.markdown("## Metrics")

agent_count = {}
for e in trace_events:
    agent = e.get("agent", "unknown")
    agent_count[agent] = agent_count.get(agent, 0) + 1

for agent, count in agent_count.items():
    st.sidebar.write(f"{agent}: {count}")
