# 🛡️ Agent-Adversary

[![GitHub License](https://img.shields.io/github/license/xbtlin/Agent-Adversary?style=flat-square)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/xbtlin/Agent-Adversary?style=flat-square)](https://github.com/xbtlin/Agent-Adversary/stargazers)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-production--ready-green?style=flat-square)](https://github.com/xbtlin/Agent-Adversary)

**Forge more reliable AI Agents through rigorous adversarial testing, real-time X-Ray diagnostics, and automated governance.**

Agent-Adversary is an enterprise-grade red-teaming framework designed specifically for the Agentic AI era. While traditional LLM benchmarks focus on static knowledge, Agent-Adversary probes the **dynamic logic, tool-calling safety, and multi-modal resilience** of your agents.

---

## 🌟 Why Agent-Adversary?

As AI move from "chatbots" to "agents" with system access, the attack surface expands exponentially. Agent-Adversary provides the "X-Ray" vision needed to secure these workflows.

- **🔍 Reasoning X-Ray**: Visualize agent decision trees using D3.js to pinpoint exactly where logic fails under pressure.
- **🖼️ Multi-Modal Exploits**: First-of-its-kind support for testing Vision-Language Models (VLM) against OCR injection and visual jailbreaks.
- **🐝 Swarm Resilience**: Stress-test multi-agent systems against Byzantine failures and cross-agent prompt pollution.
- **🛡️ Live Patching**: Automatically generate and apply prompt-level hotfixes to mitigate detected vulnerabilities in real-time.
- **🌐 Distributed Hub**: Orchestrate massive red-teaming campaigns across a global fleet of workers with HMAC-signed integrity.

---

## 🛠️ Architecture

![Architecture](assets/architecture.svg)

Agent-Adversary operates as a closed-loop security system:
1. **Connect**: Link via Shell, Browser (Playwright), Docker, or Cloud APIs.
2. **Attack**: Execute evolved payloads (Jailbreak, Logic Traps, Multi-modal).
3. **Observe**: Capture sub-millisecond telemetry and reasoning traces.
4. **Audit**: Generate executive-ready HTML security attestation reports.

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/xbtlin/Agent-Adversary.git
cd Agent-Adversary
pip install -e .
```

### Run your first Benchmark

```bash
# Test a local shell-based agent against all logic traps
adversary bench --connector shell --agent "./my_agent.sh" --scenario all
```

### Start the X-Ray Dashboard

```bash
adversary dashboard
```
*Access the interactive visualization at `http://localhost:8000`*

---

## 📊 Key Features

### 1. Advanced Diagnostics (X-Ray)
Identify "Reasoning Spikes" and "Logic Loops" before they hit production. Our D3-powered engine renders the agent's internal thought process as an interactive graph.

### 2. Enterprise Governance
- **Immutable Audit Trail**: Append-only logs for every attack and system modification.
- **Consensus Judging**: Utilizes a panel of diverse LLMs (GPT-4o, Claude 3.5) to reach an objective safety verdict.
- **Compliance Ready**: Generate reports that align with emerging AI safety standards.

### 3. Adaptive Red-Teaming
The framework learns from the agent's failures. Using a genetic algorithm, it mutates payloads to bypass specific system instructions, simulating a persistent human adversary.

---

## 🤝 Contributing

We welcome safety researchers and developers! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ for a safer AI future.
</p>
