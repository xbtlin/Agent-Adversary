import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class GraphNode:
    id: str
    type: str  # thought, tool_call, response, observation
    label: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    children: List[str] = field(default_factory=list)

class ReasoningGraph:
    """
    Captures the hierarchical reasoning process of an agent during an adversarial turn.
    """
    def __init__(self, scenario_id: str):
        self.scenario_id = scenario_id
        self.nodes: Dict[str, GraphNode] = {}
        self.root_id: Optional[str] = None

    def add_node(self, node_id: str, node_type: str, label: str, parent_id: Optional[str] = None, **metadata):
        node = GraphNode(id=node_id, type=node_type, label=label, metadata=metadata)
        self.nodes[node_id] = node
        
        if parent_id and parent_id in self.nodes:
            self.nodes[parent_id].children.append(node_id)
        
        if self.root_id is None:
            self.root_id = node_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "root_id": self.root_id,
            "nodes": {nid: n.__dict__ for nid, n in self.nodes.items()}
        }

    def export_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)
