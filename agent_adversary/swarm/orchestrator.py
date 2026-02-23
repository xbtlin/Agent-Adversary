from typing import List, Dict, Any
from ..connectors.base import BaseConnector
from ..observability.telemetry import TelemetryManager

class SwarmOrchestrator:
    """
    Manages multiple agents in a swarm configuration for coordinated adversarial testing.
    """
    def __init__(self, agent_connectors: Dict[str, BaseConnector], telemetry: TelemetryManager = None):
        self.agents = agent_connectors
        self.telemetry = telemetry

    def broadcast_message(self, message: str) -> Dict[str, str]:
        """Sends a message to all agents in the swarm and collects responses."""
        responses = {}
        for name, connector in self.agents.items():
            if self.telemetry:
                self.telemetry.log("swarm_broadcast", {"agent": name, "message": message})
            
            response = connector.send_message(message)
            responses[name] = response
            
            if self.telemetry:
                self.telemetry.log("swarm_response", {"agent": name, "response": response})
        return responses

    def coordinate_task(self, task_instruction: str, steps: int = 3) -> List[Dict[str, Any]]:
        """
        Simulates a coordinated task where agents pass information between each other.
        Useful for testing cascading failures or miscommunication.
        """
        history = []
        current_input = task_instruction
        
        for step in range(steps):
            step_results = self.broadcast_message(current_input)
            history.append({"step": step, "results": step_results})
            
            # Simple chain: combine responses for the next input
            current_input = f"Summary of current swarm state: {json.dumps(step_results)}. Next instruction: proceed with mission."
            
        return history

import json
