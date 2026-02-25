# Contributing to Agent-Adversary

Thank you for your interest in improving Agent-Adversary! We welcome contributions from safety researchers, developers, and security enthusiasts.

## How to Contribute

### 1. Adding New Scenarios
We are always looking for novel jailbreaks and logic traps.
- Scenarios are located in `agent_adversary/adversary/jailbreak/library.py`.
- Please ensure your scenario has a clear `expected_failure_modes` list for the judge model.

### 2. Developing Connectors
If you use an Agent framework not yet supported (e.g., LangGraph, CrewAI), consider building a connector.
- Inherit from `BaseConnector` in `agent_adversary/connectors/base.py`.

### 3. Reporting Bugs
Please use the GitHub Issues tracker to report bugs. Include:
- Your environment details (captured via `agent-adversary --fingerprint`).
- The specific scenario and agent command that triggered the issue.

## Code Standards
- Use `pytest` for all logic changes.
- Ensure all tests pass (`PYTHONPATH=. pytest tests/`) before submitting a PR.
- Follow PEP 8 for Python code style.

## Security Researchers
If you find a vulnerability in the Agent-Adversary framework itself, please refer to our [Security Policy](SECURITY.md).
