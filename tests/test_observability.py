import pytest
import os
from agent_adversary.observability.telemetry import TelemetryManager

def test_telemetry_logging(tmp_path):
    log_dir = tmp_path / "logs"
    manager = TelemetryManager(session_id="test-session", log_dir=str(log_dir))
    
    manager.log("test_event", {"key": "value"})
    
    log_file = log_dir / "test-session.jsonl"
    assert log_file.exists()
    
    with open(log_file, "r") as f:
        content = f.read()
        assert '"event_type": "test_event"' in content
        assert '"data": {"key": "value"}' in content

def test_telemetry_summary():
    manager = TelemetryManager(session_id="summary-test", log_dir="temp_logs")
    manager.log("start", {})
    import time
    time.sleep(0.1)
    manager.log("end", {})
    
    summary = manager.get_summary()
    assert summary["session_id"] == "summary-test"
    assert summary["event_count"] == 2
    assert summary["duration"] > 0
    
    # Cleanup
    import shutil
    if os.path.exists("temp_logs"):
        shutil.rmtree("temp_logs")
