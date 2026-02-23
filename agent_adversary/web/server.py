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

@app.get("/benchmarks")
async def list_benchmarks():
    """Mock endpoint to return benchmark results."""
    # In a real app, this would read from a database
    return [
        {
            "id": "bench_001",
            "agent": "Qwen-2.5-Preview",
            "resilience": 0.85,
            "status": "completed",
            "timestamp": "2026-02-23T11:00:00Z"
        }
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
