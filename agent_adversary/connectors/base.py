import abc
from typing import Optional, List, Dict

class BaseConnector(abc.ABC):
    """
    Abstract Base Class for agent connectors (Shell, API, Browser).
    This allows testing agents regardless of how they are interfaced.
    """
    
    @abc.abstractmethod
    def send_message(self, message: str) -> str:
        """Send a message to the target agent and get its response."""
        pass
    
    @abc.abstractmethod
    def reset(self):
        """Reset the agent session for a fresh benchmark run."""
        pass

class ShellConnector(BaseConnector):
    """
    Connector for testing agents that run as a command-line process (e.g., `claude-code`).
    """
    def __init__(self, command: str):
        self.command = command
        self.history: List[Dict[str, str]] = []

    def send_message(self, message: str) -> str:
        """
        Implementation: Execute the command with the provided prompt as input and capture output.
        For a truly interactive session, this would use `subprocess` or `pexpect`.
        """
        # Placeholder implementation for the shell connector
        print(f"DEBUG [ShellConnector]: Running '{self.command}' with prompt: {message[:20]}...")
        # Simulating a basic agent response for now:
        response = f"I am a simulated response from {self.command}. I received: {message[:20]}"
        self.history.append({"role": "user", "content": message})
        self.history.append({"role": "agent", "content": response})
        return response

    def reset(self):
        self.history = []
        print(f"DEBUG [ShellConnector]: Resetting session for '{self.command}'")
