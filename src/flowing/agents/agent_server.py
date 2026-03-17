from tracer import trace_event
from flask import Flask, request
from base_agent import BaseAgent
from flowing.observability.tracer import Tracer
import time

# Example reference implementation
class SimpleAgent(BaseAgent):
    def __init__(self, name, balance=0):
        super().__init__(name)
        self.balance = balance

    def on_message(self, message: str):
        print(f"[{self.name} received]: {message}")

    def on_task(self, description: str, price: float):
        self.balance += price
        print(f"[{self.name}] completed task: {description}")
        print(f"[{self.name}] earned {price}, balance = {self.balance}")
        return {"status": "done", "balance": self.balance}


agent = SimpleAgent("AgentA", balance=10)
app = Flask(__name__)

@app.route("/receive_message", methods=["POST"])
def receive_message():
    data = request.json
    trace_id = data.get("trace_id")
    tracer = Tracer(trace_id=trace_id)
    start_time = time.time()
    tracer.log(agent.name, "message_received", {
        "from": data.get("sender"),
        "message": data.get("message")
    })
    agent.on_message(data.get("message"))
    duration = time.time() - start_time
    tracer.log(agent.name, "message_processed", {
        "duration_seconds": duration
    })
    tracer.flush()
    return {"status": "ok"}

trace_event("AgentA", "received_message", {"info": "message received"})

@app.route("/run_task", methods=["POST"])
def run_task():
    data = request.json
    trace_id = data.get("trace_id")
    tracer = Tracer(trace_id=trace_id)
    start_time = time.time()
    tracer.log(agent.name, "task_received", {
        "from": data.get("sender"),
        "description": data.get("description"),
        "price": data.get("price")
    })
    result = agent.on_task(
        data.get("description"),
        data.get("price")
    )
    duration = time.time() - start_time
    tracer.log(agent.name, "task_completed", {
        "result": result,
        "duration_seconds": duration
    })
    tracer.flush()
    return result

@app.route("/message", methods=["POST"])
def message():
    data = request.json
    prompt = data.get("prompt")

    # Call your agent logic (replace with actual handling if you have it)
    response = agent.on_task(prompt, price=None) if hasattr(agent, "on_task") else f"Received: {prompt}"

    # Log the decision in the tracer
    if 'tracer' in globals() and hasattr(tracer, "record"):
        from flowing.decision.event import DecisionEvent
        event = DecisionEvent(
            agent_id=agent.name,
            prompt=prompt,
            model="demo-model",
            temperature=0.0,
            output=response
        )
        tracer.record(event)

    return {"response": response}

if __name__ == "__main__":
    app.run(port=5000)

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
