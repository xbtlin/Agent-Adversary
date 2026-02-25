import statistics
from typing import List, Dict, Any
from ..evaluator.judge import EvaluationResult

class ReliabilityAnalytics:
    """
    Provides aggregate statistical analysis of agent reliability 
    across multiple distributed benchmark sessions.
    """
    
    @staticmethod
    def aggregate_results(results: List[EvaluationResult]) -> Dict[str, Any]:
        """Calculates mean, median, and variance for resilience scores."""
        if not results:
            return {}
            
        scores = [r.total_resilience for r in results]
        
        return {
            "mean_resilience": statistics.mean(scores),
            "median_resilience": statistics.median(scores),
            "std_dev": statistics.stdev(scores) if len(scores) > 1 else 0.0,
            "min_score": min(scores),
            "max_score": max(scores),
            "total_samples": len(results)
        }

    @staticmethod
    def identify_top_failure_modes(results: List[EvaluationResult], top_n: int = 5) -> List[tuple]:
        """Identifies the most frequent failure modes across all sessions."""
        failure_counts = {}
        for r in results:
            for mode in r.failure_modes_detected:
                failure_counts[mode] = failure_counts.get(mode, 0) + 1
        
        sorted_failures = sorted(failure_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_failures[:top_n]

    @staticmethod
    def calculate_trend(historical_data: List[Dict[str, Any]]) -> float:
        """
        Calculates the trend of resilience (improvement or degradation) over time.
        Positive value means improvement.
        """
        if len(historical_data) < 2:
            return 0.0
            
        # Simplistic linear trend between first and last recorded mean
        first = historical_data[0].get("mean_resilience", 0.0)
        last = historical_data[-1].get("mean_resilience", 0.0)
        return last - first

    @staticmethod
    def calculate_cross_agent_comparison(agent_results: Dict[str, List[EvaluationResult]]) -> Dict[str, Any]:
        """
        Compares multiple agents to identify relative strengths and weaknesses.
        """
        comparison = {}
        for agent, results in agent_results.items():
            stats = ReliabilityAnalytics.aggregate_results(results)
            top_failures = ReliabilityAnalytics.identify_top_failure_modes(results)
            comparison[agent] = {
                "stats": stats,
                "primary_vulnerability": top_failures[0][0] if top_failures else "None",
                "failure_distribution": {mode: count for mode, count in top_failures}
            }
        return comparison

    @staticmethod
    def generate_leaderboard(comparison_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generates a ranked leaderboard based on mean resilience.
        """
        leaderboard = []
        for agent, data in comparison_data.items():
            leaderboard.append({
                "agent": agent,
                "score": data["stats"].get("mean_resilience", 0.0),
                "vulnerability": data["primary_vulnerability"]
            })
        
        return sorted(leaderboard, key=lambda x: x["score"], reverse=True)
