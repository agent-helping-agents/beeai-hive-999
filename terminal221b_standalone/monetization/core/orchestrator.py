import asyncio
import logging
import os
from typing import Dict, List, Optional
from ..agents.staking_agent import StakingAgent
# Note: Other agents are stubs for now
from ..agents.base_agent import BaseMonetizationAgent
from .portfolio_manager import PortfolioManager
from .risk_calculator import RiskCalculator

class MonetizationOrchestrator:
    """
    Coordinates all 9 monetization agents.
    - Initializes agents with shared core logic.
    - Manages execution schedule and parallel monitoring.
    - Aggregates status for the TUI Dashboard.
    """
    
    def __init__(self):
        self.logger = logging.getLogger("MonetizationOrchestrator")
        self.is_running = False
        
        # 1. Initialize Core Infrastructure
        self.portfolio = PortfolioManager(initial_capital=5000.0)
        self.risk = RiskCalculator()
        
        # 2. Initialize Agents (Passing core components)
        solana_rpc = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
        
        self.agents: Dict[str, BaseMonetizationAgent] = {
            'staking': StakingAgent(self.portfolio, self.risk, solana_rpc=solana_rpc),
            # Other agents will be added as they are implemented
        }
        
        # Track agent health and findings for UI
        self.status_registry = {
            name: {"status": "Idle", "last_run": None, "opportunities": 0} 
            for name in ['staking', 'arbitrage', 'lending', 'nft', 'freelance', 'airdrop', 'node', 'content', 'rwa']
        }

    async def start(self):
        """Start the parallel execution loop."""
        self.logger.info("Terminal 221B Monetization Engine Started.")
        self.is_running = True
        
        while self.is_running:
            try:
                await self.run_iteration()
                await asyncio.sleep(1) # Reduced for testing
            except Exception as e:
                self.logger.error(f"Orchestrator Loop Error: {e}")
                await asyncio.sleep(10)

    async def run_iteration(self):
        """Run all active agents in parallel."""
        self.logger.info("Iteration Started...")
        
        # Only run implemented agents
        active_agents = {k: v for k, v in self.agents.items() if v is not None}
        
        tasks = [self._run_agent(name, agent) for name, agent in active_agents.items()]
        await asyncio.gather(*tasks)
        
        # Periodic Rebalance Check
        self.portfolio.rebalance()

    async def _run_agent(self, name: str, agent: BaseMonetizationAgent):
        """Internal wrapper to run a single agent and update UI state."""
        try:
            self.status_registry[name]["status"] = "Scanning"
            result = await agent.monitor()
            
            opps = result.get('opportunities', [])
            self.status_registry[name]["opportunities"] = len(opps)
            self.status_registry[name]["last_run"] = asyncio.get_event_loop().time()
            
            for opp in opps:
                self.logger.info(f"Agent {name} found opportunity: {opp['title']}")
                # Automated execution based on risk profile
                await agent.execute(opp)
                
            self.status_registry[name]["status"] = "Success" if opps else "Idle"
            
        except Exception as e:
            self.logger.error(f"Agent {name} Execution Error: {e}")
            self.status_registry[name]["status"] = "Error"

    def stop(self):
        self.is_running = False
        self.logger.info("Monetization Engine Stopped.")
