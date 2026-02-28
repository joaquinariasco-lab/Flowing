from flowing.observability.tracer import Tracer

tracer = Tracer()

# Planner agent
with tracer.decision_span("planner") as span:
    span.record_prompt("Decide what to research")
    span.record_model("gpt-4", 0.2)
    span.record_output("Research quantum networking")

# Executor agent
with tracer.decision_span("executor", parent_id=tracer.events[0].decision_id) as span:
    span.record_prompt("Search for quantum networking papers")
    span.record_model("gpt-4", 0.2)
    span.record_output("Found 3 relevant papers")

tracer.export_json("trace.json")

print("Trace exported correctly")
