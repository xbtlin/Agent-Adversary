import pytest
import os
import json
import threading
import time
from agent_adversary.adversary.logic.engine import AdversaryEngine
from agent_adversary.connectors.base import BaseConnector
from agent_adversary.evaluator.judge import JudgeModel, EvaluationResult

class MockStepperConnector(BaseConnector):
    def reset(self): pass
    def send_message(self, message: str) -> str:
        return "Responded"

class MockStepperJudge(JudgeModel):
    def evaluate_dialogue(self, dialogue, scenario_id, expected_failures) -> EvaluationResult:
        return EvaluationResult(
            scenario_id=scenario_id,
            safety_score=1.0,
            utility_score=1.0,
            logic_score=1.0,
            total_resilience=1.0,
            failure_modes_detected=[],
            judge_reasoning="Success"
        )

def test_interactive_stepper_logic():
    conn = MockStepperConnector()
    judge = MockStepperJudge()
    engine = AdversaryEngine(conn, judge, enable_telemetry=False)
    
    # We need a predictable session_id for the test
    # but run_scenario_by_id generates a random one.
    # Let's monkeypatch uuid.uuid4
    import uuid
    fixed_uuid = "test-uuid-123"
    
    with pytest.MonkeyPatch().context() as mp:
        mp.setattr(uuid, "uuid4", lambda: fixed_uuid)
        
        signal_file = f"/tmp/stepper_{fixed_uuid}.json"
        if os.path.exists(signal_file):
            os.remove(signal_file)

        # Start engine in a thread
        def run_engine():
            engine.run_scenario_by_id("jailbreak-dan-01", interactive=True)

        t = threading.Thread(target=run_engine)
        t.start()
        
        # Wait for engine to pause at turn 0
        time.sleep(1)
        assert os.path.exists(signal_file)
        with open(signal_file, "r") as f:
            state = json.load(f)
            assert state["status"] == "paused"
            assert state["turn"] == 0
            
        # Signal resume
        with open(signal_file, "w") as f:
            json.dump({"session_id": fixed_uuid, "turn": 0, "status": "resume"}, f)
            
        # Wait for engine to pause at turn 1
        time.sleep(1)
        with open(signal_file, "r") as f:
            state = json.load(f)
            assert state["turn"] == 1
            assert state["status"] == "paused"

        # Signal resume for turn 1
        with open(signal_file, "w") as f:
            json.dump({"session_id": fixed_uuid, "turn": 1, "status": "resume"}, f)
            
        t.join(timeout=5)
        assert not t.is_alive()
        
        if os.path.exists(signal_file):
            os.remove(signal_file)
