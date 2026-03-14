import time
import uuid


class Span:
    def __init__(self, agent_name, parent_id=None):
        self.trace_id = str(uuid.uuid4())
        self.span_id = str(uuid.uuid4())
        self.parent_id = parent_id
        self.agent_name = agent_name
        self.start_time = time.time()
        self.end_time = None
        self.input = None
        self.output = None
        self.error = None

    def finish(self):
        self.end_time = time.time()

    @property
    def latency(self):
        if self.end_time:
            return self.end_time - self.start_time
        return None

    def to_dict(self):
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_id": self.parent_id,
            "agent_name": self.agent_name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "latency": self.latency,
            "input": self.input,
            "output": self.output,
            "error": self.error,
        }
