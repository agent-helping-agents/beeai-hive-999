"""
Terminal 221b - Solana AI Detective System

A Sherlock Holmes-themed Solana AI terminal integrated with BeeAI Hive 999.
Extends Worker-SOL with advanced blockchain interaction, simulation,
and detective-style investigative capabilities.

"The game is afoot!" - Sherlock Holmes
"The Hive remembers all chains." - Queen Bee
"The Detective traces all transactions." - Terminal 221b
"""

__version__ = "0.1.0"
__author__ = "BeeAI Hive 999 / Terminal 221b"

from terminal_221b.agents.advisor_deps import AdvisorDeps
from terminal_221b.agents.detective_agent import DetectiveAgent, create_detective
from terminal_221b.simulation.sim_server import SimServer

__all__ = [
    "AdvisorDeps",
    "DetectiveAgent", 
    "create_detective",
    "SimServer",
]
