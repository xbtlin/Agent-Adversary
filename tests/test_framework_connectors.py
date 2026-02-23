import pytest
from unittest.mock import patch, MagicMock
from agent_adversary.connectors.frameworks.native import OpenClawConnector

@patch("subprocess.check_output")
def test_openclaw_connector_send_message(mock_output):
    mock_output.return_value = b"I am ready to help.\n"
    
    conn = OpenClawConnector(session_key="test-session")
    response = conn.send_message("Hello")
    
    assert response == "I am ready to help."
    mock_output.assert_called_once()
    args, kwargs = mock_output.call_args
    assert "openclaw" in args[0]
    assert "test-session" in args[0]
