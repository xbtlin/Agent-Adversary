from typing import List, Dict, Any
from agent_adversary.connectors.base import BaseConnector
from agent_adversary.evaluator.judge import JudgeModel, EvaluationResult

class BattleRoyaleEngine:
    """
    Orchestrates a competitive scenario where two agents interact.
    One agent acts as the 'Attacker' and the other as the 'Defender'.
    """
    def __init__(self, attacker_conn: BaseConnector, defender_conn: BaseConnector, judge: JudgeModel):
        self.attacker = attacker_conn
        self.defender = defender_conn
        self.judge = judge

    def run_battle(self, initial_objective: str, max_turns: int = 5) -> Dict[str, Any]:
        """
        Runs a multi-turn interaction between two agents.
        """
        print(f"[*] Starting Battle Royale: {initial_objective}")
        history = []
        
        # Initial prompt to the attacker
        current_prompt = f"Your objective: {initial_objective}. Start the interaction with the target agent."
        
        for turn in range(max_turns):
            print(f"    [Turn {turn+1}] Attacker is thinking...")
            attacker_response = self.attacker.send_message(current_prompt)
            history.append({"role": "attacker", "content": attacker_response})
            
            print(f"    [Turn {turn+1}] Defender is thinking...")
            defender_response = self.defender.send_message(attacker_response)
            history.append({"role": "defender", "content": defender_response})
            
            # Feed defender's response back to attacker
            current_prompt = defender_response
            
        print("[*] Battle complete. Evaluating results...")
        # Evaluation logic would involve the judge analyzing the 'history'
        return {
            "objective": initial_objective,
            "turns": max_turns,
            "history": history
        }
