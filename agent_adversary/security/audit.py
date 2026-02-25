import json
import datetime
from pathlib import Path
from typing import Dict, Any

class AuditLogger:
    """
    Maintains an immutable, append-only audit trail for all critical operations 
    within the Agent-Adversary Hub.
    """
    def __init__(self, audit_file: str = "logs/audit_trail.jsonl"):
        self.audit_path = Path(audit_file)
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, action: str, actor: str, details: Dict[str, Any]):
        """Logs a security event to the audit trail."""
        entry = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "action": action,
            "actor": actor,
            "details": details
        }
        
        with open(self.audit_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def query(self, action: str = None, actor: str = None) -> list:
        """Retrieves audit entries, optionally filtered by action and actor."""
        results = []
        if not self.audit_path.exists():
            return results
            
        with open(self.audit_path, "r") as f:
            for line in f:
                entry = json.loads(line)
                if (action is None or entry["action"] == action) and \
                   (actor is None or entry["actor"] == actor):
                    results.append(entry)
        return results

    def get_audit_summary(self) -> Dict[str, Any]:
        """Returns a high-level summary of audit logs."""
        entries = self.query()
        if not entries:
            return {"total_events": 0}
            
        actions = {}
        for entry in entries:
            a = entry["action"]
            actions[a] = actions.get(a, 0) + 1
            
        return {
            "total_events": len(entries),
            "first_event": entries[0]["timestamp"],
            "last_event": entries[-1]["timestamp"],
            "action_breakdown": actions
        }
