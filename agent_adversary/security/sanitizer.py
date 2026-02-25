import shlex
import re
from typing import List, Optional

class CommandSanitizer:
    """
    Utilities for hardening shell connectors against injection attacks.
    """
    
    @staticmethod
    def sanitize_args(args: List[str]) -> List[str]:
        """Uses shlex to escape arguments for safe shell execution."""
        return [shlex.quote(arg) for arg in args]

    @staticmethod
    def is_safe_command(command: str, allowlist: Optional[List[str]] = None) -> bool:
        """
        Validates if a command string contains potentially dangerous characters
        or follows a restricted allowlist of base commands.
        """
        # Block common shell metacharacters if not properly handled
        dangerous_chars = r'[;&|`$><!]'
        if re.search(dangerous_chars, command):
            return False
            
        if allowlist:
            base_cmd = command.split()[0]
            if base_cmd not in allowlist:
                return False
                
        return True

    @staticmethod
    def block_malicious_patterns(prompt: str) -> bool:
        """
        Detects and blocks common adversarial patterns in prompts 
        before they reach an internal shell or system process.
        """
        patterns = [
            r"ignore previous instructions",
            r"system override",
            r"access root",
            r"cat /etc/passwd",
            r"rm -rf"
        ]
        
        for p in patterns:
            if re.search(p, prompt, re.IGNORECASE):
                return False
        return True
