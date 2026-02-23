import json
from typing import List, Dict, Any
from .telemetry import TelemetryEvent

class PrometheusExporter:
    """
    Converts TelemetryEvents into Prometheus-compatible metrics format.
    Focuses on counters for attack types and gauges for resource usage.
    """
    
    @staticmethod
    def export_metrics(events: List[TelemetryEvent]) -> str:
        metrics = []
        
        # 1. Total Scenarios Run
        scenario_starts = [e for e in events if e.event_type == "scenario_start"]
        metrics.append(f"# HELP agent_adversary_scenarios_total Total number of adversarial scenarios started.")
        metrics.append(f"# TYPE agent_adversary_scenarios_total counter")
        metrics.append(f"agent_adversary_scenarios_total {len(scenario_starts)}")

        # 2. Failure Modes Detected
        eval_completes = [e for e in events if e.event_type == "evaluation_complete"]
        failure_counts = {}
        for ev in eval_completes:
            failures = ev.data.get("failure_modes_detected", [])
            for f in failures:
                failure_counts[f] = failure_counts.get(f, 0) + 1
        
        metrics.append(f"# HELP agent_adversary_failures_total Total number of specific failure modes detected.")
        metrics.append(f"# TYPE agent_adversary_failures_total counter")
        for mode, count in failure_counts.items():
            metrics.append(f'agent_adversary_failures_total{{mode="{mode}"}} {count}')

        # 3. Resilience Scores (Gauge)
        metrics.append(f"# HELP agent_adversary_resilience_score Current resilience score from the last evaluation.")
        metrics.append(f"# TYPE agent_adversary_resilience_score gauge")
        if eval_completes:
            last_score = eval_completes[-1].data.get("total_resilience", 0)
            metrics.append(f"agent_adversary_resilience_score {last_score}")

        return "\n".join(metrics)

class GrafanaDashboardGenerator:
    """
    Generates JSON configuration for a Grafana dashboard optimized for Agent-Adversary.
    """
    @staticmethod
    def generate_json() -> Dict[str, Any]:
        # Minimalist mock of a Grafana dashboard JSON
        return {
            "title": "Agent Resilience Dashboard",
            "panels": [
                {"title": "Resilience Over Time", "type": "timeseries"},
                {"title": "Common Failure Modes", "type": "piechart"}
            ],
            "templating": {"list": [{"name": "agent_id"}]}
        }
