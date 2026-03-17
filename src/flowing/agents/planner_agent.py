from flowing import trace_agent
from coder_agent import coder_agent

@trace_agent
def planner_agent(task):
    plan = f"Plan for: {task}"
    return coder_agent(plan)
