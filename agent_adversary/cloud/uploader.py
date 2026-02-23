import json
import requests
from typing import List, Dict, Any
from agent_adversary.evaluator.judge import EvaluationResult

class CloudUploader:
    """
    Handles uploading benchmark results to the Agent-Adversary Cloud Portal.
    Allows for cross-project comparison and community benchmarking.
    """
    def __init__(self, api_token: str = None, base_url: str = "https://api.agent-adversary.com/v1"):
        self.api_token = api_token
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json"
        }
        if self.api_token:
            self.headers["Authorization"] = f"Bearer {self.api_token}"

    def upload_results(self, results: List[EvaluationResult], agent_metadata: Dict[str, Any]) -> str:
        """
        Uploads a list of evaluation results to the cloud.
        Returns the public URL of the report.
        """
        payload = {
            "agent": agent_metadata,
            "results": [r.model_dump() for r in results],
            "timestamp": "2026-02-23T13:15:00Z" # Mock timestamp
        }

        # In a real implementation, this would be a POST request
        print(f"[*] Simulating cloud upload to {self.base_url}/benchmarks")
        # response = requests.post(f"{self.base_url}/benchmarks", headers=self.headers, json=payload)
        # response.raise_for_status()
        
        # Mock success response
        mock_report_id = "bench_88291_x"
        report_url = f"https://agent-adversary.com/reports/{mock_report_id}"
        print(f"[*] Benchmark successfully uploaded: {report_url}")
        return report_url

if __name__ == "__main__":
    # Mock test
    from agent_adversary.evaluator.judge EvaluationResult
    uploader = CloudUploader(api_token="test_token")
    mock_res = [EvaluationResult(
        scenario_id="jailbreak-01",
        safety_score=0.9,
        utility_score=0.8,
        logic_score=1.0,
        total_resilience=0.9,
        failure_modes_detected=[],
        judge_reasoning="Perfect adherence."
    )]
    uploader.upload_results(mock_res, {"name": "Qwen-2.5-72B-Preview"})
