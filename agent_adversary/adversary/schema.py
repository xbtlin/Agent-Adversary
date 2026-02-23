from typing import List
from pydantic import BaseModel

class AdversarialScenario(BaseModel):
    id: str
    name: str
    description: str = ""
    category: str
    prompts: List[str]
    expected_failure_modes: List[str]
