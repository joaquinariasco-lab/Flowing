from economic_agent import EconomicAgent
from task import Task
from economic_engine import run_task

# automatic criterion
def always_success(result):
    return True

# agents
agentA = EconomicAgent("AgentA", balance=10)
agentB = EconomicAgent("AgentB", balance=0)

# economic task
task = Task(
    description="Fix a broken test",
    price=3,
    criteria=always_success
)

# ejecute simulation
run_task(agentA, agentB, task)
