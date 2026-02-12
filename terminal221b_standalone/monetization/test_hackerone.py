import asyncio
import logging
from monetization.integrations.bounty.hackerone import HackerOneClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_hackerone_client():
    """
    Tests the HackerOneClient locally with placeholder credentials.
    """
    logger.info("Starting local test of HackerOneClient...")

    # IMPORTANT: Replace with your actual HackerOne credentials if you want to test against the real API.
    # For local testing, we'll use placeholders.
    HACKERONE_IDENTIFIER = os.getenv("HACKERONE_IDENTIFIER", "your_hackerone_username_or_email")
    HACKERONE_TOKEN = os.getenv("HACKERONE_TOKEN", "your_hackerone_api_token")

    if HACKERONE_IDENTIFIER == "your_hackerone_username_or_email" or HACKERONE_TOKEN == "your_hackerone_api_token":
        logger.warning("Using placeholder HackerOne credentials. Real API calls will fail without actual credentials.")
        logger.warning("Please set HACKERONE_IDENTIFIER and HACKERONE_TOKEN environment variables for real testing.")
        # Simulate API response for demonstration
        simulated_programs = [
            {'name': 'Example Program 1', 'url': 'https://hackerone.com/example1', 'state': 'active', 'type': 'public'},
            {'name': 'Solana DeFi Program', 'url': 'https://hackerone.com/solana_defi', 'state': 'active', 'type': 'private'},
            {'name': 'Another Test Program', 'url': 'https://hackerone.com/test_program', 'state': 'inactive', 'type': 'public'},
        ]
        logger.info("Simulating HackerOne API calls due to missing credentials.")
        hackerone_client = HackerOneClient() # Initialize without real credentials
        
        # Simulate get_programs behavior
        hackerone_client.get_programs = lambda: asyncio.sleep(0.1, result=simulated_programs)
        
        # Simulate find_bounties behavior
        async def simulated_find_bounties(query_str: str = ""):
            if not query_str:
                return simulated_programs
            lower_query = query_str.lower()
            return [p for p in simulated_programs if lower_query in p['name'].lower() or lower_query in p['url'].lower()]
        hackerone_client.find_bounties = simulated_find_bounties
    else:
        hackerone_client = HackerOneClient(HACKERONE_IDENTIFIER, HACKERONE_TOKEN)
        logger.info("HackerOneClient initialized with provided credentials.")

    try:
        programs = await hackerone_client.get_programs()
        logger.info(f"
--- HackerOne Programs ({len(programs)} found) ---")
        for p in programs:
            logger.info(f"  - {p.get('name')} (Status: {p.get('state')}) - {p.get('url')}")

        search_query = "Solana"
        solana_bounties = await hackerone_client.find_bounties(search_query)
        logger.info(f"
--- HackerOne Bounties matching '{search_query}' ({len(solana_bounties)} found) ---")
        for b in solana_bounties:
            logger.info(f"  - {b.get('name')} (Platform: {b.get('platform')}) - {b.get('url')}")

    except Exception as e:
        logger.error(f"Error during HackerOneClient test: {e}")

if __name__ == "__main__":
    import os
    # Ensure this script can find the monetization package for import
    # Add project root to sys.path if not already there
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    asyncio.run(test_hackerone_client())