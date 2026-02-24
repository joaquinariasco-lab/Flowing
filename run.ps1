.\venv\Scripts\Activate.ps1
cd examples

Start-Process python agent_server.py
Start-Process python my_agent_server.py

Write-Host "✅ Agents running on ports 5000 and 5001."
