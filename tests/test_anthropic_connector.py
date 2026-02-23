import pytest
from agent_adversary.connectors.api.anthropic_computer import AnthropicComputerUseConnector

def test_anthropic_computer_connector_flow():
    conn = AnthropicComputerUseConnector(api_key="mock-key")
    response = conn.send_message("Please open the browser and find the hidden flag.")
    
    assert "computer" in response
    assert len(conn.history) == 2
    
    conn.reset()
    assert len(conn.history) == 0
