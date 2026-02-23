# Claude Code Integration Template for Agent-Adversary

## Overview
Automate security and reliability testing for agents built with Anthropic's Claude Code.

## Setup
1. Install Claude Code: `npm install -g @anthropic-ai/claude-code`.
2. Configure your Claude API key.

## Benchmarking Claude Code

Since Claude Code is an interactive terminal agent, we use the `agent-adversary` Shell Connector.

```bash
agent-adversary bench \
  --connector shell \
  --agent "claude" \
  --scenario jailbreak-dan-01 \
  --patch
```

## Security Hardening
Enable the `--patch` flag to automatically generate system prompt overlays if Claude Code is successfully jailbroken during a test run.
