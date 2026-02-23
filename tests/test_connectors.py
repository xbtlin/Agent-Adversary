import pytest
from agent_adversary.connectors.base import ShellConnector
import subprocess
import os

def test_shell_connector_basic():
    # Simple echo agent
    conn = ShellConnector("echo 'Agent: Hello'")
    response = conn.send_message("Hi")
    assert "Hello" in response

def test_shell_connector_multi_turn():
    # Mock agent script
    script_path = "tests/mock_echo.sh"
    with open(script_path, "w") as f:
        f.write("#!/bin/bash\nwhile true; do read input; echo \"Echo: $input\"; done")
    os.chmod(script_path, 0o755)
    
    try:
        conn = ShellConnector(f"./{script_path}")
        res1 = conn.send_message("Ping")
        assert "Ping" in res1
    finally:
        if os.path.exists(script_path):
            os.remove(script_path)

def test_shell_connector_reset():
    conn = ShellConnector("echo 'New Session'")
    conn.send_message("Hello")
    assert len(conn.history) > 0
    conn.reset()
    assert len(conn.history) == 0
