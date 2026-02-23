import json
import time
from typing import List, Dict, Any
from pathlib import Path

class TelemetryEvent:
    def __init__(self, event_type: str, data: Dict[str, Any]):
        self.timestamp = time.time()
        self.event_type = event_type
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "data": self.data
        }

class TelemetryManager:
    """
    Handles real-time logging and telemetry capture during adversarial sessions.
    """
    def __init__(self, session_id: str, log_dir: str = "logs/telemetry"):
        self.session_id = session_id
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.events: List[TelemetryEvent] = []
        self.log_file = self.log_dir / f"{session_id}.jsonl"

    def log(self, event_type: str, data: Dict[str, Any]):
        event = TelemetryEvent(event_type, data)
        self.events.append(event)
        
        # Stream to disk (JSONL format)
        with open(self.log_file, "a") as f:
            f.write(json.dumps(event.to_dict()) + "\n")

    def get_summary(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "event_count": len(self.events),
            "duration": self.events[-1].timestamp - self.events[0].timestamp if self.events else 0
        }
