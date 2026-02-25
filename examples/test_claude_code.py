import os
import json
from agent_adversary.adversary.logic.engine import AdversaryEngine
from agent_adversary.connectors.frameworks.native import OpenClawConnector
from agent_adversary.evaluator.judge import JudgeModel

def run_claude_style_benchmark():
    """
    Demonstrates how to test a high-capability agent using the Agent-Adversary framework.
    """
    print("🚀 Starting Claude-Style Resilience Benchmark...")
    
    # Initialize connector (Mocking OpenClaw as the target)
    connector = OpenClawConnector()
    judge = JudgeModel()
    engine = AdversaryEngine(connector, judge)
    
    # Target specific logic traps that challenge high-reasoning models
    scenarios = ["logic-trap-01", "indirect-injection-01"]
    
    results = []
    for sid in scenarios:
        print(f"\n[*] Probing Scenario: {sid}")
        result = engine.run_scenario_by_id(sid)
        results.append(result)
        print(f"[+] Result: Resilience Score {result.total_resilience:.2f}")

    print("\n✅ Benchmark Complete.")
    print("Exporting results to professional_report.html...")

if __name__ == "__main__":
    run_claude_style_benchmark()
