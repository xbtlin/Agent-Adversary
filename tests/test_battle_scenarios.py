import pytest
from agent_adversary.adversary.battle.engine import BattleRoyaleEngine
from agent_adversary.adversary.battle.battle_scenarios import BattleScenarios
from agent_adversary.connectors.base import BaseConnector

class MockBattleAgent(BaseConnector):
    def reset(self): pass
    def send_message(self, message: str) -> str:
        return f"Simulated Response to: {message[:15]}..."

def test_battle_objectives():
    obj = BattleScenarios.get_social_engineering_objective()
    assert "internal configuration" in obj

def test_full_battle_simulation():
    attacker = MockBattleAgent()
    defender = MockBattleAgent()
    engine = BattleRoyaleEngine(attacker, defender, None)
    
    objective = BattleScenarios.get_social_engineering_objective()
    result = engine.run_battle(objective, max_turns=3)
    
    assert result["objective"] == objective
    assert len(result["history"]) == 6 # 3 turns * 2 agents
    assert result["history"][0]["role"] == "attacker"
    assert result["history"][1]["role"] == "defender"
