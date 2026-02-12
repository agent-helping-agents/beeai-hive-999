#!/usr/bin/env python3
"""
Test suite for Poly-AI Framework
"""

import pytest
import asyncio
import os
from unittest.mock import Mock, patch, MagicMock
from poly_framework import PolyAIFramework, ToolMetrics, WorkflowConfig, PolyAIConfig

class TestPolyAIFramework:
    """Test cases for Poly-AI Framework"""
    
    @pytest.fixture
    def mock_config(self):
        """Mock configuration for testing"""
        return PolyAIConfig(
            github_token="test_token",
            github_org="test_org",
            github_user="test_user",
            scoring_weights=[0.4, 0.3, 0.2, 0.1],
            ai_enabled=True,
            perplexity_api_key="test_perplexity_key",
            openai_api_key="test_openai_key",
            cache_enabled=True
        )
    
    @pytest.fixture
    def sample_tools(self):
        """Sample tools for testing"""
        return [
            {
                "name": "test/repo1",
                "description": "Test repository 1",
                "url": "https://github.com/test/repo1",
                "metrics": [1000, 100, 1, 1],
                "detailed_metrics": ToolMetrics(
                    stars=1000,
                    forks=100,
                    has_actions=True,
                    has_ai_topics=True
                ),
                "topics": ["ai", "automation"],
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-12-01T00:00:00Z"
            },
            {
                "name": "test/repo2",
                "description": "Test repository 2",
                "url": "https://github.com/test/repo2",
                "metrics": [500, 50, 0, 0],
                "detailed_metrics": ToolMetrics(
                    stars=500,
                    forks=50,
                    has_actions=False,
                    has_ai_topics=False
                ),
                "topics": ["python"],
                "created_at": "2023-02-01T00:00:00Z",
                "updated_at": "2023-11-01T00:00:00Z"
            }
        ]
    
    @patch('poly_framework.Github')
    def test_framework_initialization(self, mock_github, mock_config):
        """Test framework initialization"""
        mock_github.return_value = Mock()
        
        with patch.object(PolyAIFramework, '_load_config', return_value=mock_config):
            framework = PolyAIFramework()
            
            assert framework.config.github_token == "test_token"
            assert framework.config.github_org == "test_org"
            assert framework.config.github_user == "test_user"
            assert framework.config.scoring_weights == [0.4, 0.3, 0.2, 0.1]
            assert framework.cache is not None
    
    def test_rank_tools(self, sample_tools):
        """Test tool ranking functionality"""
        framework = PolyAIFramework()
        ranked_tools = framework.rank_tools(sample_tools)
        
        assert len(ranked_tools) == 2
        assert ranked_tools[0][1] >= ranked_tools[1][1]  # First tool should have higher score
        
        # First tool should rank higher due to more stars and AI topics
        assert ranked_tools[0][0]["name"] == "test/repo1"
        assert ranked_tools[1][0]["name"] == "test/repo2"
    
    def test_pick_workflow_type(self):
        """Test workflow type selection"""
        framework = PolyAIFramework()
        
        # Test enterprise workflow
        env_vars = {"ENTERPRISE": "true"}
        assert framework.pick_workflow_type(env_vars) == "enterprise"
        
        # Test open source workflow
        env_vars = {"OPEN_SOURCE": "true"}
        assert framework.pick_workflow_type(env_vars) == "open_source"
        
        # Test AI/ML workflow
        env_vars = {"PROJECT_TYPE": "ai_ml"}
        assert framework.pick_workflow_type(env_vars) == "ai_ml"
        
        # Test default workflow
        env_vars = {}
        assert framework.pick_workflow_type(env_vars) == "default"
    
    def test_generate_workflow(self):
        """Test workflow generation"""
        framework = PolyAIFramework()
        
        # Test enterprise workflow
        workflow = framework.generate_workflow("enterprise")
        assert workflow.name == "Enterprise CI/CD Pipeline"
        assert "security-scan" in workflow.jobs
        assert "test" in workflow.jobs
        assert "deploy" in workflow.jobs
        assert workflow.enterprise_features is True
        
        # Test AI/ML workflow
        workflow = framework.generate_workflow("ai_ml")
        assert workflow.name == "AI/ML Pipeline"
        assert "data-validation" in workflow.jobs
        assert "model-training" in workflow.jobs
        assert "model-deployment" in workflow.jobs
        
        # Test default workflow
        workflow = framework.generate_workflow("default")
        assert workflow.name == "Standard CI/CD"
        assert "test" in workflow.jobs
        assert "build" in workflow.jobs
    
    def test_create_workflow_yaml(self):
        """Test workflow YAML generation"""
        framework = PolyAIFramework()
        workflow_config = WorkflowConfig(
            name="Test Workflow",
            triggers=["push", "pull_request"],
            jobs={
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"name": "Run tests", "run": "pytest"}
                    ]
                }
            }
        )
        
        yaml_content = framework._create_workflow_yaml(workflow_config)
        
        assert "name: Test Workflow" in yaml_content
        assert "on:" in yaml_content
        assert "push:" in yaml_content
        assert "pull_request:" in yaml_content
        assert "jobs:" in yaml_content
        assert "test:" in yaml_content
        assert "runs-on: ubuntu-latest" in yaml_content
        assert "Run tests" in yaml_content
        assert "pytest" in yaml_content
    
    @patch('poly_framework.requests.post')
    @pytest.mark.asyncio
    async def test_fetch_ai_recommendations(self, mock_post, mock_config):
        """Test AI recommendations fetching"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": "Test AI recommendation"
                }
            }],
            "model": "llama-3.1-sonar-small-128k-online",
            "usage": {"total_tokens": 100}
        }
        mock_post.return_value = mock_response
        
        with patch.object(PolyAIFramework, '_load_config', return_value=mock_config):
            framework = PolyAIFramework()
            recommendations = await framework.fetch_ai_recommendations("test query")
            
            assert "error" not in recommendations
            assert recommendations["recommendations"] == "Test AI recommendation"
            assert recommendations["model"] == "llama-3.1-sonar-small-128k-online"
    
    @patch('poly_framework.requests.post')
    @pytest.mark.asyncio
    async def test_fetch_ai_recommendations_error(self, mock_post, mock_config):
        """Test AI recommendations error handling"""
        # Mock API error
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        
        with patch.object(PolyAIFramework, '_load_config', return_value=mock_config):
            framework = PolyAIFramework()
            recommendations = await framework.fetch_ai_recommendations("test query")
            
            assert "error" in recommendations
            assert "API error: 400" in recommendations["error"]
    
    def test_get_metrics(self, mock_config):
        """Test metrics collection"""
        with patch.object(PolyAIFramework, '_load_config', return_value=mock_config):
            framework = PolyAIFramework()
            metrics = framework.get_metrics()
            
            assert "tools_discovered" in metrics
            assert "workflows_generated" in metrics
            assert "repositories_updated" in metrics
            assert "ai_recommendations" in metrics
            assert "cache_size" in metrics
            assert "ai_services_configured" in metrics
    
    def test_create_config_file(self, tmp_path):
        """Test configuration file creation"""
        framework = PolyAIFramework()
        config_file = tmp_path / "test_config.yaml"
        
        framework.create_config_file(str(config_file))
        
        assert config_file.exists()
        
        # Verify file content
        with open(config_file, 'r') as f:
            content = f.read()
            assert "poly_ai:" in content
            assert "github:" in content
            assert "scoring:" in content
            assert "ai:" in content

class TestToolMetrics:
    """Test cases for ToolMetrics class"""
    
    def test_tool_metrics_initialization(self):
        """Test ToolMetrics initialization"""
        metrics = ToolMetrics(
            stars=1000,
            forks=100,
            has_actions=True,
            has_ai_topics=True,
            language="Python",
            size=5000,
            open_issues=10,
            watchers=50
        )
        
        assert metrics.stars == 1000
        assert metrics.forks == 100
        assert metrics.has_actions is True
        assert metrics.has_ai_topics is True
        assert metrics.language == "Python"
        assert metrics.size == 5000
        assert metrics.open_issues == 10
        assert metrics.watchers == 50

class TestWorkflowConfig:
    """Test cases for WorkflowConfig class"""
    
    def test_workflow_config_initialization(self):
        """Test WorkflowConfig initialization"""
        config = WorkflowConfig(
            name="Test Workflow",
            triggers=["push", "pull_request"],
            jobs={"test": {"runs-on": "ubuntu-latest"}},
            environment="test",
            enterprise_features=True
        )
        
        assert config.name == "Test Workflow"
        assert config.triggers == ["push", "pull_request"]
        assert config.jobs == {"test": {"runs-on": "ubuntu-latest"}}
        assert config.environment == "test"
        assert config.enterprise_features is True

# Integration tests
@pytest.mark.integration
class TestIntegration:
    """Integration tests for Poly-AI Framework"""
    
    @pytest.mark.skipif(not os.getenv("GITHUB_TOKEN"), reason="GitHub token not available")
    @pytest.mark.asyncio
    async def test_real_github_discovery(self):
        """Test real GitHub API integration"""
        framework = PolyAIFramework()
        tools = await framework.discover_tools("python automation", per_page=5)
        
        assert len(tools) <= 5
        for tool in tools:
            assert "name" in tool
            assert "url" in tool
            assert "metrics" in tool
            assert len(tool["metrics"]) == 4
    
    @pytest.mark.skipif(not os.getenv("PERPLEXITY_API_KEY"), reason="Perplexity API key not available")
    @pytest.mark.asyncio
    async def test_real_ai_recommendations(self):
        """Test real AI API integration"""
        framework = PolyAIFramework()
        recommendations = await framework.fetch_ai_recommendations("GitHub automation best practices")
        
        assert "error" not in recommendations
        assert "recommendations" in recommendations

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
