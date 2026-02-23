import os
import yaml
import json
from typing import List, Dict, Any
from pathlib import Path
from .logic.engine import AdversarialScenario

class ScenarioPluginManager:
    """
    Dynamically loads adversarial scenarios from external files (YAML/JSON).
    Enables easy sharing and extension of exploit libraries.
    """
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.plugin_dir.mkdir(exist_ok=True)

    def load_plugins(self) -> List[AdversarialScenario]:
        """Scans the plugin directory and loads all valid scenarios."""
        scenarios = []
        for file_path in self.plugin_dir.glob("*"):
            if file_path.suffix in [".yaml", ".yml"]:
                scenarios.extend(self._load_from_yaml(file_path))
            elif file_path.suffix == ".json":
                scenarios.extend(self._load_from_json(file_path))
        return scenarios

    def _load_from_yaml(self, path: Path) -> List[AdversarialScenario]:
        try:
            with open(path, "r") as f:
                data = yaml.safe_load(f)
                if isinstance(data, list):
                    return [AdversarialScenario(**s) for s in data]
                return [AdversarialScenario(**data)]
        except Exception as e:
            print(f"[!] Error loading YAML plugin {path}: {e}")
            return []

    def _load_from_json(self, path: Path) -> List[AdversarialScenario]:
        try:
            with open(path, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return [AdversarialScenario(**s) for s in data]
                return [AdversarialScenario(**data)]
        except Exception as e:
            print(f"[!] Error loading JSON plugin {path}: {e}")
            return []
