# Agent-Adversary: Phase 6 - Multi-Modal & Adaptive Exploitation

## Goals
Expand red-teaming capabilities to Multi-Modal models (VLMs) and implement adaptive, multi-step evasion techniques.

## Planned Features
1. **Multi-Modal Connector (VLM)**: Support for agents that process images and documents (PDFs, Charts).
2. **Multi-Modal Exploit Library**: Initial set of scenarios for Visual Prompt Injection (e.g., adversarial patches in images).
3. **Adaptive Attack Orchestrator**: A high-level controller that uses `RedTeamAgent` to modify prompts in real-time based on the target agent's specific rejection messages.
4. **Professional Report Exporter (PDF/HTML)**: Generate polished, branded reports for enterprise security audits.
5. **Scenario Plugin System**: Dynamic loading of external YAML/JSON scenario libraries from a `plugins/` directory.

## Timeline
- **Hour 41-43**: Multi-Modal scaffolding and VLM support.
- **Hour 44-46**: Adaptive Attack logic and Feedback loops.
- **Hour 47+**: Reporting and Plugin system.
