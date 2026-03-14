from flowing import trace_agent
from tracer import trace_event
from flask import Flask, request
from my_agent import MyAgent
from flowing.observability.tracer import Tracer
from flowing.decision.event import DecisionEvent
import time

# Initialize agent and tracer
agent = MyAgent("AgentX")  # Change name if another dev clones
tracer = Tracer()
app = Flask(__name__)

@app.route("/identity", methods=["GET"])
def identity():
    return {
        "name": agent.name,
        "framework": "custom",
        "capabilities": ["example-task"],
        "accepts_tasks": True,
        "pricing_model": "fixed",
        "version": "0.1"
    }

@app.route("/message", methods=["POST"])
def message():
    data = request.json
    prompt = data.get("prompt")

    # Run agent logic
    start_time = time.time()
    response = agent.on_task(prompt, price=None) if hasattr(agent, "on_task") else f"Received: {prompt}"
    duration = time.time() - start_time

    # Log decision
    event = DecisionEvent(
        agent_id=agent.name,
        prompt=prompt,
        model="demo-model",
        temperature=0.0,
        output=response
    )
    tracer.record(event)

    return {"response": response, "duration_seconds": duration}

@app.route("/receive_message", methods=["POST"])
def receive_message():
    data = request.json
    agent.on_message(data.get("message"))
    return {"status": "ok"}

trace_event("AgentX", "received_message", {"info": "message received"})

@app.route("/run_task", methods=["POST"])
def run_task():
    data = request.json
    return execute_task(data.get("description"), data.get("price"))

# ✅ Properly defined execute_task with tracing
@trace_agent
def execute_task(task, price=None):
    start_time = time.time()
    response = agent.on_task(task, price=price) if hasattr(agent, "on_task") else f"Executed: {task}"
    duration = time.time() - start_time

    # Record in tracer
    event = DecisionEvent(
        agent_id=agent.name,
        prompt=task,
        model="demo-model",
        temperature=0.0,
        output=response
    )
    tracer.record(event)

    return {"response": response, "duration_seconds": duration}

if __name__ == "__main__":
    app.run(port=5001)
