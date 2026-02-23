# OpenClaw Integration Template for Agent-Adversary

## Overview
This template allows you to benchmark your OpenClaw-based agent using the `agent-adversary` framework.

## Setup
1. Ensure `openclaw` and `agent-adversary` are installed.
2. Define your target agent in `openclaw` (e.g., as a custom skill or a standalone CLI).

## Running the Benchmark

```bash
# Using the Shell Connector to test an OpenClaw session
agent-adversary bench \
  --connector shell \
  --agent "openclaw turn --session my-agent-session" \
  --scenario all \
  --telemetry
```

## Advanced: Monitoring via Prometheus
Add the `--export metrics.prom` flag to your run to generate Grafana-ready telemetry data for your OpenClaw agent.
