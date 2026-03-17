import sys
import json
from pathlib import Path

TRACE_DIR = Path("traces")


def show_trace(trace_id: str):
    file_path = TRACE_DIR / f"{trace_id}.json"

    if not file_path.exists():
        print(f"❌ Trace {trace_id} not found.")
        return

    with open(file_path) as f:
        events = json.load(f)

    # organize by timestamp
    events = sorted(events, key=lambda e: e["timestamp"])

    print(f"\n🔎 Trace ID: {trace_id}")
    print("=" * 60)

    for event in events:
        ts = event["timestamp"]
        agent = event["agent"]
        event_type = event["event_type"]
        payload = event.get("payload", {})

        print(f"\n[{ts:.4f}] {agent} → {event_type}")
        if payload:
            for k, v in payload.items():
                print(f"    {k}: {v}")

    print("\n✅ End of trace\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python show_trace.py <trace_id>")
        sys.exit(1)

    trace_id = sys.argv[1]
    show_trace(trace_id)
