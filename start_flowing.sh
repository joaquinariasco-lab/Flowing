#!/bin/bash

echo "🚀 Starting Flowing MVP..."

for port in 5000 5001; do
    pids=$(lsof -t -i :$port)
    if [ -n "$pids" ]; then
        echo "Killing processes on port $port: $pids"
        kill -9 $pids
    fi
done


rm -f trace_log.json trace.json

#
echo "Starting AgentA on port 5000..."
PYTHONPATH=src venv/bin/python3 examples/agent_server.py &

echo "Starting AgentX on port 5001..."
PYTHONPATH=src venv/bin/python3 examples/my_agent_server.py &

sleep 2

# 4️⃣ Test message
echo "Sending test message..."
curl -X POST http://localhost:5001/message \
  -H "Content-Type: application/json" \
  -d '{"message":"hello"}'


echo "📊 Starting Streamlit dashboard..."
if [ -f venv/bin/streamlit ]; then
    venv/bin/streamlit run dashboard.py &
else
    echo "⚠️ Streamlit not found, open manually: http://localhost:8501"
fi

echo "✅ Flowing started! Agents running and dashboard should be open."
