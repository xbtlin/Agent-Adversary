# 🛡️ Agent-Adversary: The Enterprise Red-Teaming Platform for Agentic AI

**Automated Stress-Testing, Reliability Benchmarking, and Reasoning X-Ray for the Agent Era.**

[![Star Potential](https://img.shields.io/badge/Star--Potential-1k%2B-gold?style=for-the-badge&logo=github)](https://github.com/eric-spaceship/agent-adversary)
[![Phase](https://img.shields.io/badge/Phase-10--Enterprise-blueviolet?style=for-the-badge)](https://github.com/eric-spaceship/agent-adversary)
[![Testing](https://img.shields.io/badge/Tests-33%2F33--Passing-success?style=for-the-badge)](tests/)

> "As Agents move from assistants to autonomous workers, their reliability and auditability are no longer options—they are requirements."

`Agent-Adversary` is a specialized platform designed to probe, stress-test, and benchmark the resilience of Agentic AI systems (like Claude Code, OpenClaw, and custom enterprise agents). By simulating advanced multi-turn adversarial attacks, it helps developers identify logic loops, context erasure vulnerabilities, and prompt injections before they reach production.

## 🚀 Key Features

- **🔬 Reasoning X-Ray (D3.js)**: Visualize the agent's thought process as a hierarchical decision tree. Spot exactly where the model deviates from its system constraints.
- **🌡️ Vulnerability Heatmaps**: Automatically map attack success rates back to specific segments of your system prompt.
- **🤺 Battle Royale Mode**: Configure "Agent-vs-Agent" scenarios where a specialized red-team agent attempts to autonomously exploit a target agent.
- **🛡️ Enterprise Governance**: HMAC-SHA256 signed task payloads and an immutable, append-only audit trail for compliant security operations.
- **🌐 Distributed Hub & Workers**: Scale your red-teaming audits across multiple nodes with real-time WebSocket telemetry.
- **🤖 LLM-as-a-Judge**: Objective, multi-model consensus scoring of agent resilience with automated **Mitigation Advice**.
- **🔌 Universal Connectors**: Native support for **Shell**, **Browser (Playwright)**, **Docker Sandboxes**, and **Claude Code / OpenClaw / OpenAI Assistants**.

## 🛠️ Architecture

![Architecture](assets/architecture.svg)

## 📦 Installation & Quick Start

```bash
# Install the framework
pip install agent-adversary

# List all available logic traps and jailbreaks
agent-adversary list

# Run a secure benchmark against a local CLI agent
agent-adversary bench --agent "openclaw turn" --scenario logic-trap-01 --telemetry

# Start the X-Ray Dashboard
agent-adversary dashboard --port 8000
```

## 📈 Compliance & Reporting

The platform generates audit-ready attestation reports. Use the `/compliance/report` endpoint to export verified resilience data for AI safety certifications.

---
*Created by Eric & Spaceship. Built for the era of autonomous agents.*
