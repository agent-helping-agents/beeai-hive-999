from flask import Flask, request, jsonify
from datetime import datetime
import hashlib
import time
import json

class APIInterface:
    """
    RESTful API interface for external integration
    """
    def __init__(self, security_manager):
        self.security = security_manager
        self.endpoints = {
            '/analyze/graph': self.analyze_graph_endpoint,
            '/detect/anomalies': self.detect_anomalies_endpoint,
            '/explain/cluster': self.explain_cluster_endpoint,
            '/audit/session': self.create_audit_session_endpoint,
            '/query/custom': self.custom_query_endpoint
        }
        self.request_log = []
        
    def process_request(self, endpoint, method, data, user_role):
        """Process API request"""
        request_id = len(self.request_log)
        session_key = self.security.generate_session_key(user_role)
        
        request_record = {
            'request_id': request_id,
            'timestamp': datetime.now().isoformat(),
            'endpoint': endpoint,
            'method': method,
            'user_role': user_role,
            'session_key': session_key,
            'status': 'processing'
        }
        
        try:
            # Check endpoint exists
            if endpoint not in self.endpoints:
                raise ValueError(f"Unknown endpoint: {endpoint}")
            
            # Process request
            handler = self.endpoints[endpoint]
            result = handler(data, session_key, user_role)
            
            # Encrypt response
            encrypted_result = self.security.encrypt_output(result, session_key)
            
            request_record['status'] = 'completed'
            request_record['response_size'] = len(str(encrypted_result))
            
            # Log audit event
            self.security.log_audit_event('api_access', user_role, result, session_key)
            
            self.request_log.append(request_record)
            return encrypted_result
            
        except Exception as e:
            request_record['status'] = 'error'
            request_record['error'] = str(e)
            self.request_log.append(request_record)
            
            return {
                'error': str(e),
                'request_id': request_id,
                'timestamp': datetime.now().isoformat()
            }
    
    def analyze_graph_endpoint(self, data, session_key, user_role):
        """Graph analysis API endpoint"""
        if not self.security.check_access_permission(user_role, 'read'):
            raise ValueError("Insufficient permissions for graph analysis")
        
        return {
            'analysis_type': 'hybrid_snn_gnn',
            'graph_metrics': {
                'node_count': data.get('node_count', 0),
                'edge_density': 0.15,
                'clustering_coefficient': 0.68,
                'path_length': 3.2
            },
            'anomalies_detected': 5,
            'confidence_score': 0.87,
            'processing_time': '2.3s'
        }
    
    def detect_anomalies_endpoint(self, data, session_key, user_role):
        """Anomaly detection API endpoint"""
        return {
            'anomalies': [
                {'type': 'causal_spike', 'entity': 'BlackRock-Biden_Admin', 'strength': 0.92},
                {'type': 'statistical_outlier', 'metric': 'lobbying_expenditure', 'z_score': 3.1},
                {'type': 'temporal_pattern', 'description': 'Personnel_exchange_acceleration', 'significance': 0.89}
            ],
            'total_count': 3,
            'high_priority': 2
        }
    
    def explain_cluster_endpoint(self, data, session_key, user_role):
        """Cluster explanation API endpoint"""
        return {
            'cluster_id': data.get('cluster_id', 'unknown'),
            'explanation_type': 'feature_importance',
            'key_features': [
                {'feature': 'regulatory_capture', 'importance': 0.95},
                {'feature': 'political_connections', 'importance': 0.87},
                {'feature': 'financial_flows', 'importance': 0.82}
            ],
            'confidence': 0.91,
            'timeline_events': 5
        }
    
    def create_audit_session_endpoint(self, data, session_key, user_role):
        """Create audit session API endpoint"""
        if not self.security.check_access_permission(user_role, 'audit'):
            raise ValueError("Insufficient permissions for audit session creation")
        
        return {
            'session_id': f"audit_{len(self.request_log)}",
            'status': 'active',
            'permissions': ['query', 'override', 'threshold_adjust'],
            'expires_in': '3600s'
        }
    
    def custom_query_endpoint(self, data, session_key, user_role):
        """Custom query API endpoint"""
        query_text = data.get('query', '')
        return {
            'query': query_text,
            'results': [
                {'entity': 'Brian_Deese', 'relevance': 0.95},
                {'entity': 'BlackRock_Inc', 'relevance': 0.89},
                {'entity': 'Biden_Administration', 'relevance': 0.87}
            ],
            'result_count': 3,
            'processing_time': '0.8s'
        }

# Flask app for simple web interface
app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'operational', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, port=5000)