from typing import List, Dict, Any, Optional
import datetime
import uuid
from agent_adversary.adversary.schema import AdversarialScenario
from agent_adversary.adversary.jailbreak.library import ScenarioLibrary
from agent_adversary.evaluator.judge import JudgeModel, EvaluationResult
from agent_adversary.connectors.base import BaseConnector
from agent_adversary.observability.telemetry import TelemetryManager
from agent_adversary.observability.monitor import ResourceMonitor

class AdversaryEngine:
    def __init__(self, connector: BaseConnector, judge: JudgeModel, enable_telemetry: bool = True):
        self.connector = connector
        self.judge = judge
        self.library = ScenarioLibrary()
        self.library.load_defaults()
        self.enable_telemetry = enable_telemetry
        self.telemetry: Optional[TelemetryManager] = None
        self.monitor = ResourceMonitor()

    def run_scenario_by_id(self, scenario_id: str) -> EvaluationResult:
        """Executes a specific adversarial scenario against the connected agent."""
        scenario = self.library.get_scenario(scenario_id)
        if not scenario:
            raise ValueError(f"Scenario {scenario_id} not found.")

        session_id = str(uuid.uuid4())
        if self.enable_telemetry:
            self.telemetry = TelemetryManager(session_id)
            self.telemetry.log("scenario_start", {"id": scenario_id, "name": scenario.name})

        print(f"[*] Starting Scenario: {scenario.name} ({scenario_id})")
        self.connector.reset()
        
        # Start monitoring if it's a shell connector (we have a PID)
        # Note: In a real implementation, the connector would expose its target PID
        
        dialogue = []

        for prompt in scenario.prompts:
            if self.telemetry:
                self.telemetry.log("prompt_sent", {"content": prompt})
                
            print(f"    [>] Adversary: {prompt[:50]}...")
            agent_response = self.connector.send_message(prompt)
            print(f"    [<] Agent: {agent_response[:50]}...")
            
            if self.telemetry:
                self.telemetry.log("response_received", {"content": agent_response})
            
            dialogue.append({"role": "user", "content": prompt})
            dialogue.append({"role": "agent", "content": agent_response})

        print(f"[*] Evaluating results for {scenario_id}...")
        eval_result = self.judge.evaluate_dialogue(
            dialogue=dialogue,
            scenario_id=scenario_id,
            expected_failures=scenario.expected_failure_modes
        )
        
        if self.telemetry:
            self.telemetry.log("evaluation_complete", eval_result.model_dump())
        
        return eval_result

class BenchmarkReport:
    """Helper to format and export results."""
    @staticmethod
    def to_markdown(results: List[EvaluationResult]) -> str:
        md = f"# Agent Resilience Benchmark Report\n"
        md += f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        md += "| Scenario ID | Safety | Utility | Logic | Total Resilience |\n"
        md += "| :--- | :--- | :--- | :--- | :--- |\n"
        
        for r in results:
            md += f"| {r.scenario_id} | {r.safety_score:.2f} | {r.utility_score:.2f} | {r.logic_score:.2f} | **{r.total_resilience:.2f}** |\n"
        
        md += "\n## Detailed Findings\n"
        for r in results:
            md += f"### {r.scenario_id}\n"
            md += f"- **Score**: {r.total_resilience:.2f}\n"
            md += f"- **Failures Detected**: {', '.join(r.failure_modes_detected) if r.failure_modes_detected else 'None'}\n"
            md += f"- **Judge Reasoning**: {r.judge_reasoning}\n\n"
            
        return md
