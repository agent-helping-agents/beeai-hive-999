import asyncio
import logging
import sys
import os

# Add root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from terminal221b.monetization.core.portfolio_manager import PortfolioManager
from terminal221b.monetization.core.risk_calculator import RiskCalculator
from terminal221b.monetization.agents.staking_agent import StakingAgent

async def test_flow():
    logging.basicConfig(level=logging.INFO)
    print("--- 🧪 Starting Monetization Core Test ---")
    
    # 1. Setup Core
    portfolio = PortfolioManager(initial_capital=5000.0)
    risk = RiskCalculator()
    
    # 2. Setup Agent
    agent = StakingAgent(portfolio, risk)
    
    # Mock Solana balance for testing (override actual RPC call)
    async def mock_get_balance(pk): return 10.5 # 10.5 SOL
    async def mock_stake_sol(amt, val): return True
    
    agent.solana.get_balance = mock_get_balance
    agent.solana.stake_sol = mock_stake_sol
    
    print("\n[Step 1] Monitoring for Opportunities...")
    data = await agent.monitor()
    opps = data['opportunities']
    
    if not opps:
        print("No opportunities found.")
    
    for opp in opps:
        print(f"Found: {opp['title']} | Amount: {opp['amount']} SOL | APY: {opp['expected_apy']:.1%}")
        
        print("\n[Step 2] Executing Opportunity...")
        await agent.execute(opp)
        
    print("\n[Step 3] Verifying State...")
    print(f"Total Portfolio Value: ${portfolio.get_total_value():,.2f}")
    print(f"SOL Balance: {portfolio.holdings['SOL']} SOL")
    print(f"Agent Accuracy: {agent.performance.get_accuracy():.1%}")
    
    print("\n--- ✅ Test Complete ---")

if __name__ == "__main__":
    asyncio.run(test_flow())
