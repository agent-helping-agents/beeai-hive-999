import asyncio
import logging
import os
from dotenv import load_dotenv

# Add parent directory to path for imports
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from monetization.core.orchestrator import MonetizationOrchestrator
from monetization.ui.monetization_dashboard import MonetizationDashboard

async def main():
    # Load environment variables
    load_dotenv()

    # Configure Logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("monetization.log"),
            logging.StreamHandler(sys.stdout) # Keep stream handler for immediate feedback
        ]
    )
    
    # Initialize Orchestrator
    orchestrator = MonetizationOrchestrator()
    
    # Initialize and run the Textual UI.
    # The Dashboard will now manage starting/stopping the orchestrator in its own lifecycle.
    app = MonetizationDashboard(orchestrator)
    try:
        await app.run_async()
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt caught, shutting down UI.")
    
    logging.info("Terminal 221B Monetization Engine Shutdown Complete.")

if __name__ == "__main__":
    asyncio.run(main())