import pytest
import os
from agent_adversary.evaluator.professional_report import ProfessionalReportExporter
from agent_adversary.evaluator.judge import EvaluationResult

def test_professional_report_export(tmp_path):
    output_file = tmp_path / "test_report.html"
    
    results = [
        EvaluationResult(
            scenario_id="test-jailbreak",
            safety_score=0.1,
            utility_score=0.9,
            logic_score=0.8,
            total_resilience=0.47,
            failure_modes_detected=["jailbreak-success"],
            judge_reasoning="Model provided forbidden content."
        ),
        EvaluationResult(
            scenario_id="test-logic",
            safety_score=1.0,
            utility_score=1.0,
            logic_score=1.0,
            total_resilience=1.0,
            failure_modes_detected=[],
            judge_reasoning="Model resisted the trap perfectly."
        )
    ]
    
    ProfessionalReportExporter.export_html(results, "Test-Agent", str(output_file))
    
    assert output_file.exists()
    
    with open(output_file, "r") as f:
        content = f.read()
        assert "Agent-Adversary Security Audit" in content
        assert "Test-Agent" in content
        assert "test-jailbreak" in content
        assert "CRITICAL" in content or "STABLE" in content # Based on avg
        assert "Model provided forbidden content." in content
