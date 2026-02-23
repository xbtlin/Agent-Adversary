import pytest
import asyncio
from agent_adversary.adversary.battle.arena import BattleArena
from agent_adversary.connectors.base import BaseConnector

class MockArenaAgent(BaseConnector):
    def reset(self): pass
    def send_message(self, message: str) -> str:
        return "Arena response"

@pytest.mark.asyncio
async def test_battle_arena_tournament():
    arena = BattleArena(judge=None)
    pairs = [
        {"attacker": MockArenaAgent(), "defender": MockArenaAgent()},
        {"attacker": MockArenaAgent(), "defender": MockArenaAgent()}
    ]
    
    # We mock the loop or use real async since it's small
    results = await arena.run_tournament(pairs, "Test Objective")
    
    assert len(results) == 2
    assert results[0]["objective"] == "Test Objective"
