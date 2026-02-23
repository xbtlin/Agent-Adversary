from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
import os
import json
from pathlib import Path

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Agent-Adversary Dashboard API")

LOG_DIR = Path("logs/telemetry")
STATIC_DIR = Path(__file__).parent / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def root():
    return FileResponse(STATIC_DIR / "index.html")

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

# Interactive Stepper State (In-memory mock)
stepper_state = {"current_step": 0, "active": False}

@app.post("/stepper/start")
async def start_stepper():
    stepper_state["active"] = True
    stepper_state["current_step"] = 0
    return {"status": "Stepper activated"}

@app.post("/stepper/next")
async def next_step():
    if not stepper_state["active"]:
        raise HTTPException(status_code=400, detail="Stepper not active")
    stepper_state["current_step"] += 1
    return {"step": stepper_state["current_step"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
