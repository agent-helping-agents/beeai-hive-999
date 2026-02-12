import asyncio
import json
import logging
import os
import sys

# Assume the monetization root is added to sys.path in the sandbox
# For local testing, you might need to adjust sys.path manually
# e.g., sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

# Import the StakingAgent and its dependencies
from monetization.agents.staking_agent import StakingAgent
from monetization.integrations.blockchain.solana import SolanaIntegration

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def run_staking_monitor():
    """
    Initializes StakingAgent, runs its monitor method, and prints results as JSON.
    """
    logger.info("Initializing StakingAgent for Daytona sandbox execution.")
    
    # Initialize SolanaIntegration. In a real scenario, RPC URL might come from environment variables.
    solana_rpc_url = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
    solana_integration = SolanaIntegration(rpc_url=solana_rpc_url)
    
    # Pass solana_integration if StakingAgent needs it directly, or let StakingAgent instantiate it.
    # Our StakingAgent currently instantiates it, so we can stick to that.
    staking_agent = StakingAgent(solana_rpc=solana_rpc_url)

    try:
        opportunities = await staking_agent.monitor()
        result = {"status": "success", "opportunities": opportunities}
        print(json.dumps(result, indent=2))
        logger.info("StakingAgent monitor execution complete.")
    except Exception as e:
        logger.error(f"Error during StakingAgent monitor execution: {e}", exc_info=True)
        result = {"status": "error", "message": str(e)}
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(run_staking_monitor())
