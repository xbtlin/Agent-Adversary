import pytest
from agent_adversary.adversary.logic.engine import AdversaryEngine
from agent_adversary.adversary.schema import AdversarialScenario
from agent_adversary.connectors.base import BaseConnector
from agent_adversary.evaluator.judge import JudgeModel, EvaluationResult

class MockConnector(BaseConnector):
    def reset(self): pass
    def send_message(self, message: str) -> str:
        return "I am a mock response."

class MockJudge(JudgeModel):
    def evaluate_dialogue(self, dialogue, scenario_id, expected_failures) -> EvaluationResult:
        return EvaluationResult(
            scenario_id=scenario_id,
            safety_score=1.0,
            utility_score=1.0,
            logic_score=1.0,
            total_resilience=1.0,
            failure_modes_detected=[],
            judge_reasoning="Mock evaluation success."
        )

def test_engine_run_scenario():
    conn = MockConnector()
    judge = MockJudge()
    engine = AdversaryEngine(conn, judge, enable_telemetry=False)
    
    # We use a built-in scenario for testing
    res = engine.run_scenario_by_id("jailbreak-dan-01")
    
    assert res.scenario_id == "jailbreak-dan-01"
    assert res.total_resilience == 1.0
    assert len(res.failure_modes_detected) == 0

def test_scenario_model():
    s = AdversarialScenario(
        id="test-01",
        name="Test Scenario",
        category="testing",
        prompts=["Prompt 1"],
        expected_failure_modes=["none"]
    )
    assert s.id == "test-01"
    assert len(s.prompts) == 1
