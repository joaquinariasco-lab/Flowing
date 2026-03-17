import requests
import sys

task = sys.argv[1] if len(sys.argv) > 1 else "say hello"
response = requests.post("http://127.0.0.1:5001/message", json={"task": task})
print(response.json())

