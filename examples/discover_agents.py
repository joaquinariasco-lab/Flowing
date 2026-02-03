import json
import requests

with open("agents.json") as f:
    agents = json.load(f)

for name, url in agents.items():
    try:
        r = requests.get(f"{url}/identity", timeout=2)
        print(name, "→", r.json())
    except Exception as e:
        print(name, "unreachable")
