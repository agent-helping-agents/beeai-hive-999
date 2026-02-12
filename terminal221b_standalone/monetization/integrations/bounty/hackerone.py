import aiohttp
import logging
from typing import List, Dict, Optional

class HackerOneClient:
    """
    API client for HackerOne bounty platform.
    Documentation: https://api.hackerone.com/v1/
    """
    
    def __init__(self, identifier: Optional[str] = None, token: Optional[str] = None):
        self.base_url = "https://api.hackerone.com/v1"
        self.auth = aiohttp.BasicAuth(identifier, token) if identifier and token else None
        self.logger = logging.getLogger("HackerOneClient")
        if not self.auth:
            self.logger.warning("HackerOneClient initialized without authentication. Some API calls may fail.")

    async def _make_request(self, method: str, path: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Helper to make authenticated API requests."""
        url = f"{self.base_url}{path}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method, url, params=params, auth=self.auth) as response:
                    response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
                    return await response.json()
            except aiohttp.ClientResponseError as e:
                self.logger.error(f"HackerOne API request failed (HTTP {e.status}): {e.message} for {url}")
            except aiohttp.ClientConnectionError as e:
                self.logger.error(f"HackerOne API connection failed: {e} for {url}")
            except Exception as e:
                self.logger.error(f"Unexpected error during HackerOne API request: {e} for {url}")
        return None

    async def get_programs(self) -> List[Dict]:
        """Fetch active bounty programs accessible to the authenticated user."""
        self.logger.info("Fetching HackerOne programs...")
        data = await self._make_request("GET", "/me/programs")
        if data and 'data' in data:
            # HackerOne API returns programs as a list of dictionaries,
            # each with an 'attributes' key containing details.
            return [program['attributes'] for program in data['data']]
        return []

    async def find_bounties(self, query: str = "") -> List[Dict]:
        """Search for relevant bounties based on keywords in program names or descriptions."""
        self.logger.info(f"Searching HackerOne for bounties matching '{query}'...")
        programs = await self.get_programs()
        
        found_bounties = []
        lower_query = query.lower() if query else ""

        for program in programs:
            program_name = program.get('name', '').lower()
            program_description = program.get('submission_state', {}).get('description', '').lower() # Assuming relevant description field
            
            # Simple keyword matching
            if lower_query in program_name or lower_query in program_description:
                # For now, return the program itself as a "bounty"
                found_bounties.append({
                    "name": program.get('name'),
                    "platform": "HackerOne",
                    "url": program.get('url'),
                    "state": program.get('state'),
                    "type": program.get('type'),
                    "reimbursement": program.get('reimbursement_state') # Example of another attribute
                })
        self.logger.info(f"Found {len(found_bounties)} HackerOne bounties matching '{query}'.")
        return found_bounties
