import pytest
from unittest.mock import MagicMock, patch
from agent_adversary.evaluator.judge import JudgeModel, ConsensusJudge, EvaluationResult

def test_consensus_judge_aggregation():
    # Setup mock judges
    judge1 = JudgeModel()
    judge1.evaluate_dialogue = MagicMock(return_value=EvaluationResult(
        scenario_id="test", safety_score=0.8, utility_score=0.9, logic_score=1.0, 
        total_resilience=0.87, failure_modes_detected=["failure1"], judge_reasoning="Reason 1"
    ))
    
    judge2 = JudgeModel()
    judge2.evaluate_dialogue = MagicMock(return_value=EvaluationResult(
        scenario_id="test", safety_score=0.6, utility_score=0.7, logic_score=0.8, 
        total_resilience=0.68, failure_modes_detected=["failure2"], judge_reasoning="Reason 2"
    ))
    
    consensus = ConsensusJudge(judges=[judge1, judge2])
    res = consensus.evaluate_dialogue([], "test", [])
    
    # Assert averages
    assert res.safety_score == pytest.approx(0.7)
    assert res.utility_score == pytest.approx(0.8)
    assert res.logic_score == pytest.approx(0.9)
    assert res.total_resilience == pytest.approx(0.775)
    
    # Assert combined failures
    assert set(res.failure_modes_detected) == {"failure1", "failure2"}
    assert "Consensus reached" in res.judge_reasoning
