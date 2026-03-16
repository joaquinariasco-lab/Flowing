import subprocess
import sys
import time
import webbrowser
import requests


def demo():
    print("Starting Flowing demo...\n")

    # Start agents
    agent1 = subprocess.Popen([sys.executable, "agents/agent_server.py"])
    agent2 = subprocess.Popen([sys.executable, "agents/my_agent_server.py"])

    time.sleep(2)

    url = "http://localhost:8501"

    print("Agents running:")
    print("AgentA → http://localhost:5000")
    print("AgentX → http://localhost:5001\n")

    print("Dashboard:")
    print(url)

    webbrowser.open(url)

    # Start dashboard
    subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "examples/dashboard.py"]
    )

    # Send demo task
    time.sleep(3)

    try:
        requests.post("http://localhost:5000/message", json={"task": "Build a calculator"})
        print("\nDemo task sent.")
    except:
        pass

    # keep program alive
    while True:
        time.sleep(60)


def main():
    if len(sys.argv) < 2:
        print("Usage: flowing demo")
        return

    cmd = sys.argv[1]

    if cmd == "demo":
        demo()
    else:
        print(f"Unknown command: {cmd}")
