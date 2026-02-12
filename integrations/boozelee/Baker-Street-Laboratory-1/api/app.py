#!/usr/bin/env python3
"""
Baker Street Laboratory - REST API Server
Main Flask application providing REST API endpoints for the research framework.
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource, fields, Namespace
from werkzeug.exceptions import BadRequest, InternalServerError

# Add the implementation src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "implementation" / "src"))

from core.config import Config
from core.logger import setup_logging, get_logger
from orchestrator.research_orchestrator import ResearchOrchestrator
from utils.environment import check_environment

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Flask-RESTX
api = Api(
    version='1.0',
    title='Baker Street Laboratory API',
    description='AI-Augmented Research Framework API',
    doc='/docs/',
    prefix='/api/v1'
)

# Setup logging
logger = setup_logging(level="INFO")
app_logger = get_logger(__name__)

# Global configuration
config = None
orchestrator = None

def initialize_app():
    """Initialize the application with configuration and orchestrator."""
    global config, orchestrator
    
    try:
        # Load configuration
        config_path = Path(__file__).parent.parent / "config" / "agents.yaml"
        config = Config.from_file(str(config_path))
        
        # Initialize orchestrator
        orchestrator = ResearchOrchestrator(config)
        
        app_logger.info("Baker Street Laboratory API initialized successfully")
        return True
        
    except Exception as e:
        app_logger.error(f"Failed to initialize application: {e}")
        return False

# API Namespaces
research_ns = Namespace('research', description='Research operations')
system_ns = Namespace('system', description='System status and health')
reports_ns = Namespace('reports', description='Research reports management')

# Initialize API with app
api.init_app(app)

api.add_namespace(research_ns)
api.add_namespace(system_ns)
api.add_namespace(reports_ns)

# API Models for documentation
research_query_model = api.model('ResearchQuery', {
    'query': fields.String(required=True, description='Research question or topic'),
    'output_dir': fields.String(description='Output directory for results', default='research/api_output')
})

research_response_model = api.model('ResearchResponse', {
    'session_id': fields.String(description='Unique session identifier'),
    'query': fields.String(description='Original research query'),
    'status': fields.String(description='Research status'),
    'timestamp': fields.String(description='Completion timestamp'),
    'summary': fields.String(description='Research summary'),
    'report_path': fields.String(description='Path to generated report'),
    'output_dir': fields.String(description='Output directory')
})

system_status_model = api.model('SystemStatus', {
    'status': fields.String(description='Overall system status'),
    'timestamp': fields.String(description='Status check timestamp'),
    'components': fields.Raw(description='Component status details'),
    'version': fields.String(description='API version')
})

# Research Endpoints
@research_ns.route('/conduct')
class ConductResearch(Resource):
    @research_ns.expect(research_query_model)
    @research_ns.marshal_with(research_response_model)
    @research_ns.doc('conduct_research')
    def post(self):
        """Conduct a research session with the provided query."""
        try:
            data = request.get_json()
            
            if not data or 'query' not in data:
                raise BadRequest("Query is required")
            
            query = data['query']
            output_dir = data.get('output_dir', 'research/api_output')
            
            app_logger.info(f"Starting research session for query: {query}")
            
            # Run the research orchestrator
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                results = loop.run_until_complete(
                    orchestrator.conduct_research(query, output_dir)
                )
            finally:
                loop.close()
            
            app_logger.info(f"Research completed for session: {results.get('session_id')}")
            return results
            
        except Exception as e:
            app_logger.error(f"Research failed: {e}")
            raise InternalServerError(f"Research failed: {str(e)}")

@research_ns.route('/status/<string:session_id>')
class ResearchStatus(Resource):
    @research_ns.doc('get_research_status')
    def get(self, session_id):
        """Get the status of a specific research session."""
        try:
            # In a full implementation, this would check session status from database
            # For now, return a mock status
            return {
                'session_id': session_id,
                'status': 'completed',
                'timestamp': datetime.now().isoformat(),
                'message': 'Research session status retrieved'
            }
        except Exception as e:
            app_logger.error(f"Failed to get research status: {e}")
            raise InternalServerError(f"Failed to get status: {str(e)}")

# System Endpoints
@system_ns.route('/health')
class SystemHealth(Resource):
    @system_ns.marshal_with(system_status_model)
    @system_ns.doc('system_health')
    def get(self):
        """Get system health status."""
        try:
            # Check environment
            env_status = check_environment()
            
            # Get orchestrator status
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                orchestrator_status = loop.run_until_complete(orchestrator.get_status())
            finally:
                loop.close()
            
            status = {
                'status': 'healthy' if env_status['overall_status'] else 'unhealthy',
                'timestamp': datetime.now().isoformat(),
                'components': {
                    'environment': env_status,
                    'orchestrator': orchestrator_status,
                    'api': 'running'
                },
                'version': '1.0.0'
            }
            
            return status
            
        except Exception as e:
            app_logger.error(f"Health check failed: {e}")
            return {
                'status': 'unhealthy',
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'version': '1.0.0'
            }

@system_ns.route('/info')
class SystemInfo(Resource):
    @system_ns.doc('system_info')
    def get(self):
        """Get system information."""
        return {
            'name': 'Baker Street Laboratory API',
            'version': '1.0.0',
            'description': 'AI-Augmented Research Framework',
            'timestamp': datetime.now().isoformat(),
            'endpoints': {
                'research': '/api/v1/research/',
                'system': '/api/v1/system/',
                'reports': '/api/v1/reports/',
                'documentation': '/docs/'
            }
        }

# Reports Endpoints
@reports_ns.route('/list')
class ListReports(Resource):
    @reports_ns.doc('list_reports')
    def get(self):
        """List all available research reports."""
        try:
            reports_dir = Path("research")
            reports = []
            
            if reports_dir.exists():
                for report_file in reports_dir.glob("research_report_*.md"):
                    reports.append({
                        'filename': report_file.name,
                        'path': str(report_file),
                        'size': report_file.stat().st_size,
                        'created': datetime.fromtimestamp(report_file.stat().st_ctime).isoformat()
                    })
            
            return {
                'reports': reports,
                'count': len(reports),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            app_logger.error(f"Failed to list reports: {e}")
            raise InternalServerError(f"Failed to list reports: {str(e)}")

@reports_ns.route('/<string:report_id>')
class GetReport(Resource):
    @reports_ns.doc('get_report')
    def get(self, report_id):
        """Get a specific research report."""
        try:
            report_path = Path(f"research/research_report_{report_id}.md")
            
            if not report_path.exists():
                return {'error': 'Report not found'}, 404
            
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                'report_id': report_id,
                'content': content,
                'path': str(report_path),
                'size': len(content),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            app_logger.error(f"Failed to get report: {e}")
            raise InternalServerError(f"Failed to get report: {str(e)}")

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Root endpoint
@app.route('/')
def api_root():
    """Root endpoint with API information."""
    return jsonify({
        'name': 'Baker Street Laboratory API',
        'version': '1.0.0',
        'status': 'running',
        'documentation': '/docs/',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Initialize the application
    if not initialize_app():
        sys.exit(1)
    
    # Run the Flask development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
