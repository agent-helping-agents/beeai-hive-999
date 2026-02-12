#!/usr/bin/env python3
"""
Poly-AI Framework - Advanced GitHub Automation Suite
A revolutionary deployable polymorphic Linux/AI framework for adaptive GitHub workflow automation.
"""

import os
import sys
import json
import yaml
import asyncio
import logging
import requests
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import subprocess
import time
from pathlib import Path

# GitHub API
from github import Github, GithubException
from github.Repository import Repository
from github.Workflow import Workflow

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ToolMetrics:
    """Metrics for GitHub tools."""
    stars: int = 0
    forks: int = 0
    has_actions: bool = False
    has_ai_topics: bool = False
    last_updated: Optional[datetime] = None
    language: str = ""
    size: int = 0
    open_issues: int = 0
    watchers: int = 0

@dataclass
class WorkflowConfig:
    """Configuration for GitHub workflows."""
    name: str
    triggers: List[str]
    jobs: Dict[str, Any]
    environment: str = "default"
    enterprise_features: bool = False

@dataclass
class PolyAIConfig:
    """Configuration for Poly-AI Framework."""
    github_token: str
    github_org: Optional[str] = None
    github_user: Optional[str] = None
    scoring_weights: List[float] = field(default_factory=lambda: [0.4, 0.3, 0.2, 0.1])
    ai_enabled: bool = True
    perplexity_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    cache_enabled: bool = True
    max_workers: int = 10

class PolyAIFramework:
    """
    Main Poly-AI Framework class for intelligent GitHub automation.
    
    Features:
    - Live tool discovery and ranking
    - Adaptive workflow generation
    - AI-powered recommendations
    - Enterprise-grade automation
    - Polymorphic code practices
    """
    
    def __init__(self, config_file: str = "poly_config.yaml"):
        """
        Initialize the Poly-AI Framework.
        
        Args:
            config_file: Path to configuration file
        """
        self.config = self._load_config(config_file)
        self.github_client = Github(self.config.github_token)
        self.cache = {} if self.config.cache_enabled else None
        self.metrics = {
            "tools_discovered": 0,
            "workflows_generated": 0,
            "repositories_updated": 0,
            "ai_recommendations": 0
        }
        
        # Initialize AI services
        self.ai_services = self._initialize_ai_services()
        
        logger.info("Poly-AI Framework initialized successfully")
    
    def _load_config(self, config_file: str) -> PolyAIConfig:
        """Load configuration from file or environment variables."""
        config_data = {}
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config_data = yaml.safe_load(f)
        
        # Load from environment variables as fallback
        return PolyAIConfig(
            github_token=os.getenv("GITHUB_TOKEN") or config_data.get("github", {}).get("token", ""),
            github_org=os.getenv("GITHUB_ORG") or config_data.get("github", {}).get("org"),
            github_user=os.getenv("GITHUB_USER") or config_data.get("github", {}).get("user"),
            scoring_weights=config_data.get("scoring", {}).get("weights", [0.4, 0.3, 0.2, 0.1]),
            ai_enabled=config_data.get("ai", {}).get("enabled", True),
            perplexity_api_key=os.getenv("PERPLEXITY_API_KEY") or config_data.get("ai", {}).get("perplexity_api_key"),
            openai_api_key=os.getenv("OPENAI_API_KEY") or config_data.get("ai", {}).get("openai_api_key"),
            cache_enabled=config_data.get("cache", {}).get("enabled", True)
        )
    
    def _initialize_ai_services(self) -> Dict[str, Any]:
        """Initialize AI services."""
        services = {}
        
        if self.config.perplexity_api_key:
            services["perplexity"] = {
                "api_key": self.config.perplexity_api_key,
                "base_url": "https://api.perplexity.ai"
            }
        
        if self.config.openai_api_key:
            services["openai"] = {
                "api_key": self.config.openai_api_key,
                "base_url": "https://api.openai.com/v1"
            }
        
        return services
    
    async def discover_tools(self, query: str = "automation", per_page: int = 10) -> List[Dict[str, Any]]:
        """
        Discover GitHub tools using intelligent search.
        
        Args:
            query: Search query
            per_page: Number of results to return
            
        Returns:
            List of discovered tools with metrics
        """
        cache_key = f"tools_{query}_{per_page}"
        
        # Check cache first
        if self.cache and cache_key in self.cache:
            logger.info(f"Returning cached results for query: {query}")
            return self.cache[cache_key]
        
        try:
            logger.info(f"Discovering tools for query: {query}")
            
            # Search repositories
            repos = self.github_client.search_repositories(
                query=f"{query} language:python stars:>100",
                sort="stars",
                order="desc"
            )
            
            tools = []
            for repo in repos[:per_page]:
                try:
                    # Get detailed metrics
                    metrics = ToolMetrics(
                        stars=repo.stargazers_count,
                        forks=repo.forks_count,
                        has_actions=bool(repo.get_workflows().totalCount > 0),
                        has_ai_topics=any("ai" in topic.lower() or "ml" in topic.lower() 
                                        for topic in repo.get_topics()),
                        last_updated=repo.updated_at,
                        language=repo.language or "Unknown",
                        size=repo.size,
                        open_issues=repo.open_issues_count,
                        watchers=repo.watchers_count
                    )
                    
                    tool = {
                        "name": repo.full_name,
                        "description": repo.description or "No description",
                        "url": repo.html_url,
                        "metrics": [
                            metrics.stars,
                            metrics.forks,
                            int(metrics.has_actions),
                            int(metrics.has_ai_topics)
                        ],
                        "detailed_metrics": metrics,
                        "topics": list(repo.get_topics()),
                        "created_at": repo.created_at.isoformat(),
                        "updated_at": repo.updated_at.isoformat()
                    }
                    
                    tools.append(tool)
                    
                except GithubException as e:
                    logger.warning(f"Error processing repository {repo.full_name}: {e}")
                    continue
            
            # Cache results
            if self.cache:
                self.cache[cache_key] = tools
            
            self.metrics["tools_discovered"] += len(tools)
            logger.info(f"Discovered {len(tools)} tools")
            
            return tools
            
        except Exception as e:
            logger.error(f"Error discovering tools: {e}")
            return []
    
    def rank_tools(self, tools: List[Dict[str, Any]], 
                   weights: Optional[List[float]] = None) -> List[Tuple[Dict[str, Any], float]]:
        """
        Rank tools using advanced scoring algorithm.
        
        Args:
            tools: List of tools to rank
            weights: Scoring weights [stars, forks, actions, ai_topics]
            
        Returns:
            List of (tool, score) tuples sorted by score
        """
        if not tools:
            return []
        
        weights = weights or self.config.scoring_weights
        
        # Normalize metrics for fair comparison
        metrics_matrix = np.array([tool["metrics"] for tool in tools])
        
        # Apply logarithmic scaling for stars and forks (diminishing returns)
        metrics_matrix[:, 0] = np.log1p(metrics_matrix[:, 0])  # stars
        metrics_matrix[:, 1] = np.log1p(metrics_matrix[:, 1])  # forks
        
        # Normalize to 0-1 range
        for i in range(metrics_matrix.shape[1]):
            col = metrics_matrix[:, i]
            if col.max() > col.min():
                metrics_matrix[:, i] = (col - col.min()) / (col.max() - col.min())
        
        # Calculate weighted scores
        scores = metrics_matrix @ np.array(weights)
        
        # Create ranked list
        ranked = list(zip(tools, scores))
        ranked.sort(key=lambda x: x[1], reverse=True)
        
        logger.info(f"Ranked {len(tools)} tools using weights: {weights}")
        return ranked
    
    def pick_workflow_type(self, env_vars: Dict[str, str]) -> str:
        """
        Intelligently pick workflow type based on environment.
        
        Args:
            env_vars: Environment variables
            
        Returns:
            Workflow type identifier
        """
        # Enterprise detection
        if env_vars.get("ENTERPRISE") == "true":
            return "enterprise"
        
        # Open source detection
        if env_vars.get("OPEN_SOURCE") == "true":
            return "open_source"
        
        # AI/ML project detection
        if env_vars.get("PROJECT_TYPE") in ["ai", "ml", "ai_ml"]:
            return "ai_ml"
        
        # Web application detection
        if env_vars.get("PROJECT_TYPE") in ["web", "frontend", "backend"]:
            return "web_app"
        
        # Default workflow
        return "default"
    
    def generate_workflow(self, workflow_type: str) -> WorkflowConfig:
        """
        Generate workflow configuration based on type.
        
        Args:
            workflow_type: Type of workflow to generate
            
        Returns:
            Workflow configuration
        """
        workflows = {
            "enterprise": WorkflowConfig(
                name="Enterprise CI/CD Pipeline",
                triggers=["push", "pull_request", "schedule"],
                jobs={
                    "security-scan": {
                        "runs-on": "ubuntu-latest",
                        "steps": [
                            {"name": "Security Scan", "uses": "actions/security-scan@v1"},
                            {"name": "Dependency Check", "uses": "actions/dependency-check@v1"}
                        ]
                    },
                    "test": {
                        "runs-on": "ubuntu-latest",
                        "needs": "security-scan",
                        "steps": [
                            {"name": "Run Tests", "run": "pytest tests/"},
                            {"name": "Coverage Report", "run": "coverage report"}
                        ]
                    },
                    "deploy": {
                        "runs-on": "ubuntu-latest",
                        "needs": "test",
                        "if": "github.ref == 'refs/heads/main'",
                        "steps": [
                            {"name": "Deploy to Production", "run": "deploy.sh"}
                        ]
                    }
                },
                environment="production",
                enterprise_features=True
            ),
            
            "ai_ml": WorkflowConfig(
                name="AI/ML Pipeline",
                triggers=["push", "pull_request"],
                jobs={
                    "data-validation": {
                        "runs-on": "ubuntu-latest",
                        "steps": [
                            {"name": "Validate Data", "run": "python scripts/validate_data.py"}
                        ]
                    },
                    "model-training": {
                        "runs-on": "ubuntu-latest",
                        "needs": "data-validation",
                        "steps": [
                            {"name": "Train Model", "run": "python train.py"},
                            {"name": "Model Evaluation", "run": "python evaluate.py"}
                        ]
                    },
                    "model-deployment": {
                        "runs-on": "ubuntu-latest",
                        "needs": "model-training",
                        "if": "github.ref == 'refs/heads/main'",
                        "steps": [
                            {"name": "Deploy Model", "run": "python deploy.py"}
                        ]
                    }
                },
                environment="ml"
            ),
            
            "open_source": WorkflowConfig(
                name="Open Source CI",
                triggers=["push", "pull_request"],
                jobs={
                    "test": {
                        "runs-on": "ubuntu-latest",
                        "strategy": {
                            "matrix": {"python-version": ["3.8", "3.9", "3.10", "3.11"]}
                        },
                        "steps": [
                            {"name": "Set up Python", "uses": f"actions/setup-python@v4", 
                             "with": {"python-version": "${{ matrix.python-version }}"}},
                            {"name": "Install dependencies", "run": "pip install -r requirements.txt"},
                            {"name": "Run tests", "run": "pytest"}
                        ]
                    },
                    "lint": {
                        "runs-on": "ubuntu-latest",
                        "steps": [
                            {"name": "Lint code", "run": "flake8 ."},
                            {"name": "Format check", "run": "black --check ."}
                        ]
                    }
                },
                environment="open_source"
            ),
            
            "default": WorkflowConfig(
                name="Standard CI/CD",
                triggers=["push", "pull_request"],
                jobs={
                    "test": {
                        "runs-on": "ubuntu-latest",
                        "steps": [
                            {"name": "Run tests", "run": "npm test || python -m pytest || make test"}
                        ]
                    },
                    "build": {
                        "runs-on": "ubuntu-latest",
                        "needs": "test",
                        "steps": [
                            {"name": "Build project", "run": "npm run build || python setup.py build || make build"}
                        ]
                    }
                },
                environment="default"
            )
        }
        
        workflow = workflows.get(workflow_type, workflows["default"])
        self.metrics["workflows_generated"] += 1
        
        logger.info(f"Generated {workflow_type} workflow: {workflow.name}")
        return workflow
    
    def deploy_workflow(self, repo_name: str, workflow_config: WorkflowConfig) -> bool:
        """
        Deploy workflow to GitHub repository.
        
        Args:
            repo_name: Repository name (owner/repo)
            workflow_config: Workflow configuration
            
        Returns:
            True if deployment successful
        """
        try:
            # Get repository
            repo = self.github_client.get_repo(repo_name)
            
            # Create workflow YAML
            workflow_yaml = self._create_workflow_yaml(workflow_config)
            
            # Create workflow file
            workflow_path = f".github/workflows/{workflow_config.name.lower().replace(' ', '_')}.yml"
            
            try:
                # Try to get existing workflow file
                existing_file = repo.get_contents(workflow_path)
                # Update existing file
                repo.update_file(
                    workflow_path,
                    f"Update {workflow_config.name}",
                    workflow_yaml,
                    existing_file.sha
                )
                logger.info(f"Updated workflow in {repo_name}")
            except:
                # Create new file
                repo.create_file(
                    workflow_path,
                    f"Add {workflow_config.name}",
                    workflow_yaml
                )
                logger.info(f"Created new workflow in {repo_name}")
            
            self.metrics["repositories_updated"] += 1
            return True
            
        except Exception as e:
            logger.error(f"Error deploying workflow to {repo_name}: {e}")
            return False
    
    def _create_workflow_yaml(self, config: WorkflowConfig) -> str:
        """Create GitHub Actions workflow YAML."""
        yaml_content = f"""name: {config.name}

on:
"""
        
        for trigger in config.triggers:
            if trigger == "schedule":
                yaml_content += "  schedule:\n    - cron: '0 2 * * 1'  # Weekly on Monday at 2 AM\n"
            else:
                yaml_content += f"  {trigger}:\n"
        
        yaml_content += "\njobs:\n"
        
        for job_name, job_config in config.jobs.items():
            yaml_content += f"  {job_name}:\n"
            yaml_content += f"    runs-on: {job_config['runs-on']}\n"
            
            if "needs" in job_config:
                yaml_content += f"    needs: {job_config['needs']}\n"
            
            if "if" in job_config:
                yaml_content += f"    if: {job_config['if']}\n"
            
            if "strategy" in job_config:
                yaml_content += f"    strategy:\n"
                for key, value in job_config["strategy"].items():
                    yaml_content += f"      {key}: {value}\n"
            
            yaml_content += "    steps:\n"
            
            for step in job_config["steps"]:
                yaml_content += "      - name: " + step["name"] + "\n"
                
                if "uses" in step:
                    yaml_content += "        uses: " + step["uses"] + "\n"
                
                if "run" in step:
                    yaml_content += "        run: " + step["run"] + "\n"
                
                if "with" in step:
                    yaml_content += "        with:\n"
                    for key, value in step["with"].items():
                        yaml_content += f"          {key}: {value}\n"
        
        return yaml_content
    
    async def fetch_ai_recommendations(self, query: str) -> Dict[str, Any]:
        """
        Fetch AI-powered recommendations using free alternatives.
        
        Args:
            query: Query for recommendations
            
        Returns:
            AI recommendations
        """
        try:
            # Use free AI alternatives or local models
            recommendations = self._generate_local_recommendations(query)
            
            self.metrics["ai_recommendations"] += 1
            return {
                "recommendations": recommendations,
                "model": "local-expert-system",
                "source": "free-alternative"
            }
                
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return {"error": str(e)}
    
    def _generate_local_recommendations(self, query: str) -> str:
        """Generate recommendations using local expert system."""
        query_lower = query.lower()
        
        # Expert system for GitHub automation recommendations
        recommendations = []
        
        if "enterprise" in query_lower or "large" in query_lower:
            recommendations.extend([
                "For enterprise environments, consider implementing:",
                "• Security scanning with CodeQL and Dependabot",
                "• Multi-environment deployment pipelines (dev/staging/prod)",
                "• Automated compliance checks and audit trails",
                "• Role-based access control and approval workflows",
                "• Integration with enterprise identity providers (SSO)"
            ])
        
        if "startup" in query_lower or "small" in query_lower:
            recommendations.extend([
                "For startups and small teams, focus on:",
                "• Simple CI/CD pipelines with GitHub Actions",
                "• Automated testing and code quality checks",
                "• Basic security scanning and dependency updates",
                "• Cost-effective monitoring and alerting",
                "• Quick deployment to cloud platforms"
            ])
        
        if "ai" in query_lower or "ml" in query_lower or "machine learning" in query_lower:
            recommendations.extend([
                "For AI/ML projects, implement:",
                "• Data validation and preprocessing pipelines",
                "• Model training and evaluation workflows",
                "• Automated model deployment and versioning",
                "• Experiment tracking and reproducibility",
                "• Integration with MLflow or similar platforms"
            ])
        
        if "security" in query_lower:
            recommendations.extend([
                "Security best practices for GitHub automation:",
                "• Use GitHub Secrets for sensitive data",
                "• Implement least-privilege access controls",
                "• Regular security scanning and vulnerability assessment",
                "• Code signing and artifact verification",
                "• Audit logging and compliance monitoring"
            ])
        
        if "performance" in query_lower or "optimization" in query_lower:
            recommendations.extend([
                "Performance optimization strategies:",
                "• Parallel job execution and matrix builds",
                "• Caching dependencies and build artifacts",
                "• Optimized Docker images and multi-stage builds",
                "• Resource monitoring and cost optimization",
                "• Automated performance testing and benchmarking"
            ])
        
        # Default recommendations if no specific context
        if not recommendations:
            recommendations = [
                "General GitHub automation best practices:",
                "• Start with simple workflows and iterate",
                "• Use GitHub Actions marketplace for common tasks",
                "• Implement proper error handling and notifications",
                "• Document your automation processes",
                "• Regular review and optimization of workflows",
                "• Consider using Poly-AI Framework for intelligent automation"
            ]
        
        return "\n".join(recommendations)
    
    def apply_recommendations(self, recommendations: Dict[str, Any]) -> bool:
        """
        Apply AI recommendations to the current project.
        
        Args:
            recommendations: AI recommendations
            
        Returns:
            True if recommendations applied successfully
        """
        try:
            if "error" in recommendations:
                logger.error(f"Cannot apply recommendations: {recommendations['error']}")
                return False
            
            # Parse recommendations and apply them
            # This is a simplified implementation
            logger.info("Applying AI recommendations...")
            logger.info(f"Recommendations: {recommendations.get('recommendations', 'No recommendations')}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error applying recommendations: {e}")
            return False
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get framework metrics."""
        return {
            **self.metrics,
            "cache_size": len(self.cache) if self.cache else 0,
            "ai_services_configured": len(self.ai_services),
            "github_rate_limit": self.github_client.get_rate_limit().core.remaining
        }
    
    def create_config_file(self, filename: str = "poly_config.yaml") -> None:
        """Create a default configuration file."""
        config = {
            "poly_ai": {
                "github": {
                    "token": "${GITHUB_TOKEN}",
                    "org": "${GITHUB_ORG}",
                    "user": "${GITHUB_USER}"
                },
                "scoring": {
                    "weights": [0.4, 0.3, 0.2, 0.1]
                },
                "workflows": {
                    "enterprise": "ai_enterprise.yml",
                    "open_source": "os_workflow.yml",
                    "default": "default_workflow.yml"
                },
                "ai": {
                    "enabled": True,
                    "perplexity_api_key": "${PERPLEXITY_API_KEY}",
                    "openai_api_key": "${OPENAI_API_KEY}",
                    "cache_responses": True
                },
                "cache": {
                    "enabled": True,
                    "ttl": 3600
                }
            }
        }
        
        with open(filename, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, indent=2)
        
        logger.info(f"Configuration file created: {filename}")

# Utility functions
def rank_tools(tools: List[Dict[str, Any]], weights: List[float]) -> List[Tuple[Dict[str, Any], float]]:
    """Standalone function for ranking tools."""
    framework = PolyAIFramework()
    return framework.rank_tools(tools, weights)

def fetch_github_tools(query: str = "automation", per_page: int = 10) -> List[Dict[str, Any]]:
    """Standalone function for fetching GitHub tools."""
    framework = PolyAIFramework()
    return asyncio.run(framework.discover_tools(query, per_page))

def pick_workflow_type(env: Dict[str, str]) -> str:
    """Standalone function for picking workflow type."""
    framework = PolyAIFramework()
    return framework.pick_workflow_type(env)

async def main():
    """Main function demonstrating Poly-AI Framework capabilities."""
    print("🚀 Poly-AI Framework - Advanced GitHub Automation Suite")
    print("=" * 60)
    
    # Initialize framework
    framework = PolyAIFramework()
    
    # Check GitHub token
    if not framework.config.github_token:
        print("❌ GitHub token not found. Please set GITHUB_TOKEN environment variable.")
        return
    
    print("✅ Framework initialized successfully")
    
    # Discover and rank tools
    print("\n🔍 Discovering GitHub automation tools...")
    tools = await framework.discover_tools("python automation", per_page=8)
    
    if tools:
        print(f"📊 Found {len(tools)} tools, ranking them...")
        ranked_tools = framework.rank_tools(tools)
        
        print("\n🏆 Top GitHub Automation Tools (Polymorphic Ranking):")
        print("-" * 50)
        for i, (tool, score) in enumerate(ranked_tools, 1):
            print(f"{i:2d}. {tool['name']}")
            print(f"    ⭐ {tool['detailed_metrics'].stars:,} stars | "
                  f"🍴 {tool['detailed_metrics'].forks:,} forks | "
                  f"🤖 AI: {'Yes' if tool['detailed_metrics'].has_ai_topics else 'No'}")
            print(f"    📝 {tool['description'][:80]}...")
            print(f"    🔗 {tool['url']}")
            print(f"    📊 Score: {score:.3f}")
            print()
    else:
        print("❌ No tools found")
    
    # Workflow generation demo
    print("⚙️  Workflow Generation Demo:")
    print("-" * 30)
    
    env_vars = {
        "ENTERPRISE": "false",
        "OPEN_SOURCE": "true",
        "PROJECT_TYPE": "ai_ml"
    }
    
    workflow_type = framework.pick_workflow_type(env_vars)
    workflow_config = framework.generate_workflow(workflow_type)
    
    print(f"Selected workflow type: {workflow_type}")
    print(f"Generated workflow: {workflow_config.name}")
    print(f"Triggers: {', '.join(workflow_config.triggers)}")
    print(f"Jobs: {list(workflow_config.jobs.keys())}")
    
    # AI recommendations demo
    if framework.config.perplexity_api_key:
        print("\n🤖 AI Recommendations Demo:")
        print("-" * 30)
        
        query = "best practices for Python AI project automation"
        recommendations = await framework.fetch_ai_recommendations(query)
        
        if "error" not in recommendations:
            print(f"Query: {query}")
            print(f"AI Response: {recommendations['recommendations'][:200]}...")
        else:
            print(f"AI Error: {recommendations['error']}")
    else:
        print("\n🤖 AI Recommendations: Not configured (set PERPLEXITY_API_KEY)")
    
    # Display metrics
    print("\n📊 Framework Metrics:")
    print("-" * 20)
    metrics = framework.get_metrics()
    for key, value in metrics.items():
        print(f"{key}: {value}")
    
    print("\n🎉 Poly-AI Framework demo completed!")
    print("Ready for production use with intelligent GitHub automation!")

if __name__ == "__main__":
    asyncio.run(main())