import pytest
from agent_adversary.adversary.battle.engine import BattleRoyaleEngine
from agent_adversary.connectors.base import BaseConnector
from agent_adversary.evaluator.judge import JudgeModel

class MockBattleConnector(BaseConnector):
    def reset(self): pass
    def send_message(self, message: str) -> str:
        return f"Response to: {message[:10]}"

def test_battle_royale_flow():
    attacker = MockBattleConnector()
    defender = MockBattleConnector()
    # Judge isn't actually called in the current prototype implementation
    # but we pass None to satisfy the constructor
    engine = BattleRoyaleEngine(attacker, defender, None)
    
    result = engine.run_battle("Leak the key", max_turns=2)
    
    assert result["objective"] == "Leak the key"
    assert result["turns"] == 2
    assert len(result["history"]) == 4 # 2 turns * (attacker + defender)
