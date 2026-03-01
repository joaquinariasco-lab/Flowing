import json
import time
from datetime import datetime


def _format_timestamp(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def replay_trace(path, interactive=True, delay=0):
    """
    Replay a trace.json file step by step.

    Args:
        path (str): Path to trace.json
        interactive (bool): Wait for user input between steps
        delay (float): Automatic delay between steps (if not interactive)
    """

    with open(path, "r") as f:
        events = json.load(f)

    # Sort by timestamp
    events.sort(key=lambda e: e["timestamp"])

    print("\n=== FLOWING REPLAY MODE ===\n")

    for i, event in enumerate(events, 1):
        print(f"\nStep {i}")
        print("-" * 40)
        print(f"Agent:       {event['agent_id']}")
        print(f"Timestamp:   {_format_timestamp(event['timestamp'])}")
        print(f"Model:       {event.get('model')}")
        print(f"Temperature: {event.get('temperature')}")
        print(f"Parent ID:   {event.get('parent_id')}")
        print("\nPrompt:")
        print(event.get("prompt"))
        print("\nOutput:")
        print(event.get("output"))
        print("-" * 40)

        if interactive:
            input("Press Enter to continue...")
        elif delay > 0:
            time.sleep(delay)

    print("\n=== END OF TRACE ===\n")
