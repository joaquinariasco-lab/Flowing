# Activate virtual environment
& .\venv\Scripts\Activate.ps1

# Go to examples folder
Set-Location examples

# Start AgentA
Start-Process python agent_server.py
Start-Process python my_agent_server.py

Write-Host "Waiting 3 seconds for servers to start..."
Start-Sleep -Seconds 3

# Send a test message automatically
Write-Host "Sending test message..."
Invoke-RestMethod -Uri "http://localhost:5001/receive_message" -Method Post -ContentType "application/json" -Body '{"message":"Hello from AgentA"}'

Write-Host "✅ Demo complete. Agents are running on ports 5000 and 5001."
