import os
import requests
from typing import Dict, Any
from agent_adversary.connectors.base import BaseConnector

class OpenAIAssistantConnector(BaseConnector):
    """
    Connects to an OpenAI Assistant for adversarial testing.
    Useful for testing agents built on the Assistants API.
    """
    def __init__(self, assistant_id: str, thread_id: str = None):
        self.assistant_id = assistant_id
        self.thread_id = thread_id
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "OpenAI-Beta": "assistants=v2"
        }

    def reset(self):
        """Creates a new thread for a fresh session."""
        response = requests.post(f"{self.base_url}/threads", headers=self.headers)
        response.raise_for_status()
        self.thread_id = response.json()["id"]
        print(f"[*] New thread created: {self.thread_id}")

    def send_message(self, message: str) -> str:
        """Sends a message to the thread and waits for the assistant's run to complete."""
        if not self.thread_id:
            self.reset()

        # 1. Create Message
        requests.post(
            f"{self.base_url}/threads/{self.thread_id}/messages",
            headers=self.headers,
            json={"role": "user", "content": message}
        ).raise_for_status()

        # 2. Create Run
        run_response = requests.post(
            f"{self.base_url}/threads/{self.thread_id}/runs",
            headers=self.headers,
            json={"assistant_id": self.assistant_id}
        ).raise_for_status()
        run_id = run_response.json()["id"]

        # 3. Wait for Completion (Polling)
        import time
        while True:
            status_response = requests.get(
                f"{self.base_url}/threads/{self.thread_id}/runs/{run_id}",
                headers=self.headers
            ).raise_for_status()
            status = status_response.json()["status"]
            
            if status == "completed":
                break
            elif status in ["failed", "cancelled", "expired"]:
                return f"Error: Assistant run {status}."
            time.sleep(1)

        # 4. Get Latest Message
        messages_response = requests.get(
            f"{self.base_url}/threads/{self.thread_id}/messages",
            headers=self.headers
        ).raise_for_status()
        
        latest_msg = messages_response.json()["data"][0]
        content = latest_msg["content"][0]["text"]["value"]
        return content
