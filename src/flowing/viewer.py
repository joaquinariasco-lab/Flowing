from fastapi import FastAPI
from pathlib import Path
import json

app = FastAPI()

TRACE_DIR = Path("traces")

def load_traces():
    traces = {}
    for file in TRACE_DIR.glob("*.json"):
        with open(file) as f:
            events = json.load(f)
            if events:
                trace_id = events[0]["trace_id"]
                traces[trace_id] = events
    return traces

@app.get("/traces")
def get_all_traces():
    return load_traces()

@app.get("/traces/{trace_id}")
def get_trace(trace_id: str):
    file = TRACE_DIR / f"{trace_id}.json"
    if not file.exists():
        return {"error": "Trace not found"}
    with open(file) as f:
        return json.load(f)
