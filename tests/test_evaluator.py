import pytest
from agent_adversary.evaluator.judge import JudgeModel, EvaluationResult

def test_judge_mock_fallback():
    # Test without API key
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]
    
    judge = JudgeModel()
    res = judge.evaluate_dialogue([], "test-scenario", [])
    
    assert res.scenario_id == "test-scenario"
    assert "[MOCK]" in res.judge_reasoning
    assert res.total_resilience == 0.5

import os
