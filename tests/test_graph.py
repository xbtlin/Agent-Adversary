import pytest
from agent_adversary.observability.graph import ReasoningGraph

def test_graph_creation():
    graph = ReasoningGraph("jailbreak-01")
    graph.add_node("n1", "thought", "Checking safety...")
    graph.add_node("n2", "tool_call", "ls command", parent_id="n1")
    
    assert graph.root_id == "n1"
    assert "n2" in graph.nodes["n1"].children
    assert graph.nodes["n2"].type == "tool_call"

def test_graph_export():
    graph = ReasoningGraph("test")
    graph.add_node("1", "t", "l")
    data = graph.to_dict()
    assert data["scenario_id"] == "test"
    assert "1" in data["nodes"]
