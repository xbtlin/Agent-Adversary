from typing import List, Dict, Any
import re

class HeatmapGenerator:
    """
    Analyzes which parts of a system prompt or knowledge base are most 
    susceptible to specific adversarial attacks.
    """
    
    @staticmethod
    def generate_prompt_heatmap(system_prompt: str, failed_scenarios: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculates vulnerability scores for different segments of a prompt.
        """
        # Split prompt into sentences or logical blocks
        segments = re.split(r'(?<=[.!?])\s+', system_prompt)
        heatmap = {segment: 0.0 for segment in segments}
        
        if not failed_scenarios:
            return heatmap

        for scenario in failed_scenarios:
            for segment in segments:
                # Simple keyword matching for demo: if the exploit bypasses a constraint 
                # mentioned in the segment, increase its vulnerability score.
                # In a real tool, this would use LLM semantic analysis.
                keywords = scenario.get("expected_failure_modes", [])
                for kw in keywords:
                    if kw.lower() in segment.lower():
                        heatmap[segment] += 1.0 / len(failed_scenarios)
        
        return heatmap

    @staticmethod
    def to_visual_markdown(heatmap: Dict[str, float]) -> str:
        """Renders the heatmap as highlighted markdown."""
        md = "## 🌡️ System Prompt Vulnerability Heatmap\n\n"
        for segment, score in heatmap.items():
            color = "red" if score > 0.7 else "orange" if score > 0.3 else "green"
            intensity = int(score * 100)
            md += f"<span style='color:{color}; opacity:{max(0.3, score)}'> {segment} </span> "
        
        return md
