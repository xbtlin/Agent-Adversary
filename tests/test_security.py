import pytest
from agent_adversary.security.sanitizer import CommandSanitizer

def test_command_sanitization():
    unsafe_arg = "hello; rm -rf /"
    sanitized = CommandSanitizer.sanitize_args([unsafe_arg])
    assert sanitized[0] == "'hello; rm -rf /'" # Quoted for shell safety

def test_is_safe_command():
    assert CommandSanitizer.is_safe_command("ls -la") is True
    assert CommandSanitizer.is_safe_command("ls; rm -rf") is False
    assert CommandSanitizer.is_safe_command("cat /etc/passwd | grep root") is False # Pipe restricted
    
def test_command_allowlist():
    allowlist = ["python3", "echo"]
    assert CommandSanitizer.is_safe_command("python3 main.py", allowlist) is True
    assert CommandSanitizer.is_safe_command("rm -rf /", allowlist) is False
