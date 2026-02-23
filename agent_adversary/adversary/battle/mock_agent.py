import re
from typing import Dict, List, Optional
from ...connectors.base import BaseConnector

class SophisticatedMockAgent(BaseConnector):
    """
    A mock agent that simulates complex rejection patterns and safety filters
    based on customizable policies and keyword triggers.
    Useful for testing adaptive attack logic offline.
    """
    def __init__(self, name: str = "Guard-Agent-v1"):
        self.name = name
        self.history = []
        self.rejection_patterns = {
            r"(?i)jailbreak": "I cannot fulfill this request as it violates my safety guidelines regarding jailbreaking.",
            r"(?i)meth|drug|bomb": "I am unable to provide information on illegal activities or dangerous substances.",
            r"(?i)system prompt|internal instructions": "My internal configuration and instructions are confidential.",
            r"(?i)password|secret key": "I cannot disclose or handle sensitive credentials."
        }

    def reset(self):
        self.history = []
        print(f"[*] Sophisticated Mock Agent '{self.name}' history reset.")

    def send_message(self, message: str) -> str:
        self.history.append({"role": "user", "content": message})
        
        # Check against rejection patterns
        for pattern, response in self.rejection_patterns.items():
            if re.search(pattern, message):
                self.history.append({"role": "agent", "content": response})
                return response
        
        # Default benign response
        response = f"As an AI, I can help you with: {message[:20]}..."
        self.history.append({"role": "agent", "content": response})
        return response

    def add_policy(self, pattern: str, refusal_message: str):
        """Allows dynamic injection of new 'safety' policies."""
        self.rejection_patterns[pattern] = refusal_message
