![Flowing UI](assets/Flowing_logo.png)


# Flowing: The Debugger for AI Agents Workflow.
### Instantly trace, record, and audit every decision in your multi-agent workflow.
### Stop guessing why your agents fail. Flowing provides a "Source of Truth" for complex AI interactions.

---

## ⚡ 10-Second Quick Start
### Run this in your terminal to launch the full Observability Dashboard and a live Agentic Demo:

```bash
python3 -m venv flowing-env && source flowing-env/bin/activate && pip install flowing-os && flowing demo
```

---

## 🎯 Why this matters
Multi-agent systems are complex:
- Agents plan, reason, call tools, and coordinate asynchronously.
- Silent errors and emergent behavior are common.
- Traditional logs and simple prints don’t provide enough insight.
Flowing captures rich execution data structured logs, spans, traces, and interaction graphs to help you see what’s happening and why.


---

## ⚡What you can do with it
With Flowing’s current MVP you can:
- Run multiple independent agents and record execution traces
- Capture structured events for agent actions and tool invocations
- Reconstruct cross-agent workflows
- Generate interactive trace visualizations
- Improve debugging and reproducibility of complex runs

---

## 🧠 What This Repo Includes
- Structured trace capture and logging utilities
- Execution span schema for multi-agent workflows
- Scripts to run demos and visualize behavior
- Base interfaces that emit telemetry

---

## 🚧 Current Status
This project is experimental but functional:

✔ Structured logging and trace capture

✔ Execution spans for agent actions

✔ Interactive trace visualization output

❌ Universal cross-framework interoperability (future work)

❌ Production dashboard or hosted API

---

## 📈 Roadmap
Planned improvements include:
- Enhanced visual dashboards for traces
- Standardized trace schema
- Replay mode for debugging workflows
- Plugins for external observability systems (e.g., OpenTelemetry)
- Enterprise features (enterprise API, alerting, retention)

--- 

## 🤝 Contributing
This repo is for developers building, debugging, or improving multi-agent AI workflows. If you care about:
- Agent execution visibility
- Reproducible runs
- Structured trace semantics
- Better debugging outcomes

…then this project is for you. Pull requests and feedback welcome.
