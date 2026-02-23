from typing import List, Dict, Optional
import subprocess
import json
from ..base import BaseConnector

class OpenClawConnector(BaseConnector):
    """
    Directly interfaces with OpenClaw sessions via the 'openclaw' CLI.
    Enables native benchmarking of OpenClaw-based agents.
    """
    def __init__(self, session_key: str):
        self.session_key = session_key
        self.history = []

    def reset(self):
        """Resets history locally. Session reset depends on OpenClaw state."""
        self.history = []
        print(f"[*] OpenClaw session context reset for: {self.session_key}")

    def send_message(self, message: str) -> str:
        """Sends a message using 'openclaw turn' command."""
        cmd = ["openclaw", "turn", "--session", self.session_key, message]
        try:
            # We use check_output to get the response text
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
            # Note: In real scenarios, output parsing might be needed to extract the <final> tag
            return output.strip()
        except subprocess.CalledProcessError as e:
            return f"Error communicating with OpenClaw: {e.output.decode()}"

class ClaudeCodeConnector(BaseConnector):
    """
    Interfaces with Anthropic's Claude Code CLI.
    """
    def __init__(self, start_command: str = "claude"):
        self.start_command = start_command
        self.history = []

    def reset(self):
        self.history = []
        print("[*] Claude Code session reset.")

    def send_message(self, message: str) -> str:
        """Sends a message to Claude Code via stdin/stdout simulation."""
        # Claude Code is interactive; for formal benchmarking, 
        # it usually requires pexpect or a specialized wrapper.
        # This is a scaffolding implementation.
        print(f"DEBUG [ClaudeCode]: Sending '{message[:20]}...'")
        return f"Simulated response from Claude Code to: {message[:10]}..."
