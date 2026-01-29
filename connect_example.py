# connect_example.py
"""
A minimal interoperability simulation between two ExampleAgent instances.
This script imports example_agent.py, creates two agents, and has them
send messages to each other, printing the messages to the console.
"""

from example_agent import ExampleAgent

# Create two test agents
agent1 = ExampleAgent("Agent1")
agent2 = ExampleAgent("Agent2")

# Simulate sending messages between the agents
print("=== Starting minimal interoperability simulation ===\n")

# Agent1 sends a message to Agent2
agent1.send_message(agent2, "Hello Agent2! This is Agent1.")

# Agent2 sends a reply to Agent1
agent2.send_message(agent1, "Hi Agent1! Agent2 here, nice to talk with you.")

# Additional exchange for demonstration
agent1.send_message(agent2, "How is your testing going?")
agent2.send_message(agent1, "Everything works fine. Messages are received correctly.")

print("\n=== Simulation finished ===")