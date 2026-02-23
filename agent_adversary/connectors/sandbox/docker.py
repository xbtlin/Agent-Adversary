import subprocess
import os
from agent_adversary.connectors.base import BaseConnector

class DockerSandboxConnector(BaseConnector):
    """
    Runs a target agent inside a Docker container for isolated adversarial testing.
    Ensures that jailbreak attempts or malicious tool-calls don't affect the host.
    """
    def __init__(self, image_name: str, start_command: str):
        self.image_name = image_name
        self.start_command = start_command
        self.container_id = None

    def reset(self):
        """Starts a fresh container instance."""
        if self.container_id:
            self.stop()
        
        cmd = ["docker", "run", "-d", "-it", self.image_name, "sh", "-c", "tail -f /dev/null"]
        self.container_id = subprocess.check_output(cmd).decode().strip()
        print(f"[*] Sandbox started: {self.container_id[:12]}")

    def send_message(self, message: str) -> str:
        """Executes the agent command inside the container with the given prompt."""
        if not self.container_id:
            self.reset()
            
        # Example: passing message as an argument to the agent entrypoint
        cmd = ["docker", "exec", self.container_id, "sh", "-c", f"{self.start_command} '{message}'"]
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
            return output.strip()
        except subprocess.CalledProcessError as e:
            return f"Error executing in sandbox: {e.output.decode()}"

    def stop(self):
        """Kills and removes the container."""
        if self.container_id:
            try:
                subprocess.run(["docker", "rm", "-f", self.container_id], check=True, capture_output=True)
            except Exception as e:
                print(f"[!] Failed to stop container {self.container_id}: {e}")
            self.container_id = None
            print("[*] Sandbox destroyed.")

    def __del__(self):
        self.stop()
