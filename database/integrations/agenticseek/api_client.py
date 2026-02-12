"""
AgenticSeek API Client (GPL-3.0)
Isolated integration for web automation

This file is licensed under GPL-3.0 to comply with AgenticSeek's license.
It is kept separate from the proprietary Energetic Lexicon core.

Communication with core happens ONLY via JSON/REST API boundaries.

AgenticSeek: https://github.com/Fosowl/agenticSeek
License: GPL-3.0
"""

import requests
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class AgenticSeekClient:
    """
    Client for AgenticSeek Web Automation (GPL-3.0)

    AgenticSeek is a fully local AI assistant for web browsing,
    code generation, and automation.

    This client provides:
    - Web search capabilities
    - URL scraping and content extraction
    - GitHub repository analysis
    - Automated web navigation
    """

    def __init__(self, base_url: str = "http://localhost:5000"):
        """
        Initialize AgenticSeek client

        Args:
            base_url: AgenticSeek API endpoint
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

        logger.info(f"Initialized AgenticSeek client: {base_url}")

    def web_search(
        self,
        query: str,
        max_results: int = 10
    ) -> Dict[str, Any]:
        """
        Execute web search via AgenticSeek

        Uses SearxNG integration for privacy-focused search.

        Args:
            query: Search query
            max_results: Maximum number of results

        Returns:
            dict: {
                'query': str,
                'results': List[{
                    'title': str,
                    'url': str,
                    'snippet': str
                }]
            }
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/search",
                json={
                    "query": query,
                    "max_results": max_results
                }
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Web search failed: {e}")
            return {
                'query': query,
                'results': [],
                'error': str(e)
            }

    def scrape_url(
        self,
        url: str,
        extract_type: str = "text"
    ) -> Dict[str, Any]:
        """
        Scrape URL content using AgenticSeek

        Uses Selenium with stealth mode for undetected scraping.

        Args:
            url: URL to scrape
            extract_type: text, html, markdown

        Returns:
            dict: {
                'url': str,
                'content': str,
                'metadata': dict
            }
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/scrape",
                json={
                    "url": url,
                    "extract_type": extract_type
                }
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"URL scraping failed: {e}")
            return {
                'url': url,
                'content': '',
                'error': str(e)
            }

    def extract_repo_metadata(
        self,
        repo_url: str
    ) -> Dict[str, Any]:
        """
        Extract GitHub repository metadata using AgenticSeek

        Scrapes repository page for comprehensive metadata.

        Args:
            repo_url: GitHub repository URL

        Returns:
            dict: {
                'name': str,
                'description': str,
                'stars': int,
                'forks': int,
                'language': str,
                'topics': List[str],
                'readme': str
            }
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/github/analyze",
                json={"repo_url": repo_url}
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Repo metadata extraction failed: {e}")
            return {
                'name': '',
                'description': '',
                'error': str(e)
            }

    def browse_and_extract(
        self,
        url: str,
        instructions: str
    ) -> str:
        """
        Browse URL and extract content based on instructions

        Uses AgenticSeek's AI agent to navigate and extract data.

        Args:
            url: Starting URL
            instructions: Natural language instructions

        Returns:
            str: Extracted content
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/browse/agent",
                json={
                    "url": url,
                    "instructions": instructions
                }
            )
            response.raise_for_status()
            return response.json()['content']

        except requests.exceptions.RequestException as e:
            logger.error(f"Agent browsing failed: {e}")
            return f"ERROR: {str(e)}"

    def health_check(self) -> bool:
        """
        Check if AgenticSeek is available

        Returns:
            bool: True if AgenticSeek is responding
        """
        try:
            response = self.session.get(
                f"{self.base_url}/health",
                timeout=5
            )
            return response.status_code == 200

        except requests.exceptions.RequestException:
            return False

    def __repr__(self):
        return f"<AgenticSeekClient(base_url='{self.base_url}')>"
