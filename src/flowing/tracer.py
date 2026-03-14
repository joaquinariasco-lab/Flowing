import json
import threading
from pathlib import Path

TRACE_FILE = Path("trace.json")

_span_stack = threading.local()


def get_current_span():
    return getattr(_span_stack, "current", None)


def set_current_span(span):
    _span_stack.current = span


def record_span(span):
    data = []

    if TRACE_FILE.exists():
        with open(TRACE_FILE) as f:
            data = json.load(f)

    data.append(span.to_dict())

    with open(TRACE_FILE, "w") as f:
        json.dump(data, f, indent=2)
