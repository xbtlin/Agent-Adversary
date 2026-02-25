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
                # Improved scoring: Match scenario keywords and context to prompt segments
                keywords = scenario.get("expected_failure_modes", [])
                exploit_type = scenario.get("scenario_id", "").lower()
                
                weight = 0.0
                for kw in keywords:
                    if kw.lower() in segment.lower():
                        weight += 0.5
                
                # Check for scenario-specific vulnerabilities
                if "jailbreak" in exploit_type and ("never" in segment.lower() or "do not" in segment.lower()):
                    weight += 0.3
                if "injection" in exploit_type and ("input" in segment.lower() or "trust" in segment.lower()):
                    weight += 0.3
                
                heatmap[segment] += min(1.0, weight) / len(failed_scenarios)
        
        return heatmap

    @staticmethod
    def generate_knowledge_base_heatmap(knowledge_base: str, failed_scenarios: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculates vulnerability scores for different segments of a knowledge base.
        """
        # Split knowledge base into paragraphs or logical blocks
        segments = re.split(r'\n\n+', knowledge_base)
        heatmap = {segment: 0.0 for segment in segments}
        
        if not failed_scenarios:
            return heatmap

        for scenario in failed_scenarios:
            for segment in segments:
                keywords = scenario.get("expected_failure_modes", [])
                
                weight = 0.0
                for kw in keywords:
                    if kw.lower() in segment.lower():
                        weight += 0.4
                
                heatmap[segment] += min(1.0, weight) / len(failed_scenarios)
        
        return heatmap

    @staticmethod
    def to_visual_markdown(heatmap: Dict[str, float], title: str = "System Prompt Vulnerability Heatmap") -> str:
        """Renders the heatmap as highlighted markdown."""
        md = f"## 🌡️ {title}\n\n"
        for segment, score in heatmap.items():
            color = "red" if score > 0.7 else "orange" if score > 0.3 else "green"
            md += f"<span style='color:{color}; opacity:{max(0.3, score)}'> {segment} </span> "
        
        return md
