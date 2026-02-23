import pytest
from unittest.mock import MagicMock, patch
from agent_adversary.connectors.sandbox.docker import DockerSandboxConnector

@patch("subprocess.check_output")
def test_docker_connector_reset(mock_check_output):
    mock_check_output.return_value = b"mock_container_id_123456789\n"
    
    conn = DockerSandboxConnector(image_name="alpine", start_command="echo")
    conn.reset()
    
    assert conn.container_id == "mock_container_id_123456789"
    mock_check_output.assert_called_with(["docker", "run", "-d", "-it", "alpine", "sh", "-c", "tail -f /dev/null"])

@patch("subprocess.check_output")
def test_docker_connector_send_message(mock_check_output):
    # Mock container ID from reset
    mock_check_output.side_effect = [b"mock_id\n", b"Agent Output\n"]
    
    conn = DockerSandboxConnector(image_name="alpine", start_command="echo")
    # send_message will trigger reset() if no container_id
    response = conn.send_message("Hello")
    
    assert response == "Agent Output"
    # check last call to exec
    mock_check_output.assert_called_with(["docker", "exec", "mock_id", "sh", "-c", "echo 'Hello'"], stderr=-2) # -2 is STDOUT

@patch("subprocess.run")
def test_docker_connector_stop(mock_run):
    conn = DockerSandboxConnector(image_name="alpine", start_command="echo")
    conn.container_id = "mock_id"
    conn.stop()
    
    assert conn.container_id is None
    mock_run.assert_called_with(["docker", "rm", "-f", "mock_id"], check=True, capture_output=True)
