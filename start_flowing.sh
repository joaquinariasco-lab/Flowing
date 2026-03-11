#!/bin/bash

echo "🚀 Starting Flowing MVP..."

# 1️⃣ Kill any processes using ports 5000, 5001, or 8502 (dashboard)
for port in 5000 5001 8502; do
    pids=$(lsof -t -i :$port)
    if [ -n "$pids" ]; then
        echo "Killing processes on port $port: $pids"
        kill -9 $pids
    fi
done

# 2️⃣ Remove old traces/logs
rm -f trace_log.json trace.json dashboard.log

# 3️⃣ Start AgentA and AgentX
echo "Starting AgentA on port 5000..."
PYTHONPATH=src venv/bin/python3 examples/agent_server.py &

echo "Starting AgentX on port 5001..."
PYTHONPATH=src venv/bin/python3 examples/my_agent_server.py &

# 4️⃣ Give agents time to start
sleep 2

# 5️⃣ Send test message
echo "Sending test message..."
# (Mantener la línea original de test message, si la tienes)

# 6️⃣ Start Streamlit dashboard in background (headless)
echo "📊 Starting Streamlit dashboard..."
nohup venv/bin/streamlit run dashboard.py --server.headless true --server.port 8502 > dashboard.log 2>&1 &
echo "✅ Flowing started! Dashboard should be running at http://localhost:8502"
