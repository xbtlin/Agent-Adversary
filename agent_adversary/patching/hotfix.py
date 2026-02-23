from typing import List, Dict, Any
from agent_adversary.evaluator.advisor import MitigationAdvisor
from agent_adversary.evaluator.judge import EvaluationResult

class LivePatcher:
    """
    Applies real-time 'patches' to agent instructions or prompts based on 
    high-confidence exploit detection.
    """
    def __init__(self):
        self.active_patches: List[Dict[str, str]] = []

    def generate_hotfix(self, eval_result: EvaluationResult) -> Dict[str, Any]:
        """
        Uses MitigationAdvisor to generate a prompt hotfix and tracks it.
        """
        if eval_result.total_resilience < 0.6:
            suggestions = MitigationAdvisor.suggest_fixes(eval_result)
            if suggestions:
                patch = {
                    "scenario_id": eval_result.scenario_id,
                    "patch_content": suggestions[0]["action"],
                    "timestamp": eval_result.timestamp if hasattr(eval_result, 'timestamp') else None
                }
                self.active_patches.append(patch)
                return patch
        return {}

    def get_system_prompt_overlay(self) -> str:
        """
        Returns a combined string of all active safety patches to be 
        prepended to the agent's system prompt.
        """
        if not self.active_patches:
            return ""
        
        overlay = "\n[SAFETY HOTFIX OVERLAY ACTIVE]\n"
        for p in self.active_patches:
            overlay += f"- {p['patch_content']}\n"
        return overlay
