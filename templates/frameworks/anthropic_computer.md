# Anthropic Computer Use Integration Template

## Overview
Test agents that utilize Anthropic's "Computer Use" capabilities, such as automated browser navigation or local environment manipulation.

## Setup
1. Ensure your agent is configured to use the `computer` tool.
2. Obtain an Anthropic API Key with Computer Use beta access.

## Benchmarking

```bash
# Using the API Connector for Anthropic Computer Use
agent-adversary bench \
  --connector api-anthropic-computer \
  --scenario vlm-injection-01 \
  --telemetry
```

## Scenarios
- **Visual Injections**: Test if hidden text in screenshots can hijack the agent's task.
- **Tool-Loop Paradoxes**: Test if conflicting environmental states cause the agent to enter a loop.
