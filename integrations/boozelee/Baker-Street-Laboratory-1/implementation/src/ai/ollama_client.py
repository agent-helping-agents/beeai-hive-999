#!/usr/bin/env python3
"""
Baker Street Laboratory - Ollama AI Client
Local AI model integration for research and analysis.
"""

import asyncio
import logging
import json
from typing import Dict, Any, List, Optional, AsyncGenerator
from datetime import datetime

import ollama
import httpx
from core.logger import get_logger


class OllamaClient:
    """
    Client for interacting with Ollama local AI models.
    Provides research analysis, query processing, and content generation.
    """
    
    def __init__(self, host: str = "http://localhost:11434"):
        """
        Initialize Ollama client.
        
        Args:
            host: Ollama server host URL
        """
        self.host = host
        self.client = ollama.Client(host=host)
        self.logger = get_logger(__name__)
        self.available_models = []
        
    async def initialize(self) -> bool:
        """
        Initialize the Ollama client and check connectivity.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            # Check if Ollama server is running
            await self.check_connection()
            
            # Get available models
            self.available_models = await self.list_models()
            
            self.logger.info(f"Ollama client initialized with {len(self.available_models)} models")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Ollama client: {e}")
            return False
    
    async def check_connection(self) -> bool:
        """
        Check if Ollama server is accessible.
        
        Returns:
            True if connected, False otherwise
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.host}/api/tags")
                return response.status_code == 200
        except Exception as e:
            self.logger.warning(f"Ollama connection check failed: {e}")
            return False
    
    async def list_models(self) -> List[Dict[str, Any]]:
        """
        Get list of available Ollama models.
        
        Returns:
            List of model information dictionaries
        """
        try:
            response = self.client.list()
            models = []
            
            for model in response.get('models', []):
                models.append({
                    'name': model['name'],
                    'size': model.get('size', 0),
                    'modified_at': model.get('modified_at'),
                    'digest': model.get('digest', ''),
                    'details': model.get('details', {})
                })
            
            return models
            
        except Exception as e:
            self.logger.error(f"Failed to list Ollama models: {e}")
            return []
    
    async def pull_model(self, model_name: str) -> bool:
        """
        Pull/download a model from Ollama registry.
        
        Args:
            model_name: Name of the model to pull
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info(f"Pulling Ollama model: {model_name}")
            
            # Use streaming pull to show progress
            stream = self.client.pull(model_name, stream=True)
            
            for chunk in stream:
                if 'status' in chunk:
                    self.logger.info(f"Pull progress: {chunk['status']}")
            
            self.logger.info(f"Successfully pulled model: {model_name}")
            
            # Refresh available models list
            self.available_models = await self.list_models()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to pull model {model_name}: {e}")
            return False
    
    async def generate_response(
        self, 
        prompt: str, 
        model: str = "llama3.2:latest",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """
        Generate a response using Ollama model.
        
        Args:
            prompt: User prompt/query
            model: Model name to use
            system_prompt: Optional system prompt
            temperature: Response creativity (0.0-1.0)
            max_tokens: Maximum response length
            
        Returns:
            Dictionary containing response and metadata
        """
        try:
            messages = []
            
            if system_prompt:
                messages.append({
                    'role': 'system',
                    'content': system_prompt
                })
            
            messages.append({
                'role': 'user',
                'content': prompt
            })
            
            start_time = datetime.now()
            
            response = self.client.chat(
                model=model,
                messages=messages,
                options={
                    'temperature': temperature,
                    'num_predict': max_tokens
                }
            )
            
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            return {
                'success': True,
                'response': response['message']['content'],
                'model': model,
                'processing_time': processing_time,
                'tokens_used': response.get('eval_count', 0),
                'timestamp': end_time.isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to generate response with {model}: {e}")
            return {
                'success': False,
                'error': str(e),
                'model': model,
                'timestamp': datetime.now().isoformat()
            }
    
    async def analyze_research_query(self, query: str, model: str = "llama3.2:latest") -> Dict[str, Any]:
        """
        Analyze a research query and provide structured insights.
        
        Args:
            query: Research query to analyze
            model: Model to use for analysis
            
        Returns:
            Structured analysis results
        """
        system_prompt = """You are a research analyst for Baker Street Laboratory, a psychedelic detective-themed AI research framework. 

Analyze the given research query and provide a structured response with:
1. Key concepts and themes
2. Suggested research approaches
3. Potential data sources
4. Expected challenges
5. Research methodology recommendations

Format your response as JSON with the following structure:
{
    "key_concepts": ["concept1", "concept2", ...],
    "research_approaches": ["approach1", "approach2", ...],
    "data_sources": ["source1", "source2", ...],
    "challenges": ["challenge1", "challenge2", ...],
    "methodology": "detailed methodology description",
    "complexity_score": 1-10,
    "estimated_time": "time estimate"
}"""
        
        result = await self.generate_response(
            prompt=f"Analyze this research query: {query}",
            model=model,
            system_prompt=system_prompt,
            temperature=0.3
        )
        
        if result['success']:
            try:
                # Try to parse JSON response
                analysis = json.loads(result['response'])
                result['structured_analysis'] = analysis
            except json.JSONDecodeError:
                # If JSON parsing fails, provide basic structure
                result['structured_analysis'] = {
                    'raw_analysis': result['response'],
                    'parsing_error': True
                }
        
        return result
    
    async def synthesize_research_findings(
        self, 
        findings: List[Dict[str, Any]], 
        query: str,
        model: str = "llama3.2:latest"
    ) -> Dict[str, Any]:
        """
        Synthesize research findings into a coherent report.
        
        Args:
            findings: List of research findings from various sources
            query: Original research query
            model: Model to use for synthesis
            
        Returns:
            Synthesized research report
        """
        system_prompt = """You are a research synthesizer for Baker Street Laboratory. 

Given research findings from multiple sources, create a comprehensive research report that:
1. Synthesizes key insights across sources
2. Identifies patterns and connections
3. Highlights contradictions or gaps
4. Provides evidence-based conclusions
5. Suggests areas for further investigation

Write in the style of a detective's case report - methodical, insightful, and engaging."""
        
        # Prepare findings summary for the prompt
        findings_text = "\n\n".join([
            f"Source: {finding.get('source', 'Unknown')}\n"
            f"Content: {finding.get('content', finding.get('summary', 'No content'))}"
            for finding in findings[:10]  # Limit to prevent token overflow
        ])
        
        prompt = f"""Research Query: {query}

Research Findings:
{findings_text}

Please synthesize these findings into a comprehensive research report."""
        
        return await self.generate_response(
            prompt=prompt,
            model=model,
            system_prompt=system_prompt,
            temperature=0.5,
            max_tokens=3000
        )
    
    async def generate_research_questions(
        self, 
        topic: str, 
        model: str = "llama3.2:latest"
    ) -> Dict[str, Any]:
        """
        Generate follow-up research questions for a given topic.
        
        Args:
            topic: Research topic
            model: Model to use
            
        Returns:
            Generated research questions
        """
        system_prompt = """You are a research question generator for Baker Street Laboratory.

Generate 10 insightful research questions related to the given topic. Questions should be:
1. Specific and focused
2. Researchable with available data sources
3. Intellectually stimulating
4. Varied in scope (some broad, some narrow)
5. Suitable for AI-augmented research

Format as a numbered list."""
        
        return await self.generate_response(
            prompt=f"Generate research questions for the topic: {topic}",
            model=model,
            system_prompt=system_prompt,
            temperature=0.8
        )
    
    async def stream_response(
        self, 
        prompt: str, 
        model: str = "llama3.2:latest",
        system_prompt: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream response from Ollama model for real-time display.
        
        Args:
            prompt: User prompt
            model: Model to use
            system_prompt: Optional system prompt
            
        Yields:
            Response chunks as they're generated
        """
        try:
            messages = []
            
            if system_prompt:
                messages.append({
                    'role': 'system',
                    'content': system_prompt
                })
            
            messages.append({
                'role': 'user',
                'content': prompt
            })
            
            stream = self.client.chat(
                model=model,
                messages=messages,
                stream=True
            )
            
            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    yield chunk['message']['content']
                    
        except Exception as e:
            self.logger.error(f"Streaming failed: {e}")
            yield f"Error: {str(e)}"
    
    def get_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Model information or None if not found
        """
        for model in self.available_models:
            if model['name'] == model_name:
                return model
        return None
    
    def get_recommended_models(self) -> List[str]:
        """
        Get list of recommended models for research tasks.
        
        Returns:
            List of recommended model names
        """
        recommended = [
            "llama3.2:latest",
            "llama3.1:8b",
            "mistral:latest",
            "codellama:latest",
            "phi3:latest"
        ]
        
        # Filter to only include available models
        available_names = [model['name'] for model in self.available_models]
        return [model for model in recommended if model in available_names]
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform comprehensive health check of Ollama integration.
        
        Returns:
            Health check results
        """
        health_status = {
            'timestamp': datetime.now().isoformat(),
            'connection': False,
            'models_available': 0,
            'recommended_models': [],
            'server_info': None,
            'status': 'unhealthy'
        }
        
        try:
            # Check connection
            health_status['connection'] = await self.check_connection()
            
            if health_status['connection']:
                # Get models
                models = await self.list_models()
                health_status['models_available'] = len(models)
                health_status['recommended_models'] = self.get_recommended_models()
                
                # Test basic functionality
                test_response = await self.generate_response(
                    "Hello, this is a test.",
                    model=health_status['recommended_models'][0] if health_status['recommended_models'] else "llama3.2:latest"
                )
                
                if test_response['success']:
                    health_status['status'] = 'healthy'
                else:
                    health_status['status'] = 'degraded'
                    health_status['test_error'] = test_response.get('error')
            
        except Exception as e:
            health_status['error'] = str(e)
            self.logger.error(f"Ollama health check failed: {e}")
        
        return health_status
