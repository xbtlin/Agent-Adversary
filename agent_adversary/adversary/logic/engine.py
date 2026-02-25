from typing import List, Dict, Any, Optional
import datetime
import uuid
import json
import time
import os
import requests
from agent_adversary.adversary.schema import AdversarialScenario
from agent_adversary.adversary.jailbreak.library import ScenarioLibrary
from agent_adversary.evaluator.judge import JudgeModel, EvaluationResult
from agent_adversary.connectors.base import BaseConnector
from agent_adversary.observability.telemetry import TelemetryManager
from agent_adversary.observability.monitor import ResourceMonitor

import time

class AdversaryEngine:
    def __init__(self, connector: BaseConnector, judge: JudgeModel, enable_telemetry: bool = True, dashboard_url: Optional[str] = None):
        self.connector = connector
        self.judge = judge
        self.library = ScenarioLibrary()
        self.library.load_defaults()
        self.enable_telemetry = enable_telemetry
        self.telemetry: Optional[TelemetryManager] = None
        self.monitor = ResourceMonitor()
        self.dashboard_url = dashboard_url

    def _broadcast_telemetry(self, event_type: str, data: Dict[str, Any], session_id: Optional[str] = None):
        """Sends event to the real-time dashboard API."""
        if not self.dashboard_url:
            return
        try:
            payload = {
                "event_type": event_type, 
                "data": data, 
                "session_id": session_id or (self.telemetry.session_id if self.telemetry else None),
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
            requests.post(f"{self.dashboard_url}/telemetry/event", json=payload, timeout=1)
        except:
            pass # Silently fail if dashboard is offline

    def run_scenario_by_id(self, scenario_id: str, interactive: bool = False) -> EvaluationResult:
        """Executes a specific adversarial scenario against the connected agent."""
        scenario = self.library.get_scenario(scenario_id)
        if not scenario:
            raise ValueError(f"Scenario {scenario_id} not found.")

        session_id = str(uuid.uuid4())
        if self.enable_telemetry:
            self.telemetry = TelemetryManager(session_id)
            self.telemetry.log("scenario_start", {"id": scenario_id, "name": scenario.name})
            self._broadcast_telemetry("scenario_start", {"id": scenario_id, "name": scenario.name}, session_id=session_id)

        print(f"[*] Starting Scenario: {scenario.name} ({scenario_id})")
        if interactive:
            print("[!] Interactive Mode Enabled. Waiting for 'next' signal via API/Dashboard...")
        
        self.connector.reset()
        dialogue = []

        for turn, prompt in enumerate(scenario.prompts):
            if interactive:
                prompt = self._wait_for_stepper(session_id, turn, prompt)
            
            if self.telemetry:
                self.telemetry.log("prompt_sent", {"content": prompt})
                self._broadcast_telemetry("prompt_sent", {"content": prompt}, session_id=session_id)
                
            print(f"    [>] Adversary: {prompt[:50]}...")
            agent_response = self.connector.send_message(prompt)
            print(f"    [<] Agent: {agent_response[:50]}...")
            
            if self.telemetry:
                self.telemetry.log("response_received", {"content": agent_response})
                self._broadcast_telemetry("response_received", {"content": agent_response}, session_id=session_id)
            
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
            self._broadcast_telemetry("evaluation_complete", eval_result.model_dump(), session_id=session_id)
        
        return eval_result

    def _wait_for_stepper(self, session_id: str, turn: int, current_prompt: str) -> str:
        """Pauses execution until a signal is received from the UI/API. Returns (potentially modified) prompt."""
        signal_file = f"/tmp/stepper_{session_id}.json"
        
        # Initial state including the current prompt to be edited
        with open(signal_file, "w") as f:
            json.dump({
                "session_id": session_id, 
                "turn": turn, 
                "status": "paused",
                "current_prompt": current_prompt
            }, f)

        modified_prompt = current_prompt
        while True:
            if os.path.exists(signal_file):
                with open(signal_file, "r") as f:
                    try:
                        state = json.load(f)
                        if state.get("status") == "resume" and state.get("turn") == turn:
                            modified_prompt = state.get("current_prompt", current_prompt)
                            break
                    except json.JSONDecodeError:
                        pass
            time.sleep(0.5)
        
        # Cleanup or update state to indicate progressing
        with open(signal_file, "w") as f:
            json.dump({"session_id": session_id, "turn": turn, "status": "active"}, f)
            
        return modified_prompt

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
