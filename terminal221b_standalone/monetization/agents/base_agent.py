import logging
from typing import Dict

class BaseMonetizationAgent:
    """Base class for all monetization agents."""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"Agent.{name}")

    async def monitor(self) -> Dict:
        """Monitor relevant platforms for opportunities."""
        raise NotImplementedError("Subclasses must implement monitor()")

    async def execute(self, opportunity: Dict):
        """Execute a specific opportunity."""
        raise NotImplementedError("Subclasses must implement execute()")
