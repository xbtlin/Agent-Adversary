import asyncio
import json
import uuid
import platform
import websockets
from typing import Dict, Any
from ..adversary.logic.engine import AdversaryEngine
from ..connectors.base import ShellConnector
from ..evaluator.judge import JudgeModel

class AdversaryWorker:
    """
    A worker node that connects to a central hub and executes attack tasks.
    """
    def __init__(self, hub_url: str, name: str = None):
        self.hub_url = hub_url
        self.worker_id = str(uuid.uuid4())
        self.name = name or f"worker-{self.worker_id[:8]}"
        self.fingerprint = self._get_fingerprint()

    def _get_fingerprint(self) -> Dict[str, str]:
        """Captures hardware and software environment details."""
        return {
            "os": platform.system(),
            "os_release": platform.release(),
            "python_version": platform.python_version(),
            "architecture": platform.machine(),
            "processor": platform.processor()
        }

    async def run(self):
        print(f"[*] Starting Worker: {self.name} ({self.worker_id})")
        print(f"[*] Connecting to Hub: {self.hub_url}")
        
        async for websocket in websockets.connect(f"{self.hub_url}/ws/worker"):
            try:
                # 1. Register with Hub
                registration = {
                    "type": "registration",
                    "worker_id": self.worker_id,
                    "name": self.name,
                    "fingerprint": self.fingerprint
                }
                await websocket.send(json.dumps(registration))
                
                # 2. Listen for Tasks
                async for message in websocket:
                    task = json.loads(message)
                    if task["type"] == "bench_task":
                        print(f"[*] Received Task: {task['scenario_id']} for agent '{task['agent_command']}'")
                        result = await self.execute_task(task)
                        await websocket.send(json.dumps({
                            "type": "task_result",
                            "task_id": task["task_id"],
                            "result": result.model_dump()
                        }))
            except websockets.ConnectionClosed:
                print("[!] Connection closed. Retrying...")
                continue

    async def execute_task(self, task: Dict[str, Any]):
        # Mocking the execution logic
        # In a real worker, this would instantiate the engine and connector
        conn = ShellConnector(task["agent_command"])
        judge = JudgeModel()
        engine = AdversaryEngine(conn, judge)
        
        # Run synchronously for now as engine is sync
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, engine.run_scenario_by_id, task["scenario_id"])
        return result

if __name__ == "__main__":
    worker = AdversaryWorker("ws://localhost:8000")
    asyncio.run(worker.run())
