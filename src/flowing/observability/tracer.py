from typing import List
from flowing.decision.event import DecisionEvent
from flowing.decision.span import DecisionSpan


class Tracer:
    def __init__(self):
        self.events: List[DecisionEvent] = []

    def decision_span(self, agent_id: str, parent_id=None):
        return DecisionSpan(self, agent_id, parent_id)

    def record(self, event: DecisionEvent):
        self.events.append(event)

    def export(self):
        return [event.__dict__ for event in self.events]
