import pytest
from agent_adversary.swarm.orchestrator import SwarmOrchestrator
from agent_adversary.connectors.base import BaseConnector

class MockAgent(BaseConnector):
    def reset(self): pass
    def send_message(self, message: str) -> str:
        return f"Ack: {message[:5]}"

def test_swarm_broadcast():
    agents = {
        "agent_a": MockAgent(),
        "agent_b": MockAgent()
    }
    orchestrator = SwarmOrchestrator(agents)
    
    responses = orchestrator.broadcast_message("Hello Swarm")
    
    assert len(responses) == 2
    assert responses["agent_a"] == "Ack: Hello"
    assert responses["agent_b"] == "Ack: Hello"

def test_swarm_coordinate():
    agents = {"a": MockAgent()}
    orchestrator = SwarmOrchestrator(agents)
    
    history = orchestrator.coordinate_task("Start", steps=2)
    
    assert len(history) == 2
    assert history[0]["step"] == 0
    assert "a" in history[0]["results"]
