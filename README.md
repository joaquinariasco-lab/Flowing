![Flowing UI](assets/Flowing_logo.png)

---

# Flowing
### Reproducibility and traceability of LLM decisions in multi-agent workflows in Python

Flowing is designed for developers building multi-agent LLM systems who need to **understand, reproduce, and debug exactly why the system made each decision**.  

This is not generic observability, monitoring, or general-purpose AI tooling.  
Flowing focuses solely on **capturing every agent decision, its inputs, outputs, and parent-child relationships**, enabling full step-by-step reconstruction of any workflow execution.

If you work with multiple LLM agents and **cannot reproduce or explain why a certain outcome was reached**, Flowing provides the tools to:

- Record every decision from each agent
- Connect parent and child decisions
- Store prompts, outputs, context, and relevant metadata
- Export reproducible traces for analysis and debugging

---

## 🎯 Why This Matters
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

## 🚀 30-Second Quick Start

### Mac / Linux:
Open the terminal and paste:
```bash
git clone https://github.com/joaquinariasco-lab/Flowing.git && cd Flowing && chmod +x install.sh run.sh && ./install.sh
```

Result:

![Linux result](assets/linux.jpg)

### Window:
#### With git already installed:
Open PowerShell and paste:
```bash
git clone https://github.com/joaquinariasco-lab/Flowing.git; cd Flowing; ./install.ps1
```
#### Without git already installed:
##### 1- Download the repository ZIP: "https://github.com/joaquinariasco-lab/Flowing/archive/refs/heads/main.zip"
##### 2- Extract it to a folder, e.g., C:\Users\YourName\Flowing
##### 3- Open PowerShell in the main folder (Shift + Right Click → “Open PowerShell window here”)
##### 4- Allow running scripts (only needed the first time):
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
##### 5- Unblock the files:
```bash
Unblock-File .\install.ps1
```
```bash
Unblock-File .\run.ps1
```
##### 6- Execute the demo:
```bash
./install.ps1
```

Here’s a quick demonstration of the agents interacting:

![Agent Interaction Demo](assets/Animation.gif)

---

## 📋 Demo Steps

This flowchart shows the steps when running the demo:

```mermaid
flowchart LR
    User -->|Open Terminal| Terminal
    Terminal -->|Run install.ps1 / run.sh| VirtualEnv
    VirtualEnv --> AgentA
    VirtualEnv --> AgentX
    AgentA -->|Send Test Message| AgentX
    AgentX -->|Print Message & Execute Task| Terminal
```

## 🔄 Agent Interaction Example

```mermaid
sequenceDiagram
    participant A as AgentA
    participant X as AgentX

    A->>X: {"message": "Hello from AgentA"}
    X-->>A: {"status": "ok"}
    A->>X: {"description": "Test task", "price": 10}
    X-->>A: {"balance": 10}
```

---

## 🏗️ Architecture

This diagram shows how AgentA and AgentX communicate:

```mermaid
flowchart TD
    Repo[Flowing Repo] --> AgentA
    Repo --> AgentX
    AgentA -->|send message| AgentX
    AgentX -->|respond| AgentA
    AgentA -->|run task| AgentX
    AgentX -->|update balance| AgentA
```

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
