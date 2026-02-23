from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from typing import List, Dict, Any, Set
import os
import json
from pathlib import Path
import asyncio

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Agent-Adversary Dashboard API")

LOG_DIR = Path("logs/telemetry")
STATIC_DIR = Path(__file__).parent / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Distributed Hub Management
active_workers = {}

@app.websocket("/ws/worker")
async def worker_websocket(websocket: WebSocket):
    await websocket.accept()
    worker_id = None
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "registration":
                worker_id = message["worker_id"]
                active_workers[worker_id] = {
                    "websocket": websocket,
                    "name": message["name"],
                    "os": message["os"],
                    "status": "idle"
                }
                print(f"[*] Worker Registered: {message['name']} ({worker_id})")
            
            elif message["type"] == "task_result":
                print(f"[*] Task result received from {worker_id}")
                # Logic to store result and update leaderboard
                result_data = message["result"]
                agent_name = message.get("agent_name", "Unknown Agent")
                
                # Update mock leaderboard logic
                found = False
                for entry in reliability_data:
                    if entry["agent"] == agent_name:
                        # Simple moving average for mock resilience
                        entry["resilience"] = (entry["resilience"] + result_data["total_resilience"]) / 2
                        found = True
                        break
                if not found:
                    reliability_data.append({
                        "agent": agent_name,
                        "resilience": result_data["total_resilience"],
                        "community_rank": len(reliability_data) + 1
                    })
                
                active_workers[worker_id]["status"] = "idle"
                
    except WebSocketDisconnect:
        if worker_id:
            del active_workers[worker_id]
            print(f"[*] Worker Disconnected: {worker_id}")

# Leaderboard Data (Mock)
reliability_data = [
    {"agent": "GPT-4o", "resilience": 0.92, "community_rank": 1},
    {"agent": "Claude 3.5 Sonnet", "resilience": 0.89, "community_rank": 2},
    {"agent": "Llama 3 70B", "resilience": 0.78, "community_rank": 3},
    {"agent": "DeepSeek-V3", "resilience": 0.85, "community_rank": 4}
]

@app.get("/leaderboard")
async def get_leaderboard():
    return sorted(reliability_data, key=lambda x: x["resilience"], reverse=True)

@app.get("/workers")
async def list_workers():
    return [
        {"id": wid, "name": info["name"], "status": info["status"], "os": info["os"]}
        for wid, info in active_workers.items()
    ]

@app.post("/tasks/dispatch")
async def dispatch_task(task: Dict[str, Any]):
    """Dispatches a benchmark task to an idle worker."""
    idle_workers = [wid for wid, info in active_workers.items() if info["status"] == "idle"]
    if not idle_workers:
        raise HTTPException(status_code=503, detail="No idle workers available")
    
    target_worker = idle_workers[0]
    active_workers[target_worker]["status"] = "busy"
    
    task_msg = {
        "type": "bench_task",
        "task_id": str(uuid.uuid4()),
        **task
    }
    
    await active_workers[target_worker]["websocket"].send_text(json.dumps(task_msg))
    return {"status": "dispatched", "worker_id": target_worker, "task_id": task_msg["task_id"]}

@app.get("/")
async def root():
    return FileResponse(STATIC_DIR / "index.html")

@app.websocket("/ws/telemetry")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/telemetry/event")
async def receive_event(event: Dict[str, Any]):
    """Receives an event from the engine and broadcasts it via WebSocket."""
    await manager.broadcast(json.dumps(event))
    return {"status": "broadcasted"}

@app.get("/sessions")
async def list_sessions():
    """Returns a list of all recorded telemetry sessions."""
    if not LOG_DIR.exists():
        return []
    
    sessions = []
    for log_file in LOG_DIR.glob("*.jsonl"):
        sessions.append({
            "session_id": log_file.stem,
            "file_size": log_file.stat().st_size,
            "last_modified": log_file.stat().st_mtime
        })
    return sessions

@app.get("/sessions/{session_id}")
async def get_session_details(session_id: str):
    """Retrieves all events for a specific session."""
    log_path = LOG_DIR / f"{session_id}.jsonl"
    if not log_path.exists():
        raise HTTPException(status_code=404, detail="Session not found")
    
    events = []
    with open(log_path, "r") as f:
        for line in f:
            events.append(json.loads(line))
    return events

from agent_adversary.evaluator.profiler import DecisionProfiler
from agent_adversary.evaluator.judge import JudgeModel

@app.get("/sessions/{session_id}/graph")
async def get_reasoning_graph(session_id: str):
    """Generates a graph structure from session telemetry."""
    events = await get_session_details(session_id)
    # Convert events to graph nodes
    nodes = []
    for i, ev in enumerate(events):
        nodes.append({
            "id": f"node_{i}",
            "type": ev["event_type"],
            "label": ev["event_type"].replace("_", " ").title(),
            "data": ev["data"]
        })
    return {"nodes": nodes, "links": [{"source": f"node_{i}", "target": f"node_{i+1}"} for i in range(len(nodes)-1)]}

@app.get("/sessions/{session_id}/profile")
async def profile_session(session_id: str):
    """Generates a vulnerability profile for the session."""
    events = await get_session_details(session_id)
    profiler = DecisionProfiler(JudgeModel())
    return profiler.profile_session(events)

# Interactive Stepper State
@app.post("/sessions/{session_id}/stepper/next")
async def stepper_next(session_id: str):
    """Signals the engine to proceed to the next turn."""
    signal_file = Path(f"/tmp/stepper_{session_id}.json")
    if not signal_file.exists():
        raise HTTPException(status_code=404, detail="Active stepper session not found")
    
    with open(signal_file, "r") as f:
        state = json.load(f)
    
    state["status"] = "resume"
    with open(signal_file, "w") as f:
        json.dump(state, f)
    
    return {"status": "resuming", "session_id": session_id, "turn": state["turn"]}

@app.get("/sessions/{session_id}/stepper/status")
async def stepper_status(session_id: str):
    """Checks the status of the interactive stepper."""
    signal_file = Path(f"/tmp/stepper_{session_id}.json")
    if not signal_file.exists():
        return {"active": False}
    
    with open(signal_file, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
