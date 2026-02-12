import aiohttp
import logging
from typing import List, Dict, Optional

class BugcrowdClient:
    """
    API client for Bugcrowd bounty platform.
    Documentation: https://api.bugcrowd.com/v1/
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.base_url = "https://api.bugcrowd.com/v1"
        self.headers = {
            "Accept": "application/vnd.bugcrowd.v4+json", # Bugcrowd API uses a specific Accept header
            "Authorization": f"Token {api_key}" if api_key else ""
        }
        self.logger = logging.getLogger("BugcrowdClient")
        if not api_key:
            self.logger.warning("BugcrowdClient initialized without API key. Some API calls may fail.")

    async def _make_request(self, method: str, path: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Helper to make authenticated API requests."""
        url = f"{self.base_url}{path}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method, url, params=params, headers=self.headers) as response:
                    response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
                    return await response.json()
            except aiohttp.ClientResponseError as e:
                self.logger.error(f"Bugcrowd API request failed (HTTP {e.status}): {e.message} for {url}")
            except aiohttp.ClientConnectionError as e:
                self.logger.error(f"Bugcrowd API connection failed: {e} for {url}")
            except Exception as e:
                self.logger.error(f"Unexpected error during Bugcrowd API request: {e} for {url}")
        return None

    async def get_programs(self) -> List[Dict]:
        """Fetch all available Bugcrowd programs."""
        self.logger.info("Fetching Bugcrowd programs...")
        data = await self._make_request("GET", "/programs")
        if data and 'programs' in data:
            # Bugcrowd API returns programs as a list of dictionaries,
            # each representing a program with its details.
            return data['programs']
        return []

    async def find_bounties(self, query: str = "") -> List[Dict]:
        """Search for relevant Bugcrowd bounties based on keywords in program names or descriptions."""
        self.logger.info(f"Searching Bugcrowd for bounties matching '{query}'...")
        programs = await self.get_programs()
        
        found_bounties = []
        lower_query = query.lower() if query else ""

        for program in programs:
            program_name = program.get('name', '').lower()
            program_description = program.get('brief', '').lower() # 'brief' often contains a description
            
            # Simple keyword matching
            if lower_query in program_name or lower_query in program_description:
                # For now, return the program itself as a "bounty"
                found_bounties.append({
                    "name": program.get('name'),
                    "platform": "Bugcrowd",
                    "url": program.get('bug_url'), # URL to the program on Bugcrowd
                    "state": program.get('state'),
                    "target_types": [target.get('type') for target in program.get('target_groups', [])] # Example of extracting target types
                })
        self.logger.info(f"Found {len(found_bounties)} Bugcrowd bounties matching '{query}'.")
        return found_bounties
