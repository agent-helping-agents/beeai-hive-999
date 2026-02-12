#!/usr/bin/env python3
"""
Baker Street Laboratory - Production API Server
Enhanced Flask application with rate limiting, caching, monitoring, and multiple data sources.
"""

import os
import sys
import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource, fields, Namespace
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from prometheus_flask_exporter import PrometheusMetrics
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.exceptions import BadRequest, InternalServerError, TooManyRequests

# External API integrations
import wikipedia
import arxiv
from newsapi import NewsApiClient

# Add the implementation src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "implementation" / "src"))

from core.config import Config
from core.logger import setup_logging, get_logger
from orchestrator.research_orchestrator import ResearchOrchestrator
from utils.environment import check_environment
from ai.ollama_client import OllamaClient

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config.update(

# Validate required environment variables
if not app.config['SECRET_KEY']:
    app_logger.error("SECRET_KEY environment variable is required")
    sys.exit(1)

    SECRET_KEY=os.getenv('SECRET_KEY'),
    CACHE_TYPE='simple',
    CACHE_DEFAULT_TIMEOUT=300,
    RATELIMIT_STORAGE_URL='memory://',
    RATELIMIT_DEFAULT='100 per hour'
)

# Initialize extensions
cache = Cache(app)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Initialize monitoring
metrics = PrometheusMetrics(app)
metrics.info('baker_street_api_info', 'Baker Street Laboratory API', version='2.0.0')

# Initialize Sentry for error tracking (if configured)
if os.getenv('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0
    )

# Configure Flask-RESTX
api = Api(
    version='2.0',
    title='Baker Street Laboratory Production API',
    description='AI-Augmented Research Framework with Multiple Data Sources',
    doc='/docs/',
    prefix='/api/v2'
)

# Initialize API with app
api.init_app(app)

# Setup logging
logger = setup_logging(level="INFO")
app_logger = get_logger(__name__)

# Global configuration
config = None
orchestrator = None
news_api = None
ollama_client = None

async def initialize_app():
    """Initialize the application with configuration and external APIs."""
    global config, orchestrator, news_api, ollama_client

    try:
        # Load configuration
        config_path = Path(__file__).parent.parent / "config" / "agents.yaml"
        config = Config.from_file(str(config_path))

        # Initialize orchestrator
        orchestrator = ResearchOrchestrator(config)
        await orchestrator.initialize()

        # Initialize Ollama client
        ollama_client = OllamaClient()
        ollama_available = await ollama_client.initialize()

        if ollama_available:
            app_logger.info("Ollama client initialized successfully")
        else:
            app_logger.warning("Ollama client not available")

        # Initialize News API (if configured)
        news_api_key = os.getenv('NEWS_API_KEY')
        if news_api_key:
            news_api = NewsApiClient(api_key=news_api_key)

        app_logger.info("Baker Street Laboratory Production API initialized successfully")
        return True

    except Exception as e:
        app_logger.error(f"Failed to initialize application: {e}")
        return False

# API Namespaces
research_ns = Namespace('research', description='Enhanced research operations')
system_ns = Namespace('system', description='System monitoring and health')
reports_ns = Namespace('reports', description='Research reports management')
data_ns = Namespace('data', description='External data source integration')
ollama_ns = Namespace('ollama', description='Local AI model operations')

api.add_namespace(research_ns)
api.add_namespace(system_ns)
api.add_namespace(reports_ns)
api.add_namespace(data_ns)
api.add_namespace(ollama_ns)

# Enhanced API Models
enhanced_research_query_model = api.model('EnhancedResearchQuery', {
    'query': fields.String(required=True, description='Research question or topic'),
    'output_dir': fields.String(description='Output directory for results', default='research/api_output'),
    'data_sources': fields.List(fields.String, description='Specific data sources to use', 
                                default=['wikipedia', 'arxiv', 'news']),
    'max_results': fields.Integer(description='Maximum results per source', default=10),
    'language': fields.String(description='Language preference', default='en')
})

data_source_response_model = api.model('DataSourceResponse', {
    'source': fields.String(description='Data source name'),
    'results': fields.Raw(description='Results from the data source'),
    'count': fields.Integer(description='Number of results'),
    'timestamp': fields.String(description='Query timestamp')
})

# Enhanced Research Endpoints
@research_ns.route('/conduct')
class EnhancedConductResearch(Resource):
    @research_ns.expect(enhanced_research_query_model)
    @limiter.limit("10 per minute")
    @cache.cached(timeout=300, query_string=True)
    def post(self):
        """Conduct enhanced research with multiple data sources."""
        try:
            data = request.get_json()
            
            if not data or 'query' not in data:
                raise BadRequest("Query is required")
            
            query = data['query']
            output_dir = data.get('output_dir', 'research/api_output')
            data_sources = data.get('data_sources', ['wikipedia', 'arxiv', 'news'])
            max_results = data.get('max_results', 10)
            
            app_logger.info(f"Starting enhanced research session for query: {query}")
            
            # Collect data from external sources
            external_data = {}
            
            # Wikipedia data
            if 'wikipedia' in data_sources:
                external_data['wikipedia'] = self._get_wikipedia_data(query, max_results)
            
            # ArXiv data
            if 'arxiv' in data_sources:
                external_data['arxiv'] = self._get_arxiv_data(query, max_results)
            
            # News data
            if 'news' in data_sources and news_api:
                external_data['news'] = self._get_news_data(query, max_results)
            
            # Run the research orchestrator with enhanced data
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                results = loop.run_until_complete(
                    orchestrator.conduct_research(query, output_dir)
                )
                # Add external data to results
                results['external_data'] = external_data
                results['data_sources_used'] = data_sources
                
            finally:
                loop.close()
            
            app_logger.info(f"Enhanced research completed for session: {results.get('session_id')}")
            return results
            
        except Exception as e:
            app_logger.error(f"Enhanced research failed: {e}")
            raise InternalServerError(f"Research failed: {str(e)}")
    
    def _get_wikipedia_data(self, query: str, max_results: int) -> Dict[str, Any]:
        """Get data from Wikipedia."""
        try:
            # Search for pages
            search_results = wikipedia.search(query, results=max_results)
            
            articles = []
            for title in search_results[:3]:  # Limit to top 3 to avoid rate limits
                try:
                    page = wikipedia.page(title)
                    articles.append({
                        'title': page.title,
                        'summary': page.summary[:500] + "..." if len(page.summary) > 500 else page.summary,
                        'url': page.url
                    })
                except:
                    continue
            
            return {
                'search_results': search_results,
                'articles': articles,
                'count': len(articles)
            }
        except Exception as e:
            app_logger.warning(f"Wikipedia API error: {e}")
            return {'error': str(e), 'count': 0}
    
    def _get_arxiv_data(self, query: str, max_results: int) -> Dict[str, Any]:
        """Get data from ArXiv."""
        try:
            import arxiv
            
            # Search ArXiv
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            papers = []
            for result in search.results():
                papers.append({
                    'title': result.title,
                    'authors': [author.name for author in result.authors],
                    'summary': result.summary[:500] + "..." if len(result.summary) > 500 else result.summary,
                    'published': result.published.isoformat(),
                    'url': result.entry_id,
                    'categories': result.categories
                })
            
            return {
                'papers': papers,
                'count': len(papers)
            }
        except Exception as e:
            app_logger.warning(f"ArXiv API error: {e}")
            return {'error': str(e), 'count': 0}
    
    def _get_news_data(self, query: str, max_results: int) -> Dict[str, Any]:
        """Get data from News API."""
        try:
            if not news_api:
                return {'error': 'News API not configured', 'count': 0}
            
            # Search for news articles
            articles = news_api.get_everything(
                q=query,
                language='en',
                sort_by='relevancy',
                page_size=min(max_results, 20)  # News API limit
            )
            
            news_items = []
            for article in articles.get('articles', []):
                news_items.append({
                    'title': article['title'],
                    'description': article['description'],
                    'url': article['url'],
                    'source': article['source']['name'],
                    'published_at': article['publishedAt'],
                    'author': article.get('author')
                })
            
            return {
                'articles': news_items,
                'total_results': articles.get('totalResults', 0),
                'count': len(news_items)
            }
        except Exception as e:
            app_logger.warning(f"News API error: {e}")
            return {'error': str(e), 'count': 0}

# Data Source Endpoints
@data_ns.route('/wikipedia/<string:query>')
class WikipediaData(Resource):
    @limiter.limit("30 per minute")
    @cache.cached(timeout=600)
    def get(self, query):
        """Get Wikipedia data for a specific query."""
        max_results = request.args.get('max_results', 5, type=int)
        
        research_resource = EnhancedConductResearch()
        data = research_resource._get_wikipedia_data(query, max_results)
        
        return {
            'source': 'wikipedia',
            'query': query,
            'results': data,
            'timestamp': datetime.now().isoformat()
        }

@data_ns.route('/arxiv/<string:query>')
class ArxivData(Resource):
    @limiter.limit("20 per minute")
    @cache.cached(timeout=600)
    def get(self, query):
        """Get ArXiv data for a specific query."""
        max_results = request.args.get('max_results', 5, type=int)
        
        research_resource = EnhancedConductResearch()
        data = research_resource._get_arxiv_data(query, max_results)
        
        return {
            'source': 'arxiv',
            'query': query,
            'results': data,
            'timestamp': datetime.now().isoformat()
        }

@data_ns.route('/news/<string:query>')
class NewsData(Resource):
    @limiter.limit("15 per minute")
    @cache.cached(timeout=300)
    def get(self, query):
        """Get news data for a specific query."""
        max_results = request.args.get('max_results', 10, type=int)
        
        research_resource = EnhancedConductResearch()
        data = research_resource._get_news_data(query, max_results)
        
        return {
            'source': 'news',
            'query': query,
            'results': data,
            'timestamp': datetime.now().isoformat()
        }

# Enhanced System Endpoints
@system_ns.route('/metrics')
class SystemMetrics(Resource):
    def get(self):
        """Get Prometheus metrics."""
        return metrics.generate_latest()

@system_ns.route('/health')
class EnhancedSystemHealth(Resource):
    @cache.cached(timeout=60)
    def get(self):
        """Enhanced system health check with external API status."""
        try:
            # Check environment
            env_status = check_environment()
            
            # Check external APIs
            external_apis = {
                'wikipedia': self._check_wikipedia(),
                'arxiv': self._check_arxiv(),
                'news_api': self._check_news_api(),
                'ollama': self._check_ollama()
            }
            
            # Get orchestrator status
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                orchestrator_status = loop.run_until_complete(orchestrator.get_status())
            finally:
                loop.close()
            
            overall_healthy = (
                env_status['overall_status'] and
                all(api_status['status'] == 'healthy' for api_status in external_apis.values())
            )
            
            return {
                'status': 'healthy' if overall_healthy else 'degraded',
                'timestamp': datetime.now().isoformat(),
                'components': {
                    'environment': env_status,
                    'orchestrator': orchestrator_status,
                    'external_apis': external_apis,
                    'cache': 'enabled',
                    'rate_limiting': 'enabled',
                    'monitoring': 'enabled'
                },
                'version': '2.0.0'
            }
            
        except Exception as e:
            app_logger.error(f"Health check failed: {e}")
            return {
                'status': 'unhealthy',
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'version': '2.0.0'
            }
    
    def _check_wikipedia(self) -> Dict[str, str]:
        """Check Wikipedia API status."""
        try:
            wikipedia.search("test", results=1)
            return {'status': 'healthy', 'message': 'Wikipedia API accessible'}
        except:
            return {'status': 'unhealthy', 'message': 'Wikipedia API unavailable'}
    
    def _check_arxiv(self) -> Dict[str, str]:
        """Check ArXiv API status."""
        try:
            import arxiv
            search = arxiv.Search(query="test", max_results=1)
            list(search.results())
            return {'status': 'healthy', 'message': 'ArXiv API accessible'}
        except:
            return {'status': 'unhealthy', 'message': 'ArXiv API unavailable'}
    
    def _check_news_api(self) -> Dict[str, str]:
        """Check News API status."""
        if not news_api:
            return {'status': 'disabled', 'message': 'News API not configured'}
        try:
            news_api.get_top_headlines(page_size=1)
            return {'status': 'healthy', 'message': 'News API accessible'}
        except:
            return {'status': 'unhealthy', 'message': 'News API unavailable'}

    def _check_ollama(self) -> Dict[str, str]:
        """Check Ollama AI status."""
        if not ollama_client:
            return {'status': 'disabled', 'message': 'Ollama client not initialized'}
        try:
            # Run async function in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                connected = loop.run_until_complete(ollama_client.check_connection())
                if connected:
                    models_count = len(ollama_client.available_models)
                    return {
                        'status': 'healthy',
                        'message': f'Ollama accessible with {models_count} models'
                    }
                else:
                    return {'status': 'unhealthy', 'message': 'Ollama server not accessible'}
            finally:
                loop.close()

        except Exception as e:
            return {'status': 'unhealthy', 'message': f'Ollama check failed: {str(e)}'}

# Ollama AI Endpoints
@ollama_ns.route('/models')
class OllamaModels(Resource):
    @limiter.limit("10 per minute")
    def get(self):
        """Get list of available Ollama models."""
        try:
            if not ollama_client:
                return {'error': 'Ollama client not initialized'}, 503

            models = ollama_client.available_models
            recommended = ollama_client.get_recommended_models()

            return {
                'models': models,
                'recommended': recommended,
                'count': len(models),
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            app_logger.error(f"Failed to get Ollama models: {e}")
            return {'error': str(e)}, 500

@ollama_ns.route('/generate')
class OllamaGenerate(Resource):
    @limiter.limit("5 per minute")
    def post(self):
        """Generate response using Ollama model."""
        try:
            if not ollama_client:
                return {'error': 'Ollama client not initialized'}, 503

            data = request.get_json()
            if not data or 'prompt' not in data:
                return {'error': 'Prompt is required'}, 400

            prompt = data['prompt']
            model = data.get('model', 'llama3.2:latest')
            system_prompt = data.get('system_prompt')
            temperature = data.get('temperature', 0.7)
            max_tokens = data.get('max_tokens', 2000)

            # Run async function in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                result = loop.run_until_complete(
                    ollama_client.generate_response(
                        prompt=prompt,
                        model=model,
                        system_prompt=system_prompt,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                )
            finally:
                loop.close()

            return result

        except Exception as e:
            app_logger.error(f"Ollama generation failed: {e}")
            return {'error': str(e)}, 500

@ollama_ns.route('/analyze')
class OllamaAnalyze(Resource):
    @limiter.limit("3 per minute")
    def post(self):
        """Analyze research query using Ollama."""
        try:
            if not ollama_client:
                return {'error': 'Ollama client not initialized'}, 503

            data = request.get_json()
            if not data or 'query' not in data:
                return {'error': 'Query is required'}, 400

            query = data['query']
            model = data.get('model', 'llama3.2:latest')

            # Run async function in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                result = loop.run_until_complete(
                    ollama_client.analyze_research_query(query, model)
                )
            finally:
                loop.close()

            return result

        except Exception as e:
            app_logger.error(f"Ollama analysis failed: {e}")
            return {'error': str(e)}, 500

@ollama_ns.route('/health')
class OllamaHealth(Resource):
    @cache.cached(timeout=60)
    def get(self):
        """Get Ollama health status."""
        try:
            if not ollama_client:
                return {
                    'status': 'unavailable',
                    'message': 'Ollama client not initialized',
                    'timestamp': datetime.now().isoformat()
                }

            # Run async function in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                health_status = loop.run_until_complete(
                    ollama_client.health_check()
                )
            finally:
                loop.close()

            return health_status

        except Exception as e:
            app_logger.error(f"Ollama health check failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

# Error handlers
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Rate limit exceeded', 'message': str(e)}), 429

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Root endpoint
@app.route('/')
def api_root():
    """Root endpoint with enhanced API information."""
    return jsonify({
        'name': 'Baker Street Laboratory Production API',
        'version': '2.0.0',
        'status': 'running',
        'features': [
            'Rate Limiting',
            'Caching',
            'Monitoring',
            'Multiple Data Sources',
            'Error Tracking'
        ],
        'data_sources': [
            'Wikipedia',
            'ArXiv',
            'News API',
            'Internal Research Pipeline'
        ],
        'documentation': '/docs/',
        'metrics': '/api/v2/system/metrics',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Initialize the application
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        if not loop.run_until_complete(initialize_app()):
            sys.exit(1)
    finally:
        loop.close()
    
    # Run with Gunicorn in production
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    if debug:
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        # Production mode - use Gunicorn
        import gunicorn.app.base
        
        class StandaloneApplication(gunicorn.app.base.BaseApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super().__init__()
            
            def load_config(self):
                for key, value in self.options.items():
                    self.cfg.set(key.lower(), value)
            
            def load(self):
                return self.application
        
        options = {
            'bind': f'0.0.0.0:{port}',
            'workers': 4,
            'worker_class': 'sync',
            'timeout': 120,
            'keepalive': 2,
            'max_requests': 1000,
            'max_requests_jitter': 100,
        }
        
        StandaloneApplication(app, options).run()
