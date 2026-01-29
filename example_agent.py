# example_agent.py
"""
A simple test agent class with methods to receive and send messages.
"""

class ExampleAgent:
    def __init__(self, name):
        """
        Initialize the agent with a name.
        """
        self.name = name

    def receive_message(self, message):
        """
        Receive a message and print it.

        Args:
            message (str): The message received by the agent.
        """
        print(f"[{self.name} received]: {message}")

    def send_message(self, target_agent, message):
        """
        Send a message to another agent.

        Args:
            target_agent (ExampleAgent): The agent to send the message to.
            message (str): The message to send.
        """
        print(f"[{self.name} sending to {target_agent.name}]: {message}")
        target_agent.receive_message(message)


# Example usage when running this script directly
if __name__ == "__main__":
    # Create two agents
    agent1 = ExampleAgent("Agent1")
    agent2 = ExampleAgent("Agent2")

    # Agent1 sends a message to Agent2
    agent1.send_message(agent2, "Hello, Agent2! How are you?")

    # Agent2 replies to Agent1
    agent2.send_message(agent1, "Hi Agent1! I'm fine, thank you!")