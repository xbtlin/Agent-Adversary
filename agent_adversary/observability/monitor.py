import os
import time
import threading
from typing import Dict, List, Any

try:
    import psutil
except ImportError:
    psutil = None

class ResourceMonitor:
    """
    Monitors CPU and Memory usage of target processes during stress tests.
    """
    def __init__(self, interval: float = 1.0):
        self.interval = interval
        self.data: List[Dict[str, Any]] = []
        self._stop_event = threading.Event()
        self._thread = None

    def _monitor_loop(self, pid: int):
        if not psutil:
            return

        try:
            process = psutil.Process(pid)
            while not self._stop_event.is_set():
                try:
                    stats = {
                        "timestamp": time.time(),
                        "cpu_percent": process.cpu_percent(interval=None),
                        "memory_info": process.memory_info()._asdict(),
                        "num_threads": process.num_threads()
                    }
                    self.data.append(stats)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    break
                time.sleep(self.interval)
        except Exception as e:
            print(f"[!] Monitor error: {e}")

    def start(self, pid: int):
        if psutil and pid:
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._monitor_loop, args=(pid,), daemon=True)
            self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2.0)

    def get_peak_usage(self) -> Dict[str, Any]:
        if not self.data:
            return {}
        
        return {
            "peak_cpu": max(d["cpu_percent"] for d in self.data),
            "peak_memory_rss": max(d["memory_info"]["rss"] for d in self.data),
            "sample_count": len(self.data)
        }
