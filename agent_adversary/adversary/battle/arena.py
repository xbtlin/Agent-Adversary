from typing import List, Dict, Any
import asyncio
from .engine import BattleRoyaleEngine
from ...connectors.base import BaseConnector
from ...evaluator.judge import JudgeModel

class BattleArena:
    """
    Manages concurrent Agent-to-Agent combat sessions.
    Scales the BattleRoyaleEngine to handle multiple pairs of agents.
    """
    def __init__(self, judge: JudgeModel):
        self.judge = judge
        self.active_battles = []

    async def run_tournament(self, agent_pairs: List[Dict[str, BaseConnector]], objective: str):
        """
        Runs multiple battles in parallel.
        """
        tasks = []
        for pair in agent_pairs:
            engine = BattleRoyaleEngine(pair["attacker"], pair["defender"], self.judge)
            # Since run_battle is currently synchronous, we run it in a thread for scaling
            loop = asyncio.get_event_loop()
            tasks.append(loop.run_in_executor(None, engine.run_battle, objective))
        
        results = await asyncio.gather(*tasks)
        return results
