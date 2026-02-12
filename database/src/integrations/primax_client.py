"""
PRIMAX Integration Client
🔒 PRIVATE - PROPRIETARY
© 2025 Baker Street Laboratory

Connects Energetic Lexicon to PRIMAX neuromorphic AI runtime.
PRIMAX provides self-learning capabilities and dynamic tool discovery.
"""

import requests
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class PRIMAXClient:
    """
    Client for PRIMAX AI Runtime Integration

    PRIMAX is a self-learning neuromorphic AI system with AutomationCodex.
    This client provides:
    - Concept understanding and expansion
    - Tool discovery
    - Automation execution
    - Graph resilience analysis
    """

    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        """
        Initialize PRIMAX client

        Args:
            base_url: PRIMAX API endpoint
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()

        if api_key:
            self.session.headers['Authorization'] = f"Bearer {api_key}"

        logger.info(f"Initialized PRIMAX client: {base_url}")

    def query_lexicon(self, concept: str) -> Dict[str, Any]:
        """
        Query PRIMAX for concept understanding

        Uses PRIMAX's neuromorphic reasoning to expand concept definitions
        from the Energetic Lexicon with graph-theory-informed relationships.

        Args:
            concept: Concept term to query

        Returns:
            dict: {
                'term': str,
                'definition': str,
                'related_concepts': List[str],
                'graph_metrics': dict,
                'automation_patterns': List[str]
            }
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/lexicon/query",
                json={"concept": concept}
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"PRIMAX lexicon query failed: {e}")
            return {
                'term': concept,
                'definition': 'ERROR: PRIMAX unavailable',
                'related_concepts': [],
                'graph_metrics': {},
                'automation_patterns': []
            }

    def discover_tools(self) -> List[Dict[str, Any]]:
        """
        Discover available tools from PRIMAX runtime

        PRIMAX maintains a dynamic registry of tools and capabilities.

        Returns:
            list: [{
                'name': str,
                'description': str,
                'capabilities': List[str],
                'automation_codex_role': str
            }]
        """
        try:
            response = self.session.get(f"{self.base_url}/api/tools")
            response.raise_for_status()
            return response.json()['tools']

        except requests.exceptions.RequestException as e:
            logger.error(f"PRIMAX tool discovery failed: {e}")
            return []

    def execute_automation(
        self,
        automation_id: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute AutomationCodex pattern via PRIMAX

        PRIMAX uses graph theory and information theory to optimize
        automation execution paths.

        Args:
            automation_id: Automation pattern identifier
            params: Execution parameters

        Returns:
            dict: {
                'success': bool,
                'result': Any,
                'graph_metrics': dict,
                'execution_path': List[str]
            }
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/automation/{automation_id}",
                json=params or {}
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"PRIMAX automation execution failed: {e}")
            return {
                'success': False,
                'result': None,
                'error': str(e)
            }

    def analyze_graph_resilience(
        self,
        graph_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze knowledge graph resilience using PRIMAX

        Uses graph theory metrics to assess robustness:
        - Betweenness centrality
        - Clustering coefficient
        - Community detection

        Args:
            graph_data: Graph structure {nodes: [], edges: []}

        Returns:
            dict: {
                'resilience_score': float,
                'critical_nodes': List[str],
                'communities': List[List[str]],
                'metrics': dict
            }
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/graph/analyze",
                json=graph_data
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"PRIMAX graph analysis failed: {e}")
            return {
                'resilience_score': 0.0,
                'critical_nodes': [],
                'communities': [],
                'metrics': {}
            }

    def health_check(self) -> bool:
        """
        Check if PRIMAX runtime is available

        Returns:
            bool: True if PRIMAX is responding
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
        return f"<PRIMAXClient(base_url='{self.base_url}')>"
