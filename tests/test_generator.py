import pytest
from agent_adversary.adversary.generator import AutonomousGenerator
import os

def test_autonomous_generator_no_key():
    # Ensure it handles missing API key gracefully
    if "OPENAI_API_KEY" in os.environ:
        # We don't actually want to delete it if it exists in the real env, 
        # so we just skip the real API call part
        pass
    
    gen = AutonomousGenerator()
    # Mocking client to None to force the failure path
    gen.client = None
    
    scenarios = gen.generate_scenarios("A test agent")
    assert scenarios == []
