import time
from typing import Dict, List, Any

class HumanAuditInterface:
    """
    Human-in-the-loop audit interface for query processing and session management
    """
    def __init__(self):
        self.active_sessions = {}
        self.query_history = []
        self.audit_permissions = {
            'query': ['analyst', 'auditor'],
            'override': ['auditor'],
            'threshold_adjust': ['admin']
        }

    def create_audit_session(self, graph_data: Dict[str, Any], anomalies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a new audit session
        """
        session_id = f"audit_{int(time.time())}"

        session = {
            'session_id': session_id,
            'created_at': time.time(),
            'status': 'active',
            'graph_summary': {
                'entities': len(graph_data.get('entities', [])),
                'anomalies': len(anomalies),
                'high_priority_anomalies': sum(1 for a in anomalies if a.get('confidence', 0) > 0.8)
            },
            'permissions': ['query', 'override', 'threshold_adjust'],
            'query_count': 0,
            'last_activity': time.time()
        }

        self.active_sessions[session_id] = session

        return session

    def process_custom_query(self, session_id: str, query_text: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process custom audit query
        """
        if session_id not in self.active_sessions:
            raise ValueError(f"Invalid session ID: {session_id}")

        session = self.active_sessions[session_id]
        session['query_count'] += 1
        session['last_activity'] = time.time()

        # Parse query and extract entities
        query_lower = query_text.lower()
        matching_entities = []

        # Simple keyword-based entity matching
        entity_keywords = {
            'government_official': ['deese', 'adeyemo', 'pyle', 'blass', 'fink', 'kapito', 'wagner'],
            'financial_institution': ['blackrock', 'vanguard', 'state_street', 'fed', 'treasury', 'sec'],
            'political_party': ['democrat', 'republican'],
            'policy_area': ['esg', 'climate', 'regulation', 'lobbying']
        }

        for category, keywords in entity_keywords.items():
            if parameters.get('entity_type') == category or any(kw in query_lower for kw in keywords):
                for keyword in keywords:
                    if keyword in query_lower:
                        matching_entities.append({
                            'entity': keyword.title(),
                            'category': category,
                            'relevance': 0.8 + 0.1 * len([k for k in keywords if k in query_lower]),
                            'confidence': 0.85
                        })

        # Add some mock results if no matches found
        if not matching_entities:
            mock_entities = [
                {'entity': 'Brian_Deese', 'category': 'government_official', 'relevance': 0.95, 'confidence': 0.9},
                {'entity': 'BlackRock_Inc', 'category': 'financial_institution', 'relevance': 0.89, 'confidence': 0.87},
                {'entity': 'Biden_Administration', 'category': 'government_official', 'relevance': 0.87, 'confidence': 0.85}
            ]
            matching_entities.extend(mock_entities[:parameters.get('limit', 3)])

        # Sort by relevance
        matching_entities.sort(key=lambda x: x['relevance'], reverse=True)

        # Limit results
        limit = parameters.get('limit', 10)
        matching_entities = matching_entities[:limit]

        # Log query
        query_record = {
            'session_id': session_id,
            'timestamp': time.time(),
            'query_text': query_text,
            'parameters': parameters,
            'result_count': len(matching_entities),
            'processing_time': 0.5  # Mock processing time
        }
        self.query_history.append(query_record)

        return {
            'query': query_text,
            'matching_entities': matching_entities,
            'result_count': len(matching_entities),
            'processing_time': 0.5,
            'session_info': {
                'session_id': session_id,
                'total_queries': session['query_count']
            }
        }

    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """
        Get audit session status
        """
        if session_id not in self.active_sessions:
            return {'error': 'Session not found'}

        session = self.active_sessions[session_id]

        # Check if session is expired (24 hours)
        if time.time() - session['created_at'] > 86400:
            session['status'] = 'expired'

        return {
            'session_id': session_id,
            'status': session['status'],
            'created_at': session['created_at'],
            'query_count': session['query_count'],
            'last_activity': session['last_activity'],
            'time_elapsed': time.time() - session['created_at']
        }

    def close_audit_session(self, session_id: str) -> Dict[str, Any]:
        """
        Close an audit session
        """
        if session_id not in self.active_sessions:
            return {'error': 'Session not found'}

        session = self.active_sessions[session_id]
        session['status'] = 'closed'
        session['closed_at'] = time.time()

        return {
            'session_id': session_id,
            'status': 'closed',
            'total_queries': session['query_count'],
            'duration': session['closed_at'] - session['created_at']
        }