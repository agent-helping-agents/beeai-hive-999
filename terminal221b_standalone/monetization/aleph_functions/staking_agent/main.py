import asyncio
import json
import logging
import os
import sys

from aleph_client.vm.app import AlephApp, app
from aleph_client.vm.cache import aleph_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Adjust sys.path to allow importing from the parent 'monetization' directory
# This assumes main.py is in '.../monetization/aleph_functions/staking_agent'
# and the actual agent is in '.../monetization/agents'
current_dir = os.path.dirname(os.path.abspath(__file__))
monetization_root = os.path.abspath(os.path.join(current_dir, "../../.."))
sys.path.insert(0, monetization_root)

# Now, import the StakingAgent from the project structure
from monetization.agents.staking_agent import StakingAgent
from monetization.integrations.blockchain.solana import SolanaIntegration


# Initialize the AlephApp
# Using a global app instance for simplicity
app = AlephApp()

# Instantiate the StakingAgent globally or within the request handler
# For a persistent VM, this could be global. For a stateless function, it might be in the handler.
# For now, we'll instantiate it per request/event to keep it stateless.

@app.event(event_type="message", channels=["STAKING_AGENT_COMMAND"])
async def process_command(message):
    """
    Aleph function entry point to process commands from a message.
    """
    logger.info(f"Received message: {message.content.decode()}")
    try:
        command = json.loads(message.content.decode())
        action = command.get("action")

        staking_agent = StakingAgent() # Instantiate per request
        solana_integration = SolanaIntegration() # Instantiate per request

        if action == "monitor":
            opportunities = await staking_agent.monitor()
            # Post results back to Aleph message channel or return HTTP response if applicable
            return {"status": "success", "opportunities": opportunities}
        elif action == "execute":
            opportunity = command.get("opportunity")
            if opportunity:
                await staking_agent.execute(opportunity)
                return {"status": "success", "message": "Execution initiated."}
            else:
                return {"status": "error", "message": "Missing opportunity for execution."}
        else:
            return {"status": "error", "message": "Unknown action."}
    except Exception as e:
        logger.exception("Error processing message in StakingAgent Aleph function")
        return {"status": "error", "message": str(e)}

@app.http("/monitor-staking")
async def http_monitor_staking():
    """
    HTTP endpoint to trigger the staking agent monitor and return opportunities.
    """
    logger.info("HTTP monitor-staking endpoint called.")
    try:
        staking_agent = StakingAgent()
        opportunities = await staking_agent.monitor()
        return {"status": "success", "opportunities": opportunities}
    except Exception as e:
        logger.exception("Error in HTTP monitor-staking endpoint")
        return {"status": "error", "message": str(e)}, 500

# Example of using Aleph cache (optional)
@app.event(event_type="message", channels=["CACHE_TEST"])
async def cache_test(message):
    key = message.content.decode()
    with aleph_cache(key) as cache:
        if cache.value is None:
            cache.value = {"data": "This is cached data", "timestamp": os.time()}
            return {"status": "cached_new", "data": cache.value}
        else:
            return {"status": "cached_existing", "data": cache.value}
