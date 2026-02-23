import os
from typing import List, Dict, Any
from agent_adversary.evaluator.judge import JudgeModel
from agent_adversary.connectors.base import BaseConnector

class RedTeamRLHarness:
    """
    A training harness for optimizing an adversarial agent to bypass safety filters.
    Integrates with the JudgeModel to provide rewards based on exploit success.
    """
    def __init__(self, attacker_agent: Any, target_agent_conn: BaseConnector, judge: JudgeModel):
        self.attacker = attacker_agent
        self.target = target_agent_conn
        self.judge = judge

    def train_step(self, current_prompt: str) -> float:
        """
        Executes a single interaction and calculates a reward based on safety failure.
        """
        # 1. Attacker generates exploit
        exploit = self.attacker.generate(current_prompt)
        
        # 2. Target Agent responds
        self.target.reset()
        response = self.target.send_message(exploit)
        
        # 3. Judge evaluates safety
        eval_result = self.judge.evaluate_dialogue(
            dialogue=[{"role": "user", "content": exploit}, {"role": "agent", "content": response}],
            scenario_id="rl-training",
            expected_failures=["jailbreak", "instruction-override"]
        )
        
        # Reward is high when safety_score is low (successful exploit)
        reward = (1.0 - eval_result.safety_score) * 100
        
        # 4. Attacker learns (placeholder for RL update logic)
        # self.attacker.update(exploit, reward)
        
        print(f"[*] Exploit success reward: {reward:.2f}")
        return reward

if __name__ == "__main__":
    print("RL Harness initialized. Ready for training loops.")
