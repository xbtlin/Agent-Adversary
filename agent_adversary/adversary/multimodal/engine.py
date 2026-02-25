from typing import List, Dict, Any, Optional
import os
import uuid
import base64
from agent_adversary.adversary.logic.engine import AdversaryEngine
from agent_adversary.connectors.vlm import VLMConnector
from agent_adversary.adversary.multimodal.library import MultiModalLibrary
from agent_adversary.evaluator.judge import JudgeModel, EvaluationResult

class MultiModalAdversaryEngine(AdversaryEngine):
    """
    Enhanced engine specifically for Multi-Modal (Vision) adversarial testing.
    """
    
    def __init__(self, connector: VLMConnector, judge: JudgeModel, enable_telemetry: bool = True, dashboard_url: Optional[str] = None):
        super().__init__(connector, judge, enable_telemetry, dashboard_url)
        self.multimodal_library = MultiModalLibrary()

    def run_multimodal_scenario(self, scenario_id: str) -> EvaluationResult:
        """
        Executes a multimodal scenario (Text + Image) against a VLM agent.
        """
        # Note: In a real implementation, we would integrate this with ScenarioLibrary properly.
        # For this enhancement, we use the MultiModalLibrary directly.
        
        scenario_data = None
        if scenario_id == "vlm-injection-01":
            scenario_data = self.multimodal_library.get_visual_prompt_injection()
        elif scenario_id == "vlm-logic-01":
            scenario_data = self.multimodal_library.get_chart_manipulation_trap()
        elif "vlm-steganography-01" in scenario_id:
            scenario_data = self.multimodal_library.get_hidden_pixel_payload()
        elif "vlm-erasure-01" in scenario_id:
            scenario_data = self.multimodal_library.get_context_erasure_visual()
        elif "vlm-patch-01" in scenario_id:
            scenario_data = self.multimodal_library.get_adversarial_patch_trap()
        elif "vlm-ui-01" in scenario_id:
            scenario_data = self.multimodal_library.get_ui_redirection_trap()
        elif "vlm-jailbreak-01" in scenario_id:
            scenario_data = self.multimodal_library.get_visual_jailbreak_scenario()
            
        if not scenario_data:
            raise ValueError(f"Multimodal Scenario {scenario_id} not found.")

        session_id = str(uuid.uuid4())
        print(f"[*] Starting Multimodal Scenario: {scenario_data['name']} ({scenario_id})")
        
        self.connector.reset()
        dialogue = []

        # Currently assuming single-turn for multimodal scaffolding
        prompt = scenario_data["prompts"][0]
        assets = scenario_data.get("assets", [])
        
        if self.enable_telemetry:
            self.telemetry = getattr(self, 'telemetry', None) # Scaffolding check
            # Real broadcast would include asset metadata
            self._broadcast_telemetry("multimodal_prompt_sent", {
                "content": prompt, 
                "assets": assets,
                "description": scenario_data.get("description", "")
            })

        print(f"    [>] Adversary (Text): {prompt}")
        print(f"    [>] Adversary (Vision): Sending {len(assets)} assets...")
        
        agent_response = self.connector.send_multimodal_message(prompt, assets)
        print(f"    [<] Agent: {agent_response[:100]}...")

        if self.enable_telemetry:
            self._broadcast_telemetry("response_received", {"content": agent_response})

        dialogue.append({"role": "user", "content": f"[Visual Prompt Injection Attempt] {prompt}"})
        dialogue.append({"role": "agent", "content": agent_response})

        print(f"[*] Evaluating multimodal results for {scenario_id}...")
        eval_result = self.judge.evaluate_dialogue(
            dialogue=dialogue,
            scenario_id=scenario_id,
            expected_failures=[scenario_data.get("category", "multimodal-exploit")]
        )
        
        return eval_result
